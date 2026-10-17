# Google Cloud Storage Plugin

The official plugin for
[Google Cloud Storage](https://cloud.google.com/storage). It bundles a growing
collection of [Agent Skills](https://agentskills.io/home) with a
[Cloud Storage MCP server](#cloud-storage-mcp-server), so your coding agent gets
both vetted GCS expertise and structured tools for buckets and objects.

The skills let you work with your storage resources through natural language in
your preferred CLI or IDE: everyday bucket and object management, file-system
mounts with Cloud Storage FUSE, access-error diagnostics, security assessments,
and infrastructure code generation.

> [!NOTE]
> This plugin is under active development. More skills will be added
> over time.

> [!IMPORTANT]
> **We Want Your Feedback!** Please share your thoughts with us by
> opening an issue on
> [GitHub](https://github.com/GoogleCloudPlatform/google-cloud-storage-plugin/issues).
> Your input is invaluable and helps us improve the project for everyone.

## Contents

-   [Installation](#installation)
-   [Available Skills](#available-skills)
-   [Cloud Storage MCP Server](#cloud-storage-mcp-server)
-   [Prerequisites](#prerequisites)
-   [Authentication](#authentication)
-   [Additional Setup: GCS Security Assessment](#additional-setup-gcs-security-assessment)
-   [Example Use Cases](#example-use-cases)
-   [Security Reminder: Agent Environment Hardening](#security-reminder-agent-environment-hardening)
-   [Support](#support)
-   [Contributing](#contributing)
-   [License](#license)

## Installation

### Installing in Antigravity CLI

```bash
agy plugin install https://github.com/GoogleCloudPlatform/google-cloud-storage-plugin
```

### Installing in Claude Code

This plugin is listed in Claude Code's official marketplace, which is built in,
so no marketplace needs to be added first:

```bash
claude plugin install google-cloud-storage@claude-plugins-official
```

### Installing in Codex

Add this repository as a marketplace, then install from it:

```bash
codex plugin marketplace add GoogleCloudPlatform/google-cloud-storage-plugin
codex plugin add google-cloud-storage@google-cloud-storage
```

### Installing in Gemini CLI

```bash
gemini extensions install https://github.com/GoogleCloudPlatform/google-cloud-storage-plugin
```

### Installing Skills Only (Skills CLI)

To install the skills without the bundled
[Cloud Storage MCP server](#cloud-storage-mcp-server) or plugin configuration
(prefer a native plugin installation above for the full package), use the
[Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add GoogleCloudPlatform/google-cloud-storage-plugin
```

From the `npx` prompt, select the skills to install, or pass `--skill` to
install a single skill directly:

```bash
npx skills add GoogleCloudPlatform/google-cloud-storage-plugin --skill google-cloud-storage-basics
```

## Available Skills

-   [**Google Cloud Storage Basics**](./skills/google-cloud-storage-basics/) —
    Everyday GCS expertise: create and configure buckets; upload, download, and
    transfer data; control access; manage storage classes, lifecycle, cost, and
    data protection — via the gcloud CLI, JSON/XML APIs, client libraries,
    Terraform, or Cloud Storage MCP servers.
-   [**Google Cloud Storage Bucket Architect**](./skills/google-cloud-storage-bucket-architect/)
    — Creates Google Cloud Storage (GCS) buckets: analyzes the workload
    (sensitive data, media hosting, ingestion, web hosting, archiving, backup,
    logging, analytics, AI/ML, or general-purpose), validates project-level
    security settings, and designs a secure-by-default, cost-effective
    configuration (location, storage class, security, lifecycle) before creating
    it via gcloud, JSON/REST API, Terraform, or SDK client libraries (C++, Java,
    Python, and Go).
-   [**Google Cloud Storage FUSE**](./skills/google-cloud-storage-fuse/) — Mount
    buckets as a POSIX file system with gcsfuse: decide when to use FUSE vs.
    direct storage reads, deploy tuned mounts on GKE, Compute Engine, and Cloud
    Run, size the file, stat, and list caches, keep file writes and ML
    checkpointing safe, and diagnose slow or costly mounts with gcsfuse metrics.
-   [**Google Cloud Storage Diagnostic**](./skills/google-cloud-storage-diagnostic/)
    — Root-cause access failures: diagnose 403 Permission Denied and other
    access errors by analyzing IAM policy bindings, ACLs, Uniform Bucket-Level
    Access, Bucket-Level IP Filtering, and VPC Service Controls perimeters, then
    walk through a verified fix.
-   [**GCS Security Assessment**](./skills/gcs-security-assessment/) — Assess
    the security posture of GCS projects and buckets against Google's
    [Secure AI Framework (SAIF)](https://saif.google/secure-ai-framework/saif-map):
    correlate real telemetry signals to surface **toxic combinations** of
    vulnerabilities — scenarios where individually low-risk configurations
    combine into a critical exposure — with actionable, verified remediation.
    Needs [additional setup](#additional-setup-gcs-security-assessment) for a
    complete assessment.
-   [**Google Cloud Storage OKF**](./skills/google-cloud-storage-okf/) —
    Token-efficient search, semantic navigation, and progressive disclosure of
    unstructured or semi-structured objects (PDFs, logs, JSON/CSV dumps, media,
    large documents) in GCS using the Open Knowledge Format (OKF) and Model
    Context Protocol (MCP).

## Cloud Storage MCP Server

Installing the plugin also configures a local Cloud Storage MCP server, so your
agent can call structured storage tools instead of only shelling out to the CLI.
The server is [MCP Toolbox](https://github.com/googleapis/mcp-toolbox) running
its prebuilt `cloud-storage` tools over stdio. It starts on demand through
`npx`, so there is no binary to download, but Node.js must be installed.

It authenticates with the same Application Default Credentials as the skills
(see [Authentication](#authentication)), and needs the `roles/storage.*` roles
for the operations you call: `roles/storage.objectViewer` to read,
`roles/storage.objectAdmin` to copy, move, and delete objects, and
`roles/storage.admin` to create or delete buckets.

### Configuration

The server needs one setting:

*   `CLOUD_STORAGE_PROJECT`: the Google Cloud project it operates on.

How you supply it depends on the harness:

*   **Antigravity** and **Codex**: export it before starting your agent:

    ```bash
    export CLOUD_STORAGE_PROJECT="<your-project-id>"
    ```

*   **Claude Code**: pass `--config cloud_storage_project=<project-id>` on
    install, or run `/plugin` inside Claude Code.
*   **Gemini CLI**: prompted on install. View or update later with `gemini
    extensions config google-cloud-storage` (restart the CLI to apply).

### Available Tools

Tool                    | Description
:---------------------- | :----------------------------------------------
`list_buckets`          | List buckets in the project.
`get_bucket_metadata`   | Get a bucket's metadata.
`get_bucket_iam_policy` | Get a bucket's IAM policy.
`create_bucket`         | Create a bucket.
`delete_bucket`         | Delete an empty bucket.
`list_objects`          | List objects in a bucket.
`get_object_metadata`   | Get an object's metadata.
`read_object`           | Read UTF-8 text content (up to 8 MiB).
`download_object`       | Download an object (binary included) to a file.
`write_object`          | Write text content to an object (overwrites).
`upload_object`         | Upload a local file (binary included).
`copy_object`           | Copy an object.
`move_object`           | Rename an object; deletes the source.
`delete_object`         | Delete an object.

> [!CAUTION]
> Five of these tools destroy or overwrite data: `delete_bucket`,
> `delete_object`, `move_object` (deletes the source), `write_object`, and
> `upload_object`. Your agent must ask for explicit permission before calling
> them.

For a comparison with the Google-hosted remote Cloud Storage MCP server, which
supports Model Armor screening and IAM deny policies, see the
[MCP usage reference](./skills/google-cloud-storage-basics/references/mcp-usage.md).

If your agent reports `spawn npx ENOENT`, Node.js is not installed or `npx` is
not on your `PATH`.

### Cloud Storage OKF MCP Server

Installing the plugin also registers a second local server,
`google-cloud-storage-okf`, which serves the `peek`, `list_regions`, `expand`,
and `write_okf` tools used by the
[Google Cloud Storage OKF skill](./skills/google-cloud-storage-okf/). It is a
Python script bundled with the skill and launched through
[`uv`](https://docs.astral.sh/uv/), which installs its dependencies (`mcp`,
`google-cloud-storage`) into an isolated environment on first start, so there is
nothing to `pip install`, but `uv` must be installed.

It uses the same Application Default Credentials and `CLOUD_STORAGE_PROJECT`
setting as the Toolbox server, and needs `storage.objects.get` to read objects
and `storage.objects.update` to write OKF indices.

If your agent reports `spawn uv ENOENT`, `uv` is not installed or not on your
`PATH`.

## Prerequisites

Ensure you have the following:

*   **A Google Cloud project** with the resources you want to work with.
*   **Google Cloud SDK (gcloud CLI):**
    [Install and initialize](https://cloud.google.com/sdk/docs/install) the
    gcloud CLI and ensure
    [Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/provide-credentials-adc)
    are configured.
*   **A compatible coding agent**, such as Antigravity CLI, Claude Code, Codex,
    or Gemini CLI.
*   **[Node.js](https://nodejs.org/)**: the
    [Cloud Storage MCP server](#cloud-storage-mcp-server) runs via `npx`.
*   **[uv](https://docs.astral.sh/uv/getting-started/installation/)**: the
    [Cloud Storage OKF MCP server](#cloud-storage-okf-mcp-server) runs via `uv
    run`.

## Authentication

Before using the skills, authenticate with Google Cloud so your agent can read
your storage resources and run any changes you approve. It is recommended to run
**both** of the following commands:

```bash
gcloud auth login
gcloud auth application-default login
```

*   **`gcloud auth application-default login`** is **required**: skill scripts
    use Application Default Credentials (ADC) to generate access tokens for GCP
    API calls.
*   **`gcloud auth login`** allows the agent (or you) to run standard `gcloud`
    commands to explore configurations or dig deeper into specific resources
    beyond what the skill scripts cover.

## Additional Setup: GCS Security Assessment

The GCS Security Assessment skill runs with nothing more than working
Application Default Credentials (see [Authentication](#authentication)) — there
is no required IAM permission. However, signals the skill cannot read are
reported as `UNKNOWN`, so for a complete assessment grant the recommended
**read-only** roles covering Storage Insights telemetry (bucket/object analysis)
and project-level posture (IAM and audit config, org policies, VPC Service
Controls, and Model Armor). See **[PERMISSIONS.md](./PERMISSIONS.md)** for the
full permission tables and a ready-to-apply custom IAM role
([`gcs-security-assessment-role.yaml`](./gcs-security-assessment-role.yaml)).

> [!TIP]
> For the best analysis, we highly recommend being a
> [Storage Intelligence](https://docs.cloud.google.com/storage/docs/storage-intelligence/overview)
> customer. When Storage Intelligence is enabled, the skill can query your
> Storage Insights datasets to perform deep, bucket-level and object-level
> assessments. Without it, the skill falls back to a project-level assessment
> only.

The other skills need no permissions beyond the [prerequisites](#prerequisites)
and whatever IAM access your identity already has to the buckets you work with.

## Example Use Cases

The skills cover the full storage lifecycle — provisioning, data movement,
file-system access, access control, troub