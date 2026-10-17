# NCBI Nucleotide Retrieval & Parsing (From-Scratch Python)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NCBI E-utilities](https://img.shields.io/badge/NCBI-E--utilities-green.svg)](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
[![Dependencies: Standard Library](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-brightgreen.svg)](#)

> **Bioinformatics Course — Assignment #01**  
> **Master of Science in Data Science (MSDS) — Fall 2026**  
> **Punjab University College of Information Technology (PUCIT)**  
> **Student:** Muhammad Imran Mian (Roll No: `MSDSF25A007`)  
> **Instructor:** Dr. Shahid Manzoor  

---

## 📌 Overview

Biopython's `Bio.Entrez` and `Bio.SeqIO` modules handle critical network requests, data sanitization, and flat-file parsing under high-level abstractions. 

This repository implements a **from-scratch bioinformatics retrieval and conversion pipeline** relying **strictly on the Python standard library** (`urllib`, `re`, `ssl`, `time`, `os`). It directly connects to the National Center for Biotechnology Information (NCBI) Entrez E-utilities REST API, parses raw GenBank flat-files using regular expressions, calculates sequence statistics, and formats the output into standard 70-character line-wrapped FASTA files.

---

## 🎯 Key Objectives & Features

- **Direct E-utilities REST Requests:** Programmatically constructs NCBI `efetch` URLs and issues HTTP GET requests using `urllib.request.urlopen()`.
- **Zero Third-Party Dependencies:** Pure Python standard library implementation without Biopython, requests, or external parsers.
- **Robust Regular Expression Parsing:**
  - Extracts organism taxonomic names directly from multi-line `ORGANISM` records.
  - Slices nucleotide sequences strictly bounded by the `ORIGIN` block and `//` record terminator.
  - Strips numeric line counters (`\d`) and whitespace/newlines (`\s`).
- **Standard-Compliant FASTA Formatting:** Generates `>Header` records with sequence content wrapped precisely at **70 characters per line**.
- **On-the-Fly Direct String Mathematics:** Computes exact sequence length and Guanine-Cytosine (GC) content percentages directly from raw sequence strings:
  $$\text{GC\%} = \frac{\text{Count}(\text{G}) + \text{Count}(\text{C})}{\text{Total Sequence Length}} \times 100$$
- **Production-Grade Resilience & Rate Limiting:**
  - Per-record `try/except` fault isolation (invalid queries do not crash batch execution).
  - SSL verification fallback for institutional networks and proxy chains.
  - Polite 0.4s inter-request pause adhering to NCBI API fair usage limits (< 3 requests/sec without API key).

---

## 🔬 Benchmark Dataset (Planned Accessions)

Rather than querying arbitrary accessions that may resolve to empty contigs or whole mammalian chromosomes, 5 biologically diverse benchmark accessions were selected, plus 1 simulated invalid accession to verify error recovery:

| Accession | Biological Entity | Type | Length (bp) | GC Content (%) | Description / Rationale |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **`NC_045512.2`** | SARS-CoV-2 | ssRNA Virus | 29,903 bp | 37.97% | Complete viral reference genome; moderate GC content. |
| **`NM_000518.5`** | *Homo sapiens* *HBB* mRNA | Eukaryotic mRNA | 628 bp | 51.27% | Human hemoglobin subunit beta coding transcript; balanced GC. |
| **`NR_046235.3`** | *Homo sapiens* 45S pre-rRNA | Non-coding RNA | 13,357 bp | 72.55% | Human ribosomal precursor RNA; benchmark for high-GC structural RNA. |
| **`NC_001416.1`** | Escherichia phage Lambda | dsDNA Bacteriophage | 48,502 bp | 49.86% | Canonical molecular biology model organism (~48.5 kb). |
| **`AY278741.1`** | SARS-CoV Urbani | Complete Genome | 29,727 bp | 40.80% | Historical 2003 coronavirus reference strain. |
| `INVALID_ACC123` | *Synthetic Control* | *Error Test* | 0 bp | 0.00% | Fault-injection probe confirming graceful exception handling. |

---

## 📁 Repository Structure

```text
├── Assignment#01_NCBI_Retrieval.pdf  # Official assignment prompt & rubric
├── ASSIGNMENT_REPORT.md              # Detailed submission report & Biopython comparative review
├── FASTA_GENERATION_METHODOLOGY.md   # Theoretical rationale and step-by-step methodology
├── FASTA_GENERATION_METHODOLOGY.docx # Professional Word document export
├── FASTA_GENERATION_METHODOLOGY.pdf  # PDF compilation of the methodology report
├── retrieve_sequences_plain.py       # Core execution script (Python standard library only)
├── .gitignore                        # Git exclusion rules for clean version control
├── README.md                         # Project documentation and reproduction guide
└── Output FASTA Files:
    ├── NC_045512.2.fasta             # SARS-CoV-2 complete genome FASTA (wrapped at 70 chars)
    ├── NM_000518.5.fasta             # Homo sapiens HBB mRNA FASTA
    ├── NR_046235.3.fasta             # Homo sapiens 45S pre-rRNA FASTA
    ├── NC_001416.1.fasta             # Escherichia phage Lambda FASTA
    └── AY278741.1.fasta              # SARS-CoV Urbani complete genome FASTA
```

---

## 🚀 Getting Started & Execution

### Prerequisites
- Python 3.8 or higher.
- No third-party packages required (uses built-in `urllib`, `re`, `ssl`, `time`, `os`).

### Running the Retrieval Pipeline
Clone the repository and run the script:

```bash
git clone https://github.com/memrranmian/ncbi-retrieval-from-scratch.git
cd ncbi-retrieval-from-scratch
python retrieve_sequences_plain.py
```

### Sample Console Output
```text
================================================================================
BIOINFORMATICS ASSIGNMENT # 01: NCBI RETRIEVAL IN PYTHON (STANDARD LIBRARY)
Student: Muhammad Imran Mian (Roll No: MSDSF25A007) | Uni: PUCIT
================================================================================

Processing 6 accession(s)...

[1/6] Processing Accession: NC_045512.2
  -> Requesting URL: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=NC_045512.2&rettype=gb&retmode=text
  -> Successfully generated FASTA: .\NC_045512.2.fasta
  -> Organism   : Severe acute respiratory syndrome coronavirus 2
  -> Length     : 29,903 bp
  -> GC Content : 37.97%
  -> Pausing 0.4s to respect NCBI API rate limits...

...

================================================================================
SUMMARY OF RETRIEVED NUCLEOTIDE RECORDS
================================================================================
Accession        Organism                               Length (bp)     GC (%)
--------------------------------------------------------------------------------
NC_045512.2      Severe acute respiratory syndrome c...     29,903     37.97%
NM_000518.5      Homo sapiens                                  628     51.27%
NR_046235.3      Homo sapiens                               13,357     72.55%
NC_001416.1      Escherichia phage Lambda                   48,502     49.86%
AY278741.1       SARS coronavirus Urbani                    29,727     40.80%
INVALID_ACC123   [FETCH FAILED: Failed (ValueError)]
================================================================================
All tasks completed successfully!
```

---

## ⚖️ Comparative Reflection: Plain Python vs. Biopython

> **"What did Biopython save you from writing?"**

Implementing NCBI extraction directly with Python's standard library underscores the substantial engineering abstracted away by Biopython (`Bio.Entrez` and `Bio.SeqIO`):

1. **HTTP Transport & URL Query Construction:**  
   In Biopython, `Entrez.efetch(db="nucleotide", id=acc, rettype="gb", retmode="text")` seamlessly handles parameter serialization, User-Agent formatting, API key query strings, and connection reuse. Without it, developers must build query strings manually using `urllib.parse.urlencode` and configure SSL contexts.
2. **GenBank Grammar & Delimiter Parsing:**  
   Raw GenBank files interleave sequence text with whitespace, 9-digit line counters, metadata tags, and the `//` record terminator. Writing regex queries to reliably isolate the `ORIGIN` block across varied records requires strict pattern definition. `SeqIO.read(handle, "genbank")` automates this, generating typed `SeqRecord` objects.
3. **FASTA Formatting & Statistics Utilities:**  
   Biopython abstracts sequence wrapping via `SeqIO.write()` and sequence statistics with `gc_fraction()`. In plain Python, fixed line-length slicing (wrapping at 70 characters) and nucleotide counting must be programmed by hand.

While Biopython compresses ~180 lines of boilerplate into ~25 lines, building the workflow from scratch provides vital foundational knowledge of NCBI E-utilities architectures and GenBank flat-file structures.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE) — free for educational, academic, and research use.
