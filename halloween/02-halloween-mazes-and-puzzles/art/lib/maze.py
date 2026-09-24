"""Guaranteed-single-solution maze generator + bold-wall SVG renderer.

Algorithm:
  1. Carve a perfect maze (spanning tree -> exactly one path between any two
     cells) with a randomized DFS backtracker.
  2. The unique path between chosen start/end cells is the tree path.
  3. Trim every side-branch off that path to a short stub (dead end) and keep
     only `num_dead_ends` of them; delete the rest entirely. This gives exact,
     designer-controlled difficulty while keeping the single-solution guarantee.
  4. Render as a grid of bold wall segments (thick strokes) with a generous
     open corridor between them -- the standard, kid-legible maze style.
"""
import random


class Maze:
    def __init__(self, rows, cols, seed, start, end, num_dead_ends=0, dead_end_depth=2):
        self.rows, self.cols = rows, cols
        self.start, self.end = start, end
        random.seed(seed)
        self.passages = self._carve()
        self.path = self._solution_path()
        self._trim(num_dead_ends, dead_end_depth)

    def _neighbors(self, r, c):
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                yield nr, nc

    def _carve(self):
        visited = {(r, c): False for r in range(self.rows) for c in range(self.cols)}
        passages = set()
        stack = [self.start]
        visited[self.start] = True
        while stack:
            r, c = stack[-1]
            nbrs = [n for n in self._neighbors(r, c) if not visited[n]]
            if nbrs:
                nxt = random.choice(nbrs)
                passages.add(frozenset([(r, c), nxt]))
                visited[nxt] = True
                stack.append(nxt)
            else:
                stack.pop()
        return passages

    def _graph_neighbors(self, cell, passages=None):
        passages = passages if passages is not None else self.passages
        for n in self._neighbors(*cell):
            if frozenset([cell, n]) in passages:
                yield n

    def _solution_path(self):
        # BFS from start to end over the spanning tree -> unique path.
        prev = {self.start: None}
        queue = [self.start]
        while queue:
            cur = queue.pop(0)
            if cur == self.end:
                break
            for n in self._graph_neighbors(cur):
                if n not in prev:
                    prev[n] = cur
                    queue.append(n)
        path = []
        cur = self.end
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path

    def _trim(self, num_dead_ends, depth):
        path_set = set(self.path)
        # branch roots: passages from a path-cell to a non-path-cell
        branch_edges = []
        for cell in self.path:
            for n in self._graph_neighbors(cell):
                if n not in path_set:
                    branch_edges.append((cell, n))
        random.shuffle(branch_edges)
        keep_roots = branch_edges[:num_dead_ends]
        drop_roots = branch_edges[num_dead_ends:]

        keep_cells = set(path_set)
        keep_passages = set(frozenset(p) for p in [(self.path[i], self.path[i + 1])
                                                     for i in range(len(self.path) - 1)])

        for root_cell, first in keep_roots:
            # BFS out to `depth` cells from first, staying off the solution path
            keep_passages.add(frozenset([root_cell, first]))
            keep_cells.add(first)
            frontier = [(first, 1)]
            seen = {first}
            while frontier:
                cell, d = frontier.pop(0)
                if d >= depth:
                    continue
                for n in self._graph_neighbors(cell):
                    if n in path_set or n in seen:
                        continue
                    seen.add(n)
                    keep_cells.add(n)
                    keep_passages.add(frozenset([cell, n]))
                    frontier.append((n, d + 1))

        # drop_roots: simply never add their edge/subtree -> excluded from maze.
        self.active_cells = keep_cells
        self.passages = keep_passages

    def wall(self, a, b):
        """True if there should be a wall drawn between adjacent cells a,b."""
        if a not in self.active_cells or b not in self.active_cells:
            return True
        return frozenset([a, b]) not in self.passages


def render_maze_svg(maze, x0, y0, size, wall_w=7, open_edges=()):
    """Render maze walls into an SVG string, cell grid spanning `size` units.

    open_edges: iterable of (r, c, side) where side in {'top','bottom','left','right'}
    -- the outer-boundary wall segment on that side of that cell is skipped,
    creating the entrance/exit gap for the start arrow / goal marker.
    """
    rows, cols = maze.rows, maze.cols
    cell = size / max(rows, cols)
    open_set = set(open_edges)
    lines = []

    def cx0(c):
        return x0 + c * cell

    def cy0(r):
        return y0 + r * cell

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in maze.active_cells:
                continue
            x, y = cx0(c), cy0(r)
            if (r == 0 or maze.wall((r, c), (r - 1, c))) and (r, c, 'top') not in open_set:
                lines.append((x, y, x + cell, y))
            if (c == 0 or maze.wall((r, c), (r, c - 1))) and (r, c, 'left') not in open_set:
                lines.append((x, y, x, y + cell))
            if (r == rows - 1 or (r + 1, c) not in maze.active_cells) and (r, c, 'bottom') not in open_set:
                lines.append((x, y + cell, x + cell, y + cell))
            if (c == cols - 1 or (r, c + 1) not in maze.active_cells) and (r, c, 'right') not in open_set:
                lines.append((x + cell, y, x + cell, y + cell))
            if c + 1 < cols and (r, c + 1) in maze.active_cells and maze.wall((r, c), (r, c + 1)):
                lines.append((x + cell, y, x + cell, y + cell))
            if r + 1 < rows and (r + 1, c) in maze.active_cells and maze.wall((r, c), (r + 1, c)):
                lines.append((x, y + cell, x + cell, y + cell))

    seen = set()
    out = []
    for (x1, y1, x2, y2) in lines:
        key = (round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1))
        if key in seen:
            continue
        seen.add(key)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                   f'stroke="#000" stroke-width="{wall_w}" stroke-linecap="round"/>')

    return "\n".join(out), cell


def cell_center(x0, y0, size, rows, cols, cell_rc):
    cell = size / max(rows, cols)
    r, c = cell_rc
    return x0 + c * cell + cell / 2, y0 + r * cell + cell / 2


def render_solution_svg(maze, x0, y0, size, stroke_w=3.5, color="#e0392b"):
    """Dashed centerline through the solution path -- used in the answer key."""
    pts = [cell_center(x0, y0, size, maze.rows, maze.cols, rc) for rc in maze.path]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{stroke_w}" '
            f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="10 8"/>')
