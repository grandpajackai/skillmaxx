<!-- SPDX-License-Identifier: Apache-2.0 AND CC-BY-4.0 -->
<!-- Copyright (c) 2026 NVIDIA Corporation. All rights reserved. -->

# NVIDIA Agent Skills

**Official, NVIDIA-verified Agent Skills for Claude Code, Codex, and other coding agents.**

[![NVIDIA](https://img.shields.io/badge/NVIDIA-Verified-76B900?style=flat&logo=nvidia&logoColor=white)](https://nvidia.com)
[![Agent Skills Spec](https://img.shields.io/badge/Agent%20Skills-Specification-blue)](https://agentskills.io)
[![License](https://img.shields.io/badge/License-Apache%202.0%20%2B%20CC--BY--4.0-green.svg)](#license)

> 📖 **Docs:** [docs.nvidia.com/skills](https://docs.nvidia.com/skills) &nbsp;·&nbsp;
> 📺 **Livestream:** [From Vulnerable to Verified](https://www.youtube.com/watch?v=sVpKonYJ4D4&list=PL5B692fm6--vEL0FwctKghCpyEnBGAQJA&index=1) &nbsp;·&nbsp;
> 📝 **Blog:** [NVIDIA Verified Agent Skills: Capability Governance for AI Agents](https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/)

---

Skills are portable instruction sets that teach AI agents how to use NVIDIA software optimally: Physical AI and robotics workflows, simulation, CUDA-X libraries, RAG and AI Blueprints, and platform tools. This repository is a catalog: skills are maintained in their respective product repos, and mirrored here daily via an automated sync pipeline. Skills are being added continuously, so check back for updates. We are building this infrastructure in the open, and contributions are welcome. See the [Roadmap](#roadmap) for what is planned next.

---

## Quickstart

Install NVIDIA skills with the default [`skills` CLI](https://github.com/vercel-labs/skills) flow:

```bash
npx skills add nvidia/skills
```

The CLI runs through `npx` and prompts you to choose a skill and install destination. You do not need to clone this repo or copy skill folders by hand.

> **Requires a current `skills` CLI (v1.5.16 or newer).** Installing via `npx skills@latest add nvidia/skills` always uses the latest. On older CLIs (v1.5.15 and earlier), skills may install but not appear in Claude Code — see [Troubleshooting](docs/advanced-install.mdx#troubleshooting).

The skill is available the next time your agent loads skills and encounters a relevant task. For example, ask your agent to "solve a linear programming problem with cuOpt" and the skill guides it through the cuOpt Python API. In Claude Code, run `/reload-skills` to load newly installed skills in your current session.

### Install One Skill Without Prompts

Use this when you already know the skill name and want to skip prompts.

```bash
npx skills add nvidia/skills --skill cuopt-numerical-optimization-api --yes
```

Replace `cuopt-numerical-optimization-api` with any skill name from the [Skill Catalog](#skill-catalog).

### Install for a Specific Agent

Use `--agent` to target a specific AI coding agent. Initially, we'll support common client targets, expanding the list over time. For the full list of clients supported by the spec, see the [`skills` CLI Supported Agents table](https://github.com/vercel-labs/skills#supported-agents).

**Claude Code**

```bash
npx skills add nvidia/skills --skill cuopt-numerical-optimization-api --agent claude-code
```

**Codex**

```bash
npx skills add nvidia/skills --skill cuopt-numerical-optimization-api --agent codex
```

**Snowflake CoCo**

```bash
npx skills add nvidia/skills --skill cuopt-numerical-optimization-api --agent cortex
```

**Cursor**

```bash
npx skills add nvidia/skills --skill cuopt-numerical-optimization-api --agent cursor
```

**Kiro**

```bash
npx skills add nvidia/skills --skill cuopt-numerical-optimization-api --agent kiro-cli
```

Use `--agent` more than once to install the same skill into multiple agents.

```bash
npx skills add nvidia/skills \
  --skill cuopt-numerical-optimization-api \
  --agent claude-code \
  --agent codex \
  --agent cursor \
  --agent kiro-cli
```

### Keep Skills Up to Date

New skills land continuously, and existing ones are revised, renamed, or consolidated as the catalog evolves. Refresh what you have installed with:

```bash
npx skills update
```

Run it interactively and the CLI also flags skills that were removed or merged upstream (for example, when several skills are consolidated into one) and offers to remove the stale local copies. Use `npx skills list` to see what is installed and `npx skills check` to preview what is out of date first.

### Browse the Catalog

Use this when you want to see available NVIDIA skills before installing anything.

```bash
npx skills add nvidia/skills --list
```

For non-interactive installs, global installs, agent-specific installs, updates, removals, and fallback manual copying, see [Advanced installation](docs/advanced-install.mdx).

---

## Skill Catalog

<!-- skills-table-start -->
| Product | Description | Skills |
|---------|-------------|--------|
| **Auto Ontology** | Set up Auto Ontology, model and publish its semantic layer, and run validated text-to-SQL queries through it. | [`nvidia-ontology-setup`](skills/nvidia-ontology-setup), [`nvidia-ontology-management`](skills/nvidia-ontology-management), [`nvidia-ontology-query`](skills/nvidia-ontology-query) |
| **BioNeMo Libraries** | Accelerate cheminformatics, genomic analysis, and equivariant model development with NVIDIA GPU libraries and tools. | [`bionemo-nvmolkit-usage`](skills/bionemo-nvmolkit-usage), [`bionemo-parabricks`](skills/bionemo-parabricks), [`bionemo-genomics-workflow-acceleration`](skills/bionemo-genomics-workflow-acceleration) |
| **BioNeMo NIMs** | Run and combine BioNeMo NIM microservices for biomolecular research and drug discovery through hosted APIs or local deployments. | [`bionemo-drug-discovery-pipeline`](skills/bionemo-drug-discovery-pipeline), [`bionemo-msa-structure-prediction-pipeline`](skills/bionemo-msa-structure-prediction-pipeline), [`bionemo-openfold2-nim`](skills/bionemo-openfold2-nim), [`bionemo-molmim-nim`](skills/bionemo-molmim-nim), [`bionemo-diffdock-nim`](skills/bionemo-diffdock-nim), [`bionemo-genmol-nim`](skills/bionemo-genmol-nim), [`bionemo-evo2-nim`](skills/bionemo-evo2-nim), [`bionemo-rfdiffusion-nim`](skills/bionemo-rfdiffusion-nim), [`bionemo-rfd4-proteina-nim`](skills/bionemo-rfd4-proteina-nim), [`bionemo-openfold3-nim`](skills/bionemo-openfold3-nim), [`bionemo-proteinmpnn-nim`](skills/bionemo-proteinmpnn-nim), [`bionemo-msa-search-nim`](skills/bionemo-msa-search-nim), [`bionemo-boltz2-nim`](skills/bionemo-boltz2-nim) |
| **BioNeMo Open Models** | Apply BioNeMo open models to molecular property prediction and generative protein design. | [`bionemo-codonfm-setup`](skills/bionemo-codonfm-setup), [`bionemo-codonfm-embed`](skills/bionemo-codonfm-embed), [`bionemo-codonfm-score`](skills/bionemo-codonfm-score), [`bionemo-codonfm-finetune`](skills/bionemo-codonfm-finetune), [`bionemo-complexa-evaluate-pdbs`](skills/bionemo-complexa-evaluate-pdbs), [`bionemo-complexa-sweep`](skills/bionemo-complexa-sweep), [`bionemo-complexa-target`](skills/bionemo-complexa-target), [`bionemo-kermt-add-cmim-pretrain`](skills/bionemo-kermt-add-cmim-pretrain), [`bionemo-kermt-continue-pretrain`](skills/bionemo-kermt-continue-pretrain), [`bionemo-kermt-embed`](skills/bionemo-kermt-embed), [`bionemo-kermt-finetune`](skills/bionemo-kermt-finetune), [`bionemo-kermt-infer`](skills/bionemo-kermt-infer), [`bionemo-kermt-monitor`](skills/bionemo-kermt-monitor), [`bionemo-kermt-pretrain-scratch`](skills/bionemo-kermt-pretrain-scratch), [`bionemo-kermt-setup`](skills/bionemo-kermt-setup) |
| **CDF AnomalyGen** | Run Cosmos Data Factory AnomalyGen workflows for fine-tuning, synthetic defect generation, evaluation, refinement, and pseudo-labeling. | [`cdf-anomalygen`](skills/cdf-anomalygen) |
| **CDF Augmentation** | Author, validate, and run Cosmos Data Factory augmentation pipelines for image and video generation and transformation. | [`cdf-augmentation`](skills/cdf-augmentation) |
| **CDF Auto-Labeling** | Build and run Cosmos Data Factory auto-labeling pipelines for video enhancement, tracking, captioning, and question generation. | [`cdf-auto-labeling`](skills/cdf-auto-labeling) |
| **CDF Curation and Retrieval** | Author, validate, and run Cosmos Data Factory curation and retrieval pipelines. | [`cdf-curation-and-retrieval`](skills/cdf-curation-and-retrieval) |
| **CDF Simulation** | Build and validate Cosmos Data Factory Simulation jobs and compiled payloads for PCB-AOI workflows. | [`cdf-simulation`](skills/cdf-simulation) |
| **Cosmos Data Factory Orchestration** | Build, run and monitor Cosmos Data Factory pipelines for image and video generation and transformation. | [`cdf-orchestration-preflight`](skills/cdf-orchestration-preflight), [`cdf-orchestration-setup`](skills/cdf-orchestration-setup), [`cdf-orchestration-write-dag`](skills/cdf-orchestration-write-dag), [`cdf-autonomous-vehicle-dataset-generation`](skills/cdf-autonomous-vehicle-dataset-generation), [`cdf-defect-image-generation`](skills/cdf-defect-image-generation), [`cdf-event-video-generation`](skills/cdf-event-video-generation), [`cdf-image-attribute-augmentation`](skills/cdf-image-attribute-augmentation), [`cdf-video-data-augmentation`](skills/cdf-video-data-augmentation) |
| **CUDA-Q** | Use for CUDA-Q setup, simulation targets, QPU access, and @cudaq.kernel authoring guidance. | [`cudaq-guide`](skills/cudaq-guide), [`cudaq-importing`](skills/cudaq-importing) |
| **cuDF** | Official NVIDIA-authored guidance for NVIDIA cuDF GPU DataFrames, pandas acceleration, dask-cuDF, ETL, joins, groupby, CSV/Parquet I/O, nullable semantics, and multi-GPU DataFrame workloads. | [`accelerated-computing-cudf`](skills/accelerated-computing-cudf) |
| **cuOpt** | GPU-accelerated optimization — vehicle routing, linear programming, quadratic programming, installation, server deployment, and developer tools. | [`cuopt-install`](skills/cuopt-install), [`cuopt-multi-objective-exploration`](skills/cuopt-multi-objective-exploration), [`cuopt-numerical-optimization-api`](skills/cuopt-numerical-optimization-api), [`cuopt-numerical-optimization-formulation`](skills/cuopt-numerical-optimization-formulation), [`cuopt-routing-api-python`](skills/cuopt-routing-api-python), [`cuopt-server-api-python`](skills/cuopt-server-api-python) |
| **DALI** | GPU-accelerated data loading and processing with NVIDIA DALI. | [`dali-dynamic-mode`](skills/dali-dynamic-mode) |
| **Data Designer** | Build declarative synthetic dataset generation pipelines with NeMo Data Designer. | [`data-designer`](skills/data-designer) |
| **DeepStream** | Agentic skills for guided DeepStream development. | [`amc-run-rtsp-calibration`](skills/amc-run-rtsp-calibration), [`amc-run-sample-calibration`](skills/amc-run-sample-calibration), [`amc-run-video-calibration`](skills/amc-run-video-calibration), [`amc-setup-calibration-stack`](skills/amc-setup-calibration-stack), [`deepstream-dev`](skills/deepstream-dev), [`deepstream-generate-pipeline`](skills/deepstream-generate-pipeline), [`deepstream-import-vision-model`](skills/deepstream-import-vision-model), [`deepstream-profile-pipeline`](skills/deepstream-profile-pipeline), [`deepstream-run-mv3dt`](skills/deepstream-run-mv3dt), [`deepstream-sop`](skills/deepstream-sop), [`rtvi-cv-customize-model`](skills/rtvi-cv-customize-model), [`rtvi-cv-scaffold-vss-service`](skills/rtvi-cv-scaffold-vss-service), [`rtvi-vlm-customize-model`](skills/rtvi-vlm-customize-model) |
| **DGX Spark Skills** | Agent guidance for DGX Spark and related GB10 system identification, troubleshooting, updates, playbooks, NVIDIA Sync, diagnostics, and support. | [`dgx-spark-skills`](skills/dgx-spark-skills) |
| **Digital Health** | Agent skills for (1) the clinical ASR evaluation flywheel — term curation, synthetic clinical-speech benchmark generation, KER (Keyword Error Rate) scoring, and fine-tune guidance; (2) the ambient healthcare agent creation with Nemotron Voice Agent. | [`digital-health-clinical-asr-setup`](skills/d