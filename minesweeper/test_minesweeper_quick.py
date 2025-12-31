from minesweeper import Sentence, MinesweeperAI

# Quick tests for Sentence
s = Sentence({(0,0),(0,1)}, 0)
print('known_safes expected {(0,0),(0,1)} got', s.known_safes())
print('known_mines expected set() got', s.known_mines())

s2 = Sentence({(1,1),(2,3),(3,4)}, 3)
print('known_mines expected {(1,1),(2,3),(3,4)} got', s2.known_mines())

s3 = Sentence({(2,3),(4,5)}, 1)
s3.mark_mine((2,3))
print('after mark_mine, s3.cells expected {(4,5)} got', s3.cells, 'count expected 0 got', s3.count)

s4 = Sentence({(2,3),(5,6)}, 1)
s4.mark_safe((5,6))
print('after mark_safe, s4.cells expected {(2,3)} got', s4.cells)

# Quick test for MinesweeperAI.add_knowledge not raising
ai = MinesweeperAI(4,4)
ai.mark_mine((0,1))
ai.add_knowledge((0,0), 2)
print('AI knowledge size:', len(ai.knowledge))
print('AI mines:', ai.mines)
print('AI safes:', ai.safes)

print('make_random_move:', ai.make_random_move())
