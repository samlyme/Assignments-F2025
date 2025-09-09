from typing import Counter


V = {"A", "B", "C", "D", "E"}
E = {("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("D", "E")}

graph = {v : [] for v in V}
for e in E:
    a, b = e
    graph[a].append(b)
    graph[b].append(a)

degrees = Counter(len(edges) for edges in graph.values())

for degree, count in degrees.items():
    print(f"{count} nodes have degree {degree}")

