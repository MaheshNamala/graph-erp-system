from collections import defaultdict


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id, node_type, properties):
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                "id": node_id,
                "type": node_type,
                "properties": properties
            }

    def add_edge(self, source, target, relation):
        # Ensure source node exists
        if source not in self.nodes:
            self.add_node(source, "unknown", {})

        # Ensure target node exists
        if target not in self.nodes:
            self.add_node(target, "unknown", {})

        self.edges.append({
            "source": source,
            "target": target,
            "relation": relation
        })


def build_graph(data):
    graph = Graph()

    # --- SALES ORDERS ---
    for name, df in data.items():
        if "salesOrder" in df.columns:
            for _, row in df.iterrows():
                so = row["salesOrder"]
                graph.add_node(f"SO_{so}", "sales_order", row.to_dict())

                if "soldToParty" in df.columns:
                    cust = row.get("soldToParty")
                    if cust:
                        graph.add_node(f"CUST_{cust}", "customer", {"id": cust})
                        graph.add_edge(f"CUST_{cust}", f"SO_{so}", "PLACED")

    # --- DELIVERY ---
    for name, df in data.items():
        if "deliveryDocument" in df.columns:
            for _, row in df.iterrows():
                delivery = row["deliveryDocument"]
                graph.add_node(f"DEL_{delivery}", "delivery", row.to_dict())

                if "referenceSdDocument" in df.columns:
                    so = row.get("referenceSdDocument")
                    if so:
                        graph.add_edge(f"SO_{so}", f"DEL_{delivery}", "DELIVERED")

    # --- BILLING ---
    for name, df in data.items():
        if "billingDocument" in df.columns:
            for _, row in df.iterrows():
                bill = row["billingDocument"]
                graph.add_node(f"BILL_{bill}", "billing", row.to_dict())

                if "referenceSdDocument" in df.columns:
                    so = row.get("referenceSdDocument")
                    if so:
                        graph.add_edge(f"SO_{so}", f"BILL_{bill}", "BILLED")

    # --- ACCOUNTING ---
    for name, df in data.items():
        if "accountingDocument" in df.columns:
            for _, row in df.iterrows():
                acc = row["accountingDocument"]
                graph.add_node(f"ACC_{acc}", "accounting", row.to_dict())

                if "invoiceReference" in df.columns:
                    bill = row.get("invoiceReference")
                    if bill:
                        graph.add_edge(f"BILL_{bill}", f"ACC_{acc}", "PAID")

    return graph