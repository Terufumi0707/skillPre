from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    user_input: str = Field(..., min_length=1, description="Prompt from end user")
    skill_name: str | None = Field(default=None, description="Optional explicit skill name")


class RunResponse(BaseModel):
    status: str
    selected_skill: str | None
    logs: list[str]
    output: str | None = None
    error: str | None = None
