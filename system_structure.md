# 系统结构图 — 基于人工智能的足球战术分析系统

**图示来源：自绘结构图**

```mermaid
flowchart TD
  subgraph 数据层
    A1[公开比赛事件数据\n(StatsBomb / Kaggle)] --> A2[比赛视频\n(可选)]
  end

  subgraph 数据处理
    B1[数据清洗] --> B2[事件抽取]
    B2 --> B3[轨迹合并 & 同步时间轴]
    B3 --> B4[特征工程\n(传球链、控球区域、回合特征)]
  end

  subgraph 模型层
    C1[战术识别模型\n(可解释模型：决策树/随机森林)]
    C2[关键事件检测\n(基于事件/规则)]
    C3[（后期可选）视频动作识别模块\n(CNN / 时序模型)]
    B4 --> C1
    B4 --> C2
    A2 --> C3
  end

  subgraph 可视化层
    D1[传球网络图]
    D2[场上热力图]
    D3[事件时间轴 & 回合重放]
    C1 --> D1
    C1 --> D2
    C2 --> D3
    C3 --> D3
  end

  subgraph 展示层
    E1[Web 前端 (React / Vue)]
    E2[后端 API (Flask / FastAPI)]
    E3[文件导出：PNG / JSON / 报告]
    D1 --> E2
    D2 --> E2
    D3 --> E2
    E2 --> E1
    E2 --> E3
  end

  %% 注释区
  style A1 fill:#f9f,stroke:#333,stroke-width:1px
  style B1 fill:#ffd,stroke:#333
  style C1 fill:#dfd,stroke:#333
  style D1 fill:#cfe,stroke:#333
  style E1 fill:#ddf,stroke:#333
```
