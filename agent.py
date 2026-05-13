"""
agent.py — SeminarAgent main entry point.

Two generation modes:

1. --from-plan PATH  (recommended)
   Reads a pre-approved slide plan (ADYN2026_plan.md or similar) and generates
   Beamer LaTeX in multiple passes — one per chapter. Faithful to the plan.

2. Default mode
   Reads RESEARCH_CONTEXT.md + source PDFs and generates slides from scratch.
   Use for new talks before a plan has been approved.

Usage:
    python agent.py --from-plan GNNs/ADYN2026_plan.md --output adyn2026 --compile
    python agent.py --title "My Talk" --papers GNNs/my\ papers/
    python agent.py --outline-only
"""

import argparse
import logging
import re
import sys
from pathlib import Path

import anthropic
import openai

import config
from latex_utils import compile_tex, extract_pdf_text, extract_tex_from_response
from prompts import (
    PLAN_SYSTEM_PROMPT,
    SYSTEM_PROMPT,
    build_plan_preamble_prompt,
    build_plan_section_prompt,
    build_user_prompt,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------


def call_anthropic(system: str, user: str) -> str:
    """Call the Anthropic API and return the assistant text response.

    Args:
        system: System prompt string.
        user: User message string.

    Returns:
        The assistant's text response.
    """
    client = anthropic.Anthropic()
    model = config.MODELS["anthropic"]
    logger.info("Calling Anthropic %s (max_tokens=%d)", model, config.MAX_TOKENS)

    message = client.messages.create(
        model=model,
        max_tokens=config.MAX_TOKENS,
        temperature=config.TEMPERATURE,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return message.content[0].text


def call_openai(system: str, user: str) -> str:
    """Call the OpenAI API and return the assistant text response.

    Args:
        system: System prompt string.
        user: User message string.

    Returns:
        The assistant's text response.
    """
    client = openai.OpenAI()
    model = config.MODELS["openai"]
    logger.info("Calling OpenAI %s (max_tokens=%d)", model, config.MAX_TOKENS)

    response = client.chat.completions.create(
        model=model,
        max_tokens=config.MAX_TOKENS,
        temperature=config.TEMPERATURE,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content


def call_llm(system: str, user: str) -> str:
    """Dispatch LLM call to the provider configured in config.py.

    Args:
        system: System prompt string.
        user: User message string.

    Returns:
        The assistant's text response.
    """
    if config.PROVIDER == "anthropic":
        return call_anthropic(system, user)
    if config.PROVIDER == "openai":
        return call_openai(system, user)
    raise ValueError(f"Unknown provider: {config.PROVIDER!r}. Use 'anthropic' or 'openai'.")


# ---------------------------------------------------------------------------
# Context loading
# ---------------------------------------------------------------------------


def load_context_file(path: Path) -> str:
    """Read a context file from disk and return its contents.

    Args:
        path: Path to the file.

    Returns:
        File contents as a string, or an empty string with a warning if missing.
    """
    if not path.exists():
        logger.warning("Context file not found: %s", path)
        return ""
    return path.read_text(encoding="utf-8")


def collect_paper_summaries(paper_paths: list[Path]) -> list[str]:
    """Extract text from a list of PDF papers.

    Skips non-PDF files with a warning. Returns a list of extracted text
    strings, one per paper.

    Args:
        paper_paths: List of PDF file paths.

    Returns:
        List of extracted text strings.
    """
    summaries: list[str] = []
    for p in paper_paths:
        if p.suffix.lower() != ".pdf":
            logger.warning("Skipping non-PDF file: %s", p.name)
            continue
        logger.info("Extracting text from %s", p.name)
        try:
            text = extract_pdf_text(p)
            summaries.append(f"Source: {p.name}\n\n{text}")
        except Exception as exc:
            logger.warning("Failed to extract text from %s: %s", p.name, exc)
    return summaries


# ---------------------------------------------------------------------------
# Plan-based multi-pass generation
# ---------------------------------------------------------------------------

# Section headers used to split the plan into passes.
_PLAN_SECTION_MARKERS = [
    ("Opening + Chapter 1", "### Opening + Chapter 1"),
    ("Chapter 2", "### Chapter 2"),
    ("Chapter 3", "### Chapter 3"),
    ("Chapter 4", "### Chapter 4"),
    ("Backup Slides", "### Backup Slides"),
]


def _split_plan_into_sections(plan_text: str) -> dict[str, str]:
    """Split the plan markdown into sections keyed by section name.

    Uses the section markers defined in _PLAN_SECTION_MARKERS.

    Args:
        plan_text: Full contents of the plan .md file.

    Returns:
        Dict mapping section name → section text.
    """
    sections: dict[str, str] = {}
    for i, (name, marker) in enumerate(_PLAN_SECTION_MARKERS):
        start = plan_text.find(marker)
        if start == -1:
            logger.warning("Section marker not found in plan: %r", marker)
            continue
        next_markers = [
            plan_text.find(m)
            for _, m in _PLAN_SECTION_MARKERS[i + 1 :]
            if plan_text.find(m) != -1
        ]
        # Also stop at the "Missing Inputs" or "Beamer generation" sections.
        stop_markers = ["## Missing Inputs", "## Beamer generation"]
        for s in stop_markers:
            pos = plan_text.find(s)
            if pos != -1:
                next_markers.append(pos)

        end = min(next_markers) if next_markers else len(plan_text)
        sections[name] = plan_text[start:end].strip()

    return sections


def run_from_plan(plan_path: Path, output_name: str, compile_pdf: bool) -> None:
    """Generate a Beamer deck from a pre-approved slide plan using multi-pass LLM calls.

    Splits the plan into sections (Chapter 1–4 + backup), generates LaTeX frames per
    section, assembles them with a separately generated preamble, and writes the
    final .tex to output/.

    Args:
        plan_path: Path to the approved plan .md file (e.g., GNNs/ADYN2026_plan.md).
        output_name: Base name for output files (without extension).
        compile_pdf: If True, compile the assembled .tex with pdflatex.
    """
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plan_text = plan_path.read_text(encoding="utf-8")
    sections = _split_plan_into_sections(plan_text)

    if not sections:
        raise ValueError(f"Could not parse any sections from plan: {plan_path}")

    logger.info("Plan sections found: %s", list(sections.keys()))

    parts: list[str] = []

    # --- Pass 0: preamble ---
    subtitle = getattr(config, "TALK_SUBTITLE", "")
    event = getattr(config, "TALK_EVENT", "")
    preamble_prompt = build_plan_preamble_prompt(
        title=config.TALK_TITLE,
        subtitle=subtitle,
        author=config.AUTHOR,
        institute=config.INSTITUTE,
        event=event,
        theme=config.BEAMER_THEME,
        color_theme=config.BEAMER_COLOR_THEME,
    )
    logger.info("Pass 0: generating preamble")
    preamble_raw = call_llm(PLAN_SYSTEM_PROMPT, preamble_prompt)
    preamble = extract_tex_from_response(preamble_raw)
    parts.append(preamble)

    # --- Passes 1–N: one per section ---
    section_names = list(sections.keys())
    context_so_far = "Preamble and title frame generated."

    for i, name in enumerate(section_names):
        is_backup = name == "Backup Slides"
        is_last = i == len(section_names) - 1

        logger.info("Pass %d: generating %s", i + 1, name)
        section_prompt = build_plan_section_prompt(
            section_title=name,
            section_plan=sections[name],
            previous_context=context_so_far,
            is_backup=is_backup,
            close_document=is_last,
        )
        raw = call_llm(PLAN_SYSTEM_PROMPT, section_prompt)
        tex = extract_tex_from_response(raw)
        parts.append(tex)

        # Update context summary for the next pass.
        slide_count = tex.count(r"\begin{frame}")
        context_so_far = (
            f"Generated through {name} ({slide_count} frames). "
            f"Running question introduced on Slide 3; callbacks at chapter ends. "
            f"Last section: {name}."
        )

    # --- Assemble ---
    assembled = "\n\n% " + "=" * 70 + "\n\n".join(parts)
    tex_path = config.OUTPUT_DIR / f"{output_name}.tex"
    tex_path.write_text(assembled, encoding="utf-8")
    logger.info("Assembled .tex written to %s (%d chars)", tex_path, len(assembled))

    if compile_pdf:
        try:
            pdf_path = compile_tex(tex_path)
            logger.info("PDF compiled: %s", pdf_path)
        except RuntimeError as exc:
            logger.error("Compilation failed: %s", exc)
            logger.info(
                "Fix the .tex and recompile: pdflatex -output-directory output/ %s",
                tex_path,
            )


# ---------------------------------------------------------------------------
# Outline mode (lightweight pre-generation step)
# ---------------------------------------------------------------------------


def generate_outline(
    talk_title: str,
    research_context: str,
    presentation_style: str,
    audience: str,
    duration_minutes: int,
    target_slide_count: int,
) -> str:
    """Generate a slide-level outline (no LaTeX) for human review.

    Useful before committing to full LaTeX generation. Produces a numbered
    list of slide titles with one-line purposes.

    Args:
        talk_title: Talk title.
        research_context: Text of RESEARCH_CONTEXT.md.
        presentation_style: Text of CLAUDE_PRESENTATIONS.md.
        audience: Target audience description.
        duration_minutes: Talk duration.
        target_slide_count: Desired slide count.

    Returns:
        Outline text as a string.
    """
    outline_system = (
        "You are an expert research-seminar designer. Output a numbered slide-by-slide "
        "outline for a research talk. For each slide, provide: the slide number, an "
        "assertive message-style title, and one sentence describing the slide's purpose. "
        "No LaTeX. No elaboration. Just the outline."
    )
    outline_user = (
        f"Talk: {talk_title}\n"
        f"Audience: {audience}\n"
        f"Duration: {duration_minutes} min (~{target_slide_count} slides)\n\n"
        f"## Research context\n\n{research_context}\n\n"
        f"## Presentation style\n\n{presentation_style}"
    )
    return call_llm(outline_system, outline_user)


# ---------------------------------------------------------------------------
# Main generation pipeline
# ---------------------------------------------------------------------------


def run(
    talk_title: str,
    paper_paths: list[Path],
    output_name: str,
    outline_only: bool,
    compile_pdf: bool,
) -> None:
    """Run the full slide generation pipeline.

    Loads context files, optionally extracts PDF text, calls the LLM,
    saves the .tex (and outline) to output/, and optionally compiles to PDF.

    Args:
        talk_title: Title for the talk.
        paper_paths: List of PDF paper paths to use as source material.
        output_name: Base name for the output files (without extension).
        outline_only: If True, generate and save an outline but skip LaTeX.
        compile_pdf: If True, compile the .tex to PDF after generation.
    """
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load context
    research_context = load_context_file(config.CONTEXT_FILES["research"])
    presentation_style = load_context_file(config.CONTEXT_FILES["presentation_style"])

    if not research_context:
        logger.warning("RESEARCH_CONTEXT.md is empty — slides will lack domain context.")

    # Outline mode
    if outline_only:
        logger.info("Generating outline for: %s", talk_title)
        outline = generate_outline(
            talk_title=talk_title,
            research_context=research_context,
            presentation_style=presentation_style,
            audience=config.AUDIENCE,
            duration_minutes=config.TALK_DURATION_MINUTES,
            target_slide_count=config.TARGET_SLIDE_COUNT,
        )
        outline_path = config.OUTPUT_DIR / f"{output_name}_outline.md"
        outline_path.write_text(outline, encoding="utf-8")
        logger.info("Outline saved to %s", outline_path)
        print(outline)
        return

    # Collect paper summaries
    paper_summaries = collect_paper_summaries(paper_paths)
    if not paper_summaries:
        logger.warning("No source papers provided. Slides will be based on context files only.")

    # Build prompt and call LLM
    user_prompt = build_user_prompt(
        talk_title=talk_title,
        author=config.AUTHOR,
        institute=config.INSTITUTE,
        audience=config.AUDIENCE,
        duration_minutes=config.TALK_DURATION_MINUTES,
        target_slide_count=config.TARGET_SLIDE_COUNT,
        target_backup_count=config.TARGET_BACKUP_COUNT,
        beamer_theme=config.BEAMER_THEME,
        beamer_color_theme=config.BEAMER_COLOR_THEME,
        research_context=research_context,
        presentation_style=presentation_style,
        paper_summaries=paper_summaries,
    )

    logger.info("Generating slides for: %s", talk_title)
    response = call_llm(SYSTEM_PROMPT, user_prompt)

    # Extract LaTeX
    try:
        tex_source = extract_tex_from_response(response)
    except ValueError as exc:
        # Save raw response for debugging and re-raise
        raw_path = config.OUTPUT_DIR / f"{output_name}_raw_response.txt"
        raw_path.write_text(response, encoding="utf-8")
        logger.error("Failed to extract LaTeX. Raw response saved to %s", raw_path)
        raise RuntimeError(str(exc)) from exc

    # Save .tex
    tex_path = config.OUTPUT_DIR / f"{output_name}.tex"
    tex_path.write_text(tex_source, encoding="utf-8")
    logger.info("LaTeX saved to %s", tex_path)

    # Optionally compile
    if compile_pdf:
        try:
            pdf_path = compile_tex(tex_path)
            logger.info("PDF compiled: %s", pdf_path)
        except RuntimeError as exc:
            logger.error("Compilation failed: %s", exc)
            logger.info("Fix the .tex file and run: pdflatex -output-directory output/ %s", tex_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="SeminarAgent: generate LaTeX Beamer slides from a plan or research papers.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--from-plan",
        metavar="PATH",
        default=None,
        help="Path to a pre-approved slide plan .md file. "
             "Uses multi-pass generation; recommended for approved talks.",
    )
    parser.add_argument(
        "--title",
        default=config.TALK_TITLE,
        help="Talk title (overrides config.TALK_TITLE). Ignored when --from-plan is set.",
    )
    parser.add_argument(
        "--papers",
        nargs="*",
        default=[],
        metavar="PATH",
        help="PDF files or directories to use as source material. "
             "Ignored when --from-plan is set.",
    )
    parser.add_argument(
        "--output",
        default=None,
        metavar="NAME",
        help="Base name for output files (default: derived from title or plan filename)",
    )
    parser.add_argument(
        "--outline-only",
        action="store_true",
        help="Generate a slide outline only; skip LaTeX generation.",
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        help="Compile the generated .tex to PDF using pdflatex.",
    )
    parser.add_argument(
        "--provider",
        choices=["anthropic", "openai"],
        default=config.PROVIDER,
        help="LLM provider (overrides config.PROVIDER)",
    )
    return parser.parse_args()


def resolve_paper_paths(paper_args: list[str]) -> list[Path]:
    """Expand paper CLI arguments to a list of PDF file paths.

    Directories are expanded to their contained .pdf files.

    Args:
        paper_args: List of file or directory path strings from CLI.

    Returns:
        Flat list of resolved PDF Path objects.
    """
    paths: list[Path] = []
    for arg in paper_args:
        p = Path(arg)
        if p.is_dir():
            pdfs = sorted(p.glob("*.pdf"))
            logger.info("Expanding directory %s → %d PDF(s)", p, len(pdfs))
            paths.extend(pdfs)
        elif p.is_file():
            paths.append(p)
        else:
            logger.warning("Path not found, skipping: %s", arg)
    return paths


def title_to_filename(title: str) -> str:
    """Convert a talk title to a safe filename stem.

    Args:
        title: Talk title string.

    Returns:
        Lowercase, hyphenated filename stem.
    """
    import re
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")
    return slug or "seminar"


if __name__ == "__main__":
    args = parse_args()
    config.PROVIDER = args.provider

    if args.from_plan:
        plan_path = Path(args.from_plan)
        if not plan_path.exists():
            logger.error("Plan file not found: %s", plan_path)
            sys.exit(1)
        output_name = args.output or plan_path.stem.lower().replace(" ", "-")
        run_from_plan(
            plan_path=plan_path,
            output_name=output_name,
            compile_pdf=args.compile,
        )
    else:
        paper_paths = resolve_paper_paths(args.papers)
        if not paper_paths and not args.outline_only:
            logger.info(
                "No papers specified. Using default papers dir: %s",
                config.DEFAULT_PAPERS_DIR,
            )
            paper_paths = resolve_paper_paths([str(config.DEFAULT_PAPERS_DIR)])

        output_name = args.output or title_to_filename(args.title)

        run(
            talk_title=args.title,
            paper_paths=paper_paths,
            output_name=output_name,
            outline_only=args.outline_only,
            compile_pdf=args.compile,
        )
