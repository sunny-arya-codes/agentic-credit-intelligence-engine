from typing import Dict

from app.agents.validation_agent import ValidationAgent
from app.agents.credit_reasoning_agent import CreditReasoningAgent
from app.agents.explanation_agent import ExplanationAgent


class CreditDecisionFlow:
    """
    Orchestrates the end-to-end credit decision workflow
    using multiple specialized agents.
    """

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.validation_agent = ValidationAgent()
        self.reasoning_agent = CreditReasoningAgent(
            neo4j_uri, neo4j_user, neo4j_password
        )
        self.explanation_agent = ExplanationAgent()

    def execute(self, record: Dict) -> Dict:
        """
        Executes validation -> reasoning -> explanation.
        """

        # --------------------
        # Step 1: Validation
        # --------------------
        validation_result = self.validation_agent.validate(record)

        if not validation_result["is_valid"]:
            return {
                "status": "FAILED",
                "errors": validation_result["errors"],
            }

        customer_id = record["customer_id"]

        # --------------------
        # Step 2: Credit Reasoning
        # --------------------
        risk_assessment = self.reasoning_agent.assess_risk(customer_id)

        # --------------------
        # Step 3: Explanation
        # --------------------
        explanation = self.explanation_agent.generate_explanation(
            risk_assessment
        )

        return {
            "status": "SUCCESS",
            "risk_assessment": risk_assessment,
            "explanation": explanation,
        }

    def close(self):
        self.reasoning_agent.close()
