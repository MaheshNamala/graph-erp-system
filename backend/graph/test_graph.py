from backend.data_loader.load_data import load_all_data
from backend.graph.graph_builder import build_graph
from backend.graph.flow_analysis import detect_broken_flows

data = load_all_data()
graph = build_graph(data)

print("Total Nodes:", len(graph.nodes))
print("Total Edges:", len(graph.edges))

broken = detect_broken_flows(graph)

print("\nBroken Flows:")
for i, b in enumerate(broken):
    if i > 10:
        break
    print(b)

print(f"\nTotal Broken Cases: {len(broken)}")