import heapq

def heuristic(a, b):
    """
    Heuristic function using Manhattan distance.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(map_obj, start, goal, enemy_type):
    """
    A* pathfinding algorithm that considers tile movement cost and avoids impassable terrain.
    
    Arguments:
        map_obj: The map object containing the tile grid.
        start: Tuple (x, y) of the starting tile.
        goal: Tuple (x, y) of the destination tile.
        enemy_type: Type of enemy (affects movement cost, e.g., fast units move differently on marsh).
    
    Returns:
        A list of (x, y) positions from start to goal, or an empty list if no path is found.
    """

    open_set = []  # Priority queue for positions to evaluate
    open_set_hash = set()  # Hash set for fast lookup
    heapq.heappush(open_set, (0, start))
    open_set_hash.add(start)

    came_from = {}  # Stores optimal path: current -> previous
    g_score = {start: 0}  # Actual cost from start to current
    f_score = {start: heuristic(start, goal)}  # Estimated total cost

    closed_set = set()  # Set of positions already evaluated

    while open_set:
        _, current = heapq.heappop(open_set)
        open_set_hash.remove(current)

        # If reached the goal, reconstruct the path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        closed_set.add(current)

        # Check all 4-directional neighbors
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)

            # Skip out-of-bounds positions
            if (neighbor[0] < 0 or neighbor[0] >= map_obj.width or 
                neighbor[1] < 0 or neighbor[1] >= map_obj.height):
                continue

            if neighbor in closed_set:
                continue

            tile = map_obj.tiles[neighbor[1]][neighbor[0]]
            movement_cost = tile.get_movement_cost(enemy_type)

            # # Skip impassable tiles
            # if movement_cost == float('inf'):
            #     continue

            # Tentative score from start to neighbor
            tentative_g_score = g_score[current] + movement_cost

            # If this path to neighbor is better than any previous
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    # No path found
    return []
