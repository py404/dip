# DIP — Task Checklist (portable, cross-machine)

## Phase 0 - Project Scaffolding & Bootstrap

### Repo & tooling init

- [x] git init + create GitHub repo (private)
- [x] Add .gitignore (Python, Docker, IDE, macOS)
- [x] Add README.md skeleton (title, badges placeholder, TOC)
- [x] Add LICENSE (MIT)
- [x] Install uv for Python dependency management
- [x] Create pyproject.toml with ruff + mypy + pytest config
- [x] Install pre-commit; add .pre-commit-config.yaml (ruff, mypy, end-of-file-fixer, trailing-whitespace)
- [x] Add .editorconfig
- [x] Create folder structure: src/, tests/, docs/, infra/, scripts/
- [x] Scaffold FastAPI app with single /health endpoint
- [x] Write first pytest test asserting /health returns 200
- [x] Add Makefile targets: dev, test, lint, up, down, logs, clean
- [x] Create .env.example with placeholder vars
- [x] Add pydantic-settings config loader reading .env
- [x] Write Dockerfile.api (multi-stage: builder + slim runtime)
- [x] Write docker-compose.yml skeleton with api service only
- [x] Run make up && curl /health to confirm skeleton boots
- [x] Commit initial scaffold as first commit

### Local secrets & config baseline

- [ ] Add docker-compose service: localstack (S3, SQS, Secrets Manager, STS)
- [ ] Write scripts/localstack-init.sh to bootstrap S3 bucket + SQS queue on container start
- [ ] Add awslocal alias + Makefile target for LocalStack CLI calls
- [ ] Add startup config validation (fail fast on missing required env vars)
- [ ] Split .env.local vs .env.example
- [ ] Add asdf .tool-versions to pin Python/Node versions
- [ ] Add VS Code devcontainer.json for reproducible editor env
- [ ] Add CODEOWNERS + CONTRIBUTING.md stub
- [ ] Write scripts/seed-dev-data.sh placeholder
- [ ] Verify awslocal s3 ls works against LocalStack container
- [ ] Add docker-compose healthcheck block for localstack service
- [ ] Document 'Quickstart: git clone → make up → curl /health' in README

## Phase 1 — System Design

### Problem brief (1-pager)

- [ ] Define target user + real need (legal/finance/healthcare doc Q&A)
- [ ] Define success metrics: latency (p95), retrieval accuracy, cost per query
- [ ] Define explicit v1 scope boundaries (what's out of scope)
- [ ] Write docs/brief.md with problem statement + goals
- [ ] List non-goals explicitly to prevent scope creep
- [ ] Identify the 2-3 riskiest technical unknowns up front
- [ ] Define what 'done' looks like for v1 demo
- [ ] Sketch primary user journey in 5 steps
- [ ] Define acceptable hallucination/error tolerance
- [ ] Get brief reviewed (self-review checklist) before moving on

### 3-level diagrams

- [ ] Draw context diagram (user, API, external LLM/embedding provider)
- [ ] Draw container diagram (API, worker, pgvector, redis, LocalStack)
- [ ] Draw sequence diagram — query → retrieval → grade → (reformulate/retry) → generation → feedback
- [ ] Draw sequence diagram — document upload → chunk → embed → index
- [ ] Export diagrams as mermaid.md in docs/diagrams/
- [ ] Review diagrams against brief.md for consistency
- [ ] Add diagrams to README architecture section
- [ ] Peer-review diagrams (or self-review after 24h break)

### ADRs for hard decisions

- [ ] ADR-001: pgvector vs dedicated vector DB (Pinecone/Qdrant)
- [ ] ADR-002: chunking strategy (semantic vs fixed-size vs recursive)
- [ ] ADR-003: Celery vs Prefect vs plain asyncio for async ingestion
- [ ] ADR-004: Ollama local models vs hosted API for dev/demo
- [ ] ADR-005: multi-tenant isolation strategy (schema vs row-level vs namespace)
- [ ] ADR-006: agentic grading loop (LangGraph retrieve-grade-retry) vs fixed retrieve-then-generate chain
- [ ] Create docs/adr/ folder with ADR template
- [ ] Number + link ADRs from design.md
- [ ] Mark each ADR status: proposed/accepted/superseded

### Failure modes list

- [ ] LLM call timeout / provider outage handling
- [ ] Queue backpressure when ingestion volume spikes
- [ ] Tenant quota exceeded mid-request
- [ ] Eval gate failure blocking a legitimate CI merge
- [ ] Embedding model returns malformed/empty vector
- [ ] Partial document upload (network drop mid-stream)
- [ ] Duplicate document re-ingestion
- [ ] Postgres connection pool exhaustion
- [ ] Redis cache unavailable (cache-aside fallback)
- [ ] Prompt injection via uploaded document content
- [ ] Agentic grading loop retries indefinitely without a max-retry budget

### Scale / load back-of-envelope

- [ ] Estimate expected req/s + average payload size
- [ ] Estimate embedding throughput needed at peak ingestion
- [ ] Identify likely first bottleneck (DB writes vs LLM latency)
- [ ] Sanity-check 10x load scenario on paper
- [ ] Estimate pgvector index size at 100k/1M chunks
- [ ] Decide HNSW vs IVFFlat index tradeoff for pgvector
- [ ] Document capacity assumptions in docs/capacity.md
- [ ] Note which metrics to watch first in production

## Phase 2 — Core Local Build (Docker Compose)

### Local infra up

- [ ] Add postgres + pgvector container to docker-compose.yml
- [ ] Add redis container
- [ ] Add ollama container (pull qwen3:14b + nomic-embed-text)
- [ ] Add localstack container (S3, SQS, Secrets Manager)
- [ ] Add prefect server + worker (agent) containers for pipeline orchestration
- [ ] Add jaeger container for local tracing
- [ ] Add prometheus + grafana containers
- [ ] Write init.sql migration enabling pgvector extension
- [ ] Add alembic (or raw SQL migrations folder) for schema versioning
- [ ] Write docker-compose healthchecks for every service
- [ ] Add docker-compose.override.yml for local dev volume mounts
- [ ] Add system dependencies for Docling OCR (poppler-utils, tesseract-ocr) to Dockerfile.worker
- [ ] Verify all services boot clean via make up
- [ ] Write scripts/wait-for-it.sh for service readiness in Makefile
- [ ] Confirm ollama pull models persist via named volume
- [ ] Document full local stack topology in README

### Ingestion pipeline

- [ ] Build document upload endpoint (multipart file upload)
- [ ] Validate file type + size limits on upload
- [ ] Store raw document in LocalStack S3 bucket
- [ ] Integrate Docling for multi-modal document parsing (PDF/DOCX/PPTX/images → structured text)
- [ ] Extract tables via Docling TableFormer, preserve as structured markdown/JSON
- [ ] Extract images/figures via Docling, store alongside chunk metadata (multi-modal support)
- [ ] Add OCR fallback path for scanned/image-only documents via Docling
- [ ] Write semantic chunking function (token-aware splitting) over Docling output
- [ ] Write recursive fallback chunker for edge cases
- [ ] Generate embeddings via Ollama nomic-embed-text
- [ ] Batch embedding calls for throughput
- [ ] Write Prefect flow orchestrating parse → chunk → embed → index steps
- [ ] Configure Prefect task retries + concurrency limits (no separate broker needed)
- [ ] Deploy Prefect flow to local worker pool via prefect deploy
- [ ] Persist chunk + embedding rows to pgvector table
- [ ] Add ingestion status tracking (pending/processing/done/failed) via Prefect flow run state
- [ ] Write idempotency check to skip duplicate document re-ingestion
- [ ] Write unit tests for chunking edge cases (empty doc, huge doc, scanned PDF)
- [ ] Write integration test: upload → poll Prefect flow run → done
- [ ] Add structured logging + verify runs visible in Prefect UI dashboard

### Retrieval core

- [ ] Implement dense retrieval query against pgvector
- [ ] Implement sparse retrieval via Postgres tsvector (BM25-style)
- [ ] Implement Reciprocal Rank Fusion (RRF) to merge dense + sparse
- [ ] Add cross-encoder reranking step (local model via Ollama or HF)
- [ ] Add query expansion (rewrite query into 2-3 variants)
- [ ] Implement HyDE (hypothetical document embeddings) as optional mode
- [ ] Add top-k configurable retrieval parameter
- [ ] Add retrieval latency logging per stage (dense/sparse/rerank)
- [ ] Write unit tests for RRF fusion scoring
- [ ] Write integration test: seeded corpus → known-good query → expected chunk
- [ ] Add Redis semantic cache for repeated queries
- [ ] Cache invalidation on document re-ingestion
- [ ] Benchmark retrieval latency locally (p50/p95)
- [ ] Tune HNSW ef_search parameter for latency/recall tradeoff
- [ ] Document retrieval pipeline flow in docs/retrieval.md
- [ ] Add fallback to dense-only retrieval if sparse index unavailable

### Generation + guard rails

- [ ] Implement context window packing (fit top-k chunks within token budget)
- [ ] Build prompt template with citation markers
- [ ] Add prompt versioning system (stored + hashed prompt configs)
- [ ] Wire generation call to Ollama qwen3:14b
- [ ] Add PII redaction guard rail on input + output
- [ ] Add basic prompt-injection detection on retrieved chunk content
- [ ] Implement cited-chunk feedback capture (thumbs up/down per citation)
- [ ] Add streaming response support (SSE or WebSocket)
- [ ] Add generation timeout + retry with backoff
- [ ] Add fallback response when no relevant chunks found
- [ ] Write unit tests for context packing token-budget logic
- [ ] Write integration test: query → cited answer with correct source refs
- [ ] Log full generation trace to Jaeger
- [ ] Document guard rail behavior in docs/safety.md

### Agentic grading loop (LangGraph)

- [ ] Scaffold a LangGraph graph with nodes: retrieve, grade, generate
- [ ] Define graph state schema (query, retrieved_chunks, grade_result, retry_count)
- [ ] Implement grade node: LLM call judging whether retrieved chunks sufficiently support the query
- [ ] Add conditional edge: grade fail → reformulate node → back to retrieve
- [ ] Implement reformulate node reusing query expansion/HyDE logic from the retrieval stage
- [ ] Add a max-retry limit to prevent infinite reformulate loops
- [ ] Add conditional edge: grade pass → generate node
- [ ] Wire fallback: after max retries, return an explicit 'insufficient context' response instead of hallucinating
- [ ] Log each graph node transition to LangSmith for traceability
- [ ] Write unit tests for the grade node's pass/fail decision boundary
- [ ] Write integration test: query against a deliberately thin corpus triggers reformulate + retry
- [ ] Write integration test: unanswerable query resolves to the 'insufficient context' fallback, not a hallucination
- [ ] Benchmark added latency of the grading step vs a fixed retrieve→generate chain
- [ ] Document the LangGraph state machine (nodes + edges) in docs/agentic-loop.md

### Eval harness

- [ ] Install + configure RAGAs for faithfulness + recall scoring
- [ ] Wire LangSmith trace logging for every query
- [ ] Build golden dataset (20-30 Q&A pairs with known-good answers)
- [ ] Write eval script scoring current pipeline against golden dataset
- [ ] Store eval run results with timestamp + git commit hash
- [ ] Set baseline threshold for faithfulness + recall scores
- [ ] Write CI eval gate script (fails if scores drop below threshold)
- [ ] Add MLflow experiment tracking for eval runs over time
- [ ] Build simple eval results dashboard (table or Grafana panel)
- [ ] Write regression test simulating a bad prompt change
- [ ] Prove eval gate blocks that bad change locally
- [ ] Document eval methodology in docs/eval.md
- [ ] Add script to regenerate golden dataset from feedback data
- [ ] Version golden dataset alongside code in git

### Multi-tenancy

- [ ] Add tenant_id column to all relevant tables
- [ ] Implement tenant namespace isolation in pgvector queries
- [ ] Add per-tenant config (model choice, quota, feature flags)
- [ ] Implement quota enforcement middleware (requests/day, storage cap)
- [ ] Add tenant context propagation through async Celery tasks
- [ ] Write test proving tenant A cannot retrieve tenant B's chunks
- [ ] Add tenant onboarding script (create tenant + seed config)
- [ ] Add per-tenant usage metrics logging
- [ ] Document multi-tenancy model in docs/multi-tenancy.md

### Multi-industry test corpus (legal/finance/healthcare)

- [ ] Create dummy legal tenant docs: sample contracts, NDAs, lease agreements (synthetic, no real data)
- [ ] Create dummy finance tenant docs: sample internal policy memos, compliance thresholds (synthetic)
- [ ] Create dummy healthcare tenant docs: sample clinical guideline excerpts (synthetic, no real PHI)
- [ ] Write scripts/seed-test-corpus.sh to provision all three tenants + upload their docs
- [ ] Onboard each vertical as its own tenant via the tenant onboarding script
- [ ] Write one known-good Q&A pair per tenant for smoke testing
- [ ] Write one deliberately under-supported query per tenant to exercise the agentic grading/retry loop
- [ ] Verify tenant isolation holds across all three verticals (cross-tenant query returns nothing)
- [ ] Feed all three tenants' Q&A pairs into the golden eval dataset
- [ ] Record a short demo capture per tenant (query → cited answer, or query → grading loop catching insufficient context)
- [ ] Document corpus contents + provenance (all synthetic) in docs/test-corpus.md

## Phase 3 — Local CI/CD (Jenkins)

### Jenkins bootstrap

- [ ] Add jenkins/jenkins:lts container to a docker-compose.ci.yml on a shared cicd-net Docker network
- [ ] Mount Docker socket into Jenkins container for docker-in-docker builds
- [ ] Complete initial admin unlock + install suggested plugins
- [ ] Install Git, Pipeline, Docker Pipeline, JUnit, SonarQube Scanner, and Blue Ocean plugins
- [ ] Add sonarqube:community container to the same cicd-net network
- [ ] Generate a SonarQube token + connect it in Jenkins (Manage Jenkins → SonarQube servers)
- [ ] Configure Jenkins Configuration as Code (JCasC) file for reproducible setup
- [ ] Add credentials store entry for GitHub repo (read-only PAT)
- [ ] Configure Jenkins job trigger: 'Poll SCM' (simplest) or GitHub webhook via ngrok tunnel (real-time, closer to production)
- [ ] If using webhook: install + run ngrok, expose Jenkins 8080, add payload URL to GitHub repo webhook settings
- [ ] Verify Jenkins can clone the repo and see the Jenkinsfile
- [ ] Expose Jenkins UI on localhost:8080 and confirm login
- [ ] Add Makefile targets: ci-up, ci-down, ci-logs
- [ ] Persist Jenkins home via named volume (avoid re-setup on restart)
- [ ] Document Jenkins bootstrap steps (incl. ngrok webhook option) in docs/local-ci.md
- [ ] Add backup/export of Jenkins job config to repo (JCasC yaml)
- [ ] Smoke-test: trigger a manual empty pipeline run successfully
- [ ] Smoke-test: push a commit and confirm webhook (or poll) auto-triggers a build

### Pipeline authoring (Jenkinsfile)

- [ ] Write Jenkinsfile with declarative pipeline skeleton
- [ ] Stage: checkout scm
- [ ] Stage: lint (ruff + mypy) fails pipeline on violation
- [ ] Stage: unit tests (pytest) with JUnit XML report published
- [ ] Stage: SonarQube scan (sonar-scanner) + waitForQualityGate step
- [ ] Stage: build docker image (api + worker) tagged with git SHA
- [ ] Stage: push image to local Docker registry container
- [ ] Stage: integration tests against docker-compose stack
- [ ] Stage: eval gate — run RAGAs eval, fail build if below threshold
- [ ] Stage: security scan (trivy) on built image
- [ ] Stage: publish test + coverage + SonarQube reports as Jenkins artifacts
- [ ] Add post-build notification stage (console summary)
- [ ] Add pipeline timeout + retry configuration
- [ ] Parameterize pipeline for branch vs main behavior
- [ ] Add Jenkinsfile linting via 'jenkins-cli declarative-linter'
- [ ] Test pipeline end-to-end on a feature branch
- [ ] Test pipeline correctly fails on a broken lint commit
- [ ] Test pipeline correctly fails when SonarQube quality gate is red

### Quality gates

- [ ] Add local Docker registry container (registry:2) for built images
- [ ] Configure pipeline to require lint + tests green before build stage
- [ ] Configure SonarQube quality gate as a hard-blocking condition (fails pipeline on red gate)
- [ ] Configure eval gate as a hard-blocking stage (non-optional)
- [ ] Add branch-based logic: main triggers full pipeline, feature branch skips deploy stage
- [ ] Simulate a 'bad PR' commit and prove pipeline blocks merge locally
- [ ] Add coverage threshold check (fail under 70%)
- [ ] Add pipeline status badge generation for README (local script)
- [ ] Document full quality-gate policy in docs/local-ci.md
- [ ] Add rollback instructions if a bad image was pushed to local registry
- [ ] Verify full pipeline run end-to-end takes under 5 minutes locally

## Phase 4 — Local Kubernetes (kind/k3d)

### Helm chart authoring

- [ ] Run helm create to scaffold base chart structure
- [ ] Write Deployment template — API server
- [ ] Write Deployment template — ingestion worker
- [ ] Write Service templates (ClusterIP) for API + worker metrics
- [ ] Write ConfigMap template per tenant config
- [ ] Write PVC template for pgvector data persistence
- [ ] Write Secret template sourced from LocalStack Secrets Manager
- [ ] Parameterize replica counts, resource requests/limits in values.yaml
- [ ] Create values-local.yaml matching docker-compose env vars
- [ ] Run helm lint to validate chart syntax
- [ ] Run helm template --dry-run and review rendered manifests
- [ ] Add NOTES.txt with post-install instructions
- [ ] Add chart version + appVersion bump convention
- [ ] Write helm test hook validating /health endpoint
- [ ] Document chart structure in docs/helm.md
- [ ] Add .helmignore file

### Scaling + scheduling

- [ ] Add HPA on ingestion worker keyed on Prefect pending flow-run count (custom metric)
- [ ] Add CronJob for nightly eval runner
- [ ] Wire Secret retrieval via LocalStack SM through External Secrets or init container
- [ ] Set resource requests/limits based on local load testing
- [ ] Add PodDisruptionBudget for API deployment
- [ ] Add liveness + readiness probes to all deployments
- [ ] Test HPA scale-up under simulated load locally
- [ ] Document scaling policy in docs/helm.md

### Ingress & networking

- [ ] Install nginx-ingress controller on kind/k3d cluster
- [ ] Write Ingress resource routing to API service
- [ ] Add local /etc/hosts entry for a friendly local domain
- [ ] Verify TLS termination works with local self-signed cert (optional)
- [ ] Add NetworkPolicy restricting worker-to-DB traffic only
- [ ] Test service-to-service DNS resolution inside cluster
- [ ] Port-forward Grafana/Prometheus for local dashboard access
- [ ] Document ingress setup in docs/helm.md

### Verify on kind/k3d

- [ ] Create cluster from scratch via kind create cluster / k3d cluster create
- [ ] Run helm install against values-local.yaml on the fresh cluster
- [ ] Confirm all pods reach Running/Ready state
- [ ] Run smoke test script hitting /health through Ingress
- [ ] Run Locust load test against the cluster endpoint
- [ ] Kill a pod manually and confirm it self-heals
- [ ] Tear down cluster and rebuild from scratch to prove reproducibility
- [ ] Document full 'cluster from zero' runbook in docs/helm.md

## Phase 5 — Terraform + LocalStack (Simulated Cloud)

### Terraform modules (LocalStack-targeted)

- [ ] Install tflocal wrapper (or configure provider endpoints manually)
- [ ] Write backend.tf using local state (or S3 backend pointed at LocalStack)
- [ ] Write provider.tf with LocalStack endpoint overrides for all services
- [ ] Write module: S3 bucket for document storage
- [ ] Write module: SQS queue for ingestion events
- [ ] Write module: Secrets Manager entries for API keys
- [ ] Write module: RDS Postgres instance (pgvector) against LocalStack Pro emulation or documented as AWS-parity stub
- [ ] Write variables.tf + outputs.tf for each module
- [ ] Add terraform fmt + validate as pre-commit hook
- [ ] Write README explaining LocalStack vs real-AWS parity boundaries
- [ ] Add terraform-docs generation for module documentation
- [ ] Pin terraform + provider versions in versions.tf
- [ ] Add tfsec or checkov static scan on IaC
- [ ] Document module dependency graph

### Deploy + validate against LocalStack

- [ ] Run terraform init against LocalStack endpoints
- [ ] Run terraform plan and review resource diff
- [ ] Run terraform apply — clean run with zero manual steps
- [ ] Verify awslocal s3 ls / sqs list-queues shows created resources
- [ ] Run smoke test hitting app config sourced from LocalStack Secrets Manager
- [ ] Run terraform destroy and confirm full teardown
- [ ] Re-run terraform apply from scratch to prove idempotency
- [ ] Document 'zero real AWS cost' proof in docs/iac.md
- [ ] Add Makefile targets: tf-up, tf-down, tf-plan

## Phase 6 — Testing & Hardening

### Automated test suite

- [ ] Reach unit test coverage target (70%+) across core modules
- [ ] Write end-to-end test: upload doc → query → cited answer
- [ ] Write contract test for API request/response schemas
- [ ] Add mutation testing pass on critical retrieval logic (optional)
- [ ] Add test fixtures + factories for tenants, documents, queries
- [ ] Set up pytest markers for unit vs integration vs slow tests
- [ ] Wire full test suite into Jenkins pipeline stage
- [ ] Add flaky-test quarantine process/documentation
- [ ] Verify tests run clean on a fresh clone (no hidden local state)
- [ ] Document testing strategy in docs/testing.md
- [ ] Add snapshot tests for prompt template rendering
- [ ] Add regression test suite tied to golden eval dataset
- [ ] Verify CI test stage runtime stays under 3 minutes
- [ ] Add test coverage badge generation script

### Load & chaos testing

- [ ] Write Locust locustfile simulating realistic query traffic
- [ ] Run load test against docker-compose stack, record p50/p95/p99
- [ ] Run load test against kind/k3d cluster, compare results
- [ ] Identify + fix first bottleneck found under load
- [ ] Inject Postgres downtime (pause container) and observe app behavior
- [ ] Inject Redis downtime and confirm cache-aside fallback works
- [ ] Inject Ollama slow-response latency and confirm timeout handling
- [ ] Use pumba or toxiproxy for controlled network fault injection
- [ ] Document chaos test scenarios + observed outcomes in docs/chaos.md
- [ ] Re-run eval gate after chaos tests to confirm no regressions
- [ ] Add a resilience checklist to README
- [ ] Capture before/after latency graphs from Grafana

### Security & dependency scanning

- [ ] Run trivy image scan on api + worker images, fix high/critical findings
- [ ] Run pip-audit (or uv audit) on Python dependencies
- [ ] Add bandit static security scan for Python code
- [ ] Scan Terraform with tfsec/checkov, fix flagged issues
- [ ] Verify no secrets committed to git (gitleaks scan)
- [ ] Add dependency scan as a Jenkins pipeline stage
- [ ] Document security scan results + remediations in docs/security.md
- [ ] Verify PII redaction guard rail with adversarial test inputs

## Phase 7 — Documentation & Portfolio Packaging

### Documentation

- [ ] Write full README with architecture diagram embedded
- [ ] Write design.md linking all ADRs
- [ ] Write docs/runbook.md (how to boot each environment from zero)
- [ ] Write docs/eval.md summary with final eval scores
- [ ] Clean up docs/ folder structure + add index
- [ ] Add architecture diagram exported as PNG/SVG for README
- [ ] Proofread all docs for consistency with final implementation
- [ ] Add 'lessons learned' section to design.md

### Demo & presentation

- [ ] Record demo video/GIF showing upload → query → cited answer
- [ ] Record short clip of Jenkins pipeline blocking a bad PR
- [ ] Record short clip of kind cluster self-healing after pod kill
- [ ] Write a 2-minute narrated walkthrough script
- [ ] Publish demo assets in docs/demo/

### Final CI/CD proof

- [ ] Run full Jenkins pipeline green end-to-end one final time
- [ ] Confirm eval gate, security scan, and load test all pass
- [ ] Tag release v1.0.0 in git
- [ ] Archive final Jenkins build artifacts + logs
- [ ] Verify fresh-clone-to-running-demo takes under 15 minutes
