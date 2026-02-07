---
id: 1
title: phase-iv-kubernetes-deployment-constitution-update
stage: constitution
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: claude
command: sp.constitution
labels: ["constitution", "kubernetes", "deployment", "ai-devops"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
tests: []
outcome: "Successfully updated the project constitution to reflect Phase IV requirements for local Kubernetes deployment using Minikube with AI-driven DevOps."
evaluation: "The constitution was successfully updated with all required Phase IV principles and guidelines. All placeholder tokens were replaced with concrete values, and the governance section was properly configured."
---

# PHR: Phase IV Kubernetes Deployment Constitution Update

## Original Prompt

```
# sp.constitution — Phase IV Update
## Local Kubernetes Deployment (Minikube + AI DevOps)

---

## Phase IV: Cloud-Native Local Deployment

### Objective

Deploy the **Phase III Todo Chatbot (Frontend + Backend + AI Agent)** on a **local Kubernetes cluster** using **Minikube**, following a **fully agentic, AI-assisted DevOps workflow**.
No manual infrastructure scripting is allowed.

This phase validates the ability to:
- Containerize applications using AI
- Deploy and manage Kubernetes resources using AI agents
- Apply cloud-native best practices locally

---

## Core Principles (MANDATORY)

1. **Agent-First Development**
   - All infrastructure artifacts (Dockerfiles, Helm charts, Kubernetes resources) MUST be generated via AI tools.
   - Manual authoring of Dockerfiles, YAMLs, or Helm templates is NOT allowed.

2. **Agentic Dev Stack Compliance**
   - The workflow MUST strictly follow:
     ```
     sp.specify → sp.plan → sp.tasks → sp.implement (Claude Code)
     ```
   - Each stage must be documented and reviewable.

3. **Local-Only Deployment**
   - Deployment must run on **Minikube**.
   - No cloud providers (AWS, GCP, Azure) are permitted.

4. **AI-Driven DevOps**
   - Kubernetes and Docker operations must be executed via:
     - Docker AI Agent (Gordon)
     - kubectl-ai
     - kagent
   - Direct CLI usage is allowed ONLY when AI tools are unavailable and must be justified.

---

## Required Tooling

| Category | Tool |
|--------|------|
| Containerization | Docker Desktop |
| Docker AI | Docker AI Agent (Gordon) |
| Orchestration | Kubernetes (Minikube) |
| Packaging | Helm Charts |
| AI Kubernetes Ops | kubectl-ai |
| Advanced AI Ops | kagent |
| App | Phase III Todo Chatbot |

---

## Mandatory Capabilities

### 1. Containerization
- Frontend and Backend MUST be containerized separately.
- Dockerfiles MUST be generated using:
  - Docker AI (Gordon), or
  - Claude Code prompts
- Images must be tagged and usable by Kubernetes.

---

### 2. Helm-Based Deployment
- Helm charts MUST be created for:
  - Frontend
  - Backend
- Charts MUST include:
  - Deployment
  - Service
  - values.yaml
- Charts MUST be generated via:
  - kubectl-ai and/or
  - kagent

---

### 3. Kubernetes Deployment
- Applications MUST be deployed to Minikube.
- Services must expose:
  - Frontend (NodePort or equivalent)
  - Backend (ClusterIP or equivalent)
- Scaling MUST be demonstrated using AI tools.

---

### 4. AI DevOps Operations

The following AI-powered operations MUST be demonstrated and logged:

#### Docker AI (Gordon)
```bash
docker ai "What can you do?"
docker ai "create a Dockerfile for the frontend"
docker ai "build a Docker image for backend"
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.
```

## Response Summary

The project constitution was successfully updated to reflect the Phase IV requirements for local Kubernetes deployment. The new constitution incorporates all required principles from the user's specifications:

1. Agent-First Development - requiring all infrastructure artifacts to be generated via AI tools
2. Agentic Dev Stack Compliance - following the prescribed workflow
3. Local-Only Deployment - restricting deployment to Minikube
4. AI-Driven DevOps - using Docker AI, kubectl-ai, and kagent
5. Containerization Requirements - for frontend and backend
6. Helm-Based Deployment - with proper chart structures

The constitution was updated with the proper version (1.0.0), ratification date (2026-02-05), and last amended date (2026-02-05). The Sync Impact Report was included as an HTML comment at the top of the file, indicating that the templates for plan, spec, and tasks may need updates to align with the new constitution.

The new constitution enforces AI-assisted infrastructure management for the Todo Chatbot Kubernetes deployment, ensuring consistency in development practices and compliance with the specified requirements.