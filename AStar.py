import time

from map import Map

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __gt__(self, other):
        return self.f > other.f
    
    def __ne__(self, other):
        return self.position != other.position
    
    def __hash__(self):
        """ Need to implement to use this class in the sets. """
        return hash(self.position)
    

class AStar:
    def __init__(self):
        """
        Implemented using: https://www.geeksforgeeks.org/a-search-algorithm/
        """
        self.neighborCombos = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]


    def solveAStar(self, map, start, goal, iterations=5000):
        startNode = Node(None, start)
        openList = [startNode]
        closedList = []
        count = 0

        while len(openList) > 0 and count < iterations:
            currentNode = min(openList)
            openList.remove(currentNode)

            for neighbor in self.neighborCombos:
                neighborPos = (currentNode.position[0] + neighbor[0], currentNode.position[1] + neighbor[1])
                if map.is_valid_position(neighborPos[0], neighborPos[1]):
                    neighborNode = Node(currentNode, neighborPos)
                    if neighborPos == goal:
                        return neighborNode
                    else:
                        neighborNode.g = currentNode.g + (sum([abs(neighbor[0]), abs(neighbor[1])]))**0.5
                        neighborNode.h = ((neighborPos[0] - goal[0]) ** 2) + ((neighborPos[1] - goal[1]) ** 2) ** 0.5
                        neighborNode.f = neighborNode.g + neighborNode.h

                        if neighborNode in closedList:
                            continue

                        if neighborNode in openList:
                            for openNode in openList:
                                if openNode == neighborNode and openNode.g < neighborNode.g:
                                    continue

                        openList.append(neighborNode)
            count += 1

            closedList.append(currentNode)

        return None

    def solvePath(self, map, start, goal):
        startTime = time.time()
        goalNode = self.solveAStar(map, start, goal)

        if goalNode is None:
            print("Astar could not find a path in 5000 iterations")
            return None, time.time() - startTime
        
        path = []
        currentNode = goalNode
        while currentNode is not None:
            path.append(currentNode.position)
            currentNode = currentNode.parent
        path = path[::-1]
        solveTime = time.time() - startTime
        return path, solveTime
                


if __name__ == "__main__":
    map = Map(100, 100)
    map.generate_random_obstacles(200)
    map.generate_random_start()
    map.generate_random_goal()

    print(f"Start: {map.start}")
    print(f"Goal: {map.goal}")

    # map.display_map()
    astar = AStar()
    path, solveTime = astar.solvePath(map, map.start, map.goal)

    if path is not None:
        print(path)
        print(f"Num Moves: {len(path)}")
    print(f"Solve Time: {solveTime} seconds")

    map.display_map(path)

    """
    A* scales much better than djikstra's. 100x100 takes around 0.15 s and 1000x1000 takes around 3.886 s. Overall much faster too.
    """