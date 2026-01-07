from typing import Dict
from neo4j import GraphDatabase


class CreditReasoningAgent:
    """
    Applies deterministic credit risk rules by reasoning
    over the knowledge graph.
    """

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def assess_risk(self, customer_id: str) -> Dict:
        """
        Determines credit risk for a given customer
        based on payment behavior.
        """
        with self.driver.session() as session:
            result = session.execute_read(
                self._calculate_missed_payments,
                customer_id
            )

        missed_payments = result["missed_payments"]

        # --------------------
        # Deterministic Rules
        # --------------------
        if missed_payments >= 2:
            risk_level = "HIGH"
            rule_applied = "MISSED_PAYMENTS_GTE_2"
        elif missed_payments == 1:
            risk_level = "MEDIUM"
            rule_applied = "MISSED_PAYMENTS_EQ_1"
        else:
            risk_level = "LOW"
            rule_applied = "NO_MISSED_PAYMENTS"

        return {
            "customer_id": customer_id,
            "risk_level": risk_level,
            "missed_payments": missed_payments,
            "rule_applied": rule_applied,
        }

    @staticmethod
    def _calculate_missed_payments(tx, customer_id: str) -> Dict:
        query = """
        MATCH (c:Customer {customer_id: $customer_id})
              -[:HAS_LOAN]->(l:Loan)
              -[:HAS_PAYMENT]->(p:Payment)
        WHERE l.status = 'ACTIVE' AND p.status = 'MISSED'
        RETURN count(p) AS missed_payments
        """
        record = tx.run(query, customer_id=customer_id).single()
        return {
            "missed_payments": record["missed_payments"] if record else 0
        }
    