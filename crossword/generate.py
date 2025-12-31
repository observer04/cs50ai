import re
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        ## domain = dictionary var: set of words & var = variable object 
        for var in self.domains:
            to_remove = set()
            ##domain or word list for var, check each word, 
            for word in self.domains[var]:
                if len(word) != var.length:
                    to_remove.add(word)
            self.domains[var] -= to_remove

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        #get overlap positions
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return revised
        x_pos, y_pos= overlap
        to_remove = set()
        #check if a word in x can be matched with a word in y at overlap
        for x_word in self.domains[x]:
            found = False
            for y_word in self.domains[y]:
                if x_word[x_pos] == y_word[y_pos]:      # they can overlap
                    found = True
                    break 
            if not found:          # no word in y matches x_word's letter at overlap> remove x_word
                to_remove.add(x_word)
                revised = True
        self.domains[x] -= to_remove
        return revised
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Initialize queue of arcs
        if arcs is None:
            queue = []  #of (x, y) pairs
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    queue.append((x, y))
        else:
            queue = arcs
        # Process arcs until queue is empty
        while queue:
            x, y = queue.pop(0)
            # revise x to see if any values can be removed
            if self.revise(x, y):
                #empty domain -> return false
                if not self.domains[x]:
                    return False
                #after revising x, add all arcs (z, x) back to queue
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        return True
        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        #assignment is a dict var: word
        return len(assignment) == len(self.crossword.variables)
    

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #check all assigned words are correct length
        for var in assignment:
            if len(assignment[var]) != var.length:
                return False
        #check all assigned words are unique
        if len(set(assignment.values())) < len(assignment):
            return False
        #check for conflicts between neighboring variables
        for var1 in assignment:
            for var2 in self.crossword.neighbors(var1):
                if var2 in assignment:
                    overlap = self.crossword.overlaps[var1, var2]
                    if overlap is not None:
                        i, j = overlap
                        if assignment[var1][i] != assignment[var2][j]:  #conflict: letters dont match
                            return False
        return True
    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #dictionary word: number of ruled out values
        count_dict = dict()
        for word in self.domains[var]:
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap is not None:
                        i, j = overlap
                        for neighbor_word in self.domains[neighbor]:
                            if word[i] != neighbor_word[j]:
                                count += 1
            count_dict[word] = count
        #return words sorted by count of ruled out values
        return sorted(self.domains[var], key=lambda w: count_dict[w])
    

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        #get list of unassigned variables
        unassigned_vars = [var for var in self.crossword.variables if var not in assignment]
        #sort by number of remaining values (ascending) and degree (descending) = most neighbors first 
        unassigned_vars.sort(key=lambda v: (len(self.domains[v]), -len(self.crossword.neighbors(v))))
        return unassigned_vars[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #if assignment is complete, return it
        if self.assignment_complete(assignment):
            return assignment
        #select unassigned variable
        var = self.select_unassigned_variable(assignment)
        #try each value in var's domain
        for word in self.order_domain_values(var, assignment):
            #create new assignment with var assigned to word
            new_assignment = assignment.copy()
            new_assignment[var] = word
            #if new assignment is consistent, recurse
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
