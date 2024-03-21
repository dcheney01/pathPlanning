import numpy as np
import matplotlib.pyplot as plt

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)  # Initialize an empty grid
        self.start = None
        self.goal = None
        self.obstacles = []

    def set_obstacle(self, x, y, size=4):
        """Set an obstacle at the specified position."""
        if not self.is_valid_position(x, y):
            raise ValueError("Invalid obstacle position")
        self.grid[y-size:y+size, x-size:x+size] = 1
        self.obstacles.append((x, y, size))

    def set_start(self, x, y):
        """Set the starting position."""
        if self.is_valid_position(x, y):
            self.start = (x, y)
        else:
            raise ValueError("Invalid starting position")
        
    def set_goal(self, x, y):
        """Set the goal position."""
        if self.is_valid_position(x, y):
            self.goal = (x, y)
        else:
            raise ValueError("Invalid goal position")
        
    def generate_random_start(self):
        """Generate a random starting position."""
        x = np.random.randint(0, self.width)
        y = np.random.randint(0, self.height)
        while not self.is_valid_position(x, y):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
        self.start = (x, y)
        return self.start
    
    def generate_random_goal(self):
        """Generate a random goal position."""
        x = np.random.randint(0, self.width)
        y = np.random.randint(0, self.height)
        while not self.is_valid_position(x, y):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
        self.goal = (x, y)
        return self.goal
    
    def generate_random_obstacles(self, num_obstacles):
        """Generate random obstacles."""
        for _ in range(num_obstacles):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            size = np.random.randint(1, 5)
            while not self.is_valid_position(x, y):
                x = np.random.randint(0, self.width)
                y = np.random.randint(0, self.height)
            self.set_obstacle(x, y, size)
        return self.obstacles

    def is_valid_position(self, x, y):
        """Check if the position is within the map boundaries and not an obstacle."""
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y, x] == 0

    def display_map(self, path=None, return_fig=False):
        """Display the map with the obstacles, start, goal, and path."""
        fig, ax = plt.subplots()
        ax.imshow(self.grid, cmap='Greys', origin='upper')
        ax.set_xticks(np.arange(-0.5, self.width, 1))
        ax.set_yticks(np.arange(-0.5, self.height, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid()
        ax.plot(self.start[0], self.start[1], 'rs', markersize=4)
        ax.plot(self.goal[0], self.goal[1], 'bs', markersize=4)
        ax.legend(['Start', 'Goal'])
        if path is not None:
            path = np.array(path)
            ax.plot(path[:, 0], path[:, 1], 'b', linewidth=2)
        if return_fig:
            return ax
        else:
            plt.show()
            
if __name__ == "__main__":
    map_width = 100
    map_height = 100
    test_map = Map(map_width, map_height)
    
    test_map.generate_random_obstacles(10)
    test_map.generate_random_goal()
    test_map.generate_random_start()

    test_map.display_map()
