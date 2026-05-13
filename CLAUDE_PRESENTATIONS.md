# CLAUDE_PRESENTATIONS.md

## Purpose

This file defines how to help Dan prepare research-seminar presentations about his own work.

These are not ordinary class lectures. They are research talks where the goal is to make the audience understand the problem, feel the gap, see the intuition, and only then appreciate the method and results.

The default style should be closer to a strong VC-style pitch than to a dense academic lecture.

The talk should build conviction.

---

## Core Presentation Philosophy

When preparing slides for me, do not start from the paper structure.

Do not simply convert the paper into slides.

Instead, build the talk around the following logic:

1. What is the real-world or scientific problem?
2. Why should anyone care?
3. What is the current way people think about it?
4. What is missing?
5. What is the key insight?
6. What do we contribute?
7. How does the method work, intuitively?
8. What toy example makes the idea obvious?
9. What do the results show?
10. Why does this matter?

The talk should feel like a guided argument, not a compressed manuscript.

---

## Default Talk Structure

### 1. Hook / Opening Problem

Start with a concrete setting. Use an example, story, dataset situation, failure case, or simple dilemma.

The opening should make the audience understand the problem before seeing any formalism.

Avoid opening with long literature review, formal definitions, dataset table, generic motivation, or "Machine learning has achieved great success...".

### 2. The Setting

Define the setting slowly and visually. The audience should understand what objects we work with, what the input is, what the output is, who is making a decision, what success means, and why the setting is hard.

Use diagrams before equations. Use small examples before general definitions.

### 3. The Gap

This is the most important part. Every talk should have a clear missing piece.

Bad gap: "Prior work has not studied this enough."

Good gap: "Prior work measures average performance, but practitioners need to know when expensive feature selection is worth the runtime."

Good gap: "Existing sarcasm datasets are treated as interchangeable, but they differ in affective composition. A model trained on toxic sarcasm may not transfer to playful sarcasm."

Good gap: "LLMs can retrieve many relevant archival sentences, but rare events make ordinary accuracy meaningless. The question is how much historian screening effort can actually be reduced."

The audience should be able to repeat the gap in one sentence.

### 4. Why the Obvious Solution Fails

Before presenting our method, explain why naive approaches are insufficient. This creates tension.

Examples:

- "Just train on more data" does not solve cross-domain affect mismatch.
- "Just compare feature-selection algorithms" ignores dataset hardness and runtime.
- "Just report F1" hides the cost of false positives in rare-event retrieval.
- "Just use an LLM" ignores the need for human-in-the-loop screening.
- "Just run SEM" does not explain who benefits from which retreat type.

### 5. Key Insight

Every talk should have a single central insight, stated plainly.

Examples:

- "The important question is not which method is best overall, but which method is worth its cost for a dataset of a given hardness."
- "Cross-domain sarcasm failure may reflect affective mismatch, not only topic or platform shift."
- "For rare archival phenomena, the useful metric is not accuracy but how much expert screening effort the model saves."
- "Yoga retreats may improve well-being not only through practice, but through the fit between motivation and experience."

### 6. Our Contribution

State contributions as answers to the gap. Prefer 2-3 contributions, not a long list. Each contribution should be concrete.

Bad: "We propose a novel framework."

Good: "We introduce an affective-profile view of sarcasm datasets, showing that datasets differ systematically along humor, irony, and toxicity dimensions."

Good: "We benchmark 37 feature-selection methods across 102 datasets and show that expensive methods rarely justify their runtime on easy datasets."

Good: "We evaluate LLMs on extremely rare altruistic behaviors in Holocaust testimonies and translate model performance into historian screening reduction."

---

## Slide Style

Slides should be visual, sparse, and argument-driven. Each slide should have one job. Each slide should have a strong title that states the point.

Bad slide title: "Motivation"

Good slide title: "Rare events make ordinary accuracy misleading"

Bad slide title: "Results"

Good slide title: "Most of the benefit comes from reducing the historian's search space"

---

## Preferred Slide Types

### Problem Slide

A simple visual of the setting.

```text
Archive of 15,000 sentences
        ↓
Rare caring-for-others moments
        ↓
Only 37 true cases
```

### Gap Slide

Show what prior work covers and what is missing.

```text
Prior work:
Motivations ✓
Retreat experience ✓
Well-being ✓

Missing:
How these pieces connect into a mechanism
```

### Toy Example Slide

Use a tiny artificial example to make the method intuitive.

```text
Dataset A sarcasm:
80% toxic, 10% humorous, 10% ironic

Dataset B sarcasm:
10% toxic, 70% humorous, 20% ironic

A model trained on A may learn "sarcasm = attack"
and fail on B, where sarcasm is playful.
```

Toy examples are essential. Use them before technical explanation.

### Pipeline Slide

Use a clean visual pipeline.

```text
Raw texts
  → affect classifiers
  → affective buckets
  → dataset profiles
  → mismatch estimate
  → targeted enrichment
  → cross-domain evaluation
```

### Intuition Before Equation Slide

If there is a mathematical object, first explain what it means in words.

```text
Instead of asking:
"How accurate is the model?"

We ask:
"How many sentences can a historian avoid reading
while still recovering most rare target cases?"
```

### Results Slide

Results should answer the story, not just present numbers.

Bad: "Table 3: Model Performance"

Good: "Unioning models recovers more rare cases, but increases review burden"

---

## Use of Examples

Examples are central to my presentation style.

For every important concept, try to include one verbal example, one toy example, one visual example, and one real-data example when available.

The audience should understand the idea even if they ignore the formalism.

If a concept is abstract, make it concrete. If a method is technical, create a small version of it with 3-5 objects. If a result is statistical, explain what it means operationally.

---

## Use of Illustrations

Prefer simple illustrations over decorative figures.

Good illustrations:

- before/after diagrams
- small graphs
- arrows showing causal or procedural flow
- toy datasets
- 2D geometric drawings
- small confusion matrices
- simple timelines
- screening funnels
- profile comparisons
- intuitive cartoons of the setting

Avoid dense tables, full screenshots of papers, overly detailed architecture diagrams, too many equations on one slide, unreadable SEM/path diagrams without simplification, and decorative AI/robot images that do not explain anything.

---

## Results Placement

Do not rush to results. The audience should already understand what result would be meaningful before seeing the result.

Before results, establish what success means, what failure means, what baseline matters, what comparison is fair, and what the audience should look for.

Then show results and interpret immediately.

Never show a table and leave the audience to infer the message.

---

## Technical Detail

Use enough technical detail to be credible, but not so much that the main argument is lost.

Technical slides should be layered:

1. intuition
2. toy example
3. formal object or algorithm
4. empirical use

If a slide is dense, split it.

---

## Equations

Use equations sparingly. When equations are needed, introduce the symbols first, explain the equation in words, show what it computes, and include a tiny example.

Never put an equation on a slide just because it appears in the paper.

---

## Literature

Do not create a long literature-review section. Use literature strategically to define the current paradigm, show what is missing, position our contribution, and reassure the audience that we know the field.

Example:

```text
What prior work gives us:
1. Yoga retreats can improve well-being.
2. Participants differ in motivations.
3. Retreats differ in experience components.

What prior work does not explain:
How motivation-experience fit shapes sustained outcomes.
```

---

## Talk Rhythm

The preferred rhythm is:

```text
Concrete problem
↓
Why it matters
↓
Why existing view is incomplete
↓
Toy example
↓
Key idea
↓
Method / model
↓
What we test
↓
Results
↓
Interpretation
↓
Takeaway
```

---

## Slide Titles

Use assertive slide titles. Each title should be a message, not a label.

Examples:

- "The hard part is not detecting common patterns — it is finding rare ones"
- "Dataset shift can be affective, not only topical"
- "The cheapest feature-selection methods are often enough"
- "Motivations shape which retreat components matter"
- "The cognitive process is the bridge to well-being"
- "A useful model should reduce expert workload, not just improve accuracy"
- "The right question is who benefits from which retreat"

Avoid generic titles like Introduction, Background, Literature Review, Method, Results, and Discussion.

---

## Research-Seminar Opening Templates

### Opening with a Practical Problem

```text
Imagine you are a historian facing thousands of archival sentences.
You are not looking for a common theme.
You are looking for a rare moral behavior that may appear in less than 1% of the text.

A standard classifier can look good and still be useless.
The real question is: can it reduce your reading burden without missing the rare cases?
```

### Opening with a Dataset Mismatch

```text
Suppose we train a sarcasm detector on a dataset where sarcasm is mostly toxic.
Now we test it on a dataset where sarcasm is mostly humorous.

The model may fail not because it does not understand sarcasm,
but because it learned the wrong affective version of sarcasm.
```

### Opening with a Practitioner Decision

```text
A practitioner wants to choose a feature-selection method.
There are dozens of algorithms.
Some run in seconds. Some run for hours.
The question is not which algorithm wins once.
The question is when the extra cost is justified.
```

### Opening with a Human-Centered Mechanism

```text
People go to yoga retreats for different reasons.
Some want physical progress.
Some want quiet and reflection.
Some want community.

So why would we expect the same retreat experience to help everyone in the same way?
```

---

## VC-Pitch Style Adapted to Research

Use the logic of a pitch, but keep academic credibility.

Useful VC-style elements:

- clear problem
- clear pain point
- why now
- what is missing
- simple insight
- memorable framing
- evidence of traction/results
- crisp takeaway

Avoid startup hype: "revolutionize", "game-changing", "disruptive", "unprecedented".

Prefer: "This reframes the evaluation problem", "This suggests a more useful operating point", "This gives practitioners a decision rule", or "This exposes a mechanism that was previously treated as a black box."

---

## How to Help Build a Deck

When asked to prepare slides, first propose:

1. The core message of the talk.
2. The target audience assumption.
3. The slide-level storyline.
4. The key toy examples.
5. The figures/illustrations needed.
6. The results that must appear.
7. The final takeaway.

Then generate slide drafts.

For each slide, include:

- slide title
- slide purpose
- visual idea
- minimal slide text
- speaker-note idea

Do not begin by writing long slide text.

---

## Preferred Slide Draft Format

```markdown
## Slide X — Message-style title

Purpose:
What this slide needs to achieve.

Visual:
Describe the figure, diagram, toy example, or layout.

Slide text:
Short text that appears on the slide.

Speaker note:
What Dan should say orally.
```

---

## Beamer / LaTeX Guidance

When generating Beamer slides:

- Use clean layouts.
- Prefer one main visual per slide.
- Avoid dense itemization.
- Use large readable text.
- Use simple TikZ diagrams when helpful.
- Use overlays to reveal argument step by step.
- Use examples and toy data.
- Keep tables small.
- Use backup slides for technical details.
- Do not overload the main deck.

Animations should support the argument, not decorate it.

---

## Handling Results Slides

For each result, state the interpretation.

Example:

```text
Result:
Model union recovers 87% of rare target cases.

Cost:
The historian reviews about 100x more candidates than the gold positives.

Interpretation:
This is still far less than reading the full archive, making high-recall screening feasible.
```

Never show a metric without explaining the operational meaning.

---

## Handling Limitations

Include limitations, but frame them constructively.

Example:

```text
What this study does not claim

- Cross-sectional SEM does not prove causality.
- Self-reports capture perceived change, not objective behavior.
- The Israeli yoga-tourism sample may not generalize to all retreat cultures.

Why the result still matters:
The model identifies a testable mechanism for future longitudinal work.
```

---

## Final Slide

The final slide should not be "Thank you" only. It should leave the audience with one sentence.

Example:

```text
Takeaway:
The value of yoga retreats may depend less on the retreat alone,
and more on the fit between what participants seek and what the retreat enables.
```

---

## Default Standard

When uncertain, make the presentation more concrete, visual, intuitive, example-driven, less text-heavy, less paper-like, and more focused on the gap and contribution.

The audience should leave remembering the problem, the gap, the intuition, and the main result.
