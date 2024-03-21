import time

from map import Map

class PotentialFields:
    def __init__(self):
        """
        Implemented using algorithm found here: https://medium.com/@rymshasiddiqui/path-planning-using-potential-field-algorithm-a30ad12bdb08
        """
        pass

    
    def _calculate_attractive_force(self, position, goal, C=1):
        """
        Calculates the attractive force for the given position, as the distance to the goal
        """
        return C * ((position[0] - goal[0])**2 + (position[1] - goal[1])**2)**0.5
    
    def _calculate_repulsive_force(self, position, map, dist_to_check=2, C=1, Q=1, R=1):
        """
        Calculates the repulsive force for the given position, as the distance to the closest obstacle
        """
        force = 0
        for i in range(-dist_to_check, dist_to_check):
            for j in range(-dist_to_check, dist_to_check):
                if (i == 0 and j == 0) or (position[0]+i > map.width-1) or (position[1]+j > map.height-1) or (position[0]+i < 0) or (position[1]+j < 0) \
                    or (map.grid[position[0] + i, position[1] + j] == 0):
                    continue
                force += C * (1/((i**2 + j**2)**0.5) - 1/R) * (1/((i**2 + j**2)**0.5))

        return force

    def _calculate_potentials(self, map, goal):
        """
        Calculates the potential field for each node in the map.
        """
        potentials = {}
        for y in range(map.height):
            for x in range(map.width):
                if map.is_valid_position(x, y):
                    potentials[(x, y)] = self._calculate_attractive_force((x,y), goal) + self._calculate_repulsive_force((x,y), map)
                else:
                    potentials[(x, y)] = float('inf')
        return potentials

    def solvePath(self, map, start, goal):
        startTime = time.time()

        potentials = self._calculate_potentials(map, goal)
        path = [start]

        while path[-1] != goal:
            x, y = path[-1]
            min_potential = float('inf')
            next_node = None
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if map.is_valid_position(x+i, y+j):  #TODO need to make this work if it hits  a local minimum
                        if potentials[(x+i, y+j)] < min_potential:
                            min_potential = potentials[(x+i, y+j)]
                            next_node = (x+i, y+j)
            path.append(next_node)

        solveTime = time.time() - startTime
        return path, solveTime

if __name__ == "__main__":
    map = Map(100, 100)
    map.generate_random_obstacles(50)
    map.generate_random_start()
    map.generate_random_goal()

    map.display_map()

    pf = PotentialFields()
    path, solveTime = pf.solvePath(map, map.start, map.goal)

    print(path)
    print(solveTime)

    map.display_map(path)

    