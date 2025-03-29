import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(map_obj, start, goal, enemy_type):
    open_set = []
    open_set_hash = set()
    heapq.heappush(open_set, (0, start))
    open_set_hash.add(start)

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    closed_set = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        open_set_hash.remove(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        closed_set.add(current)

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if (neighbor[0] < 0 or neighbor[0] >= map_obj.width or 
                neighbor[1] < 0 or neighbor[1] >= map_obj.height):
                continue

            if neighbor in closed_set:
                continue

            tile = map_obj.tiles[neighbor[1]][neighbor[0]]
            movement_cost = tile.get_movement_cost(enemy_type)

            tentative_g_score = g_score[current] + movement_cost

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    return []