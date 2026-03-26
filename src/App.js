import React, { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";

function App() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  // Fetch graph data
  useEffect(() => {
    fetch("http://127.0.0.1:8000/graph")
      .then(res => res.json())
      .then(data => {
        const nodes = Object.values(data.nodes).map(n => ({
          id: n.id,
          group: n.type
        }));

        const links = data.edges.map(e => ({
          source: e.source,
          target: e.target,
          label: e.relation
        }));

        setGraphData({ nodes, links });
      })
      .catch(err => console.error("Graph load error:", err));
  }, []);

  // Handle query
  const handleQuery = async () => {
    if (!query.trim()) return;

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/query?q=${encodeURIComponent(query)}`
      );
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (err) {
      setResponse("Error fetching response");
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>

      {/* GRAPH SECTION */}
      <div style={{ width: "70%", borderRight: "1px solid #ccc" }}>
        <ForceGraph2D
          graphData={graphData}
          width={window.innerWidth * 0.7}
          height={window.innerHeight}
          nodeLabel="id"
          linkLabel="label"
        />
      </div>

      {/* CHAT PANEL */}
      <div
        style={{
          width: "30%",
          padding: "15px",
          background: "#f5f5f5",
          display: "flex",
          flexDirection: "column",
          zIndex: 10
        }}
      >
        <h3>Query Panel</h3>

        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Ask something..."
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "10px",
            fontSize: "14px"
          }}
        />

        <button
          onClick={handleQuery}
          style={{
            padding: "10px",
            background: "#007bff",
            color: "white",
            border: "none",
            cursor: "pointer"
          }}
        >
          Submit
        </button>

        <div
          style={{
            marginTop: "20px",
            background: "white",
            padding: "10px",
            height: "100%",
            overflowY: "auto",
            border: "1px solid #ddd"
          }}
        >
          <pre style={{ whiteSpace: "pre-wrap" }}>{response}</pre>
        </div>
      </div>

    </div>
  );
}

export default App;