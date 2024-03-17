import time

from map import Map

class Dijkstra:
    def __init__(self):
        """
        Implemented using the wikipedia page here:
        https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        """
        pass

    def _get_nodes(self, map):
        """
        Checks to make sure that the node is not an obstacle.
        """
        nodes = []
        for y in range(map.height):
            for x in range(map.width):
                if map.is_valid_position(x, y):
                    nodes.append((x, y))
        return nodes
    
    def _get_edges(self, map, nodes):
        """ 
        There is probably a better way to do this, but since we only have to initialize
        the edges once, it's not a big deal.
        """
        edges = {}
        for node in nodes:
            x, y = node
            edges[node] = []

            if map.is_valid_position(x-1, y):
                edges[node].append((x-1, y))
            if map.is_valid_position(x+1, y):
                edges[node].append((x+1, y))
            if map.is_valid_position(x, y-1):
                edges[node].append((x, y-1))
            if map.is_valid_position(x, y+1):
                edges[node].append((x, y+1))
            if map.is_valid_position(x-1, y-1):
                edges[node].append((x-1, y-1))
            if map.is_valid_position(x-1, y+1):
                edges[node].append((x-1, y+1))
            if map.is_valid_position(x+1, y-1):
                edges[node].append((x+1, y-1))
            if map.is_valid_position(x+1, y+1):
                edges[node].append((x+1, y+1))
        return edges
    
    def _get_initial_distances(self, map, nodes):
        """
        All distances are initialized to 0, besides the start node, which is initialized to 0.
        """
        distances = {}
        for node in nodes:
            distances[node] = float('inf')
        distances[map.start] = 0
        return distances

    def _get_path_from_solve(self, start, goal, edges, distances):
        path = [goal]
        current = goal
        while current != start:
            curr_edges = edges[current]
            min_distance = float('inf')
            for edge in curr_edges:
                if distances[edge] < min_distance:
                    min_distance = distances[edge]
                    current = edge
            path.append(current)
        return path[::-1]

    def solvePath(self, map, start, goal):
        startTime = time.time()

        nodes = self._get_nodes(map)
        edges = self._get_edges(map, nodes)
        distances = self._get_initial_distances(map, nodes)

        unvisited = set(nodes)
        current = start

        while current != goal:
            unvisited.remove(current)

            curr_edges = edges[current]
            for edge in curr_edges:
                if edge in unvisited:
                    if edge[0] != current[0] and edge[1] != current[1]: # diagonal edge
                        new_distance = distances[current] + 2**0.5
                    else: # straight edge
                        new_distance = distances[current] + 1

                    if new_distance < distances[edge]:
                        distances[edge] = new_distance

            min_distance = float('inf')
            for node in unvisited:
                if distances[node] < min_distance:
                    min_distance = distances[node]
                    current = node

        path = self._get_path_from_solve(start, goal, edges, distances)
        solveTime = time.time() - startTime

        return path, solveTime
    
if __name__ == "__main__":
    map = Map(50, 50)
    map.generate_random_obstacles(30)
    map.generate_random_start()
    map.generate_random_goal()

    dijkstra = Dijkstra()
    path, solveTime = dijkstra.solvePath(map, map.start, map.goal)
    print("Number of Steps: ", len(path))
    print("Solve Time: ", solveTime, " s")

    map.display_map(path)

    """ 
    Scales pretty poorly (solving a 50x50 map taks ~0.6 s while a 100x100 map takes ~ 13.5 s)
    """