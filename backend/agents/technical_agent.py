import csv
from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path


@dataclass
class SKU:
    sku_id: str
    cores: str
    area_sqmm: str
    insulation: str
    material: str
    voltage: str


class TechnicalAgent:
    """
    Simple Technical Agent:
    - Reads SKU data from data/sku/sku.csv
    - Extracts 'Scope of Supply' lines from RFP text
    - Matches each line to SKUs using a basic score
    """

    def __init__(self) -> None:
        self.skus: List[SKU] = self._load_skus()

    def _project_root(self) -> Path:
        # backend/agents/technical_agent.py -> backend/agents -> backend -> project root
        backend_dir = Path(__file__).resolve().parent.parent  # /backend
        return backend_dir.parent  # /hackathon-rfp

    def _load_skus(self) -> List[SKU]:
        sku_file = self._project_root() / "data" / "sku" / "sku.csv"
        if not sku_file.is_file():
            return []

        skus: List[SKU] = []
        with open(sku_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                skus.append(
                    SKU(
                        sku_id=row.get("sku_id", ""),
                        cores=row.get("cores", ""),
                        area_sqmm=row.get("area_sqmm", ""),
                        insulation=row.get("insulation", ""),
                        material=row.get("material", ""),
                        voltage=row.get("voltage", ""),
                    )
                )
        return skus

    def _extract_scope_items(self, rfp_text: str) -> List[str]:
        """
        Try to extract spec lines:
        1) Prefer lines under 'Scope of Supply' / 'Scope of Work'.
        2) If not found, fallback to any line that looks like a cable spec
           (contains 'core' and 'sqmm' or 'cable').
        """
        lines = rfp_text.splitlines()
        items: List[str] = []
        in_scope = False

        # First pass: try to find a scope block
        for line in lines:
            stripped = line.strip()
            lower = stripped.lower()

            if not in_scope:
                if "scope of supply" in lower or "scope of work" in lower:
                    in_scope = True
                continue

            if stripped == "" or lower.startswith("testing") or lower.startswith("general"):
                break

            if stripped.startswith(("-", "•")):
                stripped = stripped.lstrip("-• ").strip()

            if stripped:
                items.append(stripped)

        # Fallback: if nothing found, try to pick 'spec-like' lines
        if not items:
            for line in lines:
                stripped = line.strip()
                lower = stripped.lower()
                if (
                    "core" in lower
                    and ("sqmm" in lower or "sq mm" in lower)
                ) or "cable" in lower:
                    if stripped.startswith(("-", "•")):
                        stripped = stripped.lstrip("-• ").strip()
                    if stripped:
                        items.append(stripped)

        return items

    def _score_match(self, spec_line: str, sku: SKU) -> int:
        """
        Naive matching: check cores, area, insulation, material.
        """
        spec = spec_line.lower()
        score = 0

        if sku.cores and sku.cores in spec:
            score += 30
        if sku.area_sqmm and sku.area_sqmm in spec:
            score += 30
        if sku.insulation and sku.insulation.lower() in spec:
            score += 20
        if sku.material and sku.material.lower() in spec:
            score += 20

        return score

    def match_specs(self, rfp_text: str) -> Dict[str, Any]:
        items = self._extract_scope_items(rfp_text)
        results: List[Dict[str, Any]] = []

        for item in items:
            scored: List[Dict[str, Any]] = []
            for sku in self.skus:
                score = self._score_match(item, sku)
                if score > 0:
                    scored.append(
                        {
                            "sku_id": sku.sku_id,
                            "score": score,
                            "cores": sku.cores,
                            "area_sqmm": sku.area_sqmm,
                            "insulation": sku.insulation,
                            "material": sku.material,
                            "voltage": sku.voltage,
                        }
                    )

            scored = sorted(scored, key=lambda x: x["score"], reverse=True)[:3]

            results.append(
                {
                    "rfp_item": item,
                    "top_matches": scored,
                }
            )

        return {"items": results}
