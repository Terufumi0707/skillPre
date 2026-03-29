from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


@dataclass
class Skill:
    name: str
    description: str
    body: str
    path: Path


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return {}, text

    raw_meta, body = match.groups()
    meta: dict[str, str] = {}
    for line in raw_meta.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")

    return meta, body.strip()


def _is_hidden(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts)


def load_skills(skills_dir: str) -> list[Skill]:
    root = Path(skills_dir)
    if not root.exists():
        return []

    result: list[Skill] = []
    for skill_file in root.rglob("SKILL.md"):
        if _is_hidden(skill_file.relative_to(root)):
            continue

        text = skill_file.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(text)
        default_name = "/".join(skill_file.relative_to(root).parts[:-1])
        name = meta.get("name") or default_name
        description = meta.get("description", "")
        result.append(Skill(name=name, description=description, body=body, path=skill_file))

    return sorted(result, key=lambda s: s.name)
