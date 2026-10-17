"""
Bioinformatics Course — MS Data Science — Fall 2026
Assignment # 01: NCBI Retrieval in Python or Biopython
A from-scratch version of the Entrez/SeqIO exercise, using only the Python standard library

Student Name: Muhammad Imran Mian
Roll Number:  MSDSF25A007
Instructor:   Dr. Shahid Manzoor
University:   PUCIT
Program:      MS Data Science

Script: retrieve_sequences_plain.py
Description:
    Fetches raw GenBank flat files from NCBI E-utilities using urllib,
    parses organism and sequence blocks using regular expressions,
    computes sequence statistics (length, GC content), and outputs
    standard FASTA files wrapped at 70 characters per line.
"""

import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


# ==============================================================================
# Helper Functions
# ==============================================================================

def get_ssl_context():
    """
    Creates an SSL context that handles institutional / proxy certificates
    while falling back safely to standard verification.
    """
    try:
        ctx = ssl.create_default_context()
        return ctx
    except Exception:
        pass
    ctx = ssl._create_unverified_context()
    return ctx


def build_eutils_url(accession: str) -> str:
    """
    Constructs the NCBI E-utilities efetch URL for the given nucleotide accession.
    URL format specified in instructions:
    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=<ACCESSION>&rettype=gb&retmode=text
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "nucleotide",
        "id": accession,
        "rettype": "gb",
        "retmode": "text"
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"


def fetch_genbank_record(accession: str, timeout: int = 20) -> str:
    """
    Fetches raw GenBank flat-file text using urllib.request.urlopen.
    Includes robust SSL certificate handling and custom user-agent.
    """
    url = build_eutils_url(accession)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Bioinformatics-MSDS/1.0 (PUCIT; MSDSF25A007)"}
    )

    # First attempt with default SSL verification
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        # If failure is due to SSL certificate verification, retry with unverified context
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            ctx = ssl._create_unverified_context()
            with urllib.request.urlopen(req, context=ctx, timeout=timeout) as response:
                return response.read().decode("utf-8", errors="replace")
        raise e


def parse_organism(genbank_text: str) -> str:
    """
    Extracts the organism scientific name from the ORGANISM line of the GenBank text
    using regular expressions.
    """
    match = re.search(r"^\s*ORGANISM\s+(.+)$", genbank_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Unknown Organism"


def parse_sequence(genbank_text: str) -> str:
    """
    Extracts the nucleotide sequence from the ORIGIN...// block,
    stripping out line numbers (digits) and whitespace using regular expressions.
    Returns uppercase nucleotide sequence.
    """
    match = re.search(r"\bORIGIN\s*\n([\s\S]*?)(?:\n\s*//|\Z)", genbank_text)
    if not match:
        return ""
    raw_sequence_block = match.group(1)
    # Strip digits and whitespace characters (spaces, tabs, newlines)
    clean_sequence = re.sub(r"[\d\s]", "", raw_sequence_block)
    return clean_sequence.upper()


def wrap_sequence(sequence: str, line_width: int = 70) -> str:
    """
    Wraps sequence string into fixed-width lines (default 70 characters).
    """
    return "\n".join(sequence[i:i + line_width] for i in range(0, len(sequence), line_width))


def write_fasta_file(accession: str, organism: str, sequence: str, output_dir: str = ".") -> str:
    """
    Writes a formatted FASTA file named <accession>.fasta.
    Includes a '>' header line followed by the sequence wrapped at 70 characters.
    """
    # Clean accession name for filename (safe across OS filesystems)
    safe_acc = accession.replace("/", "_").replace("\\", "_")
    filename = f"{safe_acc}.fasta"
    file_path = os.path.join(output_dir, filename)

    header = f">{accession} {organism}"
    wrapped_seq = wrap_sequence(sequence, line_width=70)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        f.write(wrapped_seq + "\n")

    return file_path


def compute_statistics(sequence: str):
    """
    Computes sequence length and GC content percentage directly from plain sequence string.
    """
    length = len(sequence)
    if length == 0:
        return 0, 0.0
    g_count = sequence.count("G")
    c_count = sequence.count("C")
    gc_percent = ((g_count + c_count) / length) * 100.0
    return length, gc_percent


# ==============================================================================
# Main Execution Flow
# ==============================================================================

def main():
    print("=" * 80)
    print("BIOINFORMATICS ASSIGNMENT # 01: NCBI RETRIEVAL IN PYTHON (STANDARD LIBRARY)")
    print(f"Student: Muhammad Imran Mian (Roll No: MSDSF25A007) | Uni: PUCIT")
    print("=" * 80)

    # 1. Define a list of at least 5 NCBI nucleotide accession numbers
    # We include 5 diverse valid accessions representing viruses, human genes, and bacteriophages,
    # plus 1 intentional invalid accession to test and demonstrate graceful error handling.
    accessions = [
        "NC_045512.2",   # SARS-CoV-2 reference genome (~29.9 kb)
        "NM_000518.5",   # Homo sapiens hemoglobin subunit beta (HBB) mRNA (628 bp)
        "NR_046235.3",   # Homo sapiens 45S pre-ribosomal RNA (13.3 kb, high GC%)
        "NC_001416.1",   # Escherichia phage Lambda complete genome (48.5 kb)
        "AY278741.1",    # SARS coronavirus Urbani complete genome (29.7 kb)
        "INVALID_ACC123" # Simulated invalid accession to demonstrate robust error handling
    ]

    print(f"\nProcessing {len(accessions)} accession(s)...\n")

    results = []

    for idx, acc in enumerate(accessions, start=1):
        print(f"[{idx}/{len(accessions)}] Processing Accession: {acc}")
        try:
            # 2. Build URL and fetch with urllib.request.urlopen()
            url = build_eutils_url(acc)
            print(f"  -> Requesting URL: {url}")
            raw_text = fetch_genbank_record(acc)

            # Check if NCBI returned an error message in text
            if "<error>" in raw_text.lower() or "nothing to return" in raw_text.lower():
                raise ValueError(f"NCBI returned an error or empty result for accession '{acc}'.")

            # 3. Extract organism name using regex
            organism = parse_organism(raw_text)

            # 4. Extract sequence from ORIGIN...// block, stripping digits and whitespace
            sequence = parse_sequence(raw_text)

            if not sequence:
                raise ValueError(f"No ORIGIN sequence block found in record for accession '{acc}'.")

            # 5. Write to <accession>.fasta wrapped at 70 characters per line
            fasta_path = write_fasta_file(acc, organism, sequence)
            print(f"  -> Successfully generated FASTA: {fasta_path}")

            # 6. Compute statistics
            seq_len, gc_percent = compute_statistics(sequence)

            results.append({
                "accession": acc,
                "organism": organism,
                "length": seq_len,
                "gc_percent": gc_percent,
                "status": "Success"
            })

            print(f"  -> Organism   : {organism}")
            print(f"  -> Length     : {seq_len:,} bp")
            print(f"  -> GC Content : {gc_percent:.2f}%")

        except Exception as err:
            # 7. Wrap each network request in try/except so one bad accession doesn't stop the batch
            print(f"  [ERROR] Failed to process {acc}: {err}")
            results.append({
                "accession": acc,
                "organism": "N/A",
                "length": 0,
                "gc_percent": 0.0,
                "status": f"Failed ({err.__class__.__name__})"
            })

        # 8. Short pause between requests to avoid overloading NCBI servers
        print("  -> Pausing 0.4s to respect NCBI API rate limits...\n")
        time.sleep(0.4)

    # Summary Table Output
    print("=" * 80)
    print("SUMMARY OF RETRIEVED NUCLEOTIDE RECORDS")
    print("=" * 80)
    header_fmt = "{:<16} {:<38} {:>10} {:>10}"
    print(header_fmt.format("Accession", "Organism", "Length (bp)", "GC (%)"))
    print("-" * 80)
    for r in results:
        if r["status"] == "Success":
            org_display = (r["organism"][:35] + "...") if len(r["organism"]) > 35 else r["organism"]
            print(header_fmt.format(
                r["accession"],
                org_display,
                f"{r['length']:,}",
                f"{r['gc_percent']:.2f}%"
            ))
        else:
            print(f"{r['accession']:<16} [FETCH FAILED: {r['status']}]")
    print("=" * 80)
    print("All tasks completed successfully!\n")


if __name__ == "__main__":
    main()
