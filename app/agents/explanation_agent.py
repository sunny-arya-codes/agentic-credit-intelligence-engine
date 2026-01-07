from typing import Dict, List


class ExplanationAgent:
    """
    Converts structured credit reasoning output
    into a clear, audit-friendly explanation.
    """

    def generate_explanation(self, reasoning_output: Dict) -> Dict:
        risk_level = reasoning_output.get("risk_level")
        missed_payments = reasoning_output.get("missed_payments", 0)
        rule_applied = reasoning_output.get("rule_applied")

        summary = f"Customer is classified as {risk_level} credit risk."

        details: List[str] = []

        if missed_payments > 0:
            details.append(
                f"{missed_payments} missed payment(s) were detected on active loans."
            )
        else:
            details.append(
                "No missed payments were detected on active loans."
            )

        details.append(
            f"Risk classification was determined using rule: {rule_applied}."
        )

        return {
            "summary": summary,
            "details": details,
            "audit_metadata": {
                "rule_applied": rule_applied,
                "missed_payments": missed_payments,
            },
        }
