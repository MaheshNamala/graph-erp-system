from backend.llm.gemini_client import classify_query


def handle_query(query, graph):
    query_lower = query.lower()

    # 🔹 Step 1: Get intent from LLM
    intent = classify_query(query)
    print("Detected intent:", intent)

    # 🔹 Step 2: Fallback logic (VERY IMPORTANT)
    if intent == "UNKNOWN":
        if "trace" in query_lower:
            intent = "TRACE"
        elif "not billed" in query_lower:
            intent = "NOT_BILLED"
        elif "delivered but not billed" in query_lower:
            intent = "DELIVERED_NOT_BILLED"
        elif "not paid" in query_lower or "unpaid" in query_lower:
            intent = "NOT_PAID"

    # 🔹 Step 3: Build adjacency map
    outgoing = {}
    for edge in graph.edges:
        outgoing.setdefault(edge["source"], []).append(edge)

    # ==============================
    # 🔥 QUERY HANDLERS
    # ==============================

    # -------- NOT BILLED --------
    if intent == "NOT_BILLED":
        results = []

        for node_id, node in graph.nodes.items():
            if node["type"] == "sales_order":
                edges = outgoing.get(node_id, [])
                has_billing = any(e["relation"] == "BILLED" for e in edges)

                if not has_billing:
                    results.append(node_id)

        return {
            "type": "list",
            "data": results[:10],
            "message": f"Found {len(results)} sales orders with no billing"
        }

    # -------- DELIVERED BUT NOT BILLED --------
    if intent == "DELIVERED_NOT_BILLED":
        results = []

        for node_id, node in graph.nodes.items():
            if node["type"] == "sales_order":
                edges = outgoing.get(node_id, [])

                has_delivery = any(e["relation"] == "DELIVERED" for e in edges)
                has_billing = any(e["relation"] == "BILLED" for e in edges)

                if has_delivery and not has_billing:
                    results.append(node_id)

        return {
            "type": "list",
            "data": results[:10],
            "message": f"Found {len(results)} delivered but not billed orders"
        }

    # -------- BILLING WITHOUT PAYMENT --------
    if intent == "NOT_PAID":
        results = []

        for node_id, node in graph.nodes.items():
            if node["type"] == "billing":
                edges = outgoing.get(node_id, [])

                has_payment = any(e["relation"] == "PAID" for e in edges)

                if not has_payment:
                    results.append(node_id)

        return {
            "type": "list",
            "data": results[:10],
            "message": f"Found {len(results)} billing documents without payment"
        }

    # -------- TRACE FLOW --------
    if intent == "TRACE":
        words = query.split()
        target = None

        for w in words:
            if w.isdigit():
                target = f"SO_{w}"
                break

        if not target:
            return {"message": "Please provide a valid sales order ID"}

        flow = []
        current = target
        visited = set()

        while current in outgoing and current not in visited:
            visited.add(current)
            edges = outgoing[current]

            if not edges:
                break

            edge = edges[0]
            flow.append({
                "from": current,
                "relation": edge["relation"],
                "to": edge["target"]
            })

            current = edge["target"]

        return {
            "type": "flow",
            "data": flow
        }

    # -------- DEFAULT GUARDRAIL --------
    return {
        "message": "This system is designed to answer ERP dataset-related queries only."
    }