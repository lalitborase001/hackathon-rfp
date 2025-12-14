import csv
from dataclasses import dataclass
from typing import Dict, Any, List
from pathlib import Path


@dataclass
class PricingRow:
    sku_id: str
    base_material_cost: float
    testing_cost: float
    currency: str


class PricingAgent:
    """
    Simple Pricing Agent:
    - Loads pricing from data/pricing/pricing.csv
    - Given a list of SKUs or technical matches, computes total cost.
    """

    def __init__(self) -> None:
        self.pricing: Dict[str, PricingRow] = self._load_pricing()

    def _project_root(self) -> Path:
        backend_dir = Path(__file__).resolve().parent.parent  # /backend
        return backend_dir.parent  # /hackathon-rfp

    def _load_pricing(self) -> Dict[str, PricingRow]:
        csv_path = self._project_root() / "data" / "pricing" / "pricing.csv"
        if not csv_path.is_file():
            return {}

        pricing: Dict[str, PricingRow] = {}
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    pricing[row["sku_id"]] = PricingRow(
                        sku_id=row["sku_id"],
                        base_material_cost=float(row["base_material_cost"]),
                        testing_cost=float(row["testing_cost"]),
                        currency=row.get("currency", "INR"),
                    )
                except Exception:
                    # skip bad rows
                    continue
        return pricing

    def price_item(self, sku_id: str, quantity: float = 1.0) -> Dict[str, Any]:
        """
        Compute price for a single SKU and quantity.
        """
        if sku_id not in self.pricing:
            return {
                "sku_id": sku_id,
                "found": False,
                "message": "No pricing available",
            }

        row = self.pricing[sku_id]
        total_material = row.base_material_cost * quantity
        total_testing = row.testing_cost * quantity
        total = total_material + total_testing

        return {
            "sku_id": row.sku_id,
            "currency": row.currency,
            "quantity": quantity,
            "base_material_cost": row.base_material_cost,
            "testing_cost": row.testing_cost,
            "total_material_cost": total_material,
            "total_testing_cost": total_testing,
            "total_cost": total,
            "found": True,
        }

    def price_from_technical_result(self, technical_result: Dict[str, Any]) -> Dict[str, Any]:
        items = technical_result.get("items", [])
        priced_items: List[Dict[str, Any]] = []
        grand_total = 0.0

        for item in items:
            rfp_item = item.get("rfp_item", "")
            top_matches = item.get("top_matches", [])

            if not top_matches:
                priced_items.append({
                    "rfp_item": rfp_item,
                    "best_match_sku": "-",
                    "match_score": "-",
                    "pricing": None,
                })
                continue

            best = top_matches[0]
            sku_id = best.get("sku_id", "")
            pricing_info = self.price_item(sku_id, quantity=1.0)

            if pricing_info.get("found"):
                grand_total += pricing_info["total_cost"]

            priced_items.append({
                "rfp_item": rfp_item,
                "best_match_sku": sku_id,
                "match_score": best.get("score", 0),
                "pricing": pricing_info,
            })

        return {
            "priced_items": priced_items,
            "grand_total": grand_total,
            "currency": "INR"
        }

