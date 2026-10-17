# Bioinformatics Assignment # 01: NCBI Retrieval in Python or Biopython
**Course:** Bioinformatics Course — MS Data Science — Fall 2026  
**Institution:** Punjab University College of Information Technology (PUCIT)  
**Student Name:** Muhammad Imran Mian  
**Roll Number:** MSDSF25A007  
**Instructor:** Dr. Shahid Manzoor  

---

## 1. Executive Summary & Verification

This assignment implements an end-to-end, from-scratch pipeline in Python (`retrieve_sequences_plain.py`) using **strictly the Python standard library** (`urllib`, `re`, `ssl`, `time`, `os`). It completely replaces Biopython's `Entrez` and `SeqIO` modules to fetch, parse, calculate statistics, and format NCBI nucleotide records.

Every requirement outlined in the specification has been verified with 100% precision:
1. **At least 5 nucleotide accession numbers defined:** Tested on 5 biologically diverse accessions (`NC_045512.2`, `NM_000518.5`, `NR_046235.3`, `NC_001416.1`, `AY278741.1`), plus 1 synthetic error accession (`INVALID_ACC123`) to prove non-blocking error handling.
2. **Manual E-utilities URL Construction:** Built with `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=<ACCESSION>&rettype=gb&retmode=text` and fetched using `urllib.request.urlopen()`.
3. **Regex Extraction of Organism:** Parsed using `re.search(r"^\s*ORGANISM\s+(.+)$", genbank_text, re.MULTILINE)`.
4. **Regex Extraction of Sequence:** Extracted from the `ORIGIN...//` block and cleaned by removing line numbers (`\d`) and whitespace (`\s`) via `re.sub(r"[\d\s]", "", raw_seq).upper()`.
5. **Standard FASTA Output:** Produced `<accession>.fasta` files with a `>` header line followed by sequence wrapped precisely at **70 characters per line**.
6. **Summary Statistics:** Computed sequence length and GC content percentage directly from plain strings.
7. **Robust Error Handling:** Network queries wrapped in `try/except` blocks so that failures do not interrupt subsequent batch fetches.
8. **NCBI Politeness Interval:** Implemented `time.sleep(0.4)` between HTTP requests to adhere to NCBI E-utilities usage policies (< 3 requests/sec without API key).

---

## 2. Experimental Results & Statistics

| Accession | Description / Type | Organism | Sequence Length (bp) | GC Content (%) | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **NC_045512.2** | SARS-CoV-2 complete reference genome | *Severe acute respiratory syndrome coronavirus 2* | 29,903 bp | 37.97% | Verified |
| **NM_000518.5** | *Homo sapiens* hemoglobin subunit beta (*HBB*) mRNA | *Homo sapiens* | 628 bp | 51.27% | Verified |
| **NR_046235.3** | *Homo sapiens* RNA, 45S pre-ribosomal N4 (*RNA45SN4*) | *Homo sapiens* | 13,357 bp | 72.55% | Verified |
| **NC_001416.1** | Enterobacteria phage lambda complete genome | *Escherichia phage Lambda* | 48,502 bp | 49.86% | Verified |
| **AY278741.1** | SARS coronavirus Urbani complete genome | *SARS coronavirus Urbani* | 29,727 bp | 40.80% | Verified |
| **INVALID_ACC123** | Synthetic test record (fault injection) | N/A | 0 bp | 0.00% | Handled gracefully |

---

## 3. Comparative Analysis: Plain Python (Standard Library) vs. Biopython

> **What did Biopython save you from writing?**

Implementing NCBI retrieval and GenBank parsing purely through Python's standard library reveals the substantial low-level abstraction provided by Biopython (`Bio.Entrez` and `Bio.SeqIO`). 

Specifically, Biopython saves the developer from writing:
1. **Low-level HTTP & URL Engineering:** With Biopython, `Entrez.efetch(db="nucleotide", id=acc, rettype="gb", retmode="text")` automates URL query parameter encoding, custom User-Agent management, API key attachments, and transparent connection reuse. Without it, one must construct queries manually via `urllib.parse.urlencode` and handle request objects directly.
2. **Connection Resilience & Transport Security:** Plain `urllib` requires explicit handling of SSL context validation, institutional proxy certificates, timeout specifications, and HTTP error code parsing (e.g., handling HTTP 429 rate limit or 500 errors). Biopython bundles robust transport management out-of-the-box.
3. **Complex Flat-File Lexing & Parsing:** In raw GenBank files, extracting features without parsing tools is brittle. One must write regular expressions to capture the `ORGANISM` line, locate the `ORIGIN` delimiter, navigate multiline sequence lines, and strip leading 9-digit position counters and intermediate white spaces while ensuring the trailing `//` record terminator is respected. `SeqIO.read(handle, "genbank")` executes this automatically and constructs a structured `SeqRecord` object with fully typed attributes (`record.annotations`, `record.features`, `record.seq`).
4. **Sequence Formatting & Calculation Utilities:** Plain Python requires custom line-slicing logic to wrap sequence strings into standard 70-character FASTA lines, as well as explicit counting functions for nucleotide statistics (e.g. `(G + C) / total`). Biopython eliminates this boilerplate via `SeqIO.write(record, "output.fasta", "fasta")` and built-in sequence methods like `GC(record.seq)` or `gc_fraction(record.seq)`.

In conclusion, while Biopython minimizes boilerplate code from ~180 lines down to ~25 lines, building the workflow from scratch using `urllib` and `re` provides essential insight into the raw structure of GenBank files and the low-level mechanics of NCBI E-utilities.
