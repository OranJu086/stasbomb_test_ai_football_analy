import json
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
import numpy as np

# -----------------------------
# 基础参数
# -----------------------------
BARCA_ID = 217
MESSI_ID = 5503

PITCH_LENGTH = 120
PITCH_WIDTH = 80

# -----------------------------
# 读取事件文件（你更换自己的文件路径）
# -----------------------------
with open("266191.json", "r", encoding="utf-8") as f:
    events = json.load(f)

# -----------------------------
# 1. 过滤：梅西参与的所有传球事件
# -----------------------------
messi_passes = [
    e for e in events
    if e.get("team", {}).get("id") == BARCA_ID
       and e.get("player", {}).get("id") == MESSI_ID
       and e.get("type", {}).get("name") == "Pass"
]

print(f"找到梅西的传球事件数量：{len(messi_passes)}")

# -----------------------------
# 2. 计算梅西传球的各个位置（平均）
# -----------------------------
messi_positions = []
teammate_positions = defaultdict(list)

for p in messi_passes:
    # 梅西的位置（传球起点）
    if p.get("location"):
        messi_positions.append(p["location"])

    # 接球者的位置（传球终点）
    recipient = p.get("pass", {}).get("recipient")
    if recipient and p.get("pass", {}).get("end_location"):
        teammate_positions[recipient["name"]].append(p["pass"]["end_location"])

# 平均位置
messi_avg = (
    np.mean([pos[0] for pos in messi_positions]),
    np.mean([pos[1] for pos in messi_positions])
)

teammate_avg = {
    player: (
        np.mean([p[0] for p in locs]),
        np.mean([p[1] for p in locs])
    )
    for player, locs in teammate_positions.items()
}

# -----------------------------
# 3. 统计梅西 → 队友 的传球次数
# -----------------------------
pass_counts = defaultdict(int)

for p in messi_passes:
    recipient = p.get("pass", {}).get("recipient", {})
    if recipient:
        pass_counts[recipient["name"]] += 1

# -----------------------------
# 4. 绘制网络图
# -----------------------------
plt.figure(figsize=(10, 7))
plt.title("Messi Pass Network (Barcelona)")

plt.xlim(0, PITCH_LENGTH)
plt.ylim(0, PITCH_WIDTH)
plt.gca().invert_yaxis()

G = nx.DiGraph()

# 节点：梅西 + 所有接球者
G.add_node("Lionel Messi", pos=messi_avg)

for player, pos in teammate_avg.items():
    G.add_node(player, pos=pos)

# 边：梅西 → 队友
for player, count in pass_counts.items():
    G.add_edge("Lionel Messi", player, weight=count)

# 位置
positions = nx.get_node_attributes(G, "pos")

# 节点大小：按触球次数（梅西自己夸张一点）
node_sizes = []
for node in G.nodes:
    if node == "Lionel Messi":
        node_sizes.append(len(messi_positions) * 20)
    else:
        node_sizes.append(pass_counts.get(node, 1) * 15)

# 边宽度
edge_widths = [G[u][v]["weight"] * 0.4 for u, v in G.edges]

# 绘图元素
nx.draw_networkx_nodes(G, positions, node_size=node_sizes, node_color="#ff7f0e", alpha=0.85)
nx.draw_networkx_edges(G, positions, width=edge_widths, alpha=0.5, arrows=False, edge_color="#1f78b4")
nx.draw_networkx_labels(G, positions, font_size=9)

plt.show()
