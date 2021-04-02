import random
from tkinter import Canvas
from collections import deque


# create an empty 2D array of cells with specified dimensions
def createEmptyMaze(rows, cols):
    maze = []

    for r in range(rows):
        maze_row = []


        for c in range(cols):
            maze_row.append(Cell(r, c))

        maze.append(maze_row)

    return maze


class MazeGenerator(Canvas):
    north = 0
    south = 1
    east = 2
    west = 3

    def __init__(self, master):
        super().__init__(master=master, bg="black")

        # graphic variables
        self._start_x = 0
        self._start_y = 0
        self._maze_width = 0
        self._maze_height = 0
        self._cell_size = 0

    # update all variables used in rendering the maze
    def updateGraphicVars(self, rows, cols):
        self._cell_size = min(self.winfo_width() / cols, self.winfo_height() / rows)
        self._maze_width = self._cell_size * cols
        self._maze_height = self._cell_size * rows
        self._start_x = (self.winfo_width() - self._maze_width) / 2
        self._start_y = (self.winfo_height() - self._maze_height) / 2

    # create a randomly generated maze with specified dimensions from any starting point within the maze
    def generateMaze(self, wall_color, pointer_color, rows, cols, start_row=0, start_col=0):
        self.updateGraphicVars(rows, cols)

        # maze creation variables
        maze = createEmptyMaze(rows, cols)
        cell_stack = deque()
        curr_cell = maze[start_row][start_col]
        curr_cell.setVisited(True)
        visited_cell_count = 1

        # continue generating the maze while cells haven't been visited
        while visited_cell_count < rows * cols:
            # update graphics
            self.update()
            self.delete("all")
            self.drawMaze(maze, wall_color=wall_color)
            self.fillCell(curr_cell.getPos(), color=pointer_color)

            neighbors_and_indices = self.getUnvisitedNeighbors(maze, curr_cell.getPos())
            neighbor_cells = neighbors_and_indices[0]
            neighbor_indices = neighbors_and_indices[1]

            if len(neighbor_indices) > 0:
                # add the current cell to the stack
                cell_stack.append(curr_cell)

                # choose a random neighbor to set as the current cell
                direction = neighbor_indices[random.randrange(0, len(neighbor_indices))]
                curr_cell = neighbor_cells[direction]

                # update maze
                self.removeWalls(cell_stack[-1], curr_cell, direction)
                curr_cell.setVisited(True)
                visited_cell_count += 1
            else:
                # backtrack if there are no available cells
                curr_cell = cell_stack.pop()

    # update the list of neighbors of the current cell
    def getUnvisitedNeighbors(self, maze, curr_pos):
        neighbor_cells = [None] * 4
        neighbor_indices = []

        # check for north neighbor
        if curr_pos[0] > 0:
            north_neighbor = maze[curr_pos[0] - 1][curr_pos[1]]

            if not north_neighbor.isVisited():
                neighbor_cells[MazeGenerator.north] = north_neighbor
                neighbor_indices.append(MazeGenerator.north)

        # check for south neighbor
        if curr_pos[0] < len(maze) - 1:
            south_neighbor = maze[curr_pos[0] + 1][curr_pos[1]]

            if not south_neighbor.isVisited():
                neighbor_cells[MazeGenerator.south] = south_neighbor
                neighbor_indices.append(MazeGenerator.south)

        # check for east neighbor
        if curr_pos[1] < len(maze[0]) - 1:
            east_neighbor = maze[curr_pos[0]][curr_pos[1] + 1]

            if not east_neighbor.isVisited():
                neighbor_cells[MazeGenerator.east] = east_neighbor
                neighbor_indices.append(MazeGenerator.east)

        # check for west neighbor
        if curr_pos[1] > 0:
            west_neighbor = maze[curr_pos[0]][curr_pos[1] - 1]

            if not west_neighbor.isVisited():
                neighbor_cells[MazeGenerator.west] = west_neighbor
                neighbor_indices.append(MazeGenerator.west)

        return neighbor_cells, neighbor_indices

    # remove wall from appropriate cell based on direction moved
    def removeWalls(self, prev_cell, curr_cell, direction):
        if direction == MazeGenerator.north:
            curr_cell.setSouthWall(False)
        elif direction == MazeGenerator.south:
            prev_cell.setSouthWall(False)
        elif direction == MazeGenerator.east:
            prev_cell.setEastWall(False)
        elif direction == MazeGenerator.west:
            curr_cell.setEastWall(False)

    # draw the walls around a cell
    def drawWalls(self, cell, color):
        cell_pos = cell.getPos()
        cell_x = self._start_x + (cell_pos[1] * self._cell_size)
        cell_y = self._start_y + (cell_pos[0] * self._cell_size)

        if cell.hasSouthWall():
            self.create_line(cell_x, cell_y + self._cell_size,
                             cell_x + self._cell_size, cell_y + self._cell_size, fill=color)

        if cell.hasEastWall():
            self.create_line(cell_x + self._cell_size,
                             cell_y, cell_x + self._cell_size, cell_y + self._cell_size, fill=color)

    def fillCell(self, cell_pos, color):
        cell_x = self._start_x + (cell_pos[1] * self._cell_size)
        cell_y = self._start_y + (cell_pos[0] * self._cell_size)

        self.create_rectangle(cell_x, cell_y, cell_x + self._cell_size, cell_y + self._cell_size, fill=color)

    def drawMaze(self, maze, wall_color):
        # draw north and west walls
        self.create_line(self._start_x, self._start_y, self._maze_width, self._start_y, fill=wall_color)
        self.create_line(self._start_x, self._start_y, self._start_x, self._maze_height, fill=wall_color)

        for row in range(len(maze)):
            for col in range(len(maze[0])):
                cell = maze[row][col]

                if cell.hasSouthWall() or cell.hasEastWall():
                    self.drawWalls(cell, color=wall_color)


class Cell:

    def __init__(self, row, col):
        self._pos = (row, col)
        self._visited = False
        self._south_wall = True
        self._east_wall = True

    # Setters

    def setVisited(self, visited):
        self._visited = visited

    def setSouthWall(self, south_wall):
        self._south_wall = south_wall

    def setEastWall(self, east_wall):
        self._east_wall = east_wall

    # Getters

    def getPos(self):
        return self._pos

    def isVisited(self):
        return self._visited

    def hasSouthWall(self):
        return self._south_wall

    def hasEastWall(self):
        return self._east_wall

    def __str__(self):
        return self._pos
