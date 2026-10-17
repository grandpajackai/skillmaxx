# Life Sciences NGS Analysis Plugin

This plugin provides a guided intake and execution layer for common next-generation sequencing analyses. It routes users from BCL or FASTQ files to public, reproducible pipelines while checking local tool availability before installing anything.

## What It Does

- Inspects sequencing inputs before asking questions.
- Asks the minimum assay-specific questions needed to choose an analysis route.
- Prefers public, runtime-installable tools and nf-core workflows where practical.
- Runs tool preflight checks before suggesting downloads or installs.
- Keeps proprietary, credentialed, or cloud-upload paths explicit instead of silently using them.
- Treats preflight as validation before executing approved local workflows where supported.
- Produces timestamped run directories with manifests, validation summaries, logs, QC reports, exact command timing/return-code detail, checksummed artifact indexes, and input-to-output lineage tables.
- Produces native visualization bundles under `visualizations/` when a lane has enough downstream data to plot.

## Included Skills

- `ngs-analysis-router`: top-level intake and routing.
- `ngs-runtime-env`: package/tool existence checks and install planning.
- `ngs-bcl-to-fastq`: BCL run-folder validation, demultiplexing, and demux metric review.
- `ngs-fastq-qc`: FASTQ quality control, trimming decisions, and MultiQC interpretation.
- `ngs-dna-variant-calling`: WGS/WES/panel variant dispatcher.
- `ngs-dna-germline-variants`: germline WGS/WES/panel variant calling and QC.
- `ngs-dna-somatic-variants`: tumor-normal and tumor-only somatic variant calling and QC.
- `ngs-dna-umi-panel-variants`: UMI, duplex, and low-frequency targeted panel workflows.
- `ngs-bulk-rnaseq`: bulk RNA-seq dispatcher.
- `ngs-bulk-rnaseq-counts-qc`: bulk RNA-seq FASTQ-to-count processing and QC.
- `ngs-bulk-rnaseq-differential-expression`: bulk RNA-seq count-matrix differential expression.
- `ngs-scrna-seq`: single-cell or single-nucleus RNA-seq FASTQ-to-count kickoff.
- `scrna-seq-qc`: embedded post-count single-cell QC, annotation, clustering, and UMAP guidance.
- `ngs-epigenomics-peaks`: ATAC-seq, ChIP-seq, CUT&RUN, and CUT&Tag dispatcher.
- `ngs-atacseq-peaks-qc`: ATAC-seq QC, peak, consensus, and differential accessibility workflows.
- `ngs-chip-cutrun-peaks-qc`: ChIP-seq, CUT&RUN, and CUT&Tag QC, control, peak, and differential binding workflows.
- `ngs-amplicon-microbiome`: 16S/18S/ITS/COI amplicon analysis kickoff.
- `ngs-shotgun-metagenomics`: shotgun metagenomics taxonomic and functional profiling kickoff.

## Capability Status

This package is intentionally mixed maturity. Use the status below when deciding what to run versus what to treat as planning guidance.

Local execution lanes:

- `ngs-fastq-qc`: plugin-owned local runner for FASTQ validation, FastQC/MultiQC execution, optional trimming, logs, summaries, and artifact indexes.
- `ngs-bulk-rnaseq-counts-qc`: plugin-owned local runner for bulk RNA-seq FASTQ validation, FastQC/MultiQC, Salmon transcript quantification, TPM/NumReads/effective-length matrices, logs, summaries, and artifact indexes.
- `ngs-bulk-rnaseq-differential-expression`: plugin-owned local runner for count-matrix validation, contrast/replicate checks, automatic DESeq2/edgeR/limma method selection, QC plots, normalized matrices, result tables, logs, summaries, and artifact indexes.
- `ngs-scrna-seq`: plugin-owned local FASTQ-to-count runner for STARsolo-backed scRNA/snRNA count generation.
- `scrna-seq-qc`: post-count QC and annotation guidance, plus a matrix-level runner for 10x-style matrices. The runner uses conservative PBMC marker fallback when no matched reference is provided, so tissue-specific annotation should be reviewed or replaced before broader use.
- `ngs-dna-variant-calling`: plugin-owned BAM/CRAM-to-VCF execution package using samtools/bcftools for focused local checks, with nf-core/sarek still preferred for full WGS/WES/panel workflows.
- `ngs-dna-germline-variants`: plugin-owned higher-fidelity germline runner for BQSR, per-sample gVCFs, and optional joint genotyping when a local GATK toolchain and matched known-sites resources are available.
- `ngs-epigenomics-peaks`: plugin-owned FASTQ validation/QC execution package for ATAC-seq, ChIP-seq, CUT&RUN, and CUT&Tag intake, with readiness artifacts for the alignment and peak-calling stage.
- `ngs-amplicon-microbiome`: plugin-owned FASTQ validation/QC execution package for marker-gene amplicon inputs, with explicit primer/taxonomy backend readiness artifacts.
- `ngs-shotgun-metagenomics`: plugin-owned FASTQ validation/QC execution package for shotgun metagenomics inputs, with explicit database-gated taxonomic profiling status.
- `ngs-bcl-to-fastq`: plugin-owned BCL run-folder and sample-sheet validator that executes BCL Convert or legacy bcl2fastq when an installed converter is available.

Dispatch lanes:

- `ngs-bulk-rnaseq`: routes users to the counts/QC runner when starting from FASTQs, or to the differential-expression runner when starting from an expression matrix.

Dispatch and subtype lanes:

- `ngs-dna-germline-variants`
- `ngs-dna-somatic-variants`
- `ngs-dna-umi-panel-variants`
- `ngs-atacseq-peaks-qc`
- `ngs-chip-cutrun-peaks-qc`

These lanes route to the shared DNA or epigenomics execution packages when a compact local run is appropriate, and remain responsible for assay-specific guidance, metadata checks, controls, and full-workflow handoff.

## Runtime Preflight

From the repo root:

```bash
python plugins/ngs-analysis/scripts/ngs_preflight.py --list
python plugins/ngs-analysis/scripts/ngs_preflight.py --pipeline bulk_rnaseq --emit-install-plan
python plugins/ngs-analysis/scripts/ngs_preflight.py --pipeline bulk_rnaseq_counts_qc --emit-install-plan
python plugins/ngs-analysis/scripts/ngs_preflight.py --pipeline bulk_rnaseq_differential_expression --emit-install-plan
python plugins/ngs-analysis/scripts/ngs_preflight.py --profile local_light --emit-install-plan
python plugins/ngs-analysis/scripts/ngs_preflight.py --tool fastqc --network-checks
python plugins/ngs-analysis/scripts/ngs_preflight.py --pipeline shotgun_metagenomics --manager micromamba --install-plan-outdir runtime_readiness/shotgun_install
```

The script checks local executables first with `PATH` lookup. Optional network checks query package indexes or container registries only when requested. It does not install packages unless `--install-missing --yes` is explicitly provided.

Use `--install-plan-outdir` for a permission-ready package handoff. It writes `install_plan.json` as the canonical review artifact and a guarded `install_commands.sh` companion generated from the same plan. The shell script exits in review-only mode unless `NGS_RUN_INSTALL_COMMANDS=1` is set after explicit user approval. Reference and database downloads remain separate and should be handled through `ngs_reference_manager.py setup-plan`.

## Pipeline Dependency Matrix

Use this matrix as a quick lane-to-package guide before running a workflow. The structured source of truth remains `references/pipeline-registry.json`; use `ngs_preflight.py --pipeline <pipeline> --emit-install-plan` to check the current machine and generate a reviewable install plan.

| Pipeline lane | Required or primary tools | Useful optional tools | Reference/database requirements |
| --- | --- | --- | --- |
| BCL-to-FASTQ | `bcl-convert` | `bcl2fastq` for legacy compatibility | Illumina run folder with `RunInfo.xml`, optional `RunParameters.xml`, `Data/Intensities/BaseCalls`, and a compatible sample sheet |
| FASTQ QC and trimming | `snakemake`, `fastqc`, `multiqc` | `fastp`, `cutadapt`, `seqkit` | FASTQ files and sample sheet or explicit sample/R1/R2 paths |
| Bulk RNA-seq counts/QC | `snakemake`, `fastqc`, `multiqc`, `salmon` | `star`, `subread`, `seqkit` | Transcriptome FASTA, genome FASTA, GTF, and optional registered genome bundle |
| Bulk RNA-seq differential expression | `Rscript` plus available DE backend packages | `DESeq2`, `edgeR`, `limma`, `marimo` review surface | Count/expression matrix, sample metadata, contrast table, and design context |
| scRNA FASTQ-to-count | `snakemake`, `STAR` or configured STAR container | `kb-python`, `cellranger` when explicitly requested and licensed | Genome FASTA, GTF, chemistry/whitelist inputs, and optional registered genome bundle |
| scRNA post-count QC | Python/R analysis environment with `scanpy` and runner dependencies | Bioconductor QC packages, `marimo` review surface | 10x-style matrix bundle, barcodes/features, metadata, and optional raw droplet matrix |
| Generic DNA variant calling | `samtools`, `bcftools` | `bwa-mem2`, `gatk`, `deepvariant` container | Reference FASTA, indexes, optional target/region, optional annotation VCF |
| Germline DNA variants | `gatk`, `samtools` | `bcftools`, `bwa-mem2`, `deepvariant` container | Matched reference FASTA, known-sites resources, optional target BED, optional cohort/joint-calling resources |
| Somatic DNA variants | `gatk`, `samtools`, `bcftools` | panel-of-normals resources | Tumor-normal or tumor-only sample sheet, reference FASTA, germline resource, optional panel of normals and target BED |
| UMI panel variants | `samtools`, `bcftools`, `fgbio` when consensus generation is needed | `bwa-mem2`, `gatk`, duplex-review helpers | Reference FASTA, target BED, UMI read structure/tags, consensus or raw UMI inputs, optional hotspot/review VCF |
| ATAC-seq peaks/QC | `bowtie2`, `samtools`, `bedtools`, `macs2`, `bamCoverage` | `computeMatrix`, `plotProfile`, `plotHeatmap`, `homer`, `multiqc` | Bowtie2 index, genome size, blacklist BED, optional TSS BED, optional registered genome bundle |
| ChIP/CUT&RUN/CUT&Tag peaks/QC | `bowtie2`, `samtools`, `bedtools`, `macs2`, `bamCoverage` | `homer`, `multiqc` | Bowtie2 index, genome size, IP/control metadata, optional blacklist/TSS annotations and registered genome bundle |
| Amplicon microbiome | `qiime2` or `dada2` | `cutadapt`, `seqkit`, `multiqc` | Primer/marker metadata, taxonomy classifier or database, sample metadata, optional ASV/taxonomy tables for review |
| Shotgun metagenomics | `kraken2`, `bracken` by default | `kneaddata`, `humann`, `metaphlan`, `seqkit`, `multiqc` | Kraken2 database, optional host-depletion reference, optional Bracken and HUMAnN databases |
| nf-core adapter | `nextflow` | `multiqc`, Docker/Singularity/Apptainer or site profile | Pipeline-specific reference/database bundle and any required container/runtime profile |

Package checks and reference/database checks are intentionally separate. Missing executables should produce an install plan; missing references or databases should produce resource readiness and setup-plan artifacts before any large download is attempted.

## FASTQ QC Local Execution

The FASTQ QC lane accepts a sample sheet or a single sample, validates FASTQ structure and pairing, runs FastQC/MultiQC through a local Snakemake workflow, and writes a standardized run envelope. By default, outputs are written under `ngs_runs/fastq_qc/` in the current working directory; pass `--outdir` to choose a different run directory.

```bash
python plugins/ngs-analysis/scripts/run_fastq_qc.py \
  --sample-sheet samplesheet.csv \
  --execute
```

Single paired sample:

```bash
python plugins/ngs-analysis/scripts/run_fastq_qc.py \
  --sample sampleA \
  --r1 sampleA_R1.fastq.gz \
  --r2 sampleA_R2.fastq.gz \
  --execute
```

Optional trimming and re-QC:

```bash
python plugins/ngs-analysis/scripts/run_fastq_qc.py \
  --sample-sheet samplesheet.csv \
  --trim-mode fastp \
  --execute
```

Each successful run writes `run_manifest.json`, `config.json`, `validation/`, `workflow/Snakefile`, `logs/`, `artifact_index.json`, `summary.md`, FastQC/MultiQC outputs, browser helpers plus `visualizations/localhost_launch_hint.txt` for the preferred localhost review path, and `qc_interpretation.json`.

## Bulk RNA-seq Counts/QC Local Execution

The bulk RNA-seq counts/QC 