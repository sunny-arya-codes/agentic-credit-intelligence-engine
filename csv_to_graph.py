from app.graph.loader import CreditGraphLoader

loader = CreditGraphLoader(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password"
)

loader.load_csv("data/sample_credit_data.csv")
loader.close()
