import time
import random 

from map import Map

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent


class RRT:
    def __init__(self):
        """
        Implemented using algorithm found here: https://en.wikipedia.org/wiki/Rapidly_exploring_random_tree
        """
        self.tree = []

    def get_random_position(self, map, position=(-1,-1)):
        while not map.is_valid_position(position[0], position[1]) and position not in self.tree:
            position = (random.randint(0, map.width-1), random.randint(0, map.height-1))
        return position[0], position[1]
    
    def move_to_position(self, start, end, stepSize=1):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        print(dx, dy)
        dist = (dx**2 + dy**2)**0.5
        if dist < stepSize:
            return end
        else:
            dx = int(dx * stepSize / dist)
            dy = int(dy * stepSize / dist)
            return (start[0] + dx, start[1] + dy)
    
    def find_closest_node(self, position):
        """
        Finds the closest node in the tree to the given position
        """
        closestNode = None
        closestDist = float('inf')
        for node in self.tree:
            dist = ((position[0] - node[0])**2 + (position[1] - node[1])**2)**0.5
            if dist < closestDist:
                closestDist = dist
                closestNode = node
        return closestNode
    
    def calculate_path(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dist = (dx**2 + dy**2)**0.5
        return (start[0] + int(dx/dist), start[1] + int(dy/dist))

    def solvePath(self, map, start, goal, iterations=1000):
        startTime = time.time()
        self.tree.append(start)

        for i in range(iterations):
            randomPosition = self.get_random_position(map)
            closestNode = self.find_closest_node(randomPosition)
            # newPosition = self.move_to_position(closestNode, randomPosition)
            path = self.calculate_path(closestNode, randomPosition)
            if map.is_valid_position(newPosition[0], newPosition[1]):
                self.tree.append(newPosition)
                if newPosition == goal:
                    break
            print(newPosition)

        path = [goal]

        while path[-1] != start:
            path.append(self.find_closest_node(path[-1]))
        path = path[::-1]

        solveTime = time.time() - startTime
        return path, solveTime



if __name__=="__main__":
    map = Map(5, 5)
    # map.generate_random_obstacles(1)
    map.generate_random_start()
    map.generate_random_goal()

    print(f"Start: {map.start}")
    print(f"Goal: {map.goal}")

    rrt = RRT()
    path, solveTime = rrt.solvePath(map, map.start, map.goal)

    print(path)
    print(f"Num Moves: {len(path)}")
    print(f"Solve Time: {solveTime} seconds")

    map.display_map(path)