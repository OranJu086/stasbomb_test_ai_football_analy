import json
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
import numpy as np
from collections import Counter

# 打开 JSON 文件
with open("266191.json", "r", encoding="utf-8") as f:
    events = json.load(f)

barca_passes = [
    e for e in events
    if e.get("team", {}).get("id") == 217
       and e.get("type", {}).get("name") == "Pass"
]

# 球场尺寸（StatsBomb 坐标）
PITCH_LENGTH = 120
PITCH_WIDTH = 80

# -----------------------------
# 1. 计算球员平均位置
# -----------------------------
player_positions = defaultdict(list)

for p in barca_passes:
    player = p["player"]["name"]
    loc = p.get("location")
    if loc:
        player_positions[player].append(loc)

avg_pos = {
    player: (np.mean([p[0] for p in locs]),
             np.mean([p[1] for p in locs]))
    for player, locs in player_positions.items()
}

# -----------------------------
# 2. 统计球员之间的传球次数
# -----------------------------
pass_matrix = defaultdict(int)

for p in barca_passes:
    passer = p["player"]["name"]
    recipient = p["pass"].get("recipient", {}).get("name")
    if recipient:
        pass_matrix[(passer, recipient)] += 1

# -----------------------------
# 3. 画传球网络图
# -----------------------------
plt.figure(figsize=(10, 7))
plt.title("Barcelona Pass Network")

# 你可以把球场画出来，也可以省略，这里画一个简单版本
plt.xlim(0, PITCH_LENGTH)
plt.ylim(0, PITCH_WIDTH)
plt.gca().invert_yaxis()

G = nx.DiGraph()

# 节点：球员
for player, pos in avg_pos.items():
    G.add_node(player, pos=pos)

# 边：传球（权重=次数）
for (p1, p2), w in pass_matrix.items():
    if p1 in G.nodes and p2 in G.nodes:
        G.add_edge(p1, p2, weight=w)

# 位置：使用 StatsBomb 的坐标
positions = {player: (pos[0], pos[1]) for player, pos in avg_pos.items()}

# 节点大小（按触球次数）
node_sizes = [len(player_positions[p]) * 15 for p in G.nodes]

# 边宽度（按传球次数）
edge_widths = [G[u][v]["weight"] * 0.3 for u, v in G.edges]

# 画节点
nx.draw_networkx_nodes(G, positions, node_size=node_sizes, node_color="#1f78b4", alpha=0.85)

# 画边
nx.draw_networkx_edges(G, positions, width=edge_widths, alpha=0.4, arrows=False)

# 标签
nx.draw_networkx_labels(G, positions, font_size=9)

plt.show()