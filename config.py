"""
config.py — SeminarAgent configuration.

Central place for all hardcoded values: model selection, paths, Beamer defaults,
and talk metadata. Edit this file before running the agent for a new talk.

Belongs to: SeminarAgent / core configuration.
Update when: changing LLM provider, adding a new talk, or adjusting Beamer style.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# LLM settings
# ---------------------------------------------------------------------------

# Supported providers: "anthropic", "openai"
PROVIDER: str = "anthropic"

# Model identifiers per provider
MODELS: dict[str, str] = {
    "anthropic": "claude-opus-4-5",
    "openai": "gpt-4o",
}

MAX_TOKENS: int = 8000
TEMPERATURE: float = 0.3  # Low for structured LaTeX output; raise for more creative outlines

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE_DIR: Path = Path(__file__).parent
OUTPUT_DIR: Path = BASE_DIR / "output"

CONTEXT_FILES: dict[str, Path] = {
    "research": BASE_DIR / "RESEARCH_CONTEXT.md",
    "presentation_style": BASE_DIR / "CLAUDE_PRESENTATIONS.md",
    "data": BASE_DIR / "DATA.md",
}

# Default source materials directory (can be overridden via CLI)
DEFAULT_PAPERS_DIR: Path = BASE_DIR / "GNNs" / "my papers"

# ---------------------------------------------------------------------------
# Talk metadata — edit per talk
# ---------------------------------------------------------------------------

AUTHOR: str = "Dan Vilenchik"
INSTITUTE: str = "Ben-Gurion University of the Negev"
TALK_TITLE: str = "GNNs for Combinatorial Optimization"
AUDIENCE: str = "CS/ECE faculty and graduate students"

# Target duration in minutes (used in prompt to calibrate slide count)
TALK_DURATION_MINUTES: int = 50

# ---------------------------------------------------------------------------
# Beamer style
# ---------------------------------------------------------------------------

BEAMER_THEME: str = "Madrid"
BEAMER_COLOR_THEME: str = "default"
BEAMER_FONT_THEME: str = "default"

# Number of slides in main deck (agent uses this as a target)
TARGET_SLIDE_COUNT: int = 40

# Number of backup slides
TARGET_BACKUP_COUNT: int = 6
