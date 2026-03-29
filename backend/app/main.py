from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .gemini_client import GeminiClient
from .models import RunRequest, RunResponse
from .skills.loader import load_skills
from .skills.orchestrator import build_instruction, select_skill

app = FastAPI(title="Skill Runtime API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/run", response_model=RunResponse)
def run(req: RunRequest) -> RunResponse:
    logs: list[str] = ["request accepted"]

    skills = load_skills(settings.skills_dir)
    logs.append(f"loaded skills: {len(skills)}")

    skill = select_skill(req.user_input, skills, req.skill_name)
    logs.append(f"selected skill: {skill.name if skill else 'none'}")

    instruction = build_instruction(req.user_input, skill)
    logs.append("instruction built")

    try:
        gemini = GeminiClient(api_key=settings.gemini_api_key, model=settings.gemini_model)
        output = gemini.run(instruction)
        logs.append("gemini execution completed")
        return RunResponse(status="success", selected_skill=skill.name if skill else None, logs=logs, output=output)
    except Exception as exc:  # noqa: BLE001
        logs.append("gemini execution failed")
        return RunResponse(
            status="error",
            selected_skill=skill.name if skill else None,
            logs=logs,
            error=str(exc),
        )
