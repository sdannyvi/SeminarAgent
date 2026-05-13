# DATA.md

## Purpose

This file documents the source materials available as inputs to the seminar agent.

Before generating slides, the agent (or a human collaborator) should check what files are
available, what they contain, and which ones are authoritative for the current talk.

---

## Available Source Materials

### `GNNs/my papers/`

| File | Description | Role in talk |
|------|-------------|--------------|
| `Neuro_sat.pdf` | NeuroSAT (Selsam et al., ICLR 2019) | Core paper; main results and intuition |
| `OptGNN_elad_s (1).pdf` | OptGNN — GNN-based graph optimization | Core paper; method and approximation results |
| `graph_coloring.pdf` | GNN approach to graph coloring | Core paper; NP-hard testbed |
| `20251-AAAI26.ShohamE-ML.pdf` | AAAI 2026 submission | Most recent results; likely main focus |
| `ReverseAlg50Weizmann.pptx` | Existing Weizmann talk slides | Reference for prior talk structure and style |

### `GNNs/background/`

| File | Description | Role in talk |
|------|-------------|--------------|
| `21-0449.pdf` | Background paper (TBD — read to confirm) | Related work / motivation |
| `2310.00526v7.pdf` | Background paper (TBD — read to confirm) | Related work / motivation |

---

## How the Agent Uses These Files

The agent reads PDF source files to extract:
- Problem formulation and motivation
- Key claims and theorems
- Experimental setup and results
- Figures and diagrams (described textually for LaTeX reconstruction)

The agent reads the PPTX to understand the prior talk's structure and which slides to reuse
or improve.

---

## Priority Order for Slide Content

1. AAAI 2026 paper — most current, most important.
2. OptGNN and graph_coloring — supporting methodology.
3. NeuroSAT — foundational background, use in intro/motivation.
4. Background papers — use only when filling in related work.
5. Weizmann PPTX — structure reference only; do not copy verbatim.

---

## What to Verify Before Running the Agent

1. Confirm the AAAI 2026 paper title, authors, and venue.
2. Identify what the background PDFs are (check titles and abstracts).
3. Confirm the target talk duration and audience.
4. Set `TALK_TITLE` and `AUDIENCE` in `config.py` before running.

---

## Output Files

The agent writes to `output/`. Each run produces:

```
output/
├── <talk_name>.tex       # LaTeX Beamer source
├── <talk_name>.pdf       # Compiled PDF (if pdflatex is available)
└── <talk_name>_outline.md  # Slide-by-slide outline for review before compilation
```

Never commit compiled PDFs. Only commit `.tex` source files.
