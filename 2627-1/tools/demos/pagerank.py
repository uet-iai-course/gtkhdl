import networkx as nx

G = nx.DiGraph()

G.add_edges_from([
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("C", "A"),
    ("D", "C"),
    ("D", "A"),
    ("E", "C")
])

scores = nx.pagerank(G, alpha=0.85)

for node, score in sorted(
    scores.items(),
    key=lambda item: item[1],
    reverse=True
):
    print(node, round(score, 4))
