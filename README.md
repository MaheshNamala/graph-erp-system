📌 Graph-Based ERP Query System
🚀 Overview

This project builds a graph-based data modeling and query system over ERP data such as sales orders, deliveries, billing documents, and payments.

Traditional ERP systems store data across multiple tables, making it difficult to trace relationships. This system converts that fragmented data into a connected graph and enables users to query it using natural language.

🧠 Key Features
Graph-based modeling of ERP entities
Interactive graph visualization
Natural language query interface
LLM-powered intent classification (Gemini API)
Data-backed responses (no hallucination)
Detection of broken or incomplete business flows
🏗️ Architecture
🔹 Backend
FastAPI for API development
Graph built using in-memory structure (nodes + edges)
Custom query engine for executing structured logic
🔹 Frontend
React.js
Force-directed graph visualization
Chat interface for querying
🔹 LLM Integration
Google Gemini API
Used only for intent classification
Ensures responses are grounded in actual data
🔗 Graph Data Model
Nodes (Entities)
Sales Orders
Deliveries
Billing Documents
Payments
Customers
Edges (Relationships)
Customer → Sales Order
Sales Order → Delivery
Sales Order → Billing
Billing → Payment
💬 Supported Queries

Examples of queries supported by the system:

which sales orders are not billed
which sales orders are delivered but not billed
which billing documents are not paid
trace order 740506
🛡️ Guardrails
Only dataset-related queries are allowed
Rejects unrelated or general knowledge queries
LLM is used only for classification, not answer generation

Example response:

"This system is designed to answer ERP dataset-related queries only."
⚙️ Setup Instructions
🔹 Backend Setup
cd backend
pip install -r ../requirements.txt
uvicorn backend.app.main:app --reload
🔹 Frontend Setup
cd frontend
npm install
npm start
🌐 Running the Application
Frontend: http://localhost:3000
Backend: http://127.0.0.1:8000
🤖 LLM Strategy
The LLM classifies user queries into predefined intents:
NOT_BILLED
DELIVERED_NOT_BILLED
NOT_PAID
TRACE
The backend executes deterministic logic based on the intent
A fallback mechanism is implemented for robustness
⚡ Key Design Decisions
Graph-based modeling instead of relational joins
LLM used only for understanding, not answering
Separation of intent detection and execution logic
Fail-safe fallback to handle LLM failures
📈 Future Improvements
Natural Language → SQL / Graph query generation
Reverse flow tracing (e.g., billing → order)
Aggregation queries (top customers, products)
Highlighting nodes in graph based on query
📂 AI Coding Sessions

AI usage logs are available in:

/sessions/ai_logs.md
🧪 Evaluation Focus

This project emphasizes:

Clean architecture
Graph modeling quality
LLM integration with guardrails
Real-world business logic handling
