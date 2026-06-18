"""Profile persistence helpers for local CogniPrint research work."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .distances import cosine_similarity


class ProfileManager:
    def __init__(self, storage_dir: Path = Path("workspace/profiles")) -> None:
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save(self, profile: dict[str, Any], label: str) -> Path:
        safe_label = _slug(label)
        payload = json.dumps(profile, ensure_ascii=False, sort_keys=True)
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
        path = self.storage_dir / f"{safe_label}-{digest}.json"
        path.write_text(json.dumps(profile, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def load(self, filepath: Path) -> dict[str, Any]:
        return json.loads(filepath.read_text(encoding="utf-8"))

    def list_profiles(self) -> list[Path]:
        return sorted(self.storage_dir.glob("*.json"))

    def find_similar(self, query_vector: list[float], threshold: float = 0.95) -> list[dict[str, Any]]:
        matches = []
        for path in self.list_profiles():
            payload = self.load(path)
            vector = payload.get("fingerprint_vector")
            if not isinstance(vector, list):
                continue
            score = cosine_similarity(query_vector, [float(value) for value in vector])
            if score >= threshold:
                matches.append({"path": str(path), "cosine_similarity": round(score, 6)})
        return sorted(matches, key=lambda item: item["cosine_similarity"], reverse=True)


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug[:64] or "profile"
