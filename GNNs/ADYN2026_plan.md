# ADYN Summer School 2026 — Talk Plan (v3, pre-Beamer)

**Event:** Summerschool on Algorithms, Dynamics, and Information Flow in Networks, TU Dortmund
**Speaker:** Dan Vilenchik, Ben-Gurion University of the Negev
**Duration:** 50 minutes (~42–45 content + 5–8 questions)
**Target deck:** ~43 main slides + 6 backup slides
**Audience:** PhD students and postdocs in algorithms, combinatorics, probability, graph theory, TCS

---

## Revision log

- **v1:** Initial plan.
- **v2:** Added running question, corrected NeuroSAT framing, qualified BP analogy, expanded
  Chapter 1 to 18 slides, added evidence-status table.
- **v3 (this version):**
  1. Chapter 1 compressed from 18 → 14 slides.
  2. GNN toy example merged from 3 slides → 1 (use Beamer overlays/animations).
  3. BP + BP→GNN merged from 3 slides → 2 ("BP as template" and "limits of the analogy").
  4. Separate loss-function slide moved to backup.
  5. Absolute "GNNs don't invent new primitives" replaced throughout with "across these
     case studies, GNNs appear to rely on classical concepts."
  6. Sparse PCA claim softened: "matches Covariance Thresholding in the tested regime" —
     not "first combinatorial algorithm."
  7. All [VERIFY] placeholders removed from slide text; confirmed facts used or the item
     is moved to the Missing Inputs section.
  8. Chapter 4 described as schematic until exact numbers are confirmed.

---

## Thesis sentence (use in talk intro or closer)

> Across SAT, coloring, clique, Sparse PCA, and OptGNN variants, successful GNNs appear
> less like mysterious new solvers and more like learned message-passing systems that
> rediscover classical algorithmic concepts — support, degree, and confidence.

---

## Title

**Chosen:**
> *Learned Algorithms or Classical Messages in Disguise?*
> *GNNs for Combinatorial Optimization*

Intellectually honest, catchy, ADYN-compatible. Frames the talk as an investigation, not a sales
pitch.

---

## Abstract (for the ADYN event page)

Graph neural networks (GNNs) have shown surprising performance on NP-hard combinatorial
problems: trained on small instances, they sometimes generalize to much larger ones, creating the
impression that they may have discovered new algorithmic principles. In this talk I examine what
these networks actually learn. Using a concept-learning framework — asking whether meaningful
algorithmic quantities are decodable from learned embeddings — I present results across four
settings. In SAT and graph coloring, GNNs trained with only binary supervision develop internal
representations tightly aligned with the classical notion of *support*, a confidence-like signal central
to local-search and survey-propagation heuristics. In Max-Clique, the dominant learned concept is
degree-based ranking, which motivates a new decoder (LPR — Least-Probable Removal) that
substantially outperforms the standard top-*k* strategy, and whose principle transfers to Sparse PCA.
Finally, analyzing a family of OptGNN variants, we find that the transition from strong approximation
to exact solving is sharp and discontinuous, and is associated with whether the model learns a
confidence signal. The conclusion is nuanced: across these case studies, the GNNs' success appears
largely explainable through classical algorithmic concepts, pointing toward a principled, concept-level
theory of learned combinatorial optimization.

---

## Source Papers

| File | Paper | Role in talk |
|------|-------|--------------|
| `GNNs/my papers/Neuro_sat.pdf` | Shoham, Cohen, Wattad, Rika, Vilenchik. "Concept learning for algorithmic reasoning: Insights from SAT-solving GNNs." *Information Sciences* 726 (2026). | Chapter 2 main |
| `GNNs/my papers/graph_coloring.pdf` | Shoham, Rika, Vilenchik. "From Black Box to Algorithmic Insight: XAI in GNNs for Graph Coloring." AAAI 2025. | Chapter 2 second |
| `GNNs/my papers/20251-AAAI26.ShohamE-ML.pdf` | Shoham, Haber, Rika, Vilenchik. "Learning to Rank: How GNNs Solve Max-Clique and Sparse PCA." AAAI 2026. | Chapter 3 main |
| `GNNs/my papers/OptGNN_elad_s (1).pdf` | Anonymous. "The Last Percent: Concept Emergence and the Jump from Approximation to Solving in Neural CSPs." NeurIPS 2026 (submitted). | Chapter 4 main — **confirm attribution before any public slides** |
| `GNNs/background/2310.00526v7.pdf` | Yau, Karalias, Xu, Lu, Jegelka. "Are Graph Neural Networks Optimal Approximation Algorithms?" NeurIPS 2024. | Background for Chapter 4 |
| `GNNs/background/21-0449.pdf` | Cappart et al. "Combinatorial Optimization and Reasoning with GNNs." *JMLR* 2023. | Background / Chapter 1 survey |

**On NeuroSAT numbers:** The original NeuroSAT paper (Selsam et al., ICLR 2019) is not in the
folder. From Dan's concept learning paper (Table 1): training range n ∈ [10, 40]; analysis runs
on n ∈ {500, 1000, 1500, 2000}. Slides use "much larger than training" without citing a specific
Selsam generalization claim. Exact Selsam numbers are in the Missing Inputs list.

---

## The Running Question

> **When a GNN appears to solve a hard combinatorial problem — what did it actually learn?**

| Chapter | Setting | Answer |
|---------|---------|--------|
| 1 | GNNs in general | Maybe a transferable message-passing rule. But which rule? |
| 2 | SAT / Coloring | Support — a classical confidence signal from solver theory. |
| 3 | Max-Clique / Sparse PCA | Degree-based ranking — a classical planted-graph signal. |
| 4 | SDP / OptGNN | Whether confidence emerges determines whether it solves or only approximates. |

---

## Forty-Three-Slide Outline

---

### Opening + Chapter 1 — Crash Course: ML, GNNs, and the Promise
*(14 slides)*

---

#### Slide 1 — Title slide

**Purpose:** Establish the talk.

**Visual:** Title, name, affiliation, event, date. Below the title in smaller text: the running
question as a teaser.

**Slide text:**
```
Learned Algorithms or Classical Messages in Disguise?
GNNs for Combinatorial Optimization

Dan Vilenchik
Ben-Gurion University of the Negev
ADYN Summer School 2026

─────────────────────────────────────────────
Running question:
When a GNN appears to solve a hard combinatorial problem —
what did it actually learn?
```

**Speaker note:** "The title is a question, and so is the smaller one underneath. I'll carry both
through the entire talk. By the end we have an answer — not a complete one, but a useful one.
Let me start with a puzzle."

---

#### Slide 2 — NeuroSAT appeared to learn SAT-solving behavior from tiny instances

**Purpose:** The hook. Establish the empirical puzzle without overclaiming.

**Visual:** Two boxes side by side.
- Left: "Training — random 3-SAT, n ∈ [10, 40] variables. Label: SAT / UNSAT only."
- Right: "Test — much larger instances. Same GNN, no retraining."
- Bridge arrow: "It still works — sometimes. Why?"

**Slide text:**
```
NeuroSAT (Selsam et al., 2019):
  Train:  n ∈ [10, 40] variables
          (labels provided by an exact solver — single-bit supervision)
  Test:   instances much larger than training range
  
Observation:
  The same GNN showed surprisingly strong generalization.

Caveat:
  We still do not fully understand why this generalization happens.
  That is the puzzle.
```

**Speaker note:** "I want to be precise. NeuroSAT did not solve SAT in an algorithmic sense —
its authors did not claim that. What it did, surprisingly, is generalize to much larger instances
than it was trained on with only a binary label. That train-small/test-large behavior created a
serious interpretability puzzle. We don't fully understand it yet. What we did is start asking: what
is encoded in the model's internal representations? That question, it turns out, has an answer."

---

#### Slide 3 — The running question

**Purpose:** State the organizing question explicitly before the ML background.

**Visual:** Large centered question. Below: four chapter headings with answer slots to be
filled as the talk proceeds.

**Slide text:**
```
When a GNN appears to solve a hard combinatorial problem —
what did it actually learn?

Chapter 1:  We introduce GNNs and the puzzle.         [? — to be revealed]
Chapter 2:  SAT and Coloring                           [? — to be revealed]
Chapter 3:  Clique and Sparse PCA                      [? — to be revealed]
Chapter 4:  SDP / OptGNN                               [? — to be revealed]
```

**Speaker note:** "I'll return to this slide at the end of each chapter with the answer for that
setting. Think of it as a running scoreboard. The final slide closes the loop."

---

#### Slide 4 — The setting: combinatorial optimization on graphs

**Purpose:** Define the problem class for a theory audience.

**Visual:** A simple factor graph. Variables as circles, clauses/constraints as squares.

**Slide text:**
```
Input:    a graph or formula
Goal:     find an assignment satisfying all (or most) constraints
Hard:     NP-complete in the worst case

Problems in this talk:
  3-SAT:     assign TRUE/FALSE to variables
  Coloring:  assign colors to vertices, no two adjacent the same
  Clique:    find a large complete subgraph
```

**Speaker note:** "These are canonical NP-hard problems. Each serves as a test case. Their
different structures will matter: when we ask what concept the GNN learned, the answer
depends on what structure the problem has."

---

#### Slide 5 — Supervised learning and the loss function

**Purpose:** Define the ML setup for a non-ML audience. Loss explanation integrated here;
separate backup slide (B7) has more detail.

**Visual:** Left: small pipeline (training data → model → loss → training). Right: NeuroSAT as
the running instance of each step.

**Slide text:**
```
Training data:    (instance, label) pairs
Model:            f_θ: instance → prediction   (θ = parameters, learned)
Loss:             how wrong is f_θ compared to the label?
Training:         adjust θ to reduce loss

For NeuroSAT:
  Instance:   a SAT formula
  Label:      SAT or UNSAT (one bit, from an exact solver)
  Loss:       cross-entropy on that single bit

Note: the loss says nothing about which variables are TRUE, or about support,
      degree, or any other solver concept. Those concepts are not prescribed.
      If they appear in embeddings — they emerged spontaneously.
```

**Speaker note:** "This is the key point about NeuroSAT's loss: it tells the model nothing
about how to solve SAT. It only says whether the formula is satisfiable. Everything the model
does internally — how it organizes its representations, what algorithmic signals it encodes —
is not required by the loss. That's the puzzle."

---

#### Slide 6 — Train, test, and the generalization puzzle

**Purpose:** Establish the conceptual heart of the talk.

**Visual:** Number line of instance sizes. Training range [10, 40] on the left. Test range
"much larger" on the right, separated by a gap labeled "?"

**Slide text:**
```
Ordinary generalization:   same distribution, held-out examples
Size generalization:       test instances are much larger than training

For NeuroSAT:
  Train: n ∈ [10, 40]
  Test:  much larger (our analysis: n up to 2000)

If the model generalizes across sizes:
  → it learned something structural — not instance-specific
  → what structural invariant could possibly scale?

That invariant is our object of study.
```

**Speaker note:** "When a model generalizes to instances from the same distribution and same
size, that's ordinary generalization. What's unusual here is cross-size generalization. It suggests
the model found an invariant of the problem structure that holds at all scales. That's what we're
hunting."

---

#### Slide 7 — Four things to keep separate

**Purpose:** Give the audience a precise vocabulary before introducing GNNs. This prevents
conflating what was designed and what was learned.

**Visual:** A clean 4-row list or 2x2 grid.

**Slide text:**
```
1. Architecture:         how information flows
                         (for a GNN: nodes, edges, message-passing rounds)
                         Designed by the researcher.

2. Parameters (weights): the numerical values inside the model
                         Learned from data.

3. Training objective:   what the model is rewarded for predicting
                         Designed by the researcher.

4. Decoding strategy:    how output scores become a discrete solution
                         Designed by the researcher; can be changed post-training.

When we say "the model learned X":
  X is in the parameters — not designed, not prescribed by the loss.
  X emerged from the interaction of architecture, objective, and data.
```

**Speaker note:** "This distinction will matter a lot. When I say 'the GNN learned support,'
I mean support is decodable from the learned parameters — from the embeddings — even
though the loss never mentioned it. The concept emerged. That's the interesting part."

---

#### Slide 8 — Graph-structured problems need graph-structured models

**Purpose:** Motivate GNNs specifically.

**Visual:** Adjacency matrix of a graph under two different node labelings → same graph, same
combinatorial structure. Label: "Any useful model must be permutation-invariant."

**Slide text:**
```
Challenge: same graph, different node labels → same structure
Standard NN: fails (different inputs, no invariance)
GNN: operates on structure, ignores labels ✓

Also:
  Graphs are variable-size     → GNNs handle this naturally
  Constraints are local        → local message passing fits
  Graphs are often sparse      → GNNs scale with edges, not with n²
```

**Speaker note:** "Combinatorial problems on graphs are permutation-invariant. GNNs are built
for this. They also scale linearly with the number of edges, making them usable on large sparse
instances."

---

#### Slide 9 — What is a GNN?

**Purpose:** Formal definition.

**Visual:** A small 6-node graph. Each node labeled with h_v ∈ ℝ^d. Neighbor arrows flowing
in. Two-step update rule.

**Slide text:**
```
Each vertex v has a state (embedding) h_v ∈ ℝ^d

Each round t:
  1. Aggregate:   m_v = AGG({h_u : u ∈ N(v)})
  2. Update:      h_v ← UPDATE(h_v, m_v)

After T rounds: predict from {h_v}

AGG and UPDATE are learned neural networks (the parameters).
After T rounds: each v has seen its T-hop neighborhood.
```

**Speaker note:** "Think of it as a distributed algorithm where each node keeps a memory
vector and exchanges messages with its neighbors. The only difference from a designed algorithm
is that AGG and UPDATE are learned. What they learn to compute — that's our question."

---

#### Slide 10 — GNN message passing: animated example

**Purpose:** Make the mechanics concrete. Designed as a single slide with 3–4 Beamer overlays.

**Visual:** A 6-node graph with labeled embeddings. Overlay 1: round 0 — random embeddings,
all identical. Overlay 2: round 1 — arrows from neighbors of v, aggregate and update shown.
Overlay 3: after T rounds — embeddings now encode local structure. Overlay 4: readout — MLP
gives score s_v ∈ [0,1]; decoder converts to discrete solution.

**Slide text (base layer):**
```
Round 0:   h_v = random   (all vertices look identical)
Round 1:   h_v ← UPDATE(h_v, AGG(neighbors))
           → v now "knows about" its 1-hop neighborhood
Round T:   → v knows about its T-hop ball

Readout:   MLP(h_v) → score s_v ∈ [0,1]
Decoding:  top-k, LPR, or rounding   (designer's choice, not learned)
```

**Speaker note:** "I'll use animations here. The key takeaway: after T rounds, each node has a
summary of its T-hop neighborhood. The scores come from the learned parameters. The decoder
is separate — and that distinction matters in Chapter 3."

---

#### Slide 11 — Belief propagation: the classical template

**Purpose:** Set up the BP–GNN analogy. Covers the original BP definition and the
BP-to-GNN transition in one conceptual arc. (Merges two slides from v2.)

**Visual:** Left column: classical BP on a factor graph. Right column: GNN on the same graph.
Parallel structure shows what changes at each row.

**Slide text:**
```
                   Classical BP              GNN
Message:           scalar / probability      vector ∈ ℝ^d
Update rule:       analytically derived      learned (MLP/GRU)
Objective:         probabilistic model       task loss (e.g., SAT/UNSAT)
Convergence:       proven on trees           empirical
Interpretability:  high                      our question

A GNN is BP-inspired high-dimensional learned message passing.
Not BP — but BP is the right mental model for this audience.
```

**Speaker note:** "BP passes structured probabilistic summaries; the GNN passes high-dimensional
learned vectors. BP derives its update analytically; the GNN learns it from data. The question of
what the GNN learned is, in a sense, a question about what it reinvented from the BP world. But
there's an important caveat — next slide."

---

#### Slide 12 — The limits of the BP analogy

**Purpose:** Qualify the analogy once, clearly, and move on. Credibility slide for the TCS
audience.

**Visual:** Simple two-box diagram. Left: "Where BP analysis works" (replica-symmetric phase,
sparse random graphs near threshold). Right: "Where GNNs sometimes go further" (empirically
work past clustering threshold in some settings).

**Slide text:**
```
Classical BP has known failure regimes:
  On random CSPs: BP works in the replica-symmetric phase
  Near/past clustering and condensation: naive BP fails or gives wrong answers

GNNs are not bound by those regimes in the same way:
  They optimize a task loss, not a probabilistic model
  They may route information differently from any hand-designed BP

Part of the open puzzle:
  Why do GNNs sometimes work where BP would not?
  The concept-learning framework is one lens into this — not the final answer.
```

**Speaker note:** "Say this once and move on. BP is the analogy, not the claim. Classical BP
has known failure regimes; the point is that GNNs are learned high-dimensional message passing,
and part of the puzzle is why they sometimes behave better than this analogy predicts. We don't
fully understand this yet. Now, the result that started the puzzle."

---

#### Slide 13 — NeuroSAT: the promise

**Purpose:** Establish the motivating result precisely.

**Visual:** Factor graph for a small SAT formula (left) vs. schematic of a large formula (right).

**Slide text:**
```
NeuroSAT (Selsam et al., 2019):
  Architecture:   message-passing GNN on a CNF factor graph
  Training:       SAT/UNSAT label only — single-bit supervision
  Training set:   n ∈ [10, 40] variables, near the SAT/UNSAT phase transition

Observation:
  The trained GNN showed surprisingly strong generalization beyond training range.
  Our analysis ran it on instances with n up to 2000.
  The reason for this generalization is not fully understood.

Our question:
  What did it learn internally?
```

**Speaker note:** "NeuroSAT is not a general SAT solver. What it showed is that a very simple
GNN, trained with one bit of supervision per instance, organized its internal representations
in a way that worked on much larger instances. That suggests it found something structural. Our
project is to name that something."

---

#### Slide 14 — Chapter 1 partial answer + the research program

**Purpose:** Close Chapter 1, revisit the running question, and introduce concept learning.

**Visual:** Running question at top. Chapter 1 partial answer. Below: the concept-learning
method pipeline.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 1 answer (partial):
  Possibly: a transferable message-passing rule capturing structural invariants.
  But the training loss doesn't specify which rule.
  That is the interpretability puzzle.

Our method — concept learning:
  Project learned embeddings to low-dimensional PCA space.
  Ask: does the projection align with known algorithmic quantities?
  Verify: a simple linear probe predicts the concept on held-out instances.

A concept gϕ(v) is learned iff:
  ĝ(v) = w⊤ h_v + b   predicts gϕ(v) on held-out instances.
  Falsifiable: fails if the quantity isn't predictable above baseline.
```

**Speaker note:** "The concept-learning framework is the methodological core. We don't assume
the model learned any particular thing. We ask whether classical algorithmic quantities are
encoded in the embeddings, and test that with a linear probe. If support is encoded, the probe
can predict it on instances the probe never saw. Let's see what we find."

---

### Chapter 2 — SAT and Coloring: Support as Confidence
*(11 slides)*

---

#### Slide 15 — Running question, Chapter 2: SAT and Coloring

**Purpose:** Signal the chapter transition.

**Visual:** Running question at top, Chapter 2 highlighted. Small SAT factor graph and small
3-colored graph side by side.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 2 setting:
  Problem 1 — SAT       (NeuroSAT, Shoham et al. 2026)
  Problem 2 — 3-Coloring (GNN-GCP, Shoham et al. 2025)

Both GNNs: trained with single-bit binary supervision only.
We probe their learned embeddings.
```

**Speaker note:** "We now ask the running question for two constraint-satisfaction problems.
Both GNNs were trained with only a binary label. Neither loss mentions any solver quantity.
Here is what we found."

---

#### Slide 16 — Concept learning for algorithmic tasks

**Purpose:** Explain the concept-learning approach briefly.

**Visual:** Three boxes: vision ("beak"), medicine ("lesion boundary"), algorithms ("variable
confidence").

**Slide text:**
```
XAI usually: which input features drove this decision?
             (SHAP, LIME, GradCAM)

For algorithmic tasks: features are not enough.
  "x₁ appears in clause 7" → instance-specific, not transferable.
  "x₁ has high support"    → meaningful across instances.

A concept: a compact quantity that generalizes across instances,
           explains internal dynamics, and has algorithmic meaning.
```

**Speaker note:** "We need concepts — not feature attributions for one input, but global
algorithmic quantities that explain how the model behaves across all instances. That requires
looking at the geometry of the internal representations over many runs."

---

#### Slide 17 — SAT as a factor graph: the running example

**Purpose:** Introduce the SAT instance visually.

**Visual:** TikZ factor graph: (x₁ ∨ x̄₂ ∨ x₃) ∧ (x₁ ∨ x₂ ∨ x̄₃).
Variable nodes = circles, clause nodes = squares.

**Slide text:**
```
CNF formula: (x₁ ∨ x̄₂ ∨ x₃) ∧ (x₁ ∨ x₂ ∨ x̄₃)

Factor graph:
  Variable nodes: x₁, x₂, x₃  (and negations x̄₁, x̄₂, x̄₃)
  Clause nodes:   C₁, C₂
  Edges:          literal ↔ clause where literal appears

NeuroSAT runs T rounds of message passing on this graph.
We ask: what do the embeddings encode after training?
```

**Speaker note:** "NeuroSAT operates on the factor graph, not the formula directly. Literals and
clauses are both node types — just like in survey propagation. Now I'll tell you what we found
inside those node embeddings."

---

#### Slide 18 — What is "support"?

**Purpose:** Introduce the key concept formally before showing any data.

**Visual:** Toy formula. A TFF clause (one TRUE, two FALSE) highlighted. The TRUE literal
labeled "sole supporter."

**Slide text:**
```
Assignment ϕ. Variable x. Clause C.

x supports C under ϕ  ⟺
    C is satisfied, and x is the ONLY satisfied literal.
    (clause type TFF: True, False, False)

support_ϕ(x) = |{clauses C : x alone satisfies C}|

High support:  x is load-bearing → flipping x breaks many clauses immediately
Low support:   x is replaceable  → safe to flip in local search

This appears in: WalkSAT, Survey Propagation, backbone analysis.
All three traditions independently discovered the same signal.
```

**Speaker note:** "Support is a classical notion. Three very different algorithmic traditions —
WalkSAT (local search), Survey Propagation (message passing), backbone analysis
(combinatorial structure) — independently discovered the same signal. A variable with high
support is one you cannot safely change. It's a confidence signal. NeuroSAT, trained only on
SAT/UNSAT labels and never told about support, encodes precisely this quantity. Let me show you."

---

#### Slide 19 — Support as confidence: a toy example

**Purpose:** Concrete example before the PCA plots.

**Visual:** Two small formulas side by side.
- Formula A: x₁ is the sole TRUE literal in 3 of 4 clauses → support = 3.
- Formula B: x₁ appears in balanced clauses, rarely the sole satisfier → support = 0.

**Slide text:**
```
High support:
  x₁ = TRUE. Of 4 clauses containing x₁:
  3 are satisfied only because of x₁ (type TFF).
  Flipping x₁ breaks 3 clauses immediately.
  → Confidence is HIGH.

Low support:
  x₁ = TRUE. All clauses containing x₁ have other TRUE literals.
  Flipping x₁ costs nothing immediately.
  → Confidence is LOW. Safe to explore.
```

**Speaker note:** "If you were designing a local-search SAT solver, support is exactly the kind
of thing you'd track. NeuroSAT, which saw only binary SAT/UNSAT labels, encodes precisely
this. Let's look at the geometry."

---

#### Slide 20 — NeuroSAT embeddings: PCA reveals support

**Purpose:** Empirical evidence for concept emergence.

**Visual:** Schematic of Fig. 2 from the SAT concept learning paper. Literal embeddings
projected to 2D. Literal and negation on opposite sides of PC1 = 0. Support clauses (TFF)
with higher |PC1| values.

**Slide text:**
```
PCA of NeuroSAT's internal literal embeddings
(n = 1500 variables, run to convergence):

PC1 explains ~90% of variance
PC2 explains ~8% of variance
(~98% captured by 2 components out of 128 dimensions)

PC1 value of a literal:
  far positive  = TRUE, high support
  near 0        = uncertain, low support
  far negative  = negation of above (symmetric)

Linear probe: support is predictable from embeddings on held-out instances.
```

**Speaker note:** "The model is 128-dimensional. 98% of what matters lives in 2 dimensions.
Those 2 dimensions encode support and assignment consistency. This is verified by a linear probe
on held-out instances — not just a visual impression."

---

#### Slide 21 — Main finding: support governs NeuroSAT's dynamics

**Purpose:** State the result precisely.

**Visual:** Schematic: "Support (PC1 of embedding) → governs which variables are flipped →
support-core emerges."

**Slide text:**
```
Theorem (informal, under assumptions on distribution and weights):
  NeuroSAT's dynamics fix variables in decreasing order of support,
  starting with the r-support core — analogous to the graph-theoretic r-core.

Empirically:
  Variables with PC1 near 0 are reassigned in the next iteration.
  Variables with PC1 far from 0 are locked in, consistent with a satisfying assignment.

Payoffs from knowing this:
  StudentNeuroSAT: 91% fewer parameters, comparable performance.
  SupportSAT-01: WalkSAT variant converging faster on n = 1500.
```

**Speaker note:** "Two parts: a theoretical analysis showing the dynamics reduce to tracking
the support-core (for a simplified architecture), and the empirical probe. The concept is
immediately useful: it enables compression and algorithmic improvement."

---

#### Slide 22 — Graph coloring: same concept, different geometry

**Purpose:** Support reappears in a structurally different problem.

**Visual:** Left: small valid 3-colored graph. Right: 2D PCA of GNN-GCP embeddings — the
triangular structure.

**Slide text:**
```
GNN-GCP (Lemos et al., 2019):
  Trained to predict 3-colorability (binary label only)
  Message-passing LSTM, 64-dim embeddings

Support in coloring:
  support(v) = number of neighbors v has in each color class other than its own

2D PCA projection:
  Embeddings form a triangle; color classes cluster near corners.
  High-support vertices are closest to triangle corners (color committed).
  Low-support vertices sit near the center (still uncertain).
```

**Speaker note:** "Support in coloring has an analogous meaning: the more neighbors of
conflicting colors, the more committed a vertex is to its own color. The GNN encodes this with
a triangular geometry. Color classes are the three corners of the triangle."

---

#### Slide 23 — Coloring: support connects to a 1994 algorithm

**Purpose:** Make the classical connection explicit and surprising.

**Visual:** Side-by-side: SAT (literals on PC1 axis) and Coloring (triangle corners). Same
concept, different representation.

**Slide text:**
```
Support in SAT:      clauses uniquely satisfied by x
Support in coloring: neighbors v has in each other color class

In both:
  High support → high confidence → far from ambiguous region
  Low support  → uncertain       → near center

This concept was used in hand-designed algorithms:
  WalkSAT (1994) for SAT
  Alon–Kahale (1994) for graph coloring

Across these two case studies, GNNs trained decades later
rediscover the same classical signal from data, without supervision.
```

**Speaker note:** "The Alon–Kahale coloring algorithm from 1994 was designed around exactly
this support concept. The GNN, trained with no knowledge of that algorithm, encodes the same
quantity. Across these case studies, the GNNs don't appear to invent new primitives. They
appear to rediscover classical ones."

---

#### Slide 24 — Chapter 2: running question answered

**Purpose:** Crystallize Chapter 2 and revisit the running question.

**Visual:** Running question with Chapter 2 answer filled in.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 2 answer (SAT and Coloring):
  Support — a classical confidence signal from solver theory.
  Present in both GNNs, without supervision, across two different architectures.

Evidence:
  SAT:       linear probe + PCA structure + theoretical analysis  (formal + empirical)
  Coloring:  linear probe + triangular embedding geometry         (empirical / partially formal)

Does the same pattern hold for a structurally different problem?
→ Chapter 3: Max-Clique
```

**Speaker note:** "Chapter 2 answer: support. Two different GNNs, two different problems,
different architectures, different loss functions. Same emergent concept. Let's now move to a
structurally different problem — Max-Clique — and ask the same question."

---

### Chapter 3 — Clique: Degree, Ranking, and Cross-Domain Generalization
*(8 slides)*

---

#### Slide 25 — Running question, Chapter 3: Max-Clique

**Purpose:** Chapter transition.

**Visual:** Running question at top. Small planted clique graph on the right.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 3 setting:
  Problem — Max-Clique (Shoham et al., AAAI 2026)
  No factor graph. No clause structure.
  The signal lives in vertex degrees, not constraint satisfaction.

If the concept-learning story is robust,
it should survive this structural change.
```

**Speaker note:** "SAT and coloring have a natural factor-graph structure — that's where BP
is most natural. Clique is a different type of problem. The fact that a similar concept-learning
story holds there is a stronger test of the framework."

---

#### Slide 26 — Planted clique: three difficulty regimes

**Purpose:** Principled benchmark for evaluating GNNs on clique.

**Visual:** Three labeled regions on a number line of planted clique size k.

**Slide text:**
```
Random graph G(n, 1/2):
  Largest clique ≈ 2 log₂ n   (believed hard to find efficiently)

Planted clique: add a k-clique to G(n, 1/2)

Difficulty regimes (calibrated empirically for n = 1000):
  Easy:   k ≥ ~62  — Top-k by degree recovers the clique
  Medium: k ∈ [36, 61] — LPR or spectral methods needed
  Hard:   k ≤ 35  — planted clique conjecture; no known efficient algorithm
```

**Speaker note:** "We evaluate GNNs on instances calibrated to this landscape. Without
hardness control, you can't tell whether a GNN 'solving' clique is impressive or trivial.
Previous GNN evaluations for clique typically used uncontrolled benchmarks — that's part of the
methodological contribution here."

---

#### Slide 27 — Degree as a classical signal: helpful but noisy

**Purpose:** Establish the degree baseline.

**Visual:** Small planted clique graph (n = 10, k = 4). Degree table: clique vertices {6,7,7,8};
non-clique vertices {2,3,4,7}. The non-clique vertex at degree 7 — the "impostor" — highlighted.

**Slide text:**
```
Degree heuristic:
  Clique vertices receive a degree "boost" from within-clique edges.
  Sort by degree, take top k.

Works in the Easy regime. Fails in Medium/Hard:
  "Impostors" — non-clique vertices with high random degree — enter top k.
  The candidate set is not a valid clique.

Classical open question:
  What signal, beyond raw degree, distinguishes clique vertices in the Medium regime?
```

**Speaker note:** "The degree heuristic is the simplest possible approach. In easy cases it's
enough. In medium and hard cases it's fooled by impostors. The question is whether the GNN
does something more clever — or whether it just learns a sophisticated version of degree."

---

#### Slide 28 — What the GNN learns: degree-based ranking

**Purpose:** State the core finding for clique.

**Visual:** PCA of GNN vertex embeddings — PC1 highly correlated with degree. GNN output
score vs. degree scatter plot.

**Slide text:**
```
GNN embedding analysis (PCA):
  PC1 of vertex embeddings: highly correlated with vertex degree.
  GNN output scores ≈ monotone function of degree.

Finding (across these case studies):
  The GNN learns degree-based ranking.
  It does not appear to learn a fundamentally new signal.

But the decoder matters:
  Top-k with degree fails on medium instances.
  A smarter decoder changes the outcome substantially.
```

**Speaker note:** "The GNN is doing sophisticated degree estimation — multi-hop, so better than
raw degree, but the principle is the same. The interesting result is what happens when you pair
this concept with the right decoder."

---

#### Slide 29 — Top-k vs. LPR: same concept, very different decoding

**Purpose:** Introduce LPR and show the performance gap.

**Visual:** Side-by-side. Left (Top-k): select k highest-scoring vertices; impostor included.
Right (LPR): iteratively remove lowest-scoring vertex until remainder is a clique; impostor
eliminated.

**Slide text:**
```
Top-k:
  Select k vertices with highest GNN scores.
  O(n²). Fails on Medium: impostors included.

LPR — Least-Probable Removal:
  Start with all n vertices.
  Remove lowest-scoring vertex (least likely in clique).
  Repeat until the remaining set forms a clique.
  O(n³), practical: avg ~25s; peak ~90s for n = 47k.

LPR significantly outperforms Top-k in Medium and Hard regimes.
Lesson: the concept (degree ranking) is in the scores.
        The decoding strategy determines how well you extract it.
```

**Speaker note:** "LPR inverts the perspective: instead of selecting likely clique vertices, it
prunes unlikely ones. When impostors are present, they have lower scores — LPR removes them.
Same learned concept, very different decoding strategy, substantially different results."

---

#### Slide 30 — Cross-domain: the same GNN solves Sparse PCA

**Purpose:** The universality result — the strongest finding in the clique paper.

**Visual:** Two-panel. Left: graph with planted clique, vertices color-coded by degree boost.
Right: covariance matrix with planted spike, rows color-coded by row-sum. Connection arrow:
"row-sum ranking."

**Slide text:**
```
Sparse PCA (single-spike model):
  Covariance Σ = I + β·vv⊤,  v sparse (size k).
  Goal: recover the support of v.

Structural connection to clique:
  Clique vertices:  higher degree from within-clique edges
  Spike variables:  larger row-sums from the β·vv⊤ perturbation

Transfer experiment:
  GNN trained on Max-Clique  →  applied to Sparse PCA  →  succeeds.
  GNN trained on Sparse PCA  →  applied to Max-Clique  →  succeeds.

Learned principle: row-sum ranking — universal across both domains.

Result: GNN with LPR matches Covariance Thresholding in the tested regime,
        without problem-specific hyperparameters.
```

**Speaker note:** "We trained a GNN to find cliques. We gave it a covariance matrix from Sparse
PCA — a completely different problem. It succeeds because both problems have the same
underlying structure: identify a small subset with elevated row-sums. In learning degree ranking
for cliques, the GNN learned row-sum ranking in general. This gives a simple combinatorial
procedure matching the spectral state-of-the-art for Sparse PCA, without tuning. The exact
claim is in the paper and backup slide B6."

---

#### Slide 31 — Chapter 3: running question answered

**Purpose:** Crystallize Chapter 3.

**Visual:** Running question with Chapters 2 and 3 filled in.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 3 answer (Max-Clique / Sparse PCA):
  Degree-based (row-sum) ranking — a classical planted-graph signal.
  Transfers across domains.

Chapter 2 recap:
  SAT / Coloring → support

Theme (across these case studies):
  Different problem structures → different classical concepts.
  But each concept was known. None appears to be a genuinely new primitive.

Chapter 4: What must a model learn in order to solve, not just approximate?
```

**Speaker note:** "Chapter 3 answer: degree ranking. Different from support, but again a
classical signal. In Chapter 4 we flip the question: instead of asking what a given model learned
post-hoc, we ask what concept is necessary for a model to cross the threshold from approximating
to solving."

---

### Chapter 4 — The Last Percent: Approximation, Solving, and the Concept Gap
*(8 slides)*

**Note for Beamer generation:** Chapter 4 results (exact solving rates, probe accuracy values)
are from a NeurIPS 2026 submission. Confirm attribution and exact numbers before generating
final public slides. Slides below use schematic descriptions in place of specific numbers.

---

#### Slide 32 — Running question, Chapter 4: SDP / OptGNN

**Purpose:** Signal chapter transition and reframe the running question.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 4 new angle:
  Instead of asking what a given model learned,
  we ask: what must a model learn in order to solve, not just approximate?

Setting:
  OptGNN (Yau et al., NeurIPS 2024) and controlled variants.
  Problem: SAT and NAE-SAT (hypergraph 2-coloring).
  We run a controlled design experiment: four architectural variants,
  progressively closer to explicit constraint structure.
```

**Speaker note:** "This chapter turns the question around. Instead of reverse-engineering a
trained model, we run a controlled experiment. We start from a well-understood architecture,
make three principled modifications, and ask which one enables solving. The answer connects
back to everything in Chapters 2 and 3."

---

#### Slide 33 — The approximation–solving gap

**Purpose:** Introduce the central distinction.

**Visual:** Number line 0%–100%. "Random baseline" at 7/8 ≈ 87.5%. "OptGNN" at ~99%.
"Solving" at 100%. Gap between 99% and 100% labeled "the last percent."

**Slide text:**
```
Random 3-SAT:
  A random assignment satisfies each clause with probability 7/8.
  87.5% approximation is trivially achievable.

OptGNN (Yau et al., NeurIPS 2024): reaches ~99%.

Exact solving (100%):
  Håstad (2001): improving beyond 7/8 is NP-hard in the worst case.
  For random SAT above threshold: the last 1% may require coordinated
  changes across many variables simultaneously.

From ~99% to 100% is a qualitative transition, not a marginal gain.
```

**Speaker note:** "An assignment satisfying 99% of clauses can still be far from any satisfying
assignment — the last violated clauses may trigger cascades of required changes. The gap between
strong approximation and exact solving is the focus of this chapter."

---

#### Slide 34 — OptGNN: SDP relaxations built into a GNN

**Purpose:** Introduce the starting point concisely.

**Visual:** Pipeline: "SDP relaxation → projected gradient descent = message passing on graph
→ GNN parameterization → train with SDP-inspired loss."

**Slide text:**
```
OptGNN (Yau et al., NeurIPS 2024):
  Key insight: solving a certain SDP via projected gradient descent
               equals message passing on the graph.
  → GNN architecture captures this algorithm.
  → Train with continuous SDP-inspired unsupervised loss.
  → Inference: round continuous embeddings to discrete assignment.

Result: near-optimal approximation on Max-Cut, Max-3-SAT, Min-Vertex-Cover.
        (UGC-optimal approximation guarantees)
Limitation: strong approximation, but often fails to satisfy all constraints exactly.
```

**Speaker note:** "OptGNN is an elegant construction — the architecture is derived from an
approximation algorithm. It has provable guarantees under the Unique Games Conjecture. But
its loss function is a continuous relaxation, not designed to enforce discrete feasibility. That's
the tension."

---

#### Slide 35 — Three controlled modifications

**Purpose:** Describe the experimental design.

**Visual:** Four-box progression: OptGNN → OptGNN-IR → OptGNN-Logit → OptGNN-Logit+Clause.

**Slide text:**
```
Starting point: OptGNN (SDP-based, continuous loss)

Modification 1 — Recurrent layers (OptGNN-IR):
   Single recurrent unit, more iterations.
   Analogy: run a heuristic longer.

Modification 2 — Logit-space loss (OptGNN-Logit):
   Add rounding layer: embeddings → [0,1] → clause validity.
   Loss evaluates discrete clause satisfaction directly.

Modification 3 — Clause-level aggregation (OptGNN-Logit+Clause):
   Explicit variable–constraint bipartite structure.
   Factor-graph view built into the architecture.
```

**Speaker note:** "Each modification is inspired by classical heuristic design, not arbitrary
architecture search. Modification 1 is doing more of the same. Modifications 2 and 3 change
the qualitative structure of what information the model can form."

---

#### Slide 36 — A sharp transition: approximation doesn't predict solving

**Purpose:** Main empirical finding. Schematic until exact numbers are confirmed.

**Visual:** Two bar charts side by side. Left: approximation ratio per model variant — all bars
near 99%, roughly equal. Right: exact solving rate per variant — jumps sharply from
OptGNN/OptGNN-IR (near zero) to OptGNN-Logit (moderate) to OptGNN-Logit+Clause (strong).
Caption: "Schematic — see paper for exact values."

**Slide text:**
```
All four variants: approximation ratio ≈ 99%+
(strong approximation doesn't distinguish them)

Exact solving rate:
  OptGNN:                  near zero
  OptGNN-IR:               near zero
  OptGNN-Logit:            moderate increase
  OptGNN-Logit+Clause:     strong

More iterations (Modification 1) alone do not help.
The transition requires a qualitative architectural change.
When it happens, it's sharp — not gradual.
```

**Speaker note:** "You can run OptGNN longer — it still fails to solve. More iterations are not
enough. The transition requires changing what information the model can form. And when the
transition happens, it's discontinuous. Models go from near-zero solving to consistent solving.
There is no gradual middle ground."

---

#### Slide 37 — Confidence bridges approximation and solving

**Purpose:** Connect Chapter 4 back to the concept thread.

**Visual:** Two panels. Left: solving rate per variant (mirrors slide 36). Right: linear probe
accuracy for predicting support from embeddings per variant. The two curves are mirror images.
Caption: "Schematic — see paper for exact probe values."

**Slide text:**
```
We probe each variant: can support be decoded from embeddings?

OptGNN:                support not decodable  →  does not solve
OptGNN-IR:             support not decodable  →  does not solve
OptGNN-Logit:          support partially decodable  →  sometimes solves
OptGNN-Logit+Clause:   support strongly decodable   →  consistently solves

The logit loss exposes TFF clauses — exactly the support clauses.
(TFF = one literal preserving satisfaction; flipping it breaks the clause)
Clause-level aggregation makes support globally computable.

The presence of the confidence signal predicts the solving capability.
```

**Speaker note:** "The probe results mirror the solving results. Support is the concept that
bridges approximation and solving. When the architecture enables the model to form that
concept — which requires explicit constraint-level structure — it solves. When it can't, it
approximates."

---

#### Slide 38 — Evidence status: what we have proven vs. what we have observed

**Purpose:** Precise audit of the evidence across all four chapters. Required for this audience.

**Visual:** Table with five rows and four columns.

**Slide text:**
```
Problem           Classical concept       GNN evidence                 Status
──────────────────────────────────────────────────────────────────────────────────
SAT (NeuroSAT)    Support (literal)       PCA + linear probe +         Formal +
                                          theoretical analysis         empirical
Graph             Support (vertex /       Embedding geometry +         Empirical /
Coloring          color class)            linear probe                 partially formal
Max-Clique /      Degree-based            PCA + score correlation +    Empirical +
Sparse PCA        row-sum ranking         cross-domain transfer        algorithmic result
OptGNN            Support /               Ablations + probes           Empirical
                  confidence              across variants              (no formal theory yet)
```

**Speaker note:** "I want to be precise about what is proven versus observed. The strongest
result is for SAT: theoretical analysis, empirical probe, and PCA structure. For coloring and
clique, strong empirical evidence but less formal theory. For OptGNN, the evidence is from
ablations and probes — no formal theory yet. These are the right distinctions to make for this
audience."

---

#### Slide 39 — Chapter 4 + unified running question: final answer

**Purpose:** Deliver the unified answer to the running question.

**Visual:** Running question with all four chapter answers filled in.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 1: Possibly a transferable message-passing rule — but which?
Chapter 2: SAT/Coloring → support (classical confidence signal)
Chapter 3: Clique/Sparse PCA → degree ranking (classical planted-graph signal)
Chapter 4: SDP/OptGNN → whether confidence/support forms
           determines whether the model solves or only approximates

Unified answer (across these case studies):
  GNNs for combinatorial optimization appear less like mysterious new solvers
  and more like learned message-passing systems that rediscover classical
  algorithmic concepts — support, degree, and confidence.

  This makes them: analyzable, compressible, and designable.
```

**Speaker note:** "Four chapters, four problems. Across all of them, the successful GNNs
appear to rely on classical concepts — support, degree, confidence — rather than mysterious
new primitives. I want to be clear that this is a finding across these particular case studies, not
a proof that GNNs can never learn something genuinely new. Slide 40 makes that open."

---

#### Slide 40 — What we can do with this, and what remains open

**Purpose:** Concrete payoffs plus honest open questions. Closes the talk for a summer-school
audience.

**Visual:** Two-column layout: "What we can do now" and "Open questions."

**Slide text:**
```
What we can do now:
  Compress models by training toward the concept (91% reduction, StudentNeuroSAT)
  Improve classical solvers from concept insight (SupportSAT-01)
  Design decoders that extract the concept better (LPR)
  Design architectures that enable confidence formation (clause-level aggregation)

Open questions:
  Are there problems where GNNs learn a genuinely new concept —
  not previously identified in classical algorithmic theory?

  Can concept-level probing predict generalization failure before it occurs?

  When is confidence locally computable? Is local computability
  necessary for GNN success?

  Can we design loss functions that provably induce confidence formation?
```

**Speaker note:** "The open questions are where the interesting work is. The question I find
most intriguing is whether there exist problems where GNNs learn something genuinely new —
something not already named in the classical algorithmic literature. We don't know yet. If
anyone has ideas, I'd love to hear them."

---

#### Slide 41 — Takeaway

**Purpose:** Final slide. One sentence.

**Visual:** Minimal. Single centered statement.

**Slide text:**
```
Across SAT, coloring, clique, Sparse PCA, and OptGNN variants,
successful GNNs appear less like mysterious new solvers
and more like learned message-passing systems
that rediscover classical algorithmic concepts.

Support. Degree. Confidence.

The magic has a name.
```

**Speaker note:** "Thank you. The punchline: the surprising generalization of GNNs on hard
combinatorial problems is not mysterious. It is explainable, and the explanation points directly
to classical algorithmic theory. Questions?"

---

### Backup Slides *(after \appendix)*

**B1 — NeuroSAT architecture details**
Factor graph encoding, LSTM update equations (Eq. 1 from the concept learning paper), the
FLIP operator, readout via L_vote MLP.

**B2 — Support-core: formal construction**
r-support core definition, analogy to graph r-core, conditions under which the core coincides
with backbone variables, informal proof sketch of the dynamics theorem.

**B3 — Planted clique hardness landscape**
Regime boundaries for n = 500 and n = 1000. Known algorithmic results at each threshold:
Kucera (Easy), AKS / Feige–Grinberg (Medium), planted clique hardness conjecture (Hard).

**B4 — LPR algorithm: pseudocode and complexity**
O(n³) analysis. Runtime table from AAAI 2026 paper (avg ~25s, peak ~90s for n = 47k).

**B5 — OptGNN-Logit: rounding layer and why it exposes support**
Architecture diagram. Logit-space loss derivation. TFF clause ordering argument. Formal
Insights 1 and 2 from "The Last Percent."

**B6 — Sparse PCA: formal connection to Max-Clique**
Covariance matrix setup (Σ = I + βvv⊤), difficulty regimes, exact statement of the
Covariance Thresholding comparison result from the AAAI 2026 paper.

**B7 — Loss function deep dive**
Cross-entropy loss for NeuroSAT. Why a single-bit task loss generates rich internal structure.
Information-theoretic framing for why sparse supervision can still drive complex representation
learning.

---

## Missing Inputs: what to resolve before Beamer generation

### Blocking — do not generate public slides without these

| Item | Status | What to do |
|------|--------|------------|
| Attribution for `OptGNN_elad_s` | Anonymous NeurIPS 2026 submission | Confirm you can present this publicly. Decide how to attribute. |
| Exact solving rates from "The Last Percent" | Not yet in slides (schematic only) | Pull the four variant values from the paper. Replace schematic in Slides 36–37. |
| Exact probe accuracy values (Chapter 4) | Not yet in slides (schematic only) | Pull from paper. Replace schematic in Slide 37. |

### Important — affects accuracy

| Item | Status | What to do |
|------|--------|------------|
| Exact NeuroSAT test-size claim (Selsam 2019) | Paper not in folder; slides say "much larger than training" | Find Selsam ICLR 2019 paper, check what generalization range they reported. Update Slide 13 if a specific number is appropriate. |
| Sparse PCA claim precision | Slide 30 says "matches Covariance Thresholding in the tested regime" | Verify the exact theorem/claim wording in the AAAI 2026 paper. Use that wording on the slide. The stronger "first combinatorial algorithm" claim goes only in backup slide B6. |
| Figures from SAT paper (Figs. 2, 7) | PDFs only | TikZ or vector source needed for clean Beamer rendering of PCA plots. |
| Triangular PCA figure from coloring paper | PDF only | TikZ or vector source needed. |

### Optional

| Item | Notes |
|------|-------|
| WalkSAT vs. SupportSAT-01 convergence plot | Fig. 3 in the SAT paper. Good visual for Slide 21. |
| Weizmann PPTX | Check for reusable BP/GNN comparison diagrams. |
| ADYN abstract deadline | Confirm with organizers. |
| Audience ML background | If any attendees are ML-fluent, Slides 5–9 can be faster. |
| Beamer theme preference | `config.py` defaults to `Madrid`. Confirm or provide `.sty`. |

---

## Beamer generation command (after all blocking items resolved)

```bash
python agent.py \
  --title "Learned Algorithms or Classical Messages in Disguise?" \
  --papers "GNNs/my papers/" \
  --output adyn2026 \
  --compile
```

Settings to confirm in `config.py`:
- `TALK_TITLE` — confirmed
- `AUDIENCE` — "PhD students and postdocs in algorithms, combinatorics, TCS"
- `TALK_DURATION_MINUTES` — 50
- `TARGET_SLIDE_COUNT` — 41
- `TARGET_BACKUP_COUNT` — 7
- `BEAMER_THEME` — confirm
