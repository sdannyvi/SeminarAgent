"""
latex_utils.py — LaTeX compilation and PDF text extraction utilities.

Handles: extracting text from PDF source papers, and compiling .tex files to PDF
via pdflatex.

Belongs to: SeminarAgent / input/output utilities.
Update when: adding support for new input formats (e.g., PPTX extraction) or
switching LaTeX compilation backends.
"""

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

import pypdf

logger = logging.getLogger(__name__)


def extract_pdf_text(pdf_path: Path, max_chars: int = 15_000) -> str:
    """Extract plain text from a PDF file, truncated to max_chars.

    Uses pypdf for extraction. Strips excessive whitespace. Truncates long
    documents so they fit within LLM context budgets.

    Args:
        pdf_path: Path to the PDF file.
        max_chars: Maximum number of characters to return.

    Returns:
        Extracted text string, truncated if necessary.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = pypdf.PdfReader(str(pdf_path))
    pages_text: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages_text.append(text)

    full_text = "\n".join(pages_text)
    # Collapse runs of whitespace/blank lines
    import re
    full_text = re.sub(r"\n{3,}", "\n\n", full_text)
    full_text = re.sub(r" {2,}", " ", full_text)

    if len(full_text) > max_chars:
        logger.warning(
            "PDF text for %s truncated from %d to %d chars",
            pdf_path.name,
            len(full_text),
            max_chars,
        )
        full_text = full_text[:max_chars] + "\n\n[...truncated...]"

    return full_text


def compile_tex(tex_path: Path, output_dir: Path | None = None) -> Path:
    """Compile a .tex file to PDF using pdflatex.

    Runs pdflatex twice (to resolve cross-references). Places the output PDF
    in output_dir (defaults to the same directory as tex_path).

    Args:
        tex_path: Path to the .tex source file.
        output_dir: Directory for the compiled PDF. Defaults to tex_path.parent.

    Returns:
        Path to the compiled PDF file.

    Raises:
        RuntimeError: If pdflatex is not found or compilation fails.
    """
    if not shutil.which("pdflatex"):
        raise RuntimeError(
            "pdflatex not found. Install TeX Live or MiKTeX to compile slides."
        )

    if not tex_path.exists():
        raise FileNotFoundError(f"TeX file not found: {tex_path}")

    out_dir = output_dir or tex_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={out_dir}",
        str(tex_path),
    ]

    for run in range(1, 3):  # Run twice for cross-references
        logger.info("pdflatex pass %d for %s", run, tex_path.name)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # Show last 40 lines of stdout which contain the error
            tail = "\n".join(result.stdout.splitlines()[-40:])
            raise RuntimeError(
                f"pdflatex failed on pass {run}:\n{tail}"
            )

    pdf_path = out_dir / tex_path.with_suffix(".pdf").name
    if not pdf_path.exists():
        raise RuntimeError(f"pdflatex ran but PDF not found at {pdf_path}")

    logger.info("Compiled PDF: %s", pdf_path)
    return pdf_path


def extract_tex_from_response(response_text: str) -> str:
    """Extract the LaTeX source from an LLM response.

    The LLM is prompted to wrap the .tex output in triple backticks with the
    'tex' language tag. This function finds and returns the content inside
    that block.

    Args:
        response_text: The raw text response from the LLM.

    Returns:
        The extracted LaTeX source string.

    Raises:
        ValueError: If no valid code block is found in the response.
    """
    import re

    # Match ```tex ... ``` or ```latex ... ```
    pattern = r"```(?:tex|latex)\s*\n(.*?)```"
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback: look for \documentclass which marks the start of LaTeX
    if "\\documentclass" in response_text:
        start = response_text.index("\\documentclass")
        # Try to find matching \end{document}
        end_marker = "\\end{document}"
        end = response_text.rfind(end_marker)
        if end != -1:
            return response_text[start : end + len(end_marker)]
        return response_text[start:]

    raise ValueError(
        "Could not find LaTeX source in LLM response. "
        "Expected a ```tex ... ``` block or \\documentclass{beamer}."
    )
