# ADYN Summer School 2026 — Talk Plan

**Event:** Summerschool on Algorithms, Dynamics, and Information Flow in Networks, TU Dortmund
**Speaker:** Dan Vilenchik, Ben-Gurion University of the Negev
**Duration:** 50 minutes (~42–45 content + 5–8 questions)
**Target deck:** ~40 main slides + 6 backup slides
**Audience:** PhD students and postdocs in algorithms, combinatorics, probability, graph theory, TCS

---

## One critical terminology note

The prompt uses the term **"LDR"** — that term does not appear in your papers. The correct term is
**LPR (Least-Probable Removal)** from the AAAI 2026 clique paper. All slides below use LPR.
Clarify if LDR was intended to refer to something else.

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
problems. In SAT and graph coloring, GNNs trained with only binary supervision develop internal
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
| `GNNs/my papers/OptGNN_elad_s (1).pdf` | Anonymous. "The Last Percent: Concept Emergence and the Jump from Approximation to Solving in Neural CSPs." NeurIPS 2026 (submitted). | Chapter 4 main paper [VERIFY attribution before presenting publicly] |
| `GNNs/background/2310.00526v7.pdf` | Yau, Karalias, Xu, Lu, Jegelka. "Are Graph Neural Networks Optimal Approximation Algorithms?" NeurIPS 2024. | Background for Chapter 4 |
| `GNNs/background/21-0449.pdf` | Cappart et al. "Combinatorial Optimization and Reasoning with Graph Neural Networks." *JMLR* 2023. | Background / Chapter 1 related work |

**Missing:** Original NeuroSAT paper (Selsam et al., ICLR 2019) — not in the folder. Training range
n ∈ [10, 40] is confirmed from Dan's concept learning paper (Table 1 cites this). Test range up to
n = 2000 verified from the same paper. [VERIFY exact Selsam claims independently before citing.]

---

## Forty-Slide Outline

---

### Opening + Chapter 1 — Crash Course: ML, GNNs, and the Promise
*(~14 slides)*

---

#### Slide 1 — Title slide

**Purpose:** Establish the talk. Give the audience a moment to settle.

**Visual:** Title, name, affiliation, event, date. Optionally a small contrast image: tiny formula
(n = 20) on the left, giant formula (n = 2000) on the right.

**Slide text:**
```
Learned Algorithms or Classical Messages in Disguise?
GNNs for Combinatorial Optimization

Dan Vilenchik
Ben-Gurion University of the Negev
ADYN Summer School 2026
```

**Speaker note:** Introduce yourself briefly. The title is a question — tell the audience the talk will
answer it. It took several papers to answer it, and the answer is interesting.

---

#### Slide 2 — A neural network learned to solve SAT. On instances 100× larger than it ever saw.

**Purpose:** The hook. Make the audience feel why this is surprising.

**Visual:** Two boxes side by side.
- Left: "Training — random 3-SAT, n ∈ [10, 40] variables. Solvable with a laptop. Label: SAT/UNSAT."
- Right: "Test — random 3-SAT, n up to 2000 variables. Much harder. Same GNN."
- Bridge arrow: "Generalization? What did it learn?"

**Slide text:**
```
NeuroSAT (Selsam et al., 2019):
  Train: n ∈ [10, 40] variables
  Test:  n up to 2000 variables
  Result: it still works — sometimes

Not just interpolation.
The training search space and test search space are incomparable in size.
```

**Speaker note:** "You're a theorist. You know that the search space grows exponentially. Instances
of size 40 and instances of size 2000 are in entirely different regimes. So how can training on the
small ones help on the large ones? That question is what drives our work."

---

#### Slide 3 — The setting: combinatorial optimization on graphs

**Purpose:** Define the problem class cleanly for a theory audience.

**Visual:** A simple factor graph. Variables as circles, clauses/constraints as squares, edges
connecting each variable to the clauses it appears in.

**Slide text:**
```
Input:    a graph or formula
Goal:     find an assignment satisfying all (or most) constraints
Hard:     NP-complete in the worst case

Examples:
  3-SAT:     assign TRUE/FALSE to variables
  Coloring:  assign colors to vertices, no adjacent pair same color
  Clique:    find a large complete subgraph
```

**Speaker note:** "These are canonical NP-hard problems. I'll use all three as test cases. The
message-passing structure that makes GNNs natural here is the same structure that makes belief
propagation natural — that connection is the key to understanding what happens."

---

#### Slide 4 — Machine learning in one slide

**Purpose:** Define the ML setup for a non-ML audience. Precise and fast.

**Visual:** Clean 4-row table or left-to-right pipeline.

**Slide text:**
```
Training data:    solved examples — (instance, label) pairs
Model:            a parameterized function f_θ
Loss:             how wrong is f_θ(instance) relative to label?
Training:         adjust θ to reduce loss across examples
Test:             evaluate f_θ on new, unseen instances
```

**Speaker note:** "I'll define everything as I use it. The key thing for today: the model is trained
on one collection of instances and tested on another. Whether it succeeds on unseen instances —
that's called generalization, and for this talk it's the central issue."

---

#### Slide 5 — Generalization: why training small and testing large is the puzzle

**Purpose:** Establish the conceptual heart of the talk.

**Visual:** Number line of instance sizes. Training range [10, 40] highlighted at one end. Test range
[500, 2000] highlighted far right. A "?" bridge spanning the gap.

**Slide text:**
```
If a model generalizes across sizes:
  → it learned something structural, not instance-specific
  → the "something" is our object of study

What rule could possibly transfer from n = 40 to n = 2000?
```

**Speaker note:** "When a model generalizes across instances from the same distribution but same
size, that's ordinary generalization. When it generalizes to a completely different size regime —
orders of magnitude larger — that's remarkable. It suggests the model latched onto some invariant
of the problem structure, not just the training set."

---

#### Slide 6 — Graph-structured problems need graph-structured models

**Purpose:** Motivate GNNs specifically.

**Visual:** Left: adjacency matrix of a graph under two different node labelings. Right: both
represent the same graph structurally. Label: "Any useful model must be permutation-invariant."

**Slide text:**
```
Challenge: same graph, different node labels → same combinatorial structure
Standard NN: fails (sees different inputs)
GNN: ignores labels, operates on structure ✓

Also:
  Graphs are variable-size
  Constraints are local
  → local message-passing is a natural inductive bias
```

**Speaker note:** "Combinatorial problems on graphs are permutation-invariant: relabeling nodes
doesn't change the answer. Standard neural networks can't handle this, but GNNs are built for it.
They also scale with the number of edges, not the total number of possible graphs."

---

#### Slide 7 — What is a GNN?

**Purpose:** Give a clean definition that a theorist can hold.

**Visual:** A small graph. Each node labeled with a vector h_v. An arrow from each neighbor to a
central node. The two-step update rule written out.

**Slide text:**
```
Each vertex v has a state (embedding) h_v ∈ ℝ^d

Each round t:
  1. Aggregate:   m_v = AGG({h_u : u ∈ N(v)})
  2. Update:      h_v ← UPDATE(h_v, m_v)

After T rounds: predict from {h_v}

Both AGG and UPDATE are learned neural networks.
```

**Speaker note:** "Think of it as a distributed algorithm. Each node has a memory vector. Each
round, it collects messages from its neighbors, aggregates them, and updates its own state.
After T rounds, you read off a prediction from the final states. The only difference from a designed
algorithm is that the aggregation and update functions are learned from data."

---

#### Slide 8 — Running toy example: initial state

**Purpose:** Anchor the abstract definition with a concrete small example.

**Visual:** A specific small graph: 6 vertices (3 forming a triangle), labeled A–F. Each vertex gets
an initial random embedding shown as a small colored bar.

**Slide text:**
```
Graph:       6 vertices, 7 edges
Embeddings:  randomly initialized ∈ ℝ^d
Round 0:     no information has been shared yet
```

**Speaker note:** "I'll carry this example through the next two slides. All nodes start with random
embeddings — the network hasn't done anything yet. All vertices look the same to the model."

---

#### Slide 9 — Running toy example: one round of message passing

**Purpose:** Show the mechanics of one step.

**Visual:** Same graph. Arrows from neighbors of vertex A flowing in. Aggregate operation shown.
New embedding for A. Other vertices also updated in parallel.

**Slide text:**
```
Round 1:
  A receives messages from B, C, D
  AGG(h_B, h_C, h_D) → m_A
  h_A ← UPDATE(h_A, m_A)
  ↳ A now "knows about" its 1-hop neighborhood

After T rounds: each vertex knows about its T-hop neighborhood
```

**Speaker note:** "After one round, each node has seen its immediate neighbors. After two rounds,
its 2-hop neighborhood. After T rounds, a summary of a T-hop ball. For sparse graphs this grows
slowly. For dense graphs a few rounds cover a lot of the graph."

---

#### Slide 10 — Running toy example: readout

**Purpose:** Complete the pipeline.

**Visual:** Final embeddings for all vertices after T rounds. MLP output per vertex giving a score
s_v ∈ [0, 1]. Thresholding to a prediction (clique member / not).

**Slide text:**
```
After T rounds:
  For each vertex v: MLP(h_v) → score s_v ∈ [0, 1]
  
  s_v ≈ 1 → v likely in clique / colored correctly / TRUE
  s_v ≈ 0 → v likely not in solution
  
The GNN is a function:  (graph, weights) → per-vertex scores
To get a discrete solution: apply a decoding strategy.
```

**Speaker note:** "The scores are the output. To get an actual solution you round or apply a
decoding heuristic. The connection between those scores and classical algorithmic concepts is
exactly what we study."

---

#### Slide 11 — Belief propagation: the classical precursor

**Purpose:** Set up the BP–GNN analogy for a theory audience.

**Visual:** A small factor graph (variables = circles, clauses = squares). BP messages labeled along
edges with their interpretation: "P(x=TRUE | neighbors)".

**Slide text:**
```
Belief propagation (BP):
  Messages along edges of a factor graph
  Message = structured probabilistic summary
    (marginal belief, warning, bias, ...)
  Update rule: analytically derived from the probabilistic model
  
Works exactly on trees; approximate on graphs with cycles
Used in: LDPC decoding, survey propagation, Ising models
```

**Speaker note:** "BP is the gold standard of principled message passing. The messages have an
interpretation — they represent beliefs about variable assignments. The update rule is derived from
first principles. The question is: when you let a neural network learn its own version of BP, what
does it discover?"

---

#### Slide 12 — From belief propagation to a GNN: three steps

**Purpose:** The central analogy. Build it carefully.

**Visual:** Three-column progression.
- Column 1 (BP): scalar/probability message, hand-designed update, probabilistic objective.
- Column 2 (Relaxation): vector in ℝ^d replaces the scalar. Update still hand-designed.
- Column 3 (GNN): learned vector message, learned update (MLP/GRU), task-driven loss.

**Slide text:**
```
Step 1 — Classical BP
  message(u→v) = f_BP(assignment, neighbors)
  interpretable: marginal, warning, bias

Step 2 — Generalize the message
  message(u→v) ∈ ℝ^d    (high-dimensional, latent)

Step 3 — Learn the update rule
  UPDATE(h_v, m_v) = GRU/MLP(h_v, m_v ; θ)
  θ learned from data, guided by task loss
```

**Speaker note:** "The GNN is not BP. But for this audience, the BP analogy is the right mental
model. Both pass messages along a factor/constraint graph. BP passes structured probabilistic
summaries; the GNN passes high-dimensional learned vectors. BP derives its update rule
analytically; the GNN learns it from data. What did the GNN learn? That's a question about what
it rediscovered from BP."

---

#### Slide 13 — The loss function is where the task enters

**Purpose:** Complete the BP→GNN transformation.

**Visual:** Comparison table: BP vs. GNN on four dimensions.

**Slide text:**
```
                   BP              GNN
Message:           hand-designed   learned ∈ ℝ^d
Update:            analytic        trained (MLP/GRU)
Objective:         probabilistic   task loss (e.g., SAT/UNSAT)
Convergence:       proven (trees)  empirical
Interpretability:  high            our question
```

**Speaker note:** "The GNN has more freedom: it chooses any representation it finds useful for the
task. The interesting scientific question is whether, given this freedom, it converges to something
interpretable. Spoiler: it often does — but the thing it converges to is familiar."

---

#### Slide 14 — NeuroSAT: the original promise

**Purpose:** Establish the empirical result that motivated the research program.

**Visual:** Two-column contrast. Left: small SAT formula graph (5 variables, 3 clauses).
Right: large factor graph (schematic, many nodes). Underneath: training vs. test regime.

**Slide text:**
```
NeuroSAT (Selsam et al., 2019):
  Architecture:   message-passing GNN on CNF factor graph
  Training:       SAT/UNSAT label only (single-bit supervision)
  Training set:   n ∈ [10, 40] variables, near phase transition
  Test:           n up to 2000 variables
  
Surprise: it generalizes.
Question: what invariant did it latch onto?
```

**Speaker note:** "NeuroSAT was trained with only a single bit of supervision per instance — SAT
or UNSAT. The instances in training were small enough to solve exactly. Yet the same network,
unchanged, generalizes to much larger instances. That's either magic, or the network found a
structural principle that scales. We test the second hypothesis."

---

#### Slide 15 — Our research program: opening the black box

**Purpose:** State the research question and the conceptual tool.

**Visual:** Pipeline diagram: "Trained GNN → internal embeddings → concept probe → interpretable
quantity."

**Slide text:**
```
We ask:   what is encoded in the GNN's learned embeddings?

Method:   concept learning
  — project embeddings to low-dimensional PCA space
  — ask: does the projection align with known algorithmic quantities?
  — verify: a simple linear probe predicts the concept on held-out instances

A concept g(v) is operationally defined:
  ĝ(v) = w⊤ h_v + b    (linear probe)
  — decodable from embeddings across instances
  — falsifiable: fails if support isn't predictable above baseline
```

**Speaker note:** "We define concept rigorously: a concept is a quantity that a simple linear probe
can predict from the embeddings on held-out instances. This rules out the possibility that we're
pattern-matching into noise."

---

### Chapter 2 — SAT and Coloring: Support as Confidence
*(~11 slides)*

---

#### Slide 16 — Concept learning in AI: why it matters

**Purpose:** Give the broader XAI context. Don't linger.

**Visual:** Three boxes: vision ("beak" in a bird classifier), medicine ("lesion boundary"),
algorithms ("variable confidence").

**Slide text:**
```
XAI usually:  which input features drove this decision?
              (SHAP, LIME, GradCAM)

For algorithms: wrong question.
  "x₁ appears in clause 7" is not a concept — not transferable.
  "x₁ has high confidence" is a concept — generalizes across instances.

We want:  compact, interpretable quantities that
          explain the model's internal dynamics across inputs and iterations.
```

**Speaker note:** "Standard XAI finds important features. For combinatorial tasks, that's not
enough. We need concepts that have algorithmic meaning and that explain behavior across
instances, not just for one input. That requires looking at the internal representations as the
model runs, not just at the output."

---

#### Slide 17 — SAT as a factor graph: running example

**Purpose:** Introduce the SAT instance visually. Use a concrete small formula.

**Visual:** TikZ factor graph. Formula: (x₁ ∨ x̄₂ ∨ x₃) ∧ (x₁ ∨ x₂ ∨ x̄₃).
Variable nodes = circles, clause nodes = squares, edges connecting each variable to its clauses.

**Slide text:**
```
CNF formula: (x₁ ∨ x̄₂ ∨ x₃) ∧ (x₁ ∨ x₂ ∨ x̄₃)

Factor graph:
  Variable nodes: x₁, x₂, x₃ (and negations x̄₁, x̄₂, x̄₃)
  Clause nodes:   C₁, C₂
  Edges:          literal ↔ clause where literal appears

NeuroSAT runs message passing on this graph.
We ask: what do the node embeddings encode?
```

**Speaker note:** "NeuroSAT operates on the factor graph, not the formula directly. Literals and
clauses are both node types. Messages flow between them, just like in survey propagation. Now
I'll tell you what we found in those messages."

---

#### Slide 18 — What is "support"?

**Purpose:** Introduce the key concept clearly before showing the data.

**Visual:** Toy formula. Clause of type TFF (one TRUE literal, two FALSE) highlighted. The TRUE
literal labeled "the sole supporter of this clause."

**Slide text:**
```
Assignment ϕ. Variable x. Clause C.

x supports C under ϕ  ⟺
    C is satisfied, and x is the ONLY literal satisfying it.
    (the other two literals are FALSE — clause type TFF)

support_ϕ(x) = |{clauses C : x alone satisfies C}|

High support:  x is load-bearing → flipping x breaks many clauses
Low support:   x is easily replaceable → safe to flip
```

**Speaker note:** "Support is a classical notion. It appears in WalkSAT, survey propagation, and
backbone analysis — all different algorithmic traditions that independently discovered the same
signal. A variable with high support is one you cannot safely change. It's a confidence signal.
Now I'll show you that NeuroSAT, trained only on SAT/UNSAT labels with no knowledge of
support, encodes it anyway."

---

#### Slide 19 — Support as confidence: a toy example

**Purpose:** Make the intuition concrete before showing the PCA plots.

**Visual:** Two small formulas side by side.
- Formula A: x₁ is the sole TRUE literal in 3 of 4 clauses it appears in → support = 3 → HIGH.
- Formula B: x₁ appears in balanced clauses, rarely the sole satisfier → support = 0 → LOW.

**Slide text:**
```
High support:
  x₁ = TRUE. Of 4 clauses containing x₁:
  3 are satisfied only because of x₁ (type TFF).
  Flipping x₁ breaks those 3 clauses immediately.
  → Confidence is HIGH. Do not flip x₁.

Low support:
  x₁ = TRUE. All clauses containing x₁ have other TRUE literals.
  Flipping x₁ costs nothing immediately.
  → Confidence is LOW. Safe to flip.
```

**Speaker note:** "If you were designing a local-search SAT solver, support is exactly the kind of
thing you'd track. The surprise is that NeuroSAT — which saw only binary SAT/UNSAT labels and
never heard of support — encodes precisely this quantity in its embeddings."

---

#### Slide 20 — NeuroSAT embeddings: PCA reveals structure

**Purpose:** Show the empirical evidence for concept emergence.

**Visual:** Schematic of PCA plot (Fig. 2 in the SAT concept learning paper). Literal embeddings
projected to 2D. Literal and negation on opposite sides of PC1 = 0. Support clauses (TFF)
with higher |PC1| values.

**Slide text:**
```
PCA of NeuroSAT's internal literal embeddings
(n = 1500 variables, run to convergence):

PC1 explains ~90% of variance
PC2 explains ~8% of variance
(~98% captured by 2 components out of 128)

PC1 value of a literal:
  far positive  = TRUE with high support
  near 0        = uncertain, low support
  far negative  = negation of above
```

**Speaker note:** "The model is 128-dimensional. Yet 98% of what matters lives in 2 dimensions,
and those 2 dimensions directly encode support and assignment consistency. We verify this with
linear probes on held-out instances — it's not just a visual impression."

---

#### Slide 21 — Main finding: support governs NeuroSAT's dynamics

**Purpose:** State the result precisely.

**Visual:** Schematic: "Support (PC1 of embedding) → governs which variables are flipped each
iteration → support-core emerges."

**Slide text:**
```
Theorem (informal):
  Under assumptions on instance distribution and weights,
  NeuroSAT's dynamics fix variables in decreasing order of support,
  starting with the r-support core — a combinatorial structure
  analogous to the graph-theoretic r-core.

Empirically:
  Linear probe predicts support from embeddings on held-out instances.
  Variables with PC1 near 0 get reassigned in the next iteration.
  Variables with PC1 far from 0 are locked in, consistent with a satisfying assignment.
```

**Speaker note:** "The result has two parts: an empirical finding (support is decodable from
embeddings) and a theoretical analysis (under certain assumptions, the dynamics formally reduce
to tracking the support-core). The theory is for a simplified architecture version, but it gives a
mechanistic account of what the full model is doing."

---

#### Slide 22 — From insight to compression: StudentNeuroSAT

**Purpose:** Show the practical payoff of the concept-learning approach.

**Visual:** Teacher–student diagram. NeuroSAT (large, 128-dim LSTM) passes concept-level
knowledge (support encoding) to StudentNeuroSAT (smaller). Convergence curves for WalkSAT
vs. SupportSAT-01 underneath (from Fig. 3 of the paper).

**Slide text:**
```
If support explains the behavior:
  → train a student GNN to mimic the embedding, not the label
  → instead of SAT/UNSAT supervision, train on teacher's latent representations

StudentNeuroSAT:   91% fewer parameters than NeuroSAT
Performance:       comparable to the teacher

SupportSAT-01 (new WalkSAT variant):
  Built from concept insights.
  Converges faster than WalkSAT on n = 1500 instances.
```

**Speaker note:** "Two payoffs from interpretability. First: compression — once you know the
concept, you can train directly toward it, and a much smaller model captures the behavior.
Second: algorithmic improvement — the concept gives a design principle for improving classical
solvers. SupportSAT is a WalkSAT variant that picks which variable to flip using support, and
it's strictly faster on large instances."

---

#### Slide 23 — Graph coloring: same concept, different geometry

**Purpose:** Show that the finding is not SAT-specific.

**Visual:** Left: small valid 3-colored graph (6 vertices). Right: 2D PCA of GNN-GCP embeddings
showing the triangular structure.

**Slide text:**
```
GNN-GCP (Lemos et al., 2019):
  Trained to predict 3-colorability (binary label only)
  Message-passing LSTM, 64-dim embeddings

What the 2D PCA projection shows:
  Embeddings form a triangle.
  Color classes cluster near different triangle vertices.
  High-support vertices are closest to triangle corners.
  Low-support vertices sit near the center.
```

**Speaker note:** "In graph coloring, 'support of vertex v' means the number of neighbors v has
in each color class other than its own. A high-support vertex has many neighbors of conflicting
colors — it's strongly constrained, and the network has committed to its color. The triangular
geometry is how the GNN encodes the three-way color assignment in 2D. Color classes are the
three corners of the triangle."

---

#### Slide 24 — Coloring: support is confidence

**Purpose:** State the coloring finding and connect explicitly to SAT.

**Visual:** Side-by-side: SAT (literals on PC1 axis, support = load-bearing) and Coloring (vertices
near triangle corners, support = color-committed). Same concept, different representation.

**Slide text:**
```
Support in SAT:      clauses uniquely satisfied by x
Support in coloring: neighbors v has in each other color class

In both cases:
  High support → high confidence → embedding far from ambiguous region
  Low support  → low confidence → near center, assignment may still change

The concept was used in hand-designed algorithms:
  WalkSAT (SAT)
  Alon–Kahale coloring algorithm (1994)

GNNs rediscover them from data.
```

**Speaker note:** "The connection to Alon and Kahale (1994) is particularly satisfying. They
designed a coloring algorithm in 1994 based on exactly this support concept. The GNN, trained
thirty years later with no knowledge of that algorithm, encodes the same quantity in its embeddings.
That's the central message: GNNs don't invent new algorithmic primitives. They rediscover
classical ones."

---

#### Slide 25 — Chapter 2 takeaway

**Purpose:** Pause and crystallize before Chapter 3.

**Visual:** Two-column summary table: SAT row and Coloring row.

**Slide text:**
```
SAT:
  Model:     NeuroSAT
  Concept:   support (clauses uniquely satisfied by x)
  Geometry:  PC1 encodes confidence; symmetric around 0
  Payoff:    91% compression, faster WalkSAT variant

Coloring:
  Model:     GNN-GCP
  Concept:   support (neighbors in other color classes)
  Geometry:  triangular embedding; corners = color classes

Theme: GNNs trained with binary supervision
       learn classical solver-relevant quantities.
       The magic has a name.
```

**Speaker note:** "Two different GNNs, two different problems, different architectures, different
loss functions. Same outcome: the key emergent concept is support, a quantity that classical
algorithmic theory identified decades ago. This is not a coincidence, and the next chapter will
show the same pattern on a structurally different problem."

---

### Chapter 3 — Clique: Degree, Ranking, and Cross-Domain Generalization
*(~8 slides)*

---

#### Slide 26 — Max-Clique: a different kind of test

**Purpose:** Motivate why clique is a useful third test case.

**Visual:** A graph with a highlighted 4-clique. Vertex degrees labeled.

**Slide text:**
```
Max-Clique: find the largest complete subgraph.

Structurally different from SAT/Coloring:
  No factor graph. No clause structure.
  The signal is in vertex degrees, not constraint satisfaction.
  Classical message-passing literature is thinner here.

Same meta-question: what concept does the GNN learn?
```

**Speaker note:** "SAT and coloring both have a natural factor-graph structure. Clique is
different — purely graph-theoretic. If the concept-learning story is robust, it should survive this
change. And it does — though the concept is different: instead of support in the constraint sense,
we find degree-based ranking."

---

#### Slide 27 — Planted clique: three regimes

**Purpose:** Introduce the benchmark and the theoretical difficulty landscape.

**Visual:** Three labeled regions on a number line of planted clique size k.
- Hard: k = O(√n) — planted clique conjecture; conjectured intractable.
- Medium: k = Ω(√n) — spectral methods and LPR work.
- Easy: k = Ω(√n log n) — simple degree ranking suffices.

**Slide text:**
```
Random graph G(n, 1/2):
  Largest clique ≈ 2 log₂ n   (believed hard to find)

Planted clique: insert a k-clique into G(n, 1/2)

Regimes (calibrated empirically for n = 1000):
  Easy:   k ≥ ~62  — Top-k by degree recovers the clique
  Medium: k ∈ [36, 61] — LPR needed
  Hard:   k ≤ 35  — planted clique conjecture; no known efficient algorithm
```

**Speaker note:** "We evaluate GNNs on instances calibrated to this landscape. This lets us ask:
does the GNN work in the easy, medium, or hard regime? Without this calibration, you can't tell
whether a GNN 'solving' clique is impressive or trivial."

---

#### Slide 28 — Degree as a classical signal: helpful but noisy

**Purpose:** Establish the baseline before introducing the GNN.

**Visual:** Small planted clique graph (n = 10, k = 4). Degree table:
clique vertices {6, 7, 7, 8}; non-clique vertices {2, 3, 4, 7}. One non-clique vertex at degree 7 —
the "impostor" — highlighted.

**Slide text:**
```
Degree heuristic:
  Clique vertices receive a degree "boost" from within the clique.
  Sort vertices by degree, take top k.

Works in the Easy regime.

Fails when k is smaller:
  "Impostors" — non-clique vertices with high degree — creep in.
  Top-k selects them. The candidate is not a valid clique.
```

**Speaker note:** "The degree heuristic is the simplest possible approach and it works in easy
cases. In medium and hard cases, it gets fooled by impostors. The question is whether the GNN
does anything more clever — or whether it just learns a sophisticated version of degree."

---

#### Slide 29 — What the GNN learns: degree-based ranking

**Purpose:** State the core finding for clique.

**Visual:** PCA of GNN vertex embeddings. PC1 highly correlated with vertex degree. GNN output
score vs. degree scatter plot showing near-linear relationship.

**Slide text:**
```
GNN embedding analysis (PCA):
  PC1 of vertex embeddings predicts vertex degree with high correlation.
  Output scores ≈ monotone function of degree.

Finding:
  The GNN learns degree-based ranking.
  It does not appear to learn a fundamentally different signal.

But: the decoder matters.
  Top-k with degree fails on medium instances.
  Can a smarter decoder close the gap?
```

**Speaker note:** "The GNN is essentially doing sophisticated degree estimation — it gets a better
estimate than raw degree because it uses multi-hop information, but the principle is the same. The
concept is not support in the SAT sense: it's ranking, specifically degree-like ranking. The
interesting result comes next: even with this relatively simple concept, a better decoder
significantly improves performance."

---

#### Slide 30 — Top-k vs. LPR: two decoders, very different performance

**Purpose:** Introduce LPR and show the performance gap.

**Visual:** Side-by-side. Left: Top-k selects k highest-scoring vertices. Right: LPR iteratively
removes the lowest-scoring vertex until the remainder is a clique.

**Slide text:**
```
Top-k:
  Select k vertices with highest GNN scores.
  Fast: O(n²).
  Fails on Medium instances: impostors included.

LPR — Least-Probable Removal:
  Start with all vertices.
  Remove lowest-scoring vertex (least likely in clique).
  Repeat until the remaining set forms a clique.
  O(n³), practical (avg ~25s; peak ~90s for n = 47k).

LPR significantly outperforms Top-k in Medium and Hard regimes.
```

**Speaker note:** "The insight is different from Top-k's perspective. Rather than building up a
clique by adding likely candidates, LPR prunes away unlikely ones. When impostors are present,
LPR removes them because they have lower scores than genuine clique vertices. Top-k would
have included them immediately. The underlying concept is the same — degree-like ranking — but
the decoding strategy changes the outcome substantially."

---

#### Slide 31 — Cross-domain: the same GNN solves Sparse PCA

**Purpose:** One of the strongest results. Show the universality of the learned principle.

**Visual:** Two-panel diagram. Left: graph with planted clique, vertices color-coded by degree
boost. Right: covariance matrix with planted spike, rows color-coded by row-sum. Connection
arrow labeled "row-sum ranking."

**Slide text:**
```
Sparse PCA (single-spike model):
  Covariance Σ = I + β·vv⊤, where v is sparse (size k).
  Goal: recover the support of v.

Connection to clique:
  Clique:      degree boost for clique vertices
  Sparse PCA:  larger row-sums for spike variables

Experiment:
  GNN trained on Max-Clique → applied to Sparse PCA → succeeds.
  GNN trained on Sparse PCA → applied to Max-Clique → succeeds.

Learned principle: row-sum ranking — universal across both domains.
```

**Speaker note:** "We trained a GNN to find cliques. We then gave it a covariance matrix from a
completely different problem: recovering a sparse principal component. It succeeds — because both
problems share the same mathematical structure. In learning degree ranking for cliques, the GNN
learned row-sum ranking in general. And we show a new algorithmic result: the Max-Clique GNN
with LPR is the first combinatorial algorithm that matches Covariance Thresholding, the spectral
state-of-the-art for Sparse PCA, without any hyperparameters."

---

#### Slide 32 — Chapter 3 takeaway

**Purpose:** Summarize Chapter 3 and bridge to Chapter 4.

**Slide text:**
```
Clique and Sparse PCA:
  Concept:   degree-based (row-sum) ranking
  Decoder:   LPR outperforms Top-k
  Transfer:  same GNN solves both problems

Theme persists:
  GNN success explained by a classical, interpretable concept.
  The concept here is structural (degree/ranking), not constraint-based.

Chapter 4: what happens when the task is approximation vs. exact solving?
  Can we force the GNN to cross the threshold from approximating to solving?
  What determines whether it can?
```

**Speaker note:** "So far we've analyzed trained black boxes and found interpretable concepts
inside. In the final chapter, we show that the presence or absence of a concept — specifically
confidence/support — determines whether a GNN approximates or solves. This is a design
principle, not just a retrospective observation."

---

### Chapter 4 — The Last Percent: Approximation, Solving, and the Concept Gap
*(~8 slides)*

---

#### Slide 33 — The approximation–solving gap

**Purpose:** Introduce the central distinction of Chapter 4.

**Visual:** A number line from 0% to 100% constraint satisfaction.
- "Random baseline" marked at 7/8 = 87.5%.
- "OptGNN" marked at ~99%.
- "Solving" at 100%.
- The gap 99% → 100% labeled "the last percent."

**Slide text:**
```
Random 3-SAT:
  A random assignment satisfies each clause with probability 7/8.
  Strong approximation (87.5%) is trivially achievable.

OptGNN (Yau et al., NeurIPS 2024): reaches ~99%.

Exact solving (100%):
  Håstad: improving beyond 7/8 is NP-hard in the worst case.
  For random instances above threshold: the last 1% requires
  coordinated changes across many variables.

From ~99% to 100% is not a small step — it's a qualitative transition.
```

**Speaker note:** "I want to separate two very different capabilities. An assignment satisfying 99%
of clauses may still be far from any satisfying assignment — the last constraint violations often
propagate into many required changes. This is the gap we study, and understanding it requires
looking at what concept the model has (or hasn't) learned."

---

#### Slide 34 — OptGNN: SDP relaxations built into a GNN

**Purpose:** Introduce the starting point for Chapter 4 concisely.

**Visual:** Pipeline: "SDP relaxation → projected gradient descent = message passing on graph →
GNN parameterization → train with SDP-inspired loss."

**Slide text:**
```
OptGNN (Yau et al., NeurIPS 2024):
  Key insight: solving a certain SDP via projected gradient descent
               is equivalent to message passing on the graph.
               
  → Design a GNN whose architecture captures this algorithm.
  → Train with a continuous SDP-inspired unsupervised loss.
  → At inference: round continuous embeddings to discrete assignment.

Result: near-optimal approximation on Max-Cut, Max-3-SAT, Min-Vertex-Cover.
Limitation: strong approximation, but often fails to satisfy all constraints.
```

**Speaker note:** "OptGNN is an elegant construction — the architecture is derived from an
approximation algorithm, not just empirically tuned. It has provable guarantees under the Unique
Games Conjecture. But its loss function is a continuous relaxation, not designed to enforce discrete
feasibility. That's the tension we study."

---

#### Slide 35 — Three controlled modifications

**Purpose:** Describe the experimental design concisely.

**Visual:** Four-box progression: OptGNN → OptGNN-IR → OptGNN-Logit → OptGNN-Logit+Clause.
Each box labeled with its modification.

**Slide text:**
```
Starting point: OptGNN (SDP-based, continuous loss)

Modification 1 — Recurrent layers (OptGNN-IR):
  Replace stacked layers with one recurrent unit run for more steps.
  Analogy: running a local-search heuristic longer.

Modification 2 — Logit-space loss (OptGNN-Logit):
  Add rounding layer: embeddings → [0,1] → clause validity.
  Loss directly evaluates discrete clause satisfaction.

Modification 3 — Clause-level aggregation (OptGNN-Logit+Clause):
  Explicit variable–constraint bipartite structure in the architecture.
  Factor-graph view built in.
```

**Speaker note:** "Each modification is inspired by classical heuristic design, not arbitrary
architecture search. We want to understand which ingredient is responsible for the transition to
solving. The answer connects back to everything in Chapters 2 and 3."

---

#### Slide 36 — The transition is sharp, not gradual

**Purpose:** The main empirical finding of Chapter 4.

**Visual:** Bar chart (schematic). X-axis: the four variants. Y-axis: fraction of instances exactly
solved. OptGNN and OptGNN-IR near zero; OptGNN-Logit moderate; OptGNN-Logit+Clause
high. Approximation ratio (~99%) stays high for all variants — shown as a flat top line.

**Slide text:**
```
All four variants: approximation ratio ≈ 99%+
(strong approximation is easy; all models achieve it)

Exact solving (100% satisfied):
  OptGNN:                 ≈ 0%
  OptGNN-IR:              ≈ 0%
  OptGNN-Logit:           moderate
  OptGNN-Logit+Clause:    strong

More iterations alone do not bridge the gap.
The transition requires a qualitative architectural change.
```

[VERIFY exact numbers from paper before slide generation]

**Speaker note:** "The striking observation is that you can run OptGNN longer — it still fails to
solve. The transition requires a qualitative architectural change, not just more compute. When the
transition happens, it's sharp. Models go from almost never solving to consistently solving.
There is no gradual middle ground."

---

#### Slide 37 — Why the transition happens: confidence returns

**Purpose:** Connect Chapter 4 back to the concept thread from Chapters 2 and 3.

**Visual:** Two panels side by side. Left: solving rate per model variant. Right: linear probe
accuracy for predicting support from embeddings, per variant. The two curves mirror each other.

**Slide text:**
```
We probe each model variant: can support be decoded from embeddings?

OptGNN:                support not decodable  →  does not solve
OptGNN-IR:             support not decodable  →  does not solve
OptGNN-Logit:          support partially decodable  →  sometimes solves
OptGNN-Logit+Clause:   support strongly decodable   →  consistently solves

The presence of the confidence concept predicts the solving capability.
```

**Speaker note:** "The probe results mirror the solving results perfectly. The presence of the
confidence signal — specifically the support concept — is what distinguishes approximators from
solvers. This is not just correlation: the logit-space loss exposes a TFF-type clause pattern that
directly identifies support variables, and clause-level aggregation gives the model the structure
to compute support globally."

---

#### Slide 38 — Why the logit loss exposes confidence

**Purpose:** Give the theoretical intuition for why the logit modification matters.

**Visual:** Table of SAT clause types and their behavior under near-discrete assignments.

**Slide text:**
```
Clause types under near-discrete assignment:
  TTT: fully satisfied      → minimal loss, no signal
  TTF: safely satisfied     → low loss
  TFF: barely satisfied     → loss near violation threshold
  FFF: unsatisfied          → large loss (correction signal)

TFF clauses give a confidence signal:
  "This variable is the only one keeping this clause satisfied."
  → That's support, exactly.

SDP loss: mixes this signal with high-dimensional inner products → noisy.
Logit loss: learns a single rounding direction → isolates the signal.
```

**Speaker note:** "The logit loss, by forcing embeddings through a rounding step before evaluating
clause satisfaction, separates TFF-type clauses from others. TFF clauses are the support clauses.
The model can now identify them clearly, rather than having their signal washed out by the
high-dimensional geometry of the SDP objective. This is why the modification matters."

---

#### Slide 39 — The unified picture

**Purpose:** Synthesize all four chapters into one coherent message.

**Visual:** Table with four rows (one per problem/chapter) and three columns: Problem / Concept
found / Classical origin.

**Slide text:**
```
Problem               Concept found             Classical origin
─────────────────────────────────────────────────────────────────────
SAT (NeuroSAT)        Support (variable)        WalkSAT, Survey Prop.
Graph Coloring        Support (vertex/color)    Alon–Kahale (1994)
Max-Clique / PCA      Degree-based ranking      Planted clique theory
SDP / OptGNN          Support (again)           Classical solver design

In all cases:
  GNN success is explainable by a classical algorithmic concept.
  The concept appears in embeddings without explicit supervision.
  Its presence predicts both interpretability and capability.
```

**Speaker note:** "Four problems, four papers, same conclusion. GNNs trained on combinatorial
tasks do not invent new algorithmic primitives. They discover classical ones. This tells us what
to look for, how to design better architectures, when to expect GNNs to work, and why. It gives
a vocabulary for reasoning about learned combinatorial algorithms."

---

#### Slide 40 — What GNNs learn — and what we can do with it

**Purpose:** Payoff slide. Connect the conceptual findings to concrete outcomes.

**Visual:** Three clean takeaway boxes.

**Slide text:**
```
Finding 1 — Interpretability:
  GNNs for combinatorial optimization encode classical algorithmic concepts.
  (support, degree, ranking — decodable by linear probes)

Finding 2 — Compression and design:
  Once you know the concept, you can train toward it directly.
  91% compression in SAT. Faster WalkSAT variant.

Finding 3 — A design principle for neural solvers:
  Approximation ≠ solving.
  Architectures should explicitly support the emergence of confidence signals.
  Clause-level aggregation enables this in the SDP/OptGNN setting.
```

**Speaker note:** "Three things you can use. First: if you're trying to understand a GNN for a
combinatorial task, look for classical algorithmic quantities in the embeddings — that's a productive
first hypothesis. Second: you can compress, improve, and analyze GNNs once you identify the
concept. Third: for designing future neural solvers, we now have a concept-level criterion — does
your architecture support the formation of confidence? If not, it will approximate but not solve."

---

#### Slide 41 — Open questions

**Purpose:** Invite the audience into the research. Especially good for a summer school.

**Slide text:**
```
1. Are there problems where GNNs learn a genuinely new concept —
   one not previously identified in classical algorithmic literature?

2. Can concept-level probing predict generalization failure before it occurs?

3. What is the right theory of when confidence is locally computable?
   (In SAT: support is local. Is this always true for problems where GNNs work?)

4. Can we design loss functions that provably induce confidence formation?

5. Is there an approximation–solving gap analogue for other problem classes?
   (coloring near the threshold, independent set, max-independent-set, ...)
```

**Speaker note:** "These are open questions we're actively working on. If any of them resonate
with your own work — I'd be happy to talk after."

---

#### Slide 42 — Takeaway

**Purpose:** Final slide. One sentence the audience leaves with.

**Visual:** Clean, minimal. Single centered statement.

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
NeuroSAT factor graph encoding, LSTM update equations (Eq. 1 from Dan's concept learning
paper), FLIP operator, readout via Lvote MLP.

**B2 — Support-core: formal construction**
r-support core definition, analogy to graph r-core, conditions under which core coincides with
backbone variables, proof sketch of dynamics theorem.

**B3 — Planted clique hardness landscape**
Detailed parameter table for n = 500 and n = 1000. Easy/Medium/Hard boundaries. Known
algorithmic results at each threshold (Kucera, AKS, Feige–Ron).

**B4 — LPR algorithm: pseudocode and complexity**
O(n³) analysis, runtime table from AAAI 2026 paper (avg 25s, peak 90s for n = 47k).

**B5 — OptGNN-Logit: the rounding layer**
Architecture diagram, logit-space loss derivation, TFF-type clause ordering, formal Insight 1
and Insight 2 from the NeurIPS 2026 submission.

**B6 — Sparse PCA: formal connection to Max-Clique**
Covariance matrix setup (Σ = I + βvv⊤), difficulty regimes for Sparse PCA, Covariance
Thresholding comparison, statement of the new algorithmic result.

---

## Missing Inputs Needed from Dan

### Critical — needed before generating Beamer

| Item | Reason |
|------|--------|
| Confirm `OptGNN_elad_s` is your paper and can be presented publicly | Submitted to NeurIPS 2026 as anonymous. Need to decide how to attribute in a public talk before slides go to ADYN. |
| Exact solving-rate numbers from "The Last Percent" | Slides 36–37 use qualitative descriptions. Replace with actual values before presenting. |
| Confirm LPR runtime numbers | Slide 30 cites "avg. ~25s, peak ~90s for n = 47k" from AAAI 2026 paper. Verify this is the number you want on the slide. |
| Original NeuroSAT paper (Selsam et al., ICLR 2019) | Not in `GNNs/background/`. Training range n ∈ [10, 40] is confirmed from your concept learning paper (Table 1), but verify the generalization range stated in Selsam's paper directly before citing it. |
| Preferred Beamer template | `config.py` defaults to `Madrid`. Confirm or provide a `.sty` file. |

### Important — affects slide accuracy

| Item | Reason |
|------|--------|
| Figures from the SAT concept learning paper you want reused | Figs. 2 and 7 (PCA plots, support encoding) are strong visuals. TikZ source or vector source needed for Beamer. |
| Figure 1 from the graph coloring paper | Triangular PCA embedding diagram is the clearest illustration of the coloring concept. TikZ or vector source needed. |
| Exact probe accuracy numbers for Chapter 4 | Slide 37 uses a schematic. Replace with the actual bar chart values from the paper. |
| Sparse PCA claim framing | Slide 31 states "first combinatorial algorithm matching Covariance Thresholding, no hyperparameters." Confirm this is exactly how it is stated in the AAAI 2026 paper. |

### Optional but improves the talk

| Item | Notes |
|------|-------|
| WalkSAT vs. SupportSAT-01 convergence plot | Fig. 3 in the SAT paper. Clear and compelling for Slide 22. |
| Existing slides from the Weizmann PPTX | `GNNs/my papers/ReverseAlg50Weizmann.pptx` — check for reusable diagrams, especially the GNN/BP comparison sequence. |
| Target audience calibration | Confirm whether any ADYN attendees have ML backgrounds. This affects how much time to spend on Slides 4–13. |
| Abstract deadline for the ADYN website | The event page lists the title as TBA. If there's a deadline for submitting title/abstract, note it. |

---

## Notes for Beamer Generation

Once you approve this outline and resolve the items above, generate the Beamer deck using:

```bash
python agent.py \
  --title "Learned Algorithms or Classical Messages in Disguise?" \
  --papers "GNNs/my papers/" \
  --output adyn2026 \
  --compile
```

Or generate an outline draft first for quick review:

```bash
python agent.py --outline-only --title "Learned Algorithms or Classical Messages in Disguise?"
```

Key parameters to set in `config.py` before generating:
- `TALK_TITLE` — set to chosen title variant
- `AUDIENCE` — "PhD students and postdocs in algorithms, combinatorics, TCS"
- `TALK_DURATION_MINUTES` — 50
- `TARGET_SLIDE_COUNT` — 42
- `BEAMER_THEME` — confirm preference
