# ADYN Summer School 2026 — Talk Plan (Revised)

**Event:** Summerschool on Algorithms, Dynamics, and Information Flow in Networks, TU Dortmund
**Speaker:** Dan Vilenchik, Ben-Gurion University of the Negev
**Duration:** 50 minutes (~42–45 content + 5–8 questions)
**Target deck:** ~46 main slides + 6 backup slides
**Audience:** PhD students and postdocs in algorithms, combinatorics, probability, graph theory, TCS

---

## Revision notes (v2)

Five changes from v1:

1. **Running question** added on Slide 3 and revisited at the end of each chapter.
2. **NeuroSAT opening** de-overclaimed: "appeared to learn SAT-solving behavior," not "learned to solve SAT." Added: "We still do not fully understand why this generalization happens."
3. **BP → GNN analogy** qualified: GNNs are BP-inspired, not literally BP. Classical BP has known regime failures; the puzzle is partly why GNNs sometimes go beyond what simple BP predicts.
4. **Chapter 1 expanded** to ~18 slides with a supervised-learning toy example, an explicit loss-function slide, a clearer train/test cartoon, and a slide separating architecture / parameters / training objective / decoding.
5. **Formal/empirical/analogy table** added as a new slide before Chapter 4's unified summary.

---

## Terminology note

The prompt draft used the term **"LDR"** — that term does not appear in the papers. The correct
term is **LPR (Least-Probable Removal)** from the AAAI 2026 clique paper. All slides use LPR.

---

## Title Variants

**Option A — Hook question (recommended for ADYN):**
> *Learned Algorithms or Classical Messages in Disguise? GNNs for Combinatorial Optimization*

**Option B — Direct research-pitch:**
> *Do GNNs Learn New Algorithms? Concept Discovery Across SAT, Clique, and Beyond*

**Option C — Result-forward:**
> *What GNNs Actually Learn When Solving Hard Problems: Support, Degree, and the Approximation–Solving Gap*

**Recommendation:** Option A. It captures the central tension cleanly, fits the ADYN framing of
algorithms and dynamics, and does not overclaim. Use Option B if you want the question more
direct; Option C if you want to front-load the result.

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
substantially outperforms the standard top-*k* strategy, and whose principle transfers directly to
Sparse PCA. Finally, analyzing a family of OptGNN variants, we find that the transition from strong
approximation (~99% constraint satisfaction) to exact solving is sharp and discontinuous, and is
governed precisely by whether the model learns a confidence signal. The conclusion is nuanced but
useful: GNNs are powerful, but their success is largely explainable through classical algorithmic
concepts, pointing toward a principled, concept-level theory of learned combinatorial optimization.

---

## Source Papers

| File | Paper | Role in talk |
|------|-------|--------------|
| `GNNs/my papers/Neuro_sat.pdf` | Shoham, Cohen, Wattad, Rika, Vilenchik. "Concept learning for algorithmic reasoning: Insights from SAT-solving GNNs." *Information Sciences* 726 (2026). | Chapter 2 main paper |
| `GNNs/my papers/graph_coloring.pdf` | Shoham, Rika, Vilenchik. "From Black Box to Algorithmic Insight: XAI in GNNs for Graph Coloring." AAAI 2025. | Chapter 2 second paper |
| `GNNs/my papers/20251-AAAI26.ShohamE-ML.pdf` | Shoham, Haber, Rika, Vilenchik. "Learning to Rank: How GNNs Solve Max-Clique and Sparse PCA." AAAI 2026. | Chapter 3 main paper |
| `GNNs/my papers/OptGNN_elad_s (1).pdf` | Anonymous. "The Last Percent: Concept Emergence and the Jump from Approximation to Solving in Neural CSPs." NeurIPS 2026 (submitted). | Chapter 4 main paper — **[VERIFY attribution before presenting publicly]** |
| `GNNs/background/2310.00526v7.pdf` | Yau, Karalias, Xu, Lu, Jegelka. "Are Graph Neural Networks Optimal Approximation Algorithms?" NeurIPS 2024. | Background for Chapter 4 |
| `GNNs/background/21-0449.pdf` | Cappart et al. "Combinatorial Optimization and Reasoning with Graph Neural Networks." *JMLR* 2023. | Background / Chapter 1 related work |

**Missing:** Original NeuroSAT paper (Selsam et al., ICLR 2019) — not in the folder. Training range
n ∈ [10, 40] is confirmed from the concept learning paper (Table 1). Test range up to n = 2000
verified from the same paper. **[VERIFY exact Selsam numbers independently before citing.]**

---

## The Running Question

The talk is organized around one question, introduced on Slide 3 and revisited at the close of each
chapter:

> **When a GNN appears to solve a hard combinatorial problem — what did it actually learn?**

Each chapter gives a partial answer for one problem class:

| Chapter | Setting | Answer |
|---------|---------|--------|
| 1 | GNNs in general | Maybe it learned a transferable message-passing rule. But what rule? |
| 2 | SAT and Coloring | It learned support — a classical confidence-like signal from solver theory. |
| 3 | Max-Clique / Sparse PCA | It learned degree-based ranking — a classical planted-graph heuristic. |
| 4 | SDP / OptGNN | Whether it learns a confidence concept determines whether it approximates or solves. |

The final takeaway slide gives the unified answer.

---

## Forty-Six-Slide Outline

---

### Opening + Chapter 1 — Crash Course: ML, GNNs, and the Promise
*(~18 slides)*

---

#### Slide 1 — Title slide

**Purpose:** Establish the talk.

**Visual:** Title, name, affiliation, event, date. Below the title, in smaller text: the running
question as a teaser.

**Slide text:**
```
Learned Algorithms or Classical Messages in Disguise?
GNNs for Combinatorial Optimization

Dan Vilenchik
Ben-Gurion University of the Negev
ADYN Summer School 2026

─────────────────────────────────────
Running question:
When a GNN appears to solve a hard combinatorial problem —
what did it actually learn?
```

**Speaker note:** "The title is a question, and there's a smaller question underneath it. I'll carry
both through the entire talk. By the end we'll have an answer — not a complete one, but a
useful one. Let me start with a puzzle."

---

#### Slide 2 — NeuroSAT appeared to learn SAT-solving behavior from tiny instances

**Purpose:** The hook. Establish the empirical puzzle without overclaiming.

**Visual:** Two boxes side by side.
- Left: "Training — random 3-SAT, n ∈ [10, 40] variables. Label: SAT / UNSAT only."
- Right: "Test — random 3-SAT, n up to [VERIFY from Selsam paper] variables. Same GNN, no retraining."
- Bridge arrow underneath: "It still works — sometimes. Why?"

**Slide text:**
```
NeuroSAT (Selsam et al., 2019):
  Train:  n ∈ [10, 40] variables   (exact solver provides labels)
  Test:   much larger instances
  Label:  SAT / UNSAT only — single bit of supervision

Observation:
  The same GNN generalized surprisingly far beyond its training range.

Caveat:
  We still do not fully understand why this generalization happens.
  That is the puzzle.
```

**Speaker note:** "I want to be precise here. NeuroSAT did not solve SAT in an algorithmic
sense. It was not designed to be a general-purpose SAT solver, and its authors did not claim
that. What it did — surprisingly — is generalize to much larger instances than it was trained on,
with only a binary SAT/UNSAT label as supervision. That train-small/test-large behavior created
a serious interpretability puzzle. We don't fully understand it yet. What we did is start
asking: what is encoded in the model's internal representations? That question, it turns out,
has an answer."

---

#### Slide 3 — The running question

**Purpose:** State the organizing question of the talk explicitly before the ML background.

**Visual:** Large centered question. Below it: four chapter headings with blank answer slots to
be filled as the talk proceeds.

**Slide text:**
```
When a GNN appears to solve a hard combinatorial problem —
what did it actually learn?

Chapter 1: We introduce GNNs and the puzzle.
Chapter 2: [SAT and Coloring — answer revealed]
Chapter 3: [Clique and Sparse PCA — answer revealed]
Chapter 4: [SDP / OptGNN — answer revealed]
```

**Speaker note:** "I'll come back to this slide at the end of each chapter. Think of it as a
running scoreboard. Each chapter gives us a partial answer for one setting. The final slide will
close the loop."

---

#### Slide 4 — The problem setting: combinatorial optimization on graphs

**Purpose:** Define the problem class cleanly for a theory audience.

**Visual:** A simple factor graph. Variables as circles, clauses/constraints as squares, edges
connecting each variable to the clauses it appears in.

**Slide text:**
```
Input:    a graph or formula
Goal:     find an assignment satisfying all (or most) constraints
Hard:     NP-complete in the worst case

Examples in this talk:
  3-SAT:     assign TRUE/FALSE to variables
  Coloring:  assign colors to vertices, no two adjacent the same
  Clique:    find a large complete subgraph
```

**Speaker note:** "These are canonical NP-hard problems and they will serve as test cases
throughout the talk. Each one has a slightly different structure, and that structural difference
will matter when we ask what concept the GNN learned."

---

#### Slide 5 — Supervised learning: the basic setup

**Purpose:** Define the ML setup for a non-ML audience, grounded with a toy example.

**Visual:** A three-row pipeline with a tiny toy example running alongside each step.
- Row 1: Training data: "(formula, SAT?) pairs." Toy: 5 formulas with YES/NO labels.
- Row 2: Model: "a function f_θ that maps formula → prediction." Toy: a black box with a dial θ.
- Row 3: Training: "adjust θ so predictions match labels." Toy: arrow showing the dial turning.

**Slide text:**
```
Training data:    (instance, label) pairs — solved examples
Model:            f_θ: instance → prediction   (θ = learned parameters)
Loss:             how wrong is f_θ(instance) compared to the label?
Training:         adjust θ to reduce total loss over training data
Test:             freeze θ, evaluate f_θ on new unseen instances

Toy example:
  Instance: a small SAT formula
  Label:    SAT or UNSAT (from an exact solver)
  Task:     learn to predict without running the exact solver
```

**Speaker note:** "If you've never seen this setup: you give the model many solved examples.
It adjusts its parameters to match the labels. When done training, you freeze everything and
evaluate on new instances it has never seen. Whether it works on new instances is generalization.
That's the central question."

---

#### Slide 6 — The loss function: what it measures and why it matters

**Purpose:** Make the role of the loss explicit. This audience will want to know what exactly
is being optimized.

**Visual:** A number line from 0 to ∞ labeled "Loss." Left end: "prediction matches label
perfectly." Right end: "prediction is completely wrong." Arrow pointing left: "training pushes
here." Beneath: the specific NeuroSAT loss written out.

**Slide text:**
```
The loss function encodes what we want.

For NeuroSAT:
  Loss = cross-entropy between predicted P(SAT) and true label ∈ {0,1}
  → model learns to push P(SAT) near 1 for satisfiable instances
  → and near 0 for unsatisfiable ones

Why this matters:
  The loss says nothing about which variables are TRUE or FALSE.
  It says nothing about support, degree, or any other solver quantity.
  If those concepts appear in the embeddings, they emerged spontaneously.
```

**Speaker note:** "The loss is the only task signal the model receives. NeuroSAT's loss is a single
bit per instance: SAT or UNSAT. Everything else the model does — how it organizes its internal
representations, what concepts it encodes — is not prescribed by the loss. That is the puzzle.
The model learns far more structure than the loss requires."

---

#### Slide 7 — Train, test, and generalization: the central issue

**Purpose:** Establish train/test and why size-generalization is non-trivial.

**Visual:** A cartoon in two panels.
- Panel 1 (Train): a small pool of SAT instances, n ∈ [10, 40]. Model trained here.
- Panel 2 (Test): a much larger pool of instances, n up to [VERIFY]. Same frozen model applied.
- Underneath: "If test performance is strong, the model learned something structural — not
  instance-specific."

**Slide text:**
```
Training set:     instances from distribution D_train
Test set:         instances from distribution D_test (same problem, possibly different size)

Ordinary generalization: D_train and D_test are similar
Size generalization:     D_test instances are much larger than D_train

For NeuroSAT:
  D_train: n ∈ [10, 40]
  D_test:  much larger [VERIFY range from Selsam paper]

If the model generalizes across sizes:
  → it learned something that doesn't depend on n
  → what is that something?
```

**Speaker note:** "Ordinary generalization — same distribution, held-out examples — is the
usual story. What's unusual here is cross-size generalization. A model trained on tiny instances
working on large ones suggests the model found an invariant of the problem structure that scales.
That invariant is what we're hunting."

---

#### Slide 8 — Four things to keep separate

**Purpose:** Give the audience a precise vocabulary before introducing GNNs. This prevents
confusion between what was designed and what was learned.

**Visual:** A clean 2x2 or 4-row table.

**Slide text:**
```
1. Architecture:
   The structure of the model — how information flows.
   (For a GNN: nodes, edges, message-passing rounds)
   Designed by the researcher.

2. Parameters (weights):
   The numerical values inside the model.
   Learned from data during training.

3. Training objective (loss):
   What the model is rewarded for predicting correctly.
   Designed by the researcher.

4. Decoding strategy:
   How the model's output scores are turned into a discrete solution.
   Designed by the researcher; can be improved post-training.

When we say "the model learned X", we mean X is in the parameters —
not designed, not prescribed by the loss, but emergent.
```

**Speaker note:** "This distinction will matter a lot when I describe our results. When I say
'the GNN learned support,' I mean support is decodable from the learned parameters — from the
model's internal representations — even though the loss never mentioned support. The concept
emerged. That's the interesting part."

---

#### Slide 9 — Graph-structured problems need graph-structured models

**Purpose:** Motivate GNNs specifically.

**Visual:** Left: adjacency matrix of a graph under two different node labelings. Right: both
represent the same graph. Label: "Any useful model must be permutation-invariant."

**Slide text:**
```
Challenge: same graph, different node labels → same combinatorial structure
Standard NN: fails (different inputs, no invariance)
GNN: operates on structure, ignores labels ✓

Also:
  Graphs are variable-size     → can't use fixed-size inputs
  Constraints are local        → local message passing is a natural inductive bias
  Sparsity is common           → GNNs scale linearly with edges
```

**Speaker note:** "Combinatorial problems on graphs are permutation-invariant: relabeling nodes
doesn't change the answer. Standard neural networks can't handle this — they see different
inputs. GNNs are built for it. They also scale with the number of edges, not the total number of
possible graphs. This makes them practically usable on large instances."

---

#### Slide 10 — What is a GNN?

**Purpose:** Give a clean formal definition that a theorist can hold.

**Visual:** A small graph (6 nodes). Each node labeled with an embedding vector h_v ∈ ℝ^d.
An arrow from each neighbor to a central node, labeled "message." Two-step update rule written out.

**Slide text:**
```
Each vertex v has a state (embedding) h_v ∈ ℝ^d

Each round t:
  1. Aggregate:   m_v = AGG({h_u : u ∈ N(v)})
  2. Update:      h_v ← UPDATE(h_v, m_v)

After T rounds: predict from embeddings {h_v}

Both AGG and UPDATE are learned neural networks (the parameters).
After T rounds, each v has "seen" its T-hop neighborhood.
```

**Speaker note:** "Think of it as a distributed algorithm. Each node has a memory vector. Each
round it collects messages from neighbors, aggregates them, and updates its state. After T rounds,
it has a summary of a T-hop ball. The only difference from a designed algorithm is that
AGG and UPDATE are learned from data. What they learn is our question."

---

#### Slide 11 — Running toy example: initial state

**Purpose:** Anchor the abstract definition with a concrete example.

**Visual:** A specific small graph: 6 vertices (three forming a triangle), labeled A–F. Each vertex
gets an initial random embedding shown as a small colored bar.

**Slide text:**
```
Graph:       6 vertices, 7 edges
Embeddings:  randomly initialized ∈ ℝ^d
Round 0:     no information has been shared
             every vertex looks identical to the model
```

**Speaker note:** "I'll run this example for three slides. We start from random embeddings.
All nodes are indistinguishable to the model at this point."

---

#### Slide 12 — Running toy example: one round of message passing

**Purpose:** Show the mechanics of one step.

**Visual:** Same graph. Arrows flowing from neighbors of vertex A toward A. Aggregate operation
shown. Updated embedding for A highlighted.

**Slide text:**
```
Round 1:
  A receives messages from B, C, D
  m_A = AGG(h_B, h_C, h_D)
  h_A ← UPDATE(h_A, m_A)

After round 1: A knows about its 1-hop neighborhood
After round 2: A knows about its 2-hop neighborhood
After T rounds: A has a summary of a T-hop ball

The embedding h_A is now a function of local graph structure.
```

**Speaker note:** "One round of message passing gives each node a view of its immediate
neighbors. The T-round embedding is a function of the T-hop neighborhood. For problems where
the relevant combinatorial structure is local, this is enough."

---

#### Slide 13 — Running toy example: readout and decoding

**Purpose:** Complete the pipeline and introduce the decoding step.

**Visual:** Final embeddings after T rounds. MLP output per vertex giving scores s_v ∈ [0, 1].
Arrow to a discrete solution (colored vertices / TRUE/FALSE labels).

**Slide text:**
```
After T rounds:
  MLP(h_v) → score s_v ∈ [0, 1]   for each vertex v

Interpretation depends on the problem:
  s_v ≈ 1 → v likely in clique / colored correctly / TRUE
  s_v ≈ 0 → v likely not in solution

Decoding (not learned):
  Top-k:  take k highest-scoring vertices
  LPR:    remove lowest-scoring vertices until feasible
  Other:  problem-specific rounding

The scores are the learned output. The decoder is a design choice.
```

**Speaker note:** "The scores come from the learned parameters. The decoder does not — it's a
separate design decision. A key result in Chapter 3 is that the same learned scores can give very
different performance depending on which decoder you use. The concept is in the scores; the
decoding strategy determines how well you extract it."

---

#### Slide 14 — Belief propagation: the classical message-passing template

**Purpose:** Set up the BP–GNN analogy for a theory audience.

**Visual:** A small factor graph (variables = circles, clauses = squares). Messages labeled along
edges with their interpretation: "P(x=TRUE | neighbors)."

**Slide text:**
```
Belief propagation (BP):
  Messages along edges of a factor graph
  Message = a structured probabilistic summary
    (marginal belief, warning, bias, ...)
  Update rule: analytically derived from the probabilistic model
  Convergence: exact on trees; approximate (often good) on sparse graphs

Connections:
  Survey propagation: BP on random SAT → identifies backbone variables
  LDPC decoding: BP on Tanner graph → near-optimal for some codes
```

**Speaker note:** "BP is the gold standard of principled message passing. The messages have an
interpretation — they represent beliefs about variable assignments. The update rule is derived from
first principles, not learned. The question for GNNs is: when you let a neural network learn its
own version of BP, what does it discover?"

---

#### Slide 15 — From belief propagation to a GNN

**Purpose:** The central analogy. Build it step by step.

**Visual:** Three-column table progression.
- Column 1 (BP): scalar/probability message, hand-designed update, probabilistic model objective.
- Column 2 (Generalize message): vector in ℝ^d replaces the scalar.
- Column 3 (GNN): learned vector message, learned update, task loss.

**Slide text:**
```
Step 1 — Classical BP
  message(u→v) = f_BP(assignment, neighbors)
  interpretable: marginal, warning, bias

Step 2 — Generalize the message
  message(u→v) ∈ ℝ^d    (high-dimensional, latent)

Step 3 — Learn the update rule from data
  UPDATE(h_v, m_v) = GRU/MLP(h_v, m_v ; θ)

Result: a GNN is BP-inspired high-dimensional learned message passing.
        Not BP. But the right mental model for this audience.
```

**Speaker note:** "The GNN is not BP. But for this audience, the BP analogy is the right place
to start. Both pass messages along a factor/constraint graph. BP passes structured probabilistic
summaries; the GNN passes high-dimensional learned vectors. BP derives its update rule
analytically; the GNN learns it from data. The question of what the GNN learned is, in a sense,
a question about what it rediscovered or reinvented from the BP world."

---

#### Slide 16 — The analogy has limits — and that is part of the puzzle

**Purpose:** Qualify the BP analogy before anyone in the audience objects. This earns credibility
with a TCS / probability crowd.

**Visual:** Left column "What BP gives us": clean analytic rules, regime analysis, phase transition
theory. Right column "What the GNN does that BP doesn't explain": generalizes beyond BP's
known failure regimes, sometimes works near or past the clustering threshold.

**Slide text:**
```
Classical BP has known failure regimes:
  On random CSPs: BP works well in the replica-symmetric phase
  Near and past clustering/condensation: naive BP fails or diverges
  Beyond the satisfiability threshold: meaningless

GNNs are not bound by those regimes in the same way:
  They optimize a task loss, not a probabilistic model
  They may learn to route information differently from BP

Part of the puzzle:
  Why do GNNs sometimes generalize beyond where BP is known to work?
  That is still open. The concept-learning framework is one lens into it.
```

**Speaker note:** "I want to flag this explicitly. If you're thinking 'but BP breaks down near
the clustering threshold on random SAT' — you're right. GNNs don't literally run BP. They're
BP-inspired high-dimensional learned procedures. The BP analogy is useful for building intuition,
but it's not the literal algorithmic claim. One of the genuinely open questions is why GNNs
sometimes manage to work in regimes where simple BP would fail. Our concept-learning framework
is one step toward understanding that, not the final answer."

---

#### Slide 17 — NeuroSAT: the promise

**Purpose:** Establish the motivating result clearly, with corrected language.

**Visual:** Two-column contrast. Left: small SAT formula graph (5 variables, 3 clauses).
Right: large factor graph (schematic). Underneath: training vs. test regime side by side.

**Slide text:**
```
NeuroSAT (Selsam et al., 2019):
  Architecture:   message-passing GNN on CNF factor graph
  Training:       SAT/UNSAT label only (single-bit supervision)
  Training set:   n ∈ [10, 40] variables, near SAT/UNSAT phase transition
  Test:           much larger instances [VERIFY exact range from Selsam 2019]

Observation:
  The trained GNN showed surprisingly strong generalization beyond its training range.
  The reason is not fully understood.

Our question:
  What did it learn internally?
```

**Speaker note:** "I want to repeat the caveat: NeuroSAT is not a general SAT solver. The
original paper did not claim that. What it showed is that a very simple GNN, trained with
one bit of supervision per instance, organized its internal representations in a way that
generalized to much larger instances. That suggests it found something structural. Our project
is to name that something."

---

#### Slide 18 — Chapter 1 partial answer + the research program

**Purpose:** Close Chapter 1, revisit the running question, and introduce the concept-learning
framework.

**Visual:** Running question displayed at top. Below: the Chapter 1 partial answer. Then the
method pipeline.

**Slide text:**
```
Running question: When a GNN appears to solve a hard combinatorial problem —
                  what did it actually learn?

Chapter 1 answer (partial):
  Maybe: a transferable message-passing rule that captures structural invariants.
  But which rule? The training loss doesn't specify it.
  That's the interpretability puzzle.

Our method — concept learning:
  Project learned embeddings to low-dimensional PCA space.
  Ask: does the projection align with known algorithmic quantities?
  Verify: a simple linear probe predicts the concept on held-out instances.

A concept is operationally defined:
  ĝ(v) = w⊤ h_v + b   (linear probe, held-out instances)
  Falsifiable: fails if the quantity isn't predictable above baseline.
```

**Speaker note:** "The concept-learning framework is the methodological core. We don't assume
the model learned anything in particular. We ask whether specific classical algorithmic quantities
are encoded in the embeddings, and we test that with a probe. If support is encoded, the probe
can predict it from the embeddings on instances the probe never saw. Let's see what we find."

---

### Chapter 2 — SAT and Coloring: Support as Confidence
*(~11 slides)*

---

#### Slide 19 — Running question, Chapter 2: SAT and Coloring

**Purpose:** Signal the chapter transition and re-anchor the running question.

**Visual:** Running question at top with Chapter 2 highlighted. A small SAT factor graph and
small 3-colored graph side by side — the two problems for this chapter.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 2 setting:
  Problem 1 — SAT (NeuroSAT, Shoham et al. 2026)
  Problem 2 — Graph 3-Coloring (GNN-GCP, Shoham et al. 2025)

Both GNNs trained with single-bit binary supervision only.
We probe their learned embeddings.
```

**Speaker note:** "We now ask the running question for two constraint-satisfaction problems.
Both GNNs were trained with only a binary label. Neither loss mentions any solver quantity.
Let me show you what we found."

---

#### Slide 20 — Concept learning in AI: why it matters here

**Purpose:** Give the broader XAI context efficiently. Don't linger.

**Visual:** Three example boxes: vision ("beak" in a bird classifier), medicine ("lesion boundary"),
algorithms ("variable confidence").

**Slide text:**
```
XAI usually: which input features drove this decision?
             (SHAP, LIME, GradCAM)

For algorithmic tasks: wrong level of analysis.
  "x₁ appears in clause 7" is a feature — instance-specific, not transferable.
  "x₁ has high support" is a concept — meaningful across instances.

We want:
  Compact, interpretable quantities that explain the model's internal dynamics
  across inputs and iterations — not just for one instance.
```

**Speaker note:** "Standard XAI methods find important features for a specific input. For
combinatorial tasks, we need something different: global algorithmic concepts that explain how
the model behaves across all instances. That requires looking at the geometry of the internal
representations over many runs, not just attribution maps for one input."

---

#### Slide 21 — SAT as a factor graph: our running example

**Purpose:** Introduce the SAT instance visually before defining support.

**Visual:** TikZ factor graph. Formula: (x₁ ∨ x̄₂ ∨ x₃) ∧ (x₁ ∨ x₂ ∨ x̄₃).
Variable nodes = circles, clause nodes = squares, edges connecting literals to their clauses.

**Slide text:**
```
CNF formula: (x₁ ∨ x̄₂ ∨ x₃) ∧ (x₁ ∨ x₂ ∨ x̄₃)

Factor graph:
  Variable nodes: x₁, x₂, x₃  (and negations x̄₁, x̄₂, x̄₃)
  Clause nodes:   C₁, C₂
  Edges:          literal ↔ clause where literal appears

NeuroSAT runs T rounds of message passing on this graph.
We ask: what do the node embeddings encode after training?
```

**Speaker note:** "NeuroSAT operates on the factor graph, not the formula directly. Literals and
clauses are both node types. Messages flow between them, just like in survey propagation. Now
I'll tell you what we found in those messages."

---

#### Slide 22 — What is "support"?

**Purpose:** Introduce the key concept formally before showing any data.

**Visual:** Toy formula. A clause of type TFF (one TRUE literal, two FALSE) highlighted. The
TRUE literal labeled "the sole supporter of this clause."

**Slide text:**
```
Assignment ϕ. Variable x. Clause C.

x supports C under ϕ  ⟺
    C is satisfied, and x is the ONLY satisfied literal in C.
    (clause type TFF: one True, two False)

support_ϕ(x) = |{clauses C : x alone satisfies C}|

High support:  x is load-bearing → flipping x immediately breaks many clauses
Low support:   x is replaceable → safe to flip in local search

This quantity appears in: WalkSAT, Survey Propagation, backbone analysis.
```

**Speaker note:** "Support is a classical notion. Three very different algorithmic traditions —
WalkSAT (local search), Survey Propagation (message passing), and backbone analysis
(combinatorial structure) — independently discovered the same signal. A variable with high
support is one you cannot safely flip. It's a confidence signal. Now I'll show you that NeuroSAT,
trained only on SAT/UNSAT labels and never told about support, encodes precisely this quantity."

---

#### Slide 23 — Support as confidence: a toy example

**Purpose:** Make the intuition concrete before showing the PCA plots.

**Visual:** Two small formulas side by side.
- Formula A: x₁ is the sole TRUE literal in 3 of 4 clauses it appears in → support = 3 → HIGH.
- Formula B: x₁ appears in balanced clauses, rarely the sole satisfier → support = 0 → LOW.

**Slide text:**
```
High support (confidence):
  x₁ = TRUE. Of 4 clauses containing x₁:
  3 are satisfied only because of x₁ (type TFF).
  Flipping x₁ breaks those 3 clauses immediately.
  → Do not flip x₁.

Low support (uncertain):
  x₁ = TRUE. All clauses containing x₁ have other TRUE literals.
  Flipping x₁ costs nothing immediately.
  → Safe to flip.
```

**Speaker note:** "If you were designing a local-search SAT solver, support is exactly the kind
of thing you'd track. The variable with high support is one you want to protect. The variable
with low support is one you can explore. NeuroSAT, trained with no knowledge of this, encodes
it anyway. That's the finding."

---

#### Slide 24 — NeuroSAT embeddings: PCA reveals structure

**Purpose:** Show the empirical evidence for concept emergence.

**Visual:** Schematic of the PCA plot (Fig. 2 in the SAT concept learning paper). Literal embeddings
projected to 2D. Literal and its negation on opposite sides of PC1 = 0. Support clauses (TFF)
with higher |PC1| values. Color coding by support count.

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
```

**Speaker note:** "The model is 128-dimensional. Yet 98% of what matters lives in 2 dimensions,
and those 2 dimensions directly encode support and assignment consistency. We verify this with
linear probes on held-out instances — the structure you see here is predictive, not decorative."

---

#### Slide 25 — Main finding: support governs NeuroSAT's dynamics

**Purpose:** State the result precisely — both empirical and theoretical components.

**Visual:** Schematic: "Support (PC1 of embedding) → governs which variables get flipped each
iteration → support-core emerges (analogous to r-core in graphs)."

**Slide text:**
```
Theorem (informal):
  Under assumptions on instance distribution and weights,
  NeuroSAT's dynamics fix variables in decreasing order of support,
  starting with the r-support core — a structure analogous to the graph r-core.

Empirically:
  Linear probe predicts support from embeddings on held-out instances.
  Variables with PC1 near 0 are reassigned in the next iteration.
  Variables with PC1 far from 0 are locked in, consistent with a satisfying assignment.

Payoffs:
  StudentNeuroSAT: 91% fewer parameters, comparable performance.
  SupportSAT-01: WalkSAT variant that converges faster on n = 1500.
```

**Speaker note:** "Two parts: empirical (support is decodable by a linear probe) and theoretical
(under certain assumptions, the dynamics formally reduce to tracking the support-core). The
theory is for a simplified architecture, but it gives a mechanistic account of what the full model
is doing. And the concept is immediately useful: once you know the model learned support, you
can compress it and improve WalkSAT with the insight."

---

#### Slide 26 — Graph coloring: same concept, different geometry

**Purpose:** Show that support reappears in a structurally different problem.

**Visual:** Left: small valid 3-colored graph (6 vertices). Right: 2D PCA of GNN-GCP embeddings
showing the triangular structure. High-support vertices near triangle corners.

**Slide text:**
```
GNN-GCP (Lemos et al., 2019):
  Trained to predict 3-colorability (binary label only)
  Message-passing LSTM, 64-dim embeddings

Support in coloring:
  support(v) = number of neighbors v has in each color class other than its own

What the 2D PCA projection shows:
  Embeddings form a triangle; color classes cluster near corners.
  High-support vertices are closest to triangle corners (committed to their color).
  Low-support vertices sit near the center (color assignment still uncertain).
```

**Speaker note:** "In graph coloring, support has an analogous meaning: the number of neighbors
in competing color classes. A high-support vertex is one that has many neighbors of conflicting
colors — it's strongly committed to its own color class. Low-support vertices are still ambiguous.
The GNN encodes this with a beautiful geometry: the triangle."

---

#### Slide 27 — Coloring: support connects to a 1994 algorithm

**Purpose:** Make the classical connection explicit and surprising.

**Visual:** Side-by-side: SAT (literals on PC1 axis) and Coloring (vertices near triangle corners).
Same concept, different representation. Below: reference to Alon–Kahale (1994).

**Slide text:**
```
Support in SAT:      clauses uniquely satisfied by x
Support in coloring: neighbors v has in each other color class

In both cases:
  High support → high confidence → embedding far from ambiguous region
  Low support  → low confidence  → near center, assignment may still change

This concept was used in hand-designed algorithms:
  WalkSAT (1994) for SAT
  Alon–Kahale (1994) for graph coloring

GNNs trained in 2019 and 2023 rediscover them from data, without supervision.
```

**Speaker note:** "The Alon–Kahale coloring algorithm from 1994 was designed around exactly
this support concept. The GNN, trained thirty years later with no knowledge of that algorithm,
encodes the same quantity in its embeddings. That's the central message of Chapter 2: GNNs
don't invent new algorithmic primitives. They rediscover classical ones."

---

#### Slide 28 — Chapter 2: running question answered

**Purpose:** Pause, crystallize, and revisit the running question explicitly.

**Visual:** Running question at top, now with the Chapter 2 answer filled in.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 2 answer:
  In SAT and Coloring — it learned support.
  A classical confidence-like signal from solver theory.
  Present in both GNNs, without explicit supervision.

Evidence:
  SAT:       linear probe, PCA structure, theoretical analysis
  Coloring:  linear probe, triangular embedding geometry

Payoff:
  91% model compression (StudentNeuroSAT)
  Faster WalkSAT variant (SupportSAT-01)

Does the same pattern hold for a structurally different problem?
```

**Speaker note:** "Chapter 2 answer: support. The GNN, trained with only binary labels on two
very different constraint-satisfaction problems, learned to compute the same classical algorithmic
quantity that human experts designed into their solvers. Let's now move to a structurally different
problem — Max-Clique — and ask the same question."

---

### Chapter 3 — Clique: Degree, Ranking, and Cross-Domain Generalization
*(~8 slides)*

---

#### Slide 29 — Running question, Chapter 3: Max-Clique

**Purpose:** Signal chapter transition and re-anchor the running question.

**Visual:** Running question at top. Small planted clique graph on the right.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 3 setting:
  Problem — Max-Clique (Shoham et al., AAAI 2026)
  No factor graph. No clause structure.
  The signal is in vertex degrees, not constraint satisfaction.

If the concept-learning story is robust,
it should survive this structural change.
```

**Speaker note:** "SAT and coloring both have a natural factor-graph structure — that's where BP
is most natural. Clique is different. It's a purely graph-theoretic problem with no explicit
constraints. The fact that a similar concept-learning story holds there is a stronger test of
the framework."

---

#### Slide 30 — Planted clique: three regimes

**Purpose:** Introduce the benchmark and the theoretical difficulty landscape.

**Visual:** Three labeled regions on a number line of planted clique size k.
- Hard: k = O(√n) — planted clique conjecture; believed computationally intractable.
- Medium: k = Ω(√n) — spectral methods and LPR work.
- Easy: k = Ω(√n log n) — simple degree ranking suffices.

**Slide text:**
```
Random graph G(n, 1/2):
  Largest clique ≈ 2 log₂ n  (believed hard to find by efficient algorithms)

Planted clique: add a k-clique to G(n, 1/2)

Difficulty regimes (calibrated empirically for n = 1000):
  Easy:   k ≥ ~62  — Top-k by degree recovers the clique
  Medium: k ∈ [36, 61] — LPR or spectral methods needed
  Hard:   k ≤ 35  — planted clique conjecture; no known efficient algorithm
```

**Speaker note:** "We evaluate GNNs on instances calibrated to this landscape. This is critical:
without knowing the difficulty regime, you can't tell whether a GNN 'solving' clique is impressive
or trivial. Previous GNN evaluations for clique typically used uncontrolled benchmarks. Our
contribution here is partly methodological: evaluate under principled hardness control."

---

#### Slide 31 — Degree as a classical signal: helpful but noisy

**Purpose:** Establish the degree baseline before introducing the GNN.

**Visual:** Small planted clique graph (n = 10, k = 4). Degree table:
clique vertices {6, 7, 7, 8}; non-clique vertices {2, 3, 4, 7}. One non-clique vertex at degree 7 —
the "impostor" — highlighted.

**Slide text:**
```
Degree heuristic:
  Clique vertices receive a degree "boost" from the planted edges.
  Sort vertices by degree, take top k.

Works in the Easy regime: the boost is large enough.

Fails when k is smaller (Medium/Hard):
  "Impostors" — non-clique vertices with high random degree — creep into the top k.
  The candidate set is not a valid clique.

Classical open question: what signal, beyond degree, helps in the Medium regime?
```

**Speaker note:** "The degree heuristic is the simplest possible approach. In easy cases it's
enough. In medium and hard cases it's fooled by impostors. The interesting question is whether
the GNN does something more clever — or whether it just learns a sophisticated version of degree."

---

#### Slide 32 — What the GNN learns: degree-based ranking

**Purpose:** State the core finding for clique.

**Visual:** PCA of GNN vertex embeddings. PC1 highly correlated with vertex degree. GNN output
score vs. degree scatter plot showing near-linear relationship.

**Slide text:**
```
GNN embedding analysis (PCA):
  PC1 of vertex embeddings: highly correlated with vertex degree.
  GNN output scores ≈ monotone function of degree.

Finding:
  The GNN learns degree-based ranking.
  It does not appear to learn a fundamentally new signal.

But: the decoder matters.
  Top-k with degree fails on medium instances.
  A smarter decoder improves performance substantially.
```

**Speaker note:** "The GNN is doing sophisticated degree estimation — it uses multi-hop
information so it's better than raw degree, but the principle is the same. The concept is not
support in the SAT/coloring sense: it's ranking, specifically degree-like ranking. The interesting
result comes next: even with this relatively simple concept, a better decoder changes the outcome
substantially in the medium regime."

---

#### Slide 33 — Top-k vs. LPR: two decoders, very different performance

**Purpose:** Introduce LPR and show the performance gap.

**Visual:** Side-by-side comparison.
- Left (Top-k): select k highest-scoring vertices. Impostor included.
- Right (LPR): iteratively remove lowest-scoring vertex until remainder is a clique. Impostor eliminated.

**Slide text:**
```
Top-k:
  Select k vertices with highest GNN scores.
  O(n²). Fails on Medium instances: impostors included.

LPR — Least-Probable Removal:
  Start with all n vertices.
  Remove vertex with lowest score (least likely to be in clique).
  Repeat until the remaining set forms a clique.
  O(n³), practical: avg ~25s; peak ~90s for n = 47k.

LPR significantly outperforms Top-k in Medium and Hard regimes.
```

**Speaker note:** "LPR inverts the perspective: instead of selecting likely clique vertices, it
prunes unlikely ones. When impostors are present, they have lower scores than genuine clique
vertices — LPR removes them. Top-k would have included them immediately. Same underlying
concept (degree-based ranking), very different decoding strategy, substantially different results."

---

#### Slide 34 — Cross-domain: the same GNN solves Sparse PCA

**Purpose:** The universality result — one of the strongest in the clique paper.

**Visual:** Two-panel diagram.
- Left: graph with planted clique, vertices color-coded by degree boost.
- Right: covariance matrix with planted spike, rows color-coded by row-sum.
- Connection arrow: "row-sum ranking."

**Slide text:**
```
Sparse PCA (single-spike model):
  Covariance Σ = I + β·vv⊤,  v sparse (size k).
  Goal: recover the support of v.

Structural analogy to clique:
  Clique vertices:   higher degree due to within-clique edges
  Spike variables:   larger row-sums due to the β·vv⊤ perturbation

Transfer experiment:
  GNN trained on Max-Clique → applied to Sparse PCA → succeeds.
  GNN trained on Sparse PCA → applied to Max-Clique → succeeds.

The learned principle: row-sum ranking — universal across both domains.

New algorithmic result: the Max-Clique GNN with LPR is the first
combinatorial algorithm matching Covariance Thresholding for Sparse PCA,
with no hyperparameters.
```

**Speaker note:** "We trained a GNN to find cliques. We then gave it a covariance matrix from
Sparse PCA — a completely different problem. It succeeds, because both problems share the same
underlying mathematical structure: identify a small subset with elevated row-sums. In learning
degree ranking for cliques, the GNN learned row-sum ranking in general. And we prove a new
algorithmic result: the Max-Clique GNN with LPR is the first combinatorial algorithm that matches
Covariance Thresholding, the spectral state-of-the-art for Sparse PCA, with no hyperparameters."

---

#### Slide 35 — Chapter 3: running question answered

**Purpose:** Crystallize Chapter 3 and revisit the running question.

**Visual:** Running question with Chapter 3 answer filled in. Summary table showing Chapters 2
and 3 together.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 3 answer:
  In Max-Clique — it learned degree-based (row-sum) ranking.
  A classical signal from planted-graph theory.
  Transfers directly to Sparse PCA.

Chapter 2 answer (recap):
  In SAT/Coloring — it learned support.

Theme:
  Different problem structures → different concepts.
  But in each case: a classical, analyzable, interpretable quantity.

Chapter 4: what if we ask not "what did the GNN learn"
           but "what must it learn in order to solve, not just approximate"?
```

**Speaker note:** "Chapter 3 answer: degree ranking. Different from support, but still a classical
signal. The GNN didn't invent anything new. Let's now go to Chapter 4, where we flip the question:
instead of analyzing what a given GNN learned, we ask what concept is necessary for a GNN to
cross the threshold from approximating to solving."

---

### Chapter 4 — The Last Percent: Approximation, Solving, and the Concept Gap
*(~9 slides)*

---

#### Slide 36 — Running question, Chapter 4: SDP / OptGNN

**Purpose:** Signal chapter transition and frame the new angle on the running question.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 4 new angle:
  Instead of asking what a given model learned,
  we ask: what must a model learn in order to solve, not just approximate?

Setting:
  OptGNN (Yau et al., NeurIPS 2024) and controlled variants.
  Problem: SAT and NAE-SAT (hypergraph 2-coloring).
  We introduce architectural modifications and ask:
  which one enables exact solving? And why?
```

**Speaker note:** "This chapter turns the question around. Instead of reverse-engineering a
trained model, we run a controlled design experiment. We start from a well-understood
architecture (OptGNN), make controlled modifications inspired by classical heuristic design, and
ask which modification enables the transition from strong approximation to exact solving. The
answer, again, is a classical concept."

---

#### Slide 37 — The approximation–solving gap

**Purpose:** Introduce the central distinction of Chapter 4.

**Visual:** A number line from 0% to 100% constraint satisfaction.
- "Random baseline" at 7/8 ≈ 87.5%.
- "OptGNN" at ~99%.
- "Solving" at 100%.
- The gap 99% → 100% labeled "the last percent."

**Slide text:**
```
Random 3-SAT:
  A random assignment satisfies each clause with probability 7/8.
  So 87.5% approximation is trivially achievable.

OptGNN (Yau et al., NeurIPS 2024): reaches ~99%.

Exact solving (100%):
  Håstad (2001): improving beyond 7/8 is NP-hard in the worst case.
  For random instances above the threshold: the last 1% requires
  coordinated changes across many variables simultaneously.

From ~99% to 100% is not a marginal gain — it is a qualitative transition.
```

**Speaker note:** "I want to separate two very different capabilities. An assignment satisfying
99% of clauses can still be far from any satisfying assignment — the last violated clauses may
trigger cascades of required changes. This is the gap we study, and understanding it requires
asking what concept the model has or hasn't learned."

---

#### Slide 38 — OptGNN: SDP relaxations built into a GNN

**Purpose:** Introduce the starting point concisely.

**Visual:** Pipeline: "SDP relaxation → projected gradient descent = message passing on graph →
GNN parameterization → train with SDP-inspired loss."

**Slide text:**
```
OptGNN (Yau et al., NeurIPS 2024):
  Key insight: solving a certain SDP via projected gradient descent
               equals message passing on the graph.
  → Design a GNN architecture that captures this algorithm.
  → Train with a continuous SDP-inspired unsupervised loss.
  → At inference: round continuous embeddings to discrete assignment.

Result: near-optimal approximation on Max-Cut, Max-3-SAT, Min-Vertex-Cover
        (provably UGC-optimal approximation guarantees).
Limitation: strong approximation, but often fails to satisfy all constraints exactly.
```

**Speaker note:** "OptGNN is an elegant construction. The architecture is derived from an
approximation algorithm, not just empirically tuned. But its loss function is a continuous
relaxation designed for approximation, not for enforcing discrete feasibility. That's the
tension we study."

---

#### Slide 39 — Three controlled modifications and a sharp transition

**Purpose:** Describe the experimental design and the main empirical result together.

**Visual:** Four-box progression: OptGNN → OptGNN-IR → OptGNN-Logit → OptGNN-Logit+Clause.
Below: bar chart showing exact solving rate for each variant vs. approximation ratio
(approximation stays high for all; solving jumps sharply only for the last variant).

**Slide text:**
```
Three modifications to OptGNN:

1. Recurrent layers (OptGNN-IR):
   Single recurrent unit, more iterations. Analogy: run longer.

2. Logit-space loss (OptGNN-Logit):
   Add rounding layer: embeddings → [0,1] → clause validity.
   Loss directly evaluates discrete clause satisfaction.

3. Clause-level aggregation (OptGNN-Logit+Clause):
   Explicit variable–constraint bipartite structure built in.

All four variants: approximation ratio ≈ 99%+
Solving (100% satisfied):   OptGNN ≈ 0%,  OptGNN-IR ≈ 0%,
                             OptGNN-Logit: moderate,
                             OptGNN-Logit+Clause: strong.

More iterations alone do not bridge the gap.
```

[VERIFY exact solving-rate numbers from the paper before slide generation]

**Speaker note:** "The striking observation is that running OptGNN longer — more iterations —
does not help. The model still fails to solve. The transition requires a qualitative architectural
change. And when the transition happens, it's sharp. Models go from almost never solving to
consistently solving. There is no gradual middle ground."

---

#### Slide 40 — Confidence returns: the concept that bridges approximation and solving

**Purpose:** Connect Chapter 4 back to the concept thread from Chapters 2 and 3.

**Visual:** Two panels side by side.
- Left: solving rate per model variant (bar chart, schematic).
- Right: linear probe accuracy for predicting support from embeddings, per variant.
Both curves are mirror images.

**Slide text:**
```
We probe each variant: can support be decoded from embeddings?

OptGNN:                support not decodable  →  does not solve
OptGNN-IR:             support not decodable  →  does not solve
OptGNN-Logit:          support partially decodable  →  sometimes solves
OptGNN-Logit+Clause:   support strongly decodable   →  consistently solves

The presence of the confidence signal predicts the solving capability.
Why? The logit loss exposes TFF-type clauses (barely-satisfied, one literal keeping
     them alive) — exactly the support clauses. The SDP loss mixes this signal
     with high-dimensional geometry and obscures it.
```

**Speaker note:** "The probe results mirror the solving results perfectly. Support is the concept
that bridges approximation and solving. When the architecture gives the model the right structure
to form that concept — clause-level aggregation makes support locally computable — it solves.
When it can only approximate, it lacks that structure. The concept predicts the capability."

---

#### Slide 41 — Evidence status: what we've proven vs. what we've observed

**Purpose:** A precise audit of the evidence for each claim, per problem. Required for this
audience.

**Visual:** A table with five rows and four columns.

**Slide text:**
```
Problem          Classical concept      GNN evidence                  Status
─────────────────────────────────────────────────────────────────────────────────
SAT (NeuroSAT)   Support (literal)      PCA + linear probe +          Formal + empirical
                                        theoretical analysis
Graph            Support (vertex/       Embedding geometry +          Empirical /
Coloring         color class)           linear probe                  partially formal
Max-Clique /     Degree-based           PCA + score correlation +     Empirical +
Sparse PCA       row-sum ranking        cross-domain transfer         algorithmic result
OptGNN           Support / confidence   Ablations + linear probes     Empirical
                                        across model variants
```

**Speaker note:** "I want to be precise about what is proven versus what is observed. The
strongest result is for SAT: we have a theoretical analysis, an empirical probe, and a PCA
structure argument. For coloring and clique, we have strong empirical evidence but the formal
theory is less complete. For the OptGNN chapter, the evidence is from ablations and probes —
no formal theory yet. These are the right distinctions to make, and they point to what remains
open."

---

#### Slide 42 — Chapter 4 + unified running question: final answer

**Purpose:** Close Chapter 4 and deliver the unified answer to the running question.

**Visual:** Running question with all four chapter answers now filled in.

**Slide text:**
```
Running question: What did the GNN actually learn?

Chapter 1: A transferable message-passing rule — but which one?
Chapter 2: In SAT/Coloring → support (classical confidence signal)
Chapter 3: In Clique/Sparse PCA → degree ranking (classical planted-graph signal)
Chapter 4: In SDP/OptGNN → whether support/confidence forms
           determines whether the model solves or only approximates

Unified answer:
  GNNs for combinatorial optimization tend to learn classical algorithmic concepts.
  Not new primitives. Not mysterious black-box reasoning.
  Concepts that classical theory and classical algorithms identified decades ago.

  This makes them: analyzable, compressible, and designable.
```

**Speaker note:** "Four chapters, four problems, one answer. GNNs don't invent new algorithmic
primitives. They discover classical ones — support, degree, confidence — through high-dimensional
message passing. That's not a negative result. It's a useful one. It tells us what to look for, how
to design better architectures, and how to trust or improve these models."

---

#### Slide 43 — What we can do with this

**Purpose:** Concrete payoffs from the concept-learning framework.

**Visual:** Three clean takeaway boxes.

**Slide text:**
```
Finding 1 — Interpretability:
  GNNs for combinatorial optimization encode classical algorithmic concepts.
  Support, degree, ranking — decodable by linear probes.

Finding 2 — Compression and algorithmic improvement:
  Once you know the concept, train toward it directly.
  91% compression (StudentNeuroSAT).
  Faster WalkSAT variant (SupportSAT-01).
  New combinatorial algorithm for Sparse PCA (Max-Clique GNN + LPR).

Finding 3 — Design principle for neural solvers:
  Approximation ≠ solving.
  Architectures should explicitly support confidence signal formation.
  Clause-level aggregation enables this in the SDP/OptGNN setting.
```

**Speaker note:** "Three things you can use. First: when you see a GNN for a combinatorial
task, look for classical algorithmic quantities in the embeddings — that's a productive first
hypothesis. Second: interpretability leads directly to compression and improvement. Third: for
designing future neural solvers, we now have a concept-level criterion. Does your architecture
support the formation of confidence? If not, it will approximate but not solve."

---

#### Slide 44 — Open questions

**Purpose:** Invite the audience into the research. Appropriate for a summer school.

**Slide text:**
```
1. Are there combinatorial problems where GNNs learn a genuinely new concept —
   one not previously identified in the classical algorithmic literature?

2. Can concept-level probing predict generalization failure before it occurs?
   (Early warning from the embeddings, not from test performance)

3. When is confidence locally computable?
   In SAT: support is local — each variable sees its clauses.
   Is this always true for problems where GNNs work?
   Is local computability a necessary condition for GNN success?

4. Can we design loss functions that provably induce confidence formation?
   (Rather than discovering it empirically after the fact)

5. Is there an approximation–solving gap analogue for other problem classes?
   (Coloring near the threshold, independent set, constraint propagation, ...)
```

**Speaker note:** "These are questions we're working on or would like to work on. If they
connect to your own interests — I'd be happy to talk after."

---

#### Slide 45 — Takeaway

**Purpose:** Final slide. One sentence the audience leaves with.

**Visual:** Clean, minimal. Single statement centered.

**Slide text:**
```
GNNs for combinatorial optimization do not learn mysterious new algorithms.

They learn to compute classical algorithmic concepts —
support, degree, confidence — from high-dimensional message passing.

This makes them analyzable, compressible, and designable.

The magic has a name.
```

**Speaker note:** "Thank you. The punchline: the surprising generalization of GNNs on hard
combinatorial problems is not mysterious. It is explainable, and the explanation points directly
to classical algorithmic theory. Questions?"

---

### Backup Slides *(after \appendix)*

**B1 — NeuroSAT architecture details**
Factor graph encoding, LSTM update equations (Eq. 1 from the concept learning paper), the FLIP
operator, readout via L_vote MLP. For an audience member who wants to understand the exact model.

**B2 — Support-core: formal construction**
r-support core definition, analogy to graph r-core, conditions under which the core coincides with
backbone variables. Informal proof sketch of the dynamics theorem. For theory-oriented questions.

**B3 — Planted clique hardness landscape: full details**
Regime boundaries for n = 500 and n = 1000. Known algorithmic results at each threshold:
Kucera (Easy), AKS / Feige–Grinberg (Medium), planted clique hardness conjecture (Hard).

**B4 — LPR algorithm: pseudocode and complexity**
O(n³) analysis. Runtime table from AAAI 2026 paper (avg ~25s, peak ~90s for n = 47k).
Comparison with naive O(n²) Top-k on the full benchmark.

**B5 — OptGNN-Logit: the rounding layer and why it exposes support**
Architecture diagram. Logit-space loss derivation. TFF clause ordering argument. Formal
statement of Insights 1 and 2 from "The Last Percent" paper.

**B6 — Sparse PCA: formal connection to Max-Clique**
Covariance matrix setup (Σ = I + βvv⊤), easy/medium/hard difficulty regimes for Sparse PCA,
Covariance Thresholding comparison, precise statement of the new algorithmic result.

---

## Missing Inputs Needed from Dan

### Critical — needed before generating Beamer

| Item | Why |
|------|-----|
| Confirm `OptGNN_elad_s` is your paper and attribution for public presentation | Submitted to NeurIPS 2026 as anonymous. Decide how to attribute before any public slides. |
| Exact solving-rate numbers from "The Last Percent" | Slides 39–40 use qualitative descriptions. Replace with the actual values. |
| Verify exact NeuroSAT test range from Selsam et al. (2019) | Slide 2 and Slide 17 use "[VERIFY from Selsam paper]" placeholders. The number n = 2000 appears in your concept learning paper as a test set size; check whether Selsam's original paper claims a specific generalization range. |
| Preferred Beamer template | `config.py` defaults to `Madrid`. Confirm or provide a `.sty` file. |

### Important — affects slide accuracy

| Item | Why |
|------|-----|
| Figures from the SAT concept learning paper (Figs. 2, 7) | TikZ or vector source needed for PCA plots in Beamer. PDFs cannot be directly reused cleanly. |
| Figure 1 from the graph coloring paper | Triangular PCA embedding diagram. TikZ or vector source. |
| Exact probe accuracy numbers for Chapter 4 | Slides 39–40 use schematics. Replace with actual bar chart values. |
| Sparse PCA claim wording | Slide 34 says "first combinatorial algorithm matching Covariance Thresholding." Verify this exact claim is in the AAAI 2026 paper as submitted. |

### Optional but improves the talk

| Item | Notes |
|------|-------|
| WalkSAT vs. SupportSAT-01 convergence plot | Fig. 3 in the SAT paper. Strong visual for Slide 25. |
| Weizmann PPTX | `GNNs/my papers/ReverseAlg50Weizmann.pptx` — check for reusable diagrams, especially GNN/BP comparison sequences. |
| ADYN abstract deadline | Event page lists title as TBA. Note any deadline for submitting the abstract to the organizers. |
| Audience calibration | Confirm whether any attendees have ML backgrounds — affects how much time to spend on Slides 4–18. |

---

## Beamer generation command (once plan is approved)

```bash
python agent.py \
  --title "Learned Algorithms or Classical Messages in Disguise?" \
  --papers "GNNs/my papers/" \
  --output adyn2026 \
  --compile
```

Or generate an outline draft first:

```bash
python agent.py --outline-only --title "Learned Algorithms or Classical Messages in Disguise?"
```

Key settings to confirm in `config.py` before running:
- `TALK_TITLE` — set to chosen title variant
- `AUDIENCE` — "PhD students and postdocs in algorithms, combinatorics, TCS"
- `TALK_DURATION_MINUTES` — 50
- `TARGET_SLIDE_COUNT` — 45
- `BEAMER_THEME` — confirm preference
