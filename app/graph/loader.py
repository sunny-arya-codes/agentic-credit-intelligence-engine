import csv
from neo4j import GraphDatabase
from app.graph.schema import CUSTOMER, LOAN, PAYMENT, HAS_LOAN, HAS_PAYMENT


class CreditGraphLoader:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_csv(self, csv_path: str):
        with self.driver.session() as session:
            with open(csv_path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    session.execute_write(self._create_graph_entities, row)

    @staticmethod
    def _create_graph_entities(tx, row: dict):
        # Create Customer
        tx.run(
            f"""
            MERGE (c:{CUSTOMER} {{customer_id: $customer_id}})
            SET c.name = $name,
                c.age = $age,
                c.credit_score = $credit_score
            """,
            customer_id=row["customer_id"],
            name=row["customer_name"],
            age=int(row["age"]),
            credit_score=int(row["credit_score"]),
        )

        # Create Loan
        tx.run(
            f"""
            MERGE (l:{LOAN} {{loan_id: $loan_id}})
            SET l.amount = $amount,
                l.status = $status
            """,
            loan_id=row["loan_id"],
            amount=float(row["loan_amount"]),
            status=row["loan_status"],
        )

        # Create relationship: Customer -> Loan
        tx.run(
            f"""
            MATCH (c:{CUSTOMER} {{customer_id: $customer_id}})
            MATCH (l:{LOAN} {{loan_id: $loan_id}})
            MERGE (c)-[:{HAS_LOAN}]->(l)
            """,
            customer_id=row["customer_id"],
            loan_id=row["loan_id"],
        )

        # Create Payment
        tx.run(
            f"""
            MERGE (p:{PAYMENT} {{payment_id: $payment_id}})
            SET p.amount = $amount,
                p.due_date = date($due_date),
                p.paid_date = CASE 
                    WHEN $paid_date = "" THEN NULL 
                    ELSE date($paid_date) 
                END,
                p.status = $status
            """,
            payment_id=row["payment_id"],
            amount=float(row["payment_amount"]),
            due_date=row["due_date"],
            paid_date=row["paid_date"],
            status=row["payment_status"],
        )

        # Create relationship: Loan -> Payment
        tx.run(
            f"""
            MATCH (l:{LOAN} {{loan_id: $loan_id}})
            MATCH (p:{PAYMENT} {{payment_id: $payment_id}})
            MERGE (l)-[:{HAS_PAYMENT}]->(p)
            """,
            loan_id=row["loan_id"],
            payment_id=row["payment_id"],
        )
