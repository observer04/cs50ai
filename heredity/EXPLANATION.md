# Heredity: Genetic Inheritance Probability Calculator

## Table of Contents
1. [Problem Overview](#problem-overview)
2. [Background: Genetics Basics](#background-genetics-basics)
3. [Probability Model](#probability-model)
4. [Algorithm Approach](#algorithm-approach)
5. [Code Implementation](#code-implementation)
6. [Worked Example](#worked-example)
7. [Testing & Verification](#testing--verification)

---

## Problem Overview

### What are we solving?
We want to calculate the probability distribution of:
- **How many copies of a gene** each person in a family has (0, 1, or 2 copies)
- **Whether each person exhibits a trait** associated with that gene (True or False)

### Given Information
- Family tree structure (who the parents are)
- Whether certain people exhibit the trait (known observations)
- Probabilistic rules for:
  - Baseline gene frequencies in the population
  - How genes are passed from parents to children
  - How gene copies relate to trait expression
  - Mutation rates

### Output
For each person, we calculate:
```
Person:
  Gene:
    2: probability of having 2 copies
    1: probability of having 1 copy
    0: probability of having 0 copies
  Trait:
    True: probability of exhibiting the trait
    False: probability of not exhibiting the trait
```

---

## Background: Genetics Basics

### Gene Copies
- Humans have **2 copies** of each gene (one from each parent)
- A person can have:
  - **0 copies** of a particular gene variant
  - **1 copy** (heterozygous)
  - **2 copies** (homozygous)

### Inheritance
- Each parent passes **exactly one** of their two gene copies to their child
- Which copy is passed is random (50/50 chance for each)

### Mutations
- Occasionally, a gene can mutate during transmission
- Mutation probability: **1%** (0.01)
- A parent with the gene might pass a non-gene copy (mutation away)
- A parent without the gene might pass a gene copy (mutation into)

### Gene-to-Trait Relationship
- Having more copies of the gene increases the likelihood of expressing the trait
- But it's **not deterministic** (you can have the gene without the trait, or vice versa)

---

## Probability Model

### Given Constants (PROBS dictionary)

#### 1. Unconditional Gene Probabilities
For people with **no known parents** (baseline population frequencies):
```python
PROBS["gene"] = {
    2: 0.01,  # 1% of population has 2 copies
    1: 0.03,  # 3% of population has 1 copy
    0: 0.96   # 96% of population has 0 copies
}
```

#### 2. Trait Expression Given Gene Count
```python
PROBS["trait"] = {
    2: {True: 0.65, False: 0.35},  # 2 genes → 65% show trait
    1: {True: 0.56, False: 0.44},  # 1 gene  → 56% show trait
    0: {True: 0.01, False: 0.99}   # 0 genes → 1% show trait
}
```

#### 3. Mutation Rate
```python
PROBS["mutation"] = 0.01  # 1% chance of mutation during transmission
```

---

## Algorithm Approach

### The Challenge
We need to calculate **marginal probabilities** for each person, but we don't know the exact genetic state of anyone.

### The Solution: Joint Probability Distribution
We use the **law of total probability**:

1. **Enumerate all possible worlds** (combinations of who has how many genes and who has the trait)
2. **Calculate the joint probability** of each world
3. **Sum up probabilities** for each person's specific states across all worlds
4. **Normalize** to ensure probability distributions sum to 1

### Why This Works
- We consider every possible genetic configuration of the family
- For configurations that match known observations (e.g., "James has the trait"), we calculate how likely that configuration is
- We accumulate these probabilities for each person's possible states
- This gives us the marginal probability distribution for each person

---

## Code Implementation

### Main Program Flow

```python
def main():
    # 1. Load family data from CSV
    people = load_data(sys.argv[1])
    
    # 2. Initialize probability storage
    probabilities = {
        person: {
            "gene": {2: 0, 1: 0, 0: 0},
            "trait": {True: 0, False: 0}
        }
        for person in people
    }
    
    # 3. Iterate over all possible configurations
    names = set(people)
    for have_trait in powerset(names):          # All subsets who might have trait
        # Skip if contradicts known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue
        
        for one_gene in powerset(names):        # All subsets who might have 1 gene
            for two_genes in powerset(names - one_gene):  # All subsets who might have 2 genes
                # Calculate joint probability of this configuration
                p = joint_probability(people, one_gene, two_genes, have_trait)
                
                # Add this probability to each person's relevant buckets
                update(probabilities, one_gene, two_genes, have_trait, p)
    
    # 4. Normalize so each distribution sums to 1
    normalize(probabilities)
    
    # 5. Print results
    # ... (printing code)
```

---

### Function 1: `joint_probability`

**Purpose**: Calculate the probability that a specific configuration of genes and traits occurs.

**Parameters**:
- `people`: Dictionary of family members with parent information
- `one_gene`: Set of people with exactly 1 gene copy
- `two_genes`: Set of people with exactly 2 gene copies
- `have_trait`: Set of people who exhibit the trait

**Returns**: A probability (float between 0 and 1)

#### Line-by-Line Breakdown

```python
def joint_probability(people, one_gene, two_genes, have_trait):
    # Start with probability 1 and multiply probabilities per person
    probability = 1.0
```
- We use the **multiplication rule** for independent events
- Joint probability = P(person1) × P(person2) × ... × P(personN)

```python
    for person, info in people.items():
        # Determine number of genes for this person
        if person in two_genes:
            genes = 2
        elif person in one_gene:
            genes = 1
        else:
            genes = 0
```
- Figure out how many gene copies this person has in this configuration
- If not in `one_gene` or `two_genes`, they have 0 copies

```python
        # Probability of person having `genes` copies
        mother = info['mother']
        father = info['father']
        
        if mother is None and father is None:
            # No parents known - use unconditional probability
            gene_prob = PROBS['gene'][genes]
```
- **Case 1: No known parents** (founding generation)
- Use population baseline frequencies from `PROBS["gene"]`
- Example: P(0 genes) = 0.96

```python
        else:
            # Calculate probability each parent passes the gene
            def pass_prob(parent):
                parent_genes = 2 if parent in two_genes else 1 if parent in one_gene else 0
                if parent_genes == 2:
                    return 1 - PROBS['mutation']
                elif parent_genes == 1:
                    return 0.5
                else:
                    return PROBS['mutation']
```
- **Case 2: Known parents** - calculate inheritance probability
- Helper function: What's the probability this parent passes the gene?

**Parent has 2 gene copies**:
```
Parent: [Gene] [Gene]
         ↓
       Child gets one copy
```
- Almost certainly passes a gene (99% chance)
- 1% chance of mutation (passes non-gene)
- `pass_prob = 1 - 0.01 = 0.99`

**Parent has 1 gene copy**:
```
Parent: [Gene] [No Gene]
         ↓        ↓
      50/50 random choice
```
- 50% chance passes the gene
- 50% chance passes the non-gene
- `pass_prob = 0.5`

**Parent has 0 gene copies**:
```
Parent: [No Gene] [No Gene]
              ↓
        Mutation possible
```
- Almost certainly passes non-gene (99% chance)
- 1% chance of mutation (passes gene)
- `pass_prob = 0.01`

```python
            p_m = pass_prob(mother)
            p_f = pass_prob(father)
```
- Calculate probability mother passes gene: `p_m`
- Calculate probability father passes gene: `p_f`

```python
            if genes == 2:
                gene_prob = p_m * p_f
```
- **Child has 2 genes**: Must get gene from BOTH parents
- Probability = P(mother passes) × P(father passes)
- Example: If both parents have 1 gene → 0.5 × 0.5 = 0.25

```python
            elif genes == 1:
                gene_prob = p_m * (1 - p_f) + (1 - p_m) * p_f
```
- **Child has 1 gene**: Two mutually exclusive ways this can happen:
  1. Mother passes gene AND father doesn't: `p_m × (1 - p_f)`
  2. Mother doesn't AND father does: `(1 - p_m) × p_f`
- Add these probabilities (OR operation)
- Example: Both parents have 1 gene → 0.5×0.5 + 0.5×0.5 = 0.5

```python
            else:
                gene_prob = (1 - p_m) * (1 - p_f)
```
- **Child has 0 genes**: NEITHER parent passes gene
- Probability = P(mother doesn't pass) × P(father doesn't pass)
- Example: Both parents have 1 gene → 0.5 × 0.5 = 0.25

```python
        # Probability of trait given gene count
        trait = person in have_trait
        trait_prob = PROBS['trait'][genes][trait]
```
- Look up: Given this person has `genes` copies, what's P(trait)?
- Example: 2 genes, has trait → `PROBS['trait'][2][True]` = 0.65

```python
        # Multiply into joint probability
        probability *= gene_prob * trait_prob
```
- For this person: P(person) = P(gene count) × P(trait | gene count)
- Multiply into running product
- After loop: probability = P(person1) × P(person2) × ... × P(personN)

```python
    return probability
```
- Return the joint probability of this entire configuration

---

### Function 2: `update`

**Purpose**: Add a joint probability to the appropriate buckets in the probability distributions.

**Parameters**:
- `probabilities`: Dictionary storing accumulated probabilities for each person
- `one_gene`, `two_genes`, `have_trait`: The configuration we just calculated probability for
- `p`: The joint probability of this configuration

**Returns**: Nothing (modifies `probabilities` in place)

#### Line-by-Line Breakdown

```python
def update(probabilities, one_gene, two_genes, have_trait, p):
    for person in probabilities:
```
- Iterate through every person in the family

```python
        # Determine gene count for this person in this configuration
        if person in two_genes:
            genes = 2
        elif person in one_gene:
            genes = 1
        else:
            genes = 0
```
- Figure out: In this configuration, how many genes does this person have?

```python
        probabilities[person]['gene'][genes] += p
```
- **Key insight**: We're accumulating marginal probabilities
- Add the joint probability `p` to this person's gene count bucket
- Example: If person has 1 gene in this configuration with p=0.003, add 0.003 to their `gene[1]` total
- After all configurations are processed, `gene[1]` will contain the sum of all joint probabilities where this person had 1 gene

```python
        # Determine trait for this person in this configuration
        has_trait = person in have_trait
        probabilities[person]['trait'][has_trait] += p
```
- Similarly for trait: Add `p` to the appropriate trait bucket (True or False)
- This accumulates the marginal probability for each trait value

**Why this works (mathematical justification)**:
```
P(person has 1 gene) = Σ P(configuration) for all configurations where person has 1 gene
```
By summing joint probabilities across all relevant configurations, we get the marginal probability.

---

### Function 3: `normalize`

**Purpose**: Convert raw accumulated probabilities into proper probability distributions that sum to 1.

**Parameters**:
- `probabilities`: Dictionary with accumulated (but not normalized) probabilities

**Returns**: Nothing (modifies `probabilities` in place)

#### Line-by-Line Breakdown

```python
def normalize(probabilities):
    for person in probabilities:
```
- Process each person's distributions

```python
        # Normalize gene distribution
        gene_total = sum(probabilities[person]['gene'].values())
```
- Sum up the accumulated probabilities: P(0 genes) + P(1 gene) + P(2 genes)
- Example: 0.5351 + 0.4557 + 0.0092 = 1.0 (already normalized)
- Or might be: 0.0536 + 0.0457 + 0.0009 = 0.1002 (needs normalizing)

```python
        if gene_total != 0:
            for g in probabilities[person]['gene']:
                probabilities[person]['gene'][g] /= gene_total
```
- Divide each probability by the total
- This preserves **relative proportions** while ensuring the sum = 1
- Example: If totals were [0.0536, 0.0457, 0.0009]:
  - After normalizing: [0.0536/0.1002, 0.0457/0.1002, 0.0009/0.1002]
  - = [0.535, 0.456, 0.009] ← sums to 1.0
- Guard against division by zero (though shouldn't happen in practice)

```python
        # Normalize trait distribution
        trait_total = sum(probabilities[person]['trait'].values())
        if trait_total != 0:
            for t in probabilities[person]['trait']:
                probabilities[person]['trait'][t] /= trait_total
```
- Same process for trait distribution
- Ensures P(True) + P(False) = 1.0

**Why normalization is needed**:
- We only iterate over configurations that match known evidence
- Example: If we know "James has the trait", we skip all configurations where James doesn't have it
- This means we're working with **conditional probabilities**
- The raw sums don't add to 1 because we've excluded some possibilities
- Normalization converts these to proper conditional probability distributions

---

## Worked Example

Let's trace through a simple example: **family0.csv**

### Input Data
```csv
name,mother,father,trait
Harry,James,Lily,
James,,,1
Lily,,,0
```

**Family tree**:
```
    James (trait: True)
         \
          \
    Lily (trait: False)
           \
            → Harry (trait: unknown)
```

### Known Facts
- James has the trait (observed)
- Lily does NOT have the trait (observed)
- Harry's trait is unknown
- James and Lily have no known parents

### Processing

#### Step 1: Enumerate configurations
We need to consider all combinations of:
- Who has 0/1/2 genes: `one_gene` and `two_genes` sets
- Who has the trait: `have_trait` set

But we skip any configuration where:
- James doesn't have the trait (contradicts evidence)
- Lily has the trait (contradicts evidence)

#### Step 2: Example configuration
Let's calculate one specific configuration:
- **Genes**: James=1, Lily=0, Harry=1
- **Trait**: James=True, Lily=False, Harry=True

##### Calculate joint probability:

**James** (1 gene, has trait, no parents):
```python
gene_prob = PROBS['gene'][1] = 0.03
trait_prob = PROBS['trait'][1][True] = 0.56
P(James) = 0.03 × 0.56 = 0.0168
```

**Lily** (0 genes, no trait, no parents):
```python
gene_prob = PROBS['gene'][0] = 0.96
trait_prob = PROBS['trait'][0][False] = 0.99
P(Lily) = 0.96 × 0.99 = 0.9504
```

**Harry** (1 gene, has trait, parents known):
```python
# Probability James (1 gene) passes gene: 0.5
# Probability Lily (0 genes) passes gene: 0.01 (mutation)
p_james = 0.5
p_lily = 0.01

# Harry has 1 gene, so one parent passes, one doesn't:
gene_prob = p_james × (1 - p_lily) + (1 - p_james) × p_lily
         = 0.5 × 0.99 + 0.5 × 0.01
         = 0.495 + 0.005
         = 0.5

trait_prob = PROBS['trait'][1][True] = 0.56
P(Harry) = 0.5 × 0.56 = 0.28
```

**Joint probability**:
```python
P(configuration) = P(James) × P(Lily) × P(Harry)
                 = 0.0168 × 0.9504 × 0.28
                 = 0.00447
```

##### Update probabilities:
```python
probabilities['James']['gene'][1] += 0.00447
probabilities['James']['trait'][True] += 0.00447
probabilities['Lily']['gene'][0] += 0.00447
probabilities['Lily']['trait'][False] += 0.00447
probabilities['Harry']['gene'][1] += 0.00447
probabilities['Harry']['trait'][True] += 0.00447
```

#### Step 3: Repeat for all valid configurations
- There are many configurations to consider (exponential in family size)
- Each adds its joint probability to the relevant buckets

#### Step 4: Normalize
After accumulating all configurations, normalize each person's distributions.

### Final Output (Actual Results)
```
Harry:
  Gene:
    2: 0.0092  (0.92% chance Harry has 2 gene copies)
    1: 0.4557  (45.57% chance Harry has 1 gene copy)
    0: 0.5351  (53.51% chance Harry has 0 gene copies)
  Trait:
    True: 0.2665   (26.65% chance Harry exhibits trait)
    False: 0.7335  (73.35% chance Harry doesn't exhibit trait)

James:
  Gene:
    2: 0.1976
    1: 0.5106
    0: 0.2918
  Trait:
    True: 1.0000   (100% - this was given as evidence)
    False: 0.0000

Lily:
  Gene:
    2: 0.0036
    1: 0.0136
    0: 0.9827
  Trait:
    True: 0.0000   (0% - contradicts evidence)
    False: 1.0000  (100% - this was given as evidence)
```

### Interpretation
- **Harry** most likely has 0 genes (53.51%), but there's a significant chance (45.57%) he has 1 gene
- This uncertainty comes from not knowing James and Lily's exact gene counts
- Harry has a 26.65% chance of showing the trait
- **James** likely has 1 gene (51.06%), which makes sense given he shows the trait
- **Lily** almost certainly has 0 genes (98.27%), consistent with not showing the trait

---

## Testing & Verification

### How to Run
```bash
# Test with different families
python heredity.py data/family0.csv
python heredity.py data/family1.csv
python heredity.py data/family2.csv
```

### What to Check
1. **Probabilities sum to 1**: Each gene distribution and trait distribution should sum to ~1.0
2. **Evidence is respected**: People with known traits should have 1.0 or 0.0 for those traits
3. **Inheritance makes sense**: Children's gene probabilities should reflect their parents' likely gene counts
4. **Reasonable values**: No negative probabilities, no probabilities > 1

### Edge Cases Handled
- **No parents**: Uses unconditional probabilities
- **Known traits**: Skips contradictory configurations
- **Mutations**: Accounts for 1% mutation rate in inheritance
- **Zero division**: Guards in normalize function

---

## Key Takeaways

### Algorithmic Insights
1. **Brute force enumeration** can work for small families (exponential complexity)
2. **Joint probability** is calculated by multiplying independent person probabilities
3. **Marginal probability** is found by summing joint probabilities across configurations
4. **Normalization** converts conditional probabilities to proper distributions

### Probabilistic Reasoning
1. **Uncertainty propagates**: Not knowing parents' exact genes creates uncertainty in children
2. **Evidence constrains**: Known traits eliminate many possible configurations
3. **Independence assumption**: We assume each person's trait expression is independent given their gene count

### Implementation Details
1. **Modular design**: Separate functions for joint probability, update, and normalize
2. **Set-based encoding**: Using sets to represent who has what (elegant and efficient)
3. **Mutation handling**: Always account for small mutation probability in inheritance
4. **Defensive coding**: Guard against edge cases (zero division, missing parents)

---

## Further Extensions

### Possible Improvements
1. **More efficient algorithms**: Use dynamic programming or belief propagation instead of brute force
2. **Multiple genes**: Extend to track multiple independent genes
3. **More complex traits**: Model traits influenced by multiple genes
4. **Pedigree visualization**: Display family tree with probability overlays
5. **Sensitivity analysis**: Show how probabilities change with different mutation rates

### Related Problems
- Bayesian networks
- Hidden Markov Models
- Medical genetics counseling
- Population genetics simulation
- Disease risk assessment

---

*Generated on November 15, 2025*
