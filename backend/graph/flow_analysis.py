def detect_broken_flows(graph):
    broken = []

    # Build adjacency maps
    outgoing = {}
    for edge in graph.edges:
        src = edge["source"]
        if src not in outgoing:
            outgoing[src] = []
        outgoing[src].append(edge)

    for node_id, node in graph.nodes.items():
        if node["type"] == "sales_order":

            so = node_id
            edges = outgoing.get(so, [])

            has_delivery = any(e["relation"] == "DELIVERED" for e in edges)
            has_billing = any(e["relation"] == "BILLED" for e in edges)

            if not has_delivery:
                broken.append((so, "No Delivery"))
                continue

            if not has_billing:
                broken.append((so, "No Billing"))
                continue

    # Check billing → payment
    for node_id, node in graph.nodes.items():
        if node["type"] == "billing":

            edges = outgoing.get(node_id, [])
            has_payment = any(e["relation"] == "PAID" for e in edges)

            if not has_payment:
                broken.append((node_id, "No Payment"))

    return broken