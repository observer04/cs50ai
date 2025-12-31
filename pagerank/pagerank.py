from importlib.metadata import distribution
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a dict mapping each page to its probability under the transition model:
    - With probability damping_factor, choose a link at random from `page`'s outgoing links.
    - With probability (1 - damping_factor), choose any page uniformly at random.
    Treat pages with no outgoing links as linking to all pages.
    """
    N = len(corpus)
    probs = {p: 0.0 for p in corpus}
    links = corpus.get(page, set())

    # Handle dangling page: treat as linking to all pages
    if not links:
        for p in probs:
            probs[p] = 1.0 / N
        return probs

    uniform_prob = (1 - damping_factor) / N
    link_prob = damping_factor / len(links)

    for p in probs:
        probs[p] = uniform_prob + (link_prob if p in links else 0.0)

    return probs


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize visit counts
    visit_counts = {page: 0 for page in corpus}
    
    # Start at a random page
    current_page = random.choice(list(corpus.keys()))
    visit_counts[current_page] += 1
    
    # Sample n-1 more pages (we already sampled the first one)
    for _ in range(n - 1):
        # Get transition probabilities from current page
        probs = transition_model(corpus, current_page, damping_factor)
        
        # Choose next page based on probability distribution
        pages = list(probs.keys())
        probabilities = [probs[page] for page in pages]
        current_page = random.choices(pages, weights=probabilities, k=1)[0]
        
        visit_counts[current_page] += 1
    
    # Convert counts to probabilities (normalize by total samples)
    pagerank = {page: count / n for page, count in visit_counts.items()}
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    
    # Initialize: each page starts with equal probability
    pagerank = {page: 1 / N for page in corpus}
    
    # Iterate until convergence
    convergence_threshold = 0.001
    while True:
        new_pagerank = {}
        
        for page in corpus:
            # Start with the random jump probability
            rank = (1 - damping_factor) / N
            
            # Add contributions from all pages linking to this page
            for other_page in corpus:
                # Check if other_page links to current page
                links = corpus[other_page]
                
                # If other_page has no links, treat it as linking to all pages
                if not links:
                    rank += damping_factor * pagerank[other_page] / N
                # If other_page links to current page, add its contribution
                elif page in links:
                    rank += damping_factor * pagerank[other_page] / len(links)
            
            new_pagerank[page] = rank
        
        # Check for convergence: if all pages changed by less than threshold
        converged = all(
            abs(new_pagerank[page] - pagerank[page]) < convergence_threshold
            for page in corpus
        )
        
        pagerank = new_pagerank
        
        if converged:
            break
    
    return pagerank


if __name__ == "__main__":
    main()
