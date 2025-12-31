from pyamaze import maze, agent, COLOR
m = maze()
m.CreateMaze()

a= agent(m,2,5, footprints=True, shape='arrow')
a.position= (3,5)
print(a.x,a.y, a.position)

print(m.path)
m.run()