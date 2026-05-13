# RESEARCH_CONTEXT.md

## Project Title

GNNs for Combinatorial Optimization: Algorithms, Limits, and Learning

Representative papers are in `GNNs/my papers/`. Background papers are in `GNNs/background/`.

---

## Purpose of This File

This file gives the AI assistant the research context needed to help prepare seminar slides,
write paper sections, sharpen arguments, and flag weaknesses.

Treat this as project-specific research memory. Update it whenever the scope of the work changes.

---

## Research Area

The core thread is: **can graph neural networks (GNNs) solve, or usefully approximate, hard
combinatorial problems?**

The problems of interest include satisfiability (SAT), graph coloring, and related NP-hard
optimization tasks. The angle is both empirical (do GNNs work in practice?) and theoretical
(why do they work, and where do they fail?).

---

## Key Papers in This Repository

### NeuroSAT (`Neuro_sat.pdf`)

Selsam et al., "Learning a SAT Solver from Single-Bit Supervision," ICLR 2019.

A GNN is trained to predict satisfiability of random SAT instances using only a single bit of
supervision (SAT/UNSAT label). The model learns message-passing procedures that resemble
belief propagation. This is a foundational paper showing that GNNs can capture combinatorial
structure in an end-to-end learned way.

Key insight: a GNN trained only to predict SAT/UNSAT implicitly learns to solve SAT.

### OptGNN (`OptGNN_elad_s (1).pdf`)

Work on using GNNs for optimization problems on graphs. The central theme is whether
GNNs can serve as approximate solvers and how their solutions relate to classical algorithmic
guarantees.

### Graph Coloring (`graph_coloring.pdf`)

Work on GNN-based approaches to graph coloring, a canonical NP-hard problem. Graph coloring
is a natural testbed for combinatorial reasoning: the structure of the problem (local constraints,
global feasibility) maps cleanly to the message-passing framework.

### AAAI 2026 Paper (`20251-AAAI26.ShohamE-ML.pdf`)

Recent accepted work (AAAI 2026). [Fill in title, main contribution, and key result once confirmed.]

### Reversible Algorithms Talk (`ReverseAlg50Weizmann.pptx`)

Existing talk given at Weizmann. Covers reversible/invertible algorithmic ideas. Related to
understanding the structure of GNN computation and its limitations.

---

## Background Papers

### `21-0449.pdf`

[Identify and summarize once read — likely expander graphs, random graphs, or algorithmic lower bounds.]

### `2310.00526v7.pdf`

[Identify and summarize once read — likely a recent GNN expressiveness or combinatorial optimization survey.]

---

## Central Research Questions

1. **Expressiveness**: What can GNNs compute, and what is beyond their reach? How does
   this connect to classical algorithmic complexity (e.g., Weisfeiler-Leman hierarchy)?

2. **Approximation quality**: When GNNs are used as approximate solvers, how close do
   they get to optimal? Is there a gap, and can it be characterized theoretically?

3. **Generalization**: GNNs trained on small random instances — do they generalize to
   larger or structured instances? Why or why not?

4. **Learning vs. algorithm design**: Are GNN-based solvers discovering known algorithmic
   ideas (e.g., message passing ≈ belief propagation), or genuinely doing something new?

---

## Core Framing for Seminar Talks

Avoid: "We use deep learning to solve NP-hard problems."

Prefer: "We study whether the inductive biases of GNNs align with the structure of
combinatorial problems, and what that alignment buys us in terms of solution quality
and generalization."

The story is not "GNNs beat classical solvers." The story is "GNNs provide a new lens on
what makes combinatorial problems hard, and a new tool with particular strengths and
well-characterized failure modes."

---

## Key Claims to Support

- GNNs can capture local combinatorial structure efficiently.
- There are problems (or regimes) where message-passing GNNs provably cannot do better
  than random.
- On certain random instance families, learned solvers generalize surprisingly well.
- The boundary between tractable and intractable is visible in GNN behavior.

---

## What to Avoid Overclaiming

- Do not say GNNs "solve" NP-hard problems. They approximate or solve particular instance families.
- Do not claim theoretical results from empirical evidence alone.
- Be precise about what instance distribution results hold on.
- Be careful about the gap between average-case and worst-case performance.

---

## Seminar Audiences

- **CS/ECE faculty and graduate students** (BGU, Weizmann): can handle formalism, need
  motivation and intuition before equations.
- **ML-oriented audience**: care more about empirical behavior, generalization, training setup.
- **Theory-oriented audience**: care more about expressiveness results, reductions, lower bounds.

Adapt the balance of formalism vs. intuition per audience. Always start with a concrete
problem and a clear gap. Never open with a GNN architecture diagram.

---

## Talk Duration

Typical seminar: 45–60 minutes including 10–15 minutes of questions.
Target: 35–45 content slides + 5–8 backup slides.
