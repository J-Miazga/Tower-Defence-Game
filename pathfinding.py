import heapq

def heuristic(a, b):
    # Manhattan distance on a square grid
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(map_obj, start, goal):
    """
    A* pathfinding algorithm restricted to path and marsh tiles
    """
    # Initialize the open set (priority queue)
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    # For each position, which position it came from
    came_from = {}
    
    # For each position, the cost of getting there from the start
    g_score = {start: 0}
    
    # For each position, the estimated total cost
    f_score = {start: heuristic(start, goal)}
    
    # Set of positions already evaluated
    closed_set = set()
    
    # Define walkable tile types
    walkable_tiles = ['path', 'start', 'finish', 'marsh']
    
    while open_set:
        # Get the position with the lowest f_score
        _,current = heapq.heappop(open_set)
        #current_f, current = heapq.heappop(open_set)
        
        # Check if we've reached the goal
        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        # Mark as evaluated
        closed_set.add(current)
        
        # Check all adjacent tiles
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Down, Right, Up, Left
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Skip if out of bounds
            if (neighbor[0] < 0 or neighbor[0] >= map_obj.width or 
                neighbor[1] < 0 or neighbor[1] >= map_obj.height):
                continue
            
            # Skip if already evaluated
            if neighbor in closed_set:
                continue
            
            # Get tile at neighbor position
            tile = map_obj.tiles[neighbor[1]][neighbor[0]]
            
            # Skip if not a walkable tile type
            if tile.tile_type not in walkable_tiles:
                continue
            
            # Calculate movement cost based on tile type
            if tile.tile_type == 'marsh':
                movement_cost = 2.0  # Marsh is slower to traverse
            else:
                movement_cost = 1.0  # Normal speed on paths
            
            # Calculate tentative g_score
            tentative_g_score = g_score.get(current, float('inf')) + movement_cost
            
            # This path is better than any previous one
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                # Record it
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                
                # Add to open set if not already there
                for i, (_, pos) in enumerate(open_set):
                    if pos == neighbor:
                        # Already in open set
                        break
                else:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    # No path found
    return []