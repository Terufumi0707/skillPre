from __future__ import annotations

from .loader import Skill


def select_skill(user_input: str, skills: list[Skill], explicit_skill_name: str | None = None) -> Skill | None:
    if explicit_skill_name:
        for skill in skills:
            if skill.name == explicit_skill_name:
                return skill

    lowered = user_input.lower()
    for skill in skills:
        if skill.name.lower() in lowered:
            return skill

    return skills[0] if skills else None


def build_instruction(user_input: str, skill: Skill | None) -> str:
    if not skill:
        return user_input

    return (
        "You are an execution assistant. Follow the selected portable skill instructions carefully.\n\n"
        f"[SKILL NAME]\n{skill.name}\n\n"
        f"[SKILL DESCRIPTION]\n{skill.description}\n\n"
        f"[SKILL BODY]\n{skill.body}\n\n"
        f"[USER REQUEST]\n{user_input}"
    )
