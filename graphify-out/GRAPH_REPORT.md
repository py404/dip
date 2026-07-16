# Graph Report - .  (2026-07-16)

## Corpus Check
- Corpus is ~5,821 words - fits in a single context window. You may not need a graph.

## Summary
- 41 nodes · 40 edges · 11 communities (6 shown, 5 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.82)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Project Architecture & Tech Stack
- Agentic RAG Core
- API Health Endpoint
- Infrastructure Bootstrap
- Application Config
- Eval & Quality Stack
- MiniStack Init Script
- Workspace Root
- Docker Image

## God Nodes (most connected - your core abstractions)
1. `DIP Platform` - 22 edges
2. `Agentic Retrieval-Generation Loop` - 6 edges
3. `Automatic Quality Gates` - 3 edges
4. `MiniStack (Cloud Emulation S3/SQS/SM)` - 3 edges
5. `Settings` - 2 edges
6. `health_check()` - 2 edges
7. `Guarded Generation` - 2 edges
8. `Multi-tenancy (Tenant Isolation)` - 2 edges
9. `RAGAs (Faithfulness + Recall Eval)` - 2 edges
10. `LangSmith (Tracing)` - 2 edges

## Surprising Connections (you probably didn't know these)
- `API Service (Docker Compose)` --references--> `DIP Platform`  [INFERRED]
  docker-compose.yml → PROJECT-CONTEXT.md
- `Phase 0: Scaffolding & Bootstrap` --references--> `DIP Platform`  [INFERRED]
  TASKS.md → PROJECT-CONTEXT.md
- `Ruff (Lint + Format Hook)` --references--> `DIP Platform`  [INFERRED]
  .pre-commit-config.yaml → PROJECT-CONTEXT.md
- `ty (Type Check Hook)` --references--> `DIP Platform`  [INFERRED]
  .pre-commit-config.yaml → PROJECT-CONTEXT.md
- `DIP README Overview` --references--> `DIP Platform`  [EXTRACTED]
  README.md → PROJECT-CONTEXT.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Multi-tenant Demo Corpus** — project_context_legal_tenant, project_context_finance_tenant, project_context_healthcare_tenant [EXTRACTED 1.00]
- **RAG Quality Assurance Stack** — project_context_ragas, project_context_langsmith, project_context_automatic_quality_gates [INFERRED 0.85]
- **Local-only Infrastructure Stack** — project_context_ollama, project_context_pgvector, project_context_redis, project_context_ministack [EXTRACTED 1.00]

## Communities (11 total, 5 thin omitted)

### Community 0 - "Project Architecture & Tech Stack"
Cohesion: 0.15
Nodes (13): Ruff (Lint + Format Hook), ty (Type Check Hook), DIP Platform, Docling (Multi-modal Document Parser), Finance Tenant (Policy Q&A), Legal Tenant (Contract Review), Multi-tenant Agentic RAG, Ollama (Local LLM + Embeddings) (+5 more)

### Community 1 - "Agentic RAG Core"
Cohesion: 0.29
Nodes (7): Agentic Retrieval-Generation Loop, Guarded Generation, Healthcare Tenant (Clinical Guidelines), Hybrid Retrieval (dense + sparse + RRF), LangGraph (Agent Graph Orchestration), Multi-tenancy (Tenant Isolation), Phase 1: System Design

### Community 3 - "Infrastructure Bootstrap"
Cohesion: 0.50
Nodes (4): API Service (Docker Compose), MiniStack Service (Docker Compose), MiniStack (Cloud Emulation S3/SQS/SM), Phase 0: Scaffolding & Bootstrap

### Community 5 - "Eval & Quality Stack"
Cohesion: 0.67
Nodes (3): Automatic Quality Gates, LangSmith (Tracing), RAGAs (Faithfulness + Recall Eval)

## Knowledge Gaps
- **17 isolated node(s):** `dip-api`, `dip`, `ministack-init.sh script`, `Multi-tenant Agentic RAG`, `Hybrid Retrieval (dense + sparse + RRF)` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DIP Platform` connect `Project Architecture & Tech Stack` to `Agentic RAG Core`, `Infrastructure Bootstrap`, `Eval & Quality Stack`?**
  _High betweenness centrality (0.386) - this node is a cross-community bridge._
- **Why does `Agentic Retrieval-Generation Loop` connect `Agentic RAG Core` to `Project Architecture & Tech Stack`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `MiniStack (Cloud Emulation S3/SQS/SM)` connect `Infrastructure Bootstrap` to `Project Architecture & Tech Stack`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `DIP Platform` (e.g. with `API Service (Docker Compose)` and `Ruff (Lint + Format Hook)`) actually correct?**
  _`DIP Platform` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `dip-api`, `dip`, `ministack-init.sh script` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._