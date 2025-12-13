from typing import Dict, Any

try:
    from oumi import judge
    OUMI_AVAILABLE = True
except ImportError:
    OUMI_AVAILABLE = False


class OumiJudgeAgent:
    """
    Oumi LLM-as-a-Judge.
    Falls back gracefully if Oumi cannot be installed locally.
    """

    def evaluate_technical_output(self, technical_result: Dict[str, Any]) -> Dict[str, Any]:
        items = technical_result.get("items", [])
        judged_items = []

        for item in items:
            rfp_item = item.get("rfp_item", "")
            matches = item.get("top_matches", [])

            if not matches:
                judged_items.append({
                    "rfp_item": rfp_item,
                    "judge_score": 0,
                    "reason": "No SKU matches",
                    "oumi_used": False
                })
                continue

            best = matches[0]

            if OUMI_AVAILABLE:
                prompt = f"""
Evaluate the OEM recommendation quality for the RFP item.
Return a score from 0 to 100.

RFP ITEM:
{rfp_item}

OEM RECOMMENDATION:
{best}
"""
                score = judge.score(prompt)
            else:
                # Fallback deterministic reward score
                score = best.get("score", 50)

            judged_items.append({
                "rfp_item": rfp_item,
                "best_sku": best.get("sku_id"),
                "judge_score": score,
                "oumi_used": OUMI_AVAILABLE
            })

        return {"judged_items": judged_items}
