from collections import deque


def bfs_path(start, goal, is_walkable, cols, rows):
    #Breadth-First Search
    if start == goal:
        return []

    frontier = deque([start])
    came_from = {start: None}

    while frontier:
        current = frontier.popleft()
        if current == goal:
            break

        col, row = current
        neighbors = [(col + 1, row), (col - 1, row), (col, row + 1), (col, row - 1)]

        for next_cell in neighbors:
            if next_cell in came_from:
                continue

            ncol, nrow = next_cell
            if not (0 <= ncol < cols and 0 <= nrow < rows):
                continue
            if not is_walkable(ncol, nrow):
                continue

            came_from[next_cell] = current
            frontier.append(next_cell)

    if goal not in came_from:
        return []

    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path
