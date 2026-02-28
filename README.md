# CS50 AI — Projects

This repository contains all projects completed as part of [CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/) (CS50AI). Each project explores a different area of AI, from classical search algorithms to deep learning and transformers.

---

## Table of Contents

| # | Project | Topic |
|---|---------|-------|
| 0 | [Maze](#maze) | Depth-First Search |
| 0 | [Degrees](#degrees) | Breadth-First Search |
| 1 | [Tictactoe](#tictactoe) | Minimax / Adversarial Search |
| 1 | [Knights](#knights) | Propositional Logic |
| 2 | [Minesweeper](#minesweeper) | Knowledge-Based Agent |
| 2 | [PageRank](#pagerank) | Markov Chains / Random Surfer |
| 3 | [Heredity](#heredity) | Bayesian Networks |
| 3 | [Crossword](#crossword) | Constraint Satisfaction Problem |
| 4 | [Nim](#nim) | Reinforcement Learning (Q-Learning) |
| 4 | [Shopping](#shopping) | k-Nearest Neighbors |
| 5 | [Traffic](#traffic) | Convolutional Neural Network |
| 6 | [Parser](#parser) | Context-Free Grammar (NLP) |
| 6 | [Attention](#attention) | Transformer / BERT Self-Attention |

---

## Projects

### Maze
**`project0a/`** &nbsp;|&nbsp; *Uninformed Search — Depth-First Search*

Reads a text-based maze file, finds a path from start (`A`) to goal (`B`) using **DFS**, and exports the solution as an image annotated with walls, the solution path, and explored cells.

---

### Degrees
**`degrees/`** &nbsp;|&nbsp; *Uninformed Search — Breadth-First Search*

Finds the shortest "degree of separation" between two actors through shared movie appearances (the *Six Degrees of Kevin Bacon* problem). Uses **BFS** over a graph where actors are nodes and shared films are edges, guaranteeing the shortest path.

---

### Tictactoe
**`tictactoe/`** &nbsp;|&nbsp; *Adversarial Search — Minimax*

An unbeatable Tic-Tac-Toe AI powered by the **Minimax algorithm**. The AI exhaustively explores the game tree to always choose the optimal move, guaranteeing it never loses.

---

### Knights
**`knights/`** &nbsp;|&nbsp; *Knowledge Representation & Logical Inference*

Solves "Knights and Knaves" logic puzzles using **propositional logic** and **model checking**. The knowledge base encodes puzzle statements as logical sentences; entailment determines which assignments (knight/knave) are consistent with the clues.

---

### Minesweeper
**`minesweeper/`** &nbsp;|&nbsp; *Knowledge-Based Agent — Constraint Propagation*

An AI Minesweeper player that maintains a knowledge base of sentences of the form `{cells} = count`. It performs **subset inference** to deduce new mines and safe cells iteratively, falling back to a random uncovered cell only when no safe move can be inferred.

---

### PageRank
**`pagerank/`** &nbsp;|&nbsp; *Graph-Based Ranking — Markov Chains*

Implements Google's **PageRank** algorithm two ways:
- **Sampling**: simulates a random surfer navigating pages with damping factor `d = 0.85`.
- **Iterative**: repeatedly applies the PageRank formula until convergence (`Δ < 0.001`).

$$PR(p) = \frac{1-d}{N} + d \sum_{i \to p} \frac{PR(i)}{|L(i)|}$$

---

### Heredity
**`heredity/`** &nbsp;|&nbsp; *Probabilistic Inference — Bayesian Networks*

Computes the probability that each person in a family possesses a hereditary genetic trait using a **Bayesian network**. Joint probabilities are computed over all gene-count and trait combinations, then marginalized and normalized.

---

### Crossword
**`crossword/`** &nbsp;|&nbsp; *Constraint Satisfaction Problem (CSP)*

Fills a crossword puzzle grid by modeling it as a CSP and solving it with **backtracking search** enhanced by:
- **AC-3** arc consistency preprocessing
- **MRV** (Minimum Remaining Values) variable ordering
- **Degree heuristic** as a tiebreaker
- **Least-Constraining Value** (LCV) domain ordering

---

### Nim
**`nim/`** &nbsp;|&nbsp; *Reinforcement Learning — Q-Learning*

An AI that learns to play [Nim](https://en.wikipedia.org/wiki/Nim) optimally through **self-play**. Uses **Q-learning** with an epsilon-greedy exploration strategy:

$$Q(s,a) \leftarrow Q(s,a) + \alpha \left[\text{reward} + \max_{a'} Q(s', a') - Q(s,a)\right]$$

After training, the AI wins virtually every game against a human.

---

### Shopping
**`shopping/`** &nbsp;|&nbsp; *Supervised Machine Learning — k-Nearest Neighbors*

Predicts whether an online shopping session will result in a purchase using a **k-Nearest Neighbors** classifier (`k=1`) trained on 17 session-level features (page visits, durations, session metadata). Evaluated using sensitivity and specificity on a 60/40 train/test split.

---

### Traffic
**`traffic/`** &nbsp;|&nbsp; *Deep Learning — Convolutional Neural Network*

Trains a **CNN** to classify road signs from the [German Traffic Sign Recognition Benchmark](https://benchmark.ini.rub.de/gtsrb_news.html) (GTSRB) into 43 categories. Architecture:
- 3 × Conv2D + MaxPooling2D blocks (32 → 64 → 128 filters)
- Dense(512, ReLU) → Dropout → Softmax(43)
- Optimizer: Adam | Loss: Categorical Cross-Entropy
- Input: 30×30 RGB images loaded with OpenCV

---

### Parser
**`parser/`** &nbsp;|&nbsp; *NLP — Context-Free Grammar*

Parses English sentences with a hand-written **Context-Free Grammar (CFG)** using NLTK's `ChartParser`. After parsing, extracts **noun phrase (NP) chunks** — the innermost `NP` subtrees that contain no other `NP` subtrees.

---

### Attention
**`attention/`** &nbsp;|&nbsp; *Transformer — BERT Self-Attention*

Uses `bert-base-uncased` (via HuggingFace Transformers) to:
1. Predict the most likely word(s) for a `[MASK]` token in an input sentence.
2. Visualize **self-attention** weights across all 12 layers × 12 heads (144 diagrams total), saved as PNG images showing which tokens each head attends to.

---

## Setup

```bash
# Clone the repo
git clone https://github.com/observer04/cs50ai.git
cd cs50ai

# (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies per project
pip install -r <project>/requirements.txt
```

> **Python version:** 3.12+

---

## Course

**[CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/)**  
Harvard University — edX

Topics covered: Search, Knowledge, Uncertainty, Optimization, Learning, Neural Networks, Language.
