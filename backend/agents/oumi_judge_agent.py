from typing import Dict, Any
from oumi import judge


class OumiJudgeAgent:
    """
    Uses Oumi LLM-as-a-Judge to score OEM recommendations.
    Acts as a reward model (RL-compatible).
    """

    def evaluate_technical_output(self, technical_result: Dict[str, Any]) -> Dict[str, Any]:
        items = technical_result.get("items", [])
        judged_items = []

        for item in items:
            rfp_item = item["rfp_item"]
            matches = item.get("top_matches", [])

            if not matches:
                judged_items.append({
                    "rfp_item": rfp_item,
                    "score": 0,
                    "reason": "No matching OEM products"
                })
                continue

            # Build evaluation prompt
            prompt = f"""
You are evaluating OEM product recommendations.

RFP Requirement:
{rfp_item}

OEM Recommendations:
{matches}

Score the quality of recommendations on a scale of 0 to 100
based on specification relevance and completeness.
Return ONLY a number.
"""

            score = judge.score(prompt)

            judged_items.append({
                "rfp_item": rfp_item,
                "judge_score": score,
                "best_sku": matches[0]["sku_id"]
            })

        return {"judged_items": judged_items}
