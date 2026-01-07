from typing import Dict, List


class ValidationAgent:
    """
    Performs deterministic validation on credit-related data
    before any reasoning or scoring is applied.
    """

    ALLOWED_LOAN_STATUSES = {"ACTIVE", "CLOSED", "DEFAULT"}
    ALLOWED_PAYMENT_STATUSES = {"ON_TIME", "MISSED"}

    def validate(self, record: Dict) -> Dict:
        errors: List[str] = []

        # --------------------
        # Customer validation
        # --------------------
        if int(record.get("age", 0)) < 18:
            errors.append("Customer age must be >= 18")

        if not record.get("credit_score"):
            errors.append("Missing credit score")

        # --------------------
        # Loan validation
        # --------------------
        if float(record.get("loan_amount", 0)) <= 0:
            errors.append("Loan amount must be greater than 0")

        if record.get("loan_status") not in self.ALLOWED_LOAN_STATUSES:
            errors.append(
                f"Invalid loan status: {record.get('loan_status')}"
            )

        # --------------------
        # Payment validation
        # --------------------
        if float(record.get("payment_amount", 0)) <= 0:
            errors.append("Payment amount must be greater than 0")

        payment_status = record.get("payment_status")
        if payment_status not in self.ALLOWED_PAYMENT_STATUSES:
            errors.append(
                f"Invalid payment status: {payment_status}"
            )

        if payment_status == "ON_TIME" and not record.get("paid_date"):
            errors.append(
                "Payment marked ON_TIME but paid_date is missing"
            )

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
        }
