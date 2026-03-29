# -*- coding: utf-8 -*-
"""Market strategy blueprints for CN/US daily market recap."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class StrategyDimension:
    """Single strategy dimension used by market recap prompts."""

    name: str
    objective: str
    checkpoints: List[str]


@dataclass(frozen=True)
class MarketStrategyBlueprint:
    """Region specific market strategy blueprint."""

    region: str
    title: str
    positioning: str
    principles: List[str]
    dimensions: List[StrategyDimension]
    action_framework: List[str]

    def to_prompt_block(self) -> str:
        """Render blueprint as prompt instructions."""
        principles_text = "\n".join([f"- {item}" for item in self.principles])
        action_text = "\n".join([f"- {item}" for item in self.action_framework])

        dims = []
        for dim in self.dimensions:
            checkpoints = "\n".join([f"  - {cp}" for cp in dim.checkpoints])
            dims.append(f"- {dim.name}: {dim.objective}\n{checkpoints}")
        dimensions_text = "\n".join(dims)

        return (
            f"## Strategy Blueprint: {self.title}\n"
            f"{self.positioning}\n\n"
            f"### Strategy Principles\n{principles_text}\n\n"
            f"### Analysis Dimensions\n{dimensions_text}\n\n"
            f"### Action Framework\n{action_text}"
        )

    def to_markdown_block(self) -> str:
        """Render blueprint as markdown section for template fallback report."""
        dims = "\n".join([f"- **{dim.name}**: {dim.objective}" for dim in self.dimensions])
        section_title = "### 六、策略框架" if self.region == "cn" else "### VI. Strategy Framework"
        return f"{section_title}\n{dims}\n"


CN_BLUEPRINT = MarketStrategyBlueprint(
    region="cn",
    title="A股市场三段式复盘策略",
    positioning="聚焦指数趋势、资金博弈与板块轮动，形成次日交易计划。",
    principles=[
        "先看指数方向，再看量能结构，最后看板块持续性。",
        "结论必须映射到仓位、节奏与风险控制动作。",
        "判断使用当日数据与近3日新闻，不臆测未验证信息。",
    ],
    dimensions=[
        StrategyDimension(
            name="趋势结构",
            objective="判断市场处于上升、震荡还是防守阶段。",
            checkpoints=["上证/深证/创业板是否同向", "放量上涨或缩量下跌是否成立", "关键支撑阻力是否被突破"],
        ),
        StrategyDimension(
            name="资金情绪",
            objective="识别短线风险偏好与情绪温度。",
            checkpoints=["涨跌家数与涨跌停结构", "成交额是否扩张", "高位股是否出现分歧"],
        ),
        StrategyDimension(
            name="主线板块",
            objective="提炼可交易主线与规避方向。",
            checkpoints=["领涨板块是否具备事件催化", "板块内部是否有龙头带动", "领跌板块是否扩散"],
        ),
    ],
    action_framework=[
        "进攻：指数共振上行 + 成交额放大 + 主线强化。",
        "均衡：指数分化或缩量震荡，控制仓位并等待确认。",
        "防守：指数转弱 + 领跌扩散，优先风控与减仓。",
    ],
)

US_BLUEPRINT = MarketStrategyBlueprint(
    region="us",
    title="US Market Regime Strategy",
    positioning="Focus on index trend, macro narrative, and sector rotation to define next-session risk posture.",
    principles=[
        "Read market regime from S&P 500, Nasdaq, and Dow alignment first.",
        "Separate beta move from theme-driven alpha rotation.",
        "Translate recap into actionable risk-on/risk-off stance with clear invalidation points.",
    ],
    dimensions=[
        StrategyDimension(
            name="Trend Regime",
            objective="Classify the market as momentum, range, or risk-off.",
            checkpoints=[
                "Are SPX/NDX/DJI directionally aligned",
                "Did volume confirm the move",
                "Are key index levels reclaimed or lost",
            ],
        ),
        StrategyDimension(
            name="Macro & Flows",
            objective="Map policy/rates narrative into equity risk appetite.",
            checkpoints=[
                "Treasury yield and USD implications",
                "Breadth and leadership concentration",
                "Defensive vs growth factor rotation",
            ],
        ),
        StrategyDimension(
            name="Sector Themes",
            objective="Identify persistent leaders and vulnerable laggards.",
            checkpoints=[
                "AI/semiconductor/software trend persistence",
                "Energy/financials sensitivity to macro data",
                "Volatility signals from VIX and large-cap earnings",
            ],
        ),
    ],
    action_framework=[
        "Risk-on: broad index breakout with expanding participation.",
        "Neutral: mixed index signals; focus on selective relative strength.",
        "Risk-off: failed breakouts and rising volatility; prioritize capital preservation.",
    ],
)


TW_BLUEPRINT = MarketStrategyBlueprint(
    region="tw",
    title="台股市場三維分析策略",
    positioning="聚焦加權指數趨勢、外資法人動向與電子供應鏈輪動，形成次日交易計畫。",
    principles=[
        "先看加權指數與外資買賣超方向，再看成交量能，最後確認電子/傳產板塊持續性。",
        "結論必須對應至倉位節奏、風控動作與匯率風險評估。",
        "判斷使用當日數據與近 3 日新聞，不臆測未經驗證資訊。",
    ],
    dimensions=[
        StrategyDimension(
            name="指數趨勢",
            objective="判斷加權指數處於上升、震盪或防守階段。",
            checkpoints=[
                "加權指數與 OTC 指數是否同向",
                "成交量是否放大配合上漲或縮量下跌",
                "關鍵支撐壓力（如月線、季線）是否突破或失守",
            ],
        ),
        StrategyDimension(
            name="外資法人動向",
            objective="掌握主力資金的風險偏好與籌碼結構。",
            checkpoints=[
                "外資單日買賣超金額與連續方向",
                "投信與自營商是否形成合力或分歧",
                "台積電（2330）外資持股比例與單日異動",
            ],
        ),
        StrategyDimension(
            name="產業輪動",
            objective="辨識可交易主線與規避弱勢方向。",
            checkpoints=[
                "半導體/IC 設計板塊是否持續領漲",
                "傳產、金融、航運等非電子板塊是否出現輪漲訊號",
                "領跌板塊是否向其他板塊擴散",
            ],
        ),
    ],
    action_framework=[
        "進攻：加權指數突破壓力 + 外資持續買超 + 電子主線強化。",
        "均衡：指數震盪或外資動向分歧，控制倉位並等待確認訊號。",
        "防守：指數跌破支撐 + 外資連續賣超，優先風控與降低持股比例。",
    ],
)


def get_market_strategy_blueprint(region: str) -> MarketStrategyBlueprint:
    """Return strategy blueprint by market region."""
    if region == "us":
        return US_BLUEPRINT
    if region == "tw":
        return TW_BLUEPRINT
    return CN_BLUEPRINT
