# 文件名: generate_system_structure.py
from graphviz import Digraph

def build_graph(output_basename='system_structure', fmt='png'):
    dot = Digraph('SystemStructure', format=fmt)
    dot.attr(rankdir='TB')
    dot.attr(bgcolor='white')
    dot.attr('node', shape='rect', style='filled', fontname='Helvetica', fontsize='10', color='#333333')

    # 数据层
    dot.node('A1', '公开比赛事件数据\n(StatsBomb / Kaggle)', fillcolor='#ff99ff')
    dot.node('A2', '比赛视频\n(可选)', fillcolor='#ff99ff')

    # 数据处理
    dot.node('B1', '数据清洗', fillcolor='#ffffdd')
    dot.node('B2', '事件抽取', fillcolor='#ffffdd')
    dot.node('B3', '轨迹合并 & 同步时间轴', fillcolor='#ffffdd')
    dot.node('B4', '特征工程\n(传球链、控球区域、回合特征)', fillcolor='#ffffdd')

    # 模型层
    dot.node('C1', '战术识别模型\n(决策树 / 随机森林)', fillcolor='#ddffdd')
    dot.node('C2', '关键事件检测\n(基于事件/规则)', fillcolor='#ddffdd')
    dot.node('C3', '视频动作识别模块\n(可选)', fillcolor='#ddffdd')

    # 可视化
    dot.node('D1', '传球网络图', fillcolor='#ccffec')
    dot.node('D2', '场上热力图', fillcolor='#ccffec')
    dot.node('D3', '事件时间轴 & 回合重放', fillcolor='#ccffec')

    # 展示层
    dot.node('E1', 'Web 前端\n(React / Vue)', fillcolor='#ddddff')
    dot.node('E2', '后端 API\n(Flask / FastAPI)', fillcolor='#ddddff')
    dot.node('E3', '文件导出：PNG / JSON / 报告', fillcolor='#ddddff')

    # Edges
    dot.edges([('A1','B1'), ('B1','B2'), ('B2','B3'), ('B3','B4')])
    dot.edge('B4','C1')
    dot.edge('B4','C2')
    dot.edge('A2','C3')
    dot.edge('C1','D1')
    dot.edge('C1','D2')
    dot.edge('C2','D3')
    dot.edge('C3','D3')
    dot.edge('D1','E2')
    dot.edge('D2','E2')
    dot.edge('D3','E2')
    dot.edge('E2','E1')
    dot.edge('E2','E3')

    outpath = dot.render(filename=output_basename, cleanup=True)
    print(f'生成完成: {outpath}')

if __name__ == '__main__':
    # 生成 PNG
    build_graph(fmt='png')
    # 也生成 SVG（可选）
    build_graph(fmt='svg')
