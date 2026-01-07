from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from app.workflows.credit_decision_flow import CreditDecisionFlow

app = FastAPI(
    title="Agentic Credit Intelligence Engine",
    description="Deterministic, graph-driven credit decision workflow",
    version="0.1.0",
)

# --------------------
# Request Model
# --------------------
class CreditDecisionRequest(BaseModel):
    customer_id: str
    age: int
    credit_score: int
    loan_amount: float
    loan_status: str
    payment_amount: float
    payment_status: str
    paid_date: Optional[str] = None


# --------------------
# Workflow Initialization
# --------------------
credit_flow = CreditDecisionFlow(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password",  # move to env vars later
)


# --------------------
# API Endpoint
# --------------------
@app.post("/credit/decision")
def get_credit_decision(request: CreditDecisionRequest):
    """
    Executes the agentic credit decision workflow
    and returns a deterministic, audit-friendly result.
    """
    record = request.dict()
    return credit_flow.execute(record)
