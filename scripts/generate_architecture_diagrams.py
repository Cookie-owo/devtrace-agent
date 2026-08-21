#!/usr/bin/env python3
"""Generate the second repository-harness architecture diagram set.

The SVG files are the editable sources. PNG files are rendered with the macOS
SVG renderer (`sips`) so both directories always describe the same 30 views.
The first overview embeds a text-free image2 visual master and overlays exact
Chinese architecture labels as vectors.
"""

from __future__ import annotations

import argparse
import base64
import html
import math
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WIDTH = 1600
HEIGHT = 1000
ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "docs" / "assets" / "svg2"
PNG_DIR = ROOT / "docs" / "assets" / "png2"
IMAGE2_SOURCE = SVG_DIR / "_sources" / "image2-harness-core.png"


@dataclass(frozen=True)
class Theme:
    name: str
    background: str
    surface: str
    surface_alt: str
    ink: str
    muted: str
    line: str
    harness: str
    spec: str
    method: str
    agent: str
    product: str
    evidence: str
    danger: str


THEMES = (
    Theme("晴空", "#F3F7FC", "#FFFFFF", "#EAF1FA", "#17324D", "#5B7088", "#B8C8DA", "#2563EB", "#E05A3F", "#7C3AED", "#0891B2", "#15803D", "#C48312", "#C33B43"),
    Theme("海盐", "#F4FAF9", "#FFFFFF", "#E5F4F1", "#153C3A", "#5A7773", "#B2D2CC", "#0F766E", "#EA6A47", "#6D5BD0", "#0284C7", "#2E8B57", "#B7791F", "#C2414B"),
    Theme("夜航", "#07182B", "#102A43", "#163A57", "#F1F5F9", "#AEC1D4", "#35546E", "#38BDF8", "#F59E0B", "#A78BFA", "#2DD4BF", "#34D399", "#FBBF24", "#FB7185"),
    Theme("米纸", "#F8F1E3", "#FFFDF8", "#EFE3CE", "#293A46", "#6D726E", "#CCBFA8", "#2F7D6D", "#C94C3B", "#7A5AA6", "#25759A", "#4E7B45", "#B7872E", "#B44743"),
    Theme("石墨", "#111827", "#1F2937", "#263548", "#F8FAFC", "#B9C4D0", "#45556C", "#60A5FA", "#FB923C", "#C084FC", "#22D3EE", "#4ADE80", "#FACC15", "#F87171"),
    Theme("青瓷", "#F1F7F5", "#FFFFFF", "#DDEDE8", "#173B36", "#607A75", "#B7CEC8", "#16766B", "#D45D45", "#7656A8", "#1678A5", "#2F855A", "#A97514", "#C33C54"),
    Theme("墨蓝", "#F5F7FB", "#FFFFFF", "#E8EDF6", "#182A47", "#607089", "#BAC6D8", "#1D4ED8", "#D3543F", "#6941C6", "#0E7490", "#207A4B", "#B06F13", "#C3364A"),
    Theme("紫雾", "#F8F6FC", "#FFFFFF", "#EEE8F8", "#35294A", "#766B84", "#CEC5DC", "#6D3FC0", "#D45C45", "#9B4D9C", "#1687A7", "#3D8354", "#B47C16", "#C14254"),
    Theme("深海", "#061C24", "#0D303A", "#12404A", "#F2FBFA", "#B7D0D0", "#35616A", "#22D3EE", "#FB923C", "#A78BFA", "#38BDF8", "#4ADE80", "#FACC15", "#FB7185"),
    Theme("暖灰", "#FAF7F2", "#FFFFFF", "#F0EAE1", "#344054", "#706B67", "#D2C8BC", "#3975B7", "#D96345", "#7659B0", "#1683A3", "#3E8054", "#B57B18", "#C3414E"),
)


@dataclass(frozen=True)
class DiagramSpec:
    index: int
    slug: str
    title: str
    subtitle: str
    layout: str
    theme: int
    data: dict[str, Any]


class Canvas:
    def __init__(self, spec: DiagramSpec) -> None:
        self.spec = spec
        self.theme = THEMES[spec.theme % len(THEMES)]
        self.parts: list[str] = []
        self._begin()

    def _begin(self) -> None:
        t = self.theme
        self.parts.extend(
            [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
                f'<title id="title">{html.escape(self.spec.title)}</title>',
                f'<desc id="desc">{html.escape(self.spec.subtitle)}。核心表达是仓库级 harness 驱动 AI 编码整个项目。</desc>',
                "<defs>",
                '<filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="4" stdDeviation="7" flood-color="#0B1830" flood-opacity="0.12"/></filter>',
                self._marker("arrow-harness", t.harness),
                self._marker("arrow-spec", t.spec),
                self._marker("arrow-agent", t.agent),
                self._marker("arrow-product", t.product),
                self._marker("arrow-evidence", t.evidence),
                '<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="currentColor" opacity="0.12"/></pattern>',
                "</defs>",
                f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{t.background}"/>',
            ]
        )
        if self.spec.index % 3 == 0:
            self.parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#dots)" color="{t.line}"/>')
        elif self.spec.index % 3 == 1:
            for x in range(40, WIDTH, 80):
                self.parts.append(f'<line x1="{x}" y1="116" x2="{x}" y2="930" stroke="{t.line}" stroke-width="1" opacity="0.12"/>')

        self.text(62, 42, f"架构图 {self.spec.index:02d} / 30", 13, 700, t.harness, "start", letter_spacing=1.2)
        self.text(800, 61, self.spec.title, 32, 700, t.ink)
        self.text(800, 92, self.spec.subtitle, 15, 400, t.muted)
        self.line(56, 112, 1544, 112, t.line, 1.5)

    @staticmethod
    def _marker(marker_id: str, color: str) -> str:
        return (
            f'<marker id="{marker_id}" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">'
            f'<path d="M0 0L10 5L0 10Z" fill="{color}"/></marker>'
        )

    def finish(self) -> str:
        t = self.theme
        self.line(56, 943, 1544, 943, t.line, 1.2)
        self.text(58, 972, "仓库级 harness：规则 + 规格 + Skills + 上下文 + 工具 + 质量门禁 + 知识回流", 13, 600, t.ink, "start")
        self.text(1542, 972, "依据当前仓库代码与 OpenSpec", 12, 400, t.muted, "end")
        self.parts.append("</svg>")
        return "\n".join(self.parts) + "\n"

    def rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        *,
        fill: str | None = None,
        stroke: str | None = None,
        stroke_width: float = 1.5,
        radius: float = 16,
        opacity: float = 1,
        dash: str | None = None,
        shadow: bool = False,
    ) -> None:
        attrs = [
            f'x="{x:g}"',
            f'y="{y:g}"',
            f'width="{width:g}"',
            f'height="{height:g}"',
            f'rx="{radius:g}"',
            f'fill="{fill or "none"}"',
            f'opacity="{opacity:g}"',
        ]
        if stroke:
            attrs.extend([f'stroke="{stroke}"', f'stroke-width="{stroke_width:g}"'])
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if shadow:
            attrs.append('filter="url(#shadow)"')
        self.parts.append(f'<rect {" ".join(attrs)}/>')

    def circle(
        self,
        cx: float,
        cy: float,
        radius: float,
        *,
        fill: str,
        stroke: str | None = None,
        stroke_width: float = 1.5,
        opacity: float = 1,
        dash: str | None = None,
        shadow: bool = False,
    ) -> None:
        attrs = [f'cx="{cx:g}"', f'cy="{cy:g}"', f'r="{radius:g}"', f'fill="{fill}"', f'opacity="{opacity:g}"']
        if stroke:
            attrs.extend([f'stroke="{stroke}"', f'stroke-width="{stroke_width:g}"'])
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if shadow:
            attrs.append('filter="url(#shadow)"')
        self.parts.append(f'<circle {" ".join(attrs)}/>')

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str,
        width: float = 2,
        *,
        dash: str | None = None,
        marker: str | None = None,
        opacity: float = 1,
    ) -> None:
        attrs = [
            f'x1="{x1:g}"', f'y1="{y1:g}"', f'x2="{x2:g}"', f'y2="{y2:g}"',
            f'stroke="{color}"', f'stroke-width="{width:g}"', f'opacity="{opacity:g}"', 'fill="none"',
        ]
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if marker:
            attrs.append(f'marker-end="url(#{marker})"')
        self.parts.append(f'<line {" ".join(attrs)}/>')

    def path(
        self,
        d: str,
        color: str,
        width: float = 2,
        *,
        fill: str = "none",
        dash: str | None = None,
        marker: str | None = None,
        opacity: float = 1,
    ) -> None:
        attrs = [f'd="{d}"', f'stroke="{color}"', f'stroke-width="{width:g}"', f'fill="{fill}"', f'opacity="{opacity:g}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if marker:
            attrs.append(f'marker-end="url(#{marker})"')
        self.parts.append(f'<path {" ".join(attrs)}/>')

    def text(
        self,
        x: float,
        y: float,
        value: str,
        size: float = 16,
        weight: int = 500,
        fill: str | None = None,
        anchor: str = "middle",
        *,
        opacity: float = 1,
        letter_spacing: float = 0,
    ) -> None:
        safe = html.escape(value)
        self.parts.append(
            f'<text x="{x:g}" y="{y:g}" text-anchor="{anchor}" '
            f'font-family="PingFang SC,Noto Sans CJK SC,Microsoft YaHei,sans-serif" '
            f'font-size="{size:g}" font-weight="{weight}" fill="{fill or self.theme.ink}" '
            f'opacity="{opacity:g}" letter-spacing="{letter_spacing:g}">{safe}</text>'
        )

    def multiline(
        self,
        x: float,
        center_y: float,
        value: str,
        size: float = 17,
        weight: int = 600,
        fill: str | None = None,
        *,
        gap: float | None = None,
        anchor: str = "middle",
    ) -> None:
        lines = value.split("\n")
        line_gap = gap or size * 1.35
        first_y = center_y - (len(lines) - 1) * line_gap / 2 + size * 0.34
        for offset, line in enumerate(lines):
            self.text(x, first_y + offset * line_gap, line, size, weight, fill, anchor)

    def accent(self, name: str) -> str:
        return getattr(self.theme, name)

    def card(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        title: str,
        subtitle: str = "",
        *,
        accent: str = "harness",
        title_size: float = 17,
        shadow: bool = False,
        dashed: bool = False,
    ) -> None:
        color = self.accent(accent)
        self.rect(x, y, width, height, fill=self.theme.surface, stroke=color, stroke_width=1.7, radius=15, shadow=shadow, dash="7 5" if dashed else None)
        self.rect(x, y, 8, height, fill=color, radius=4)
        if subtitle:
            title_lines = title.split("\n")
            title_center = y + height / 2 - 12 - max(0, len(title_lines) - 1) * 4
            self.multiline(x + width / 2 + 4, title_center, title, title_size, 650)
            self.text(x + width / 2 + 4, y + height - 18, subtitle, 12.5, 400, self.theme.muted)
        else:
            self.multiline(x + width / 2 + 4, y + height / 2, title, title_size, 650)

    def tag(self, x: float, y: float, width: float, label: str, *, accent: str = "harness") -> None:
        color = self.accent(accent)
        self.rect(x, y, width, 32, fill=color, radius=16, opacity=0.14)
        self.text(x + width / 2, y + 21, label, 12.5, 650, color)


def _node(value: str | tuple[str, str]) -> tuple[str, str]:
    if isinstance(value, tuple):
        return value
    return value, ""


def _draw_harness_bar(canvas: Canvas, items: list[str | tuple[str, str]], *, y: float = 140, height: float = 132) -> None:
    t = canvas.theme
    canvas.rect(58, y, 1484, height, fill=t.surface, stroke=t.harness, stroke_width=2.6, radius=22, shadow=True)
    canvas.rect(58, y, 270, height, fill=t.harness, radius=22)
    canvas.text(193, y + 41, "开发控制面", 13, 600, t.background)
    canvas.text(193, y + 76, "仓库级 harness", 24, 700, t.background)
    canvas.text(193, y + 104, "驱动全仓 coding", 14, 500, t.background)
    count = len(items)
    gap = 16
    left = 352
    available = 1162
    width = (available - gap * (count - 1)) / count
    for pos, item in enumerate(items):
        title, subtitle = _node(item)
        canvas.card(left + pos * (width + gap), y + 24, width, height - 48, title, subtitle, accent="harness", title_size=15)


def _draw_repository_strip(canvas: Canvas, items: list[str | tuple[str, str]], *, y: float, title: str = "整个仓库") -> None:
    t = canvas.theme
    canvas.rect(58, y, 1484, 118, fill=t.surface, stroke=t.product, stroke_width=2.2, radius=20, shadow=True)
    canvas.text(190, y + 40, title, 20, 700, t.product)
    canvas.text(190, y + 70, "同一 harness 统一修改与验证", 12.5, 400, t.muted)
    left = 360
    gap = 12
    count = len(items)
    width = (1152 - gap * (count - 1)) / count
    for pos, item in enumerate(items):
        node_title, node_subtitle = _node(item)
        canvas.card(left + pos * (width + gap), y + 25, width, 68, node_title, node_subtitle, accent="product", title_size=14.5)


def draw_hub(spec: DiagramSpec) -> str:
    c = Canvas(spec)
    t = c.theme
    hub_title, hub_subtitle = _node(spec.data["hub"])
    satellites = spec.data["satellites"]
    positions = (
        (82, 160, 310, 106), (445, 142, 310, 106), (845, 142, 310, 106), (1208, 160, 310, 106),
        (82, 690, 310, 106), (445, 708, 310, 106), (845, 708, 310, 106), (1208, 690, 310, 106),
    )
    center_x, center_y = 800, 480
    for x, y, w, h in positions[: len(satellites)]:
        target_x = x + w / 2
        target_y = y + h / 2
        c.line(center_x, center_y, target_x, target_y, t.harness, 2, dash="7 6", marker="arrow-harness", opacity=0.8)
    c.circle(center_x, center_y, 214, fill=t.surface_alt, stroke=t.harness, stroke_width=3.2, shadow=True)
    c.circle(center_x, center_y, 178, fill=t.surface, stroke=t.harness, stroke_width=1.6, dash="6 6")
    c.text(center_x, 414, "一个工程入口", 14, 600, t.muted)
    c.multiline(center_x, 476, hub_title, 28, 700, t.harness)
    c.text(center_x, 540, hub_subtitle, 15, 500, t.ink)
    c.tag(675, 568, 250, spec.data.get("tag", "可理解 · 可修改 · 可验证"), accent="agent")
    accents = ("spec", "method", "harness", "evidence", "product", "agent", "spec", "method")
    for pos, item in enumerate(satellites):
        x, y, w, h = positions[pos]
        title, subtitle = _node(item)
        c.card(x, y, w, h, title, subtitle, accent=accents[pos], shadow=True)
    c.text(800, 846, spec.data.get("outcome", "仓库 harness 把整个项目变成 AI 可持续编码的工程系统"), 18, 650, t.ink)
    return c.finish()


def draw_imagegen_hub(spec: DiagramSpec) -> str:
    """Draw the image2-assisted overview with deterministic Chinese labels."""

    if not IMAGE2_SOURCE.exists():
        raise RuntimeError(f"Missing image2 visual master: {IMAGE2_SOURCE}")

    c = Canvas(spec)
    t = c.theme
    encoded = base64.b64encode(IMAGE2_SOURCE.read_bytes()).decode("ascii")
    c.parts.append("<metadata>无字背景由 image2 生成；架构文字、边界与数据流均为可编辑 SVG 矢量层。</metadata>")
    c.parts.append(
        '<image x="54" y="126" width="1492" height="792" preserveAspectRatio="xMidYMid slice" '
        f'href="data:image/png;base64,{encoded}"/>'
    )
    c.rect(54, 126, 1492, 792, fill="#031322", opacity=0.52, radius=30)
    c.rect(54, 126, 1492, 792, stroke=t.harness, stroke_width=2.6, radius=30)

    stages = spec.data["stages"]
    stage_x = (76, 377, 678, 979, 1280)
    stage_w = 244
    accents = ("spec", "harness", "agent", "product", "evidence")
    for pos in range(len(stages) - 1):
        c.line(stage_x[pos] + stage_w, 203, stage_x[pos + 1] - 10, 203, t.harness, 2.6, marker="arrow-harness")
    for pos, (title, subtitle) in enumerate(stages):
        x = stage_x[pos]
        color = c.accent(accents[pos])
        c.rect(x, 150, stage_w, 106, fill="#071B2D", stroke=color, stroke_width=2.1, radius=18, opacity=0.94, shadow=True)
        c.rect(x, 150, 8, 106, fill=color, radius=4)
        c.text(x + stage_w / 2 + 4, 194, title, 17, 700, "#F8FAFC")
        c.text(x + stage_w / 2 + 4, 225, subtitle, 12.5, 500, "#C7D7E5")
    c.path("M1402 260V292H500V260", t.evidence, 2.2, dash="8 6", marker="arrow-evidence")
    c.text(952, 286, "验证证据回到规格与仓库记忆", 12.5, 650, t.evidence)

    center_x, center_y = 800, 466
    side_left = spec.data["left_modules"]
    side_right = spec.data["right_modules"]
    for row in range(3):
        y = 330 + row * 112
        c.line(423, y + 45, 545, center_y, t.harness, 2, dash="6 6", marker="arrow-harness", opacity=0.9)
        c.line(1055, center_y, 1177, y + 45, t.harness, 2, dash="6 6", marker="arrow-harness", opacity=0.9)
    for x, items, accent in ((88, side_left, "product"), (1177, side_right, "agent")):
        for row, (title, subtitle) in enumerate(items):
            y = 330 + row * 112
            color = c.accent(accent if row != 2 else "evidence")
            c.rect(x, y, 335, 90, fill="#071B2D", stroke=color, stroke_width=1.8, radius=16, opacity=0.92)
            c.rect(x, y, 7, 90, fill=color, radius=4)
            c.text(x + 172, y + 38, title, 16, 700, "#F8FAFC")
            c.text(x + 172, y + 66, subtitle, 12.5, 500, "#C7D7E5")

    c.circle(center_x, center_y, 178, fill="#061827", stroke=t.harness, stroke_width=3.2, opacity=0.9, shadow=True)
    c.circle(center_x, center_y, 145, fill="#0A2942", stroke=t.harness, stroke_width=1.5, opacity=0.92, dash="7 6")
    c.text(center_x, 416, "仓库级 harness", 29, 750, t.harness)
    c.text(center_x, 449, "一个入口驱动整个仓库", 14, 600, "#F8FAFC")
    tags = ("AGENTS.md", "OpenSpec", "仓库 Skills", "真实代码", "本地命令", "证据回流")
    for pos, label in enumerate(tags):
        row, col = divmod(pos, 3)
        x = 676 + col * 86
        y = 476 + row * 42
        c.rect(x, y, 78, 30, fill=t.harness, radius=15, opacity=0.2)
        c.text(x + 39, y + 20, label, 10.5, 650, "#DFFBFF")

    c.rect(76, 690, 1448, 190, fill="#061827", stroke=t.product, stroke_width=2.2, radius=22, opacity=0.94)
    c.text(800, 727, "被 harness 编码出的真实运行数据流", 19, 700, t.product)
    runtime = spec.data["runtime"]
    node_w = 178
    gap = 22
    start = 94
    for pos in range(len(runtime) - 1):
        x1 = start + pos * (node_w + gap) + node_w
        x2 = start + (pos + 1) * (node_w + gap) - 8
        c.line(x1, 792, x2, 792, t.product, 2.2, marker="arrow-product")
    for pos, label in enumerate(runtime):
        x = start + pos * (node_w + gap)
        c.rect(x, 760, node_w, 64, fill="#0A2942", stroke=t.product, stroke_width=1.6, radius=14, opacity=0.96)
        c.multiline(x + node_w / 2, 792, label, 13.5, 650, "#F8FAFC")
    c.text(800, 854, spec.data["runtime_note"], 13, 600, "#C7D7E5")
    return c.finish()


def draw_boundary(spec: DiagramSpec) -> str:
    c = Canvas(spec)
    t = c.theme
    c.rect(52, 132, 1496, 788, fill=t.surface_alt, stroke=t.harness, stroke_width=2.4, radius=26, opacity=0.94, dash="10 8")
    c.rect(76, 118, 326, 34, fill=t.background, radius=12)
    c.text(92, 141, "仓库级 harness 治理边界", 14, 700, t.harness, "start")
    _draw_harness_bar(c, spec.data["harness"], y=166, height=126)
    c.card(580, 318, 440, 84, spec.data.get("agent", "AI 编码执行器"), spec.data.get("agent_subtitle", "读取规则 · 修改全仓 · 运行验证"), accent="agent", shadow=True, title_size=22)
    columns = spec.data["columns"]
    gap = 22
    width = (1436 - gap * (len(columns) - 1)) / len(columns)
    start_x = 82
    for pos, column in enumerate(columns):
        x = start_x + pos * (width + gap)
        c.rect(x, 438, width, 340, fill=t.surface, stroke=c.accent(column.get("accent", "product")), stroke_width=2, radius=20, shadow=True)
        c.text(x + width / 2, 476, column["title"], 20, 700, c.accent(column.get("accent", "product")))
        c.text(x + width / 2, 503, column.get("subtitle", ""), 12.5, 400, t.muted)
        items = column["items"]
        item_h = 54
        for row, item in enumerate(items):
            title, subtitle = _node(item)
            c.card(x + 20, 526 + row * 66, width - 40, item_h, title, subtitle, accent=column.get("accent", "product"), title_size=14.5)
        c.line(800, 402, x + width / 2, 430, t.agent, 1.8, marker="arrow-agent", opacity=0.75)
    c.rect(142, 814, 1316, 70, fill=t.surface, stroke=t.evidence, stroke_width=2, radius=18)
    c.text(800, 842, spec.data.get("feedback", "验证证据与知识归档回流，成为下一次变更的真实上下文"), 17, 650, t.ink)
    c.text(800, 868, spec.data.get("feedback_subtitle", "本地质量门禁 · OpenSpec 主规格 · WIKI · Git 历史"), 12.5, 400, t.muted)
    c.path("M1458 849H1570V228H1544", t.evidence, 2, dash="7 6", marker="arrow-evidence")
    return c.finish()


def draw_pipeline(spec: DiagramSpec) -> str:
    c = Canvas(spec)
    t = c.theme
    _draw_harness_bar(c, spec.data["harness"], y=136, height=122)
    steps = spec.data["steps"]
    count = len(steps)
    gap = 24
    width = (1480 - gap * (count - 1)) / count
    start_x = 60
    y = 344
    for pos, item in enumerate(steps):
        x = start_x + pos * (width + gap)
        title, subtitle = _node(item)
        accent = ("spec", "spec", "method", "agent", "product", "evidence", "harness")[pos % 7]
        if pos < count - 1:
            c.line(x + width, y + 74, x + width + gap - 6, y + 74, t.harness, 2.2, marker="arrow-harness")
        c.circle(x + 28, y - 18, 23, fill=c.accent(accent), stroke=t.background, stroke_width=4)
        c.text(x + 28, y - 11, f"{pos + 1:02d}", 12, 700, t.background)
        c.card(x, y, width, 148, title, subtitle, accent=accent, title_size=16.5, shadow=True)
    c.text(800, 548, spec.data.get("bridge", "仓库级 harness 在每一步都提供规则、上下文和可执行入口"), 17, 650, t.harness)
    outputs = spec.data["outputs"]
    _draw_repository_strip(c, outputs, y=594, title=spec.data.get("output_title", "完整项目产物"))
    c.rect(185, 754, 1230, 116, fill=t.surface, stroke=t.evidence, stroke_width=2, radius=20)
    evidence = spec.data.get("evidence", ["测试", "类型检查", "构建", "OpenSpec 校验", "运行证据", "文档归档"])
    c.text(302, 787, "证据回流", 18, 700, t.evidence)
    gap = 12
    left = 430
    item_width = (940 - gap * (len(evidence) - 1)) / len(evidence)
    for pos, item in enumerate(evidence):
        c.tag(left + pos * (item_width + gap), 776, item_width, item, accent="evidence")
    c.path("M1415 812H1570V196H1544", t.evidence, 2, dash="7 6", marker="arrow-evidence")
    return c.finish()


def draw_pillars(spec: DiagramSpec) -> str:
    c = Canvas(spec)
    t = c.theme
    c.path("M90 255L240 142H1360L1510 255Z", t.harness, 3, fill=t.surface_alt)
    c.text(800, 198, "仓库级 harness", 30, 700, t.harness)
    c.text(800, 228, spec.data.get("roof", "把整个仓库变成一座可持续施工的工程"), 14, 500, t.muted)
    pillars = spec.data["pillars"]
    gap = 28
    width = (1408 - gap * (len(pillars) - 1)) / len(pillars)
    start_x = 96
    for pos, item in enumerate(pillars):
        x = start_x + pos * (width + gap)
        title, subtitle = _node(item)
        accent = ("harness", "spec", "method", "agent", "evidence")[pos % 5]
        c.rect(x, 270, width, 440, fill=t.surface, stroke=c.accent(accent), stroke_width=2.2, radius=10, shadow=True)
        c.rect(x + 18, 292, width - 36, 96, fill=t.surface_alt, stroke=c.accent(accent), stroke_width=1.5, radius=14)
        c.multiline(x + width / 2, 326, title, 18, 700, c.accent(accent))
        c.text(x + width / 2, 374, subtitle, 12, 400, t.muted)
        items = spec.data["pillar_items"][pos]
        for row, label in enumerate(items):
            c.tag(x + 22, 430 + row * 66, width - 44, label, accent=accent)
    c.rect(72, 732, 1456, 150, fill=t.surface, stroke=t.product, stroke_width=2.5, radius=18)
    c.text(800, 765, "屋内：AI 编码整个项目", 21, 700, t.product)
    modules = spec.data["modules"]
    gap = 12
    left = 104
    item_width = (1392 - gap * (len(modules) - 1)) / len(modules)
    for pos, module in enumerate(modules):
        c.card(left + pos * (item_width + gap), 790, item_width, 62, module, accent="product", title_size=14)
    c.text(800, 907, spec.data.get("foundation", "地基：Git 历史 · 代码 · 测试 · 文档 · OpenSpec 归档"), 14, 600, t.ink)
    return c.finish()


def draw_board(spec: DiagramSpec) -> str:
    c = Canvas(spec)
    t = c.theme
    c.rect(66, 132, 1468, 772, fill=t.surface_alt, stroke=t.line, stroke_width=2, radius=32)
    c.text(102, 164, spec.data.get("board_label", "仓库工程母板"), 13, 700, t.muted, "start", letter_spacing=1)
    center = (800, 490)
    modules = spec.data["modules"]
    positions = (
        (110, 202, 300, 112), (470, 170, 300, 112), (830, 170, 300, 112), (1190, 202, 300, 112),
        (110, 675, 300, 112), (470, 707, 300, 112), (830, 707, 300, 112), (1190, 675, 300, 112),
    )
    for x, y, w, h in positions[: len(modules)]:
        mx, my = x + w / 2, y + h / 2
        c.path(f"M{center[0]} {center[1]}H{mx}V{my}", t.harness, 2.2, dash="5 5", marker="arrow-harness", opacity=0.78)
    c.rect(522, 336, 556, 310, fill=t.surface, stroke=t.harness, stroke_width=3, radius=36, shadow=True)
    c.rect(552, 366, 496, 250, fill=t.surface_alt, stroke=t.harness, stroke_width=1.5, radius=28, dash="7 6")
    c.text(800, 414, spec.data.get("center_kicker", "仓库级 AI 编码内核"), 14, 600, t.muted)
    c.multiline(800, 478, spec.data.get("center", "仓库级 harness"), 30, 700, t.harness)
    c.text(800, 548, spec.data.get("center_subtitle", "读取真实仓库 · 编排工具 · 修改文件 · 运行验证"), 14, 500, t.ink)
    c.tag(654, 572, 292, spec.data.get("center_tag", "一个内核，连接整个项目"), accent="agent")
    accents = ("product", "product", "spec", "method", "agent", "evidence", "harness", "product")
    for pos, item in enumerate(modules):
        x, y, w, h = positions[pos]
        title, subtitle = _node(item)
        c.card(x, y, w, h, title, subtitle, accent=accents[pos], shadow=True)
    c.text(800, 868, spec.data.get("outcome", "OpenSpec 输入变更，验证证据沿反馈线路回到 harness"), 16.5, 650, t.ink)
    return c.finish()


def draw_dual(spec: DiagramSpec) -> str:
    c = Canvas(spec)
    t = c.theme
    c.rect(64, 138, 704, 300, fill=t.surface, stroke=t.spec, stroke_width=2.5, radius=24, shadow=True)
    c.text(416, 178, spec.data["left_title"], 23, 700, t.spec)
    c.text(416, 207, spec.data.get("left_subtitle", "规定为什么做、做什么、如何验收"), 13, 400, t.muted)
    left_items = spec.data["left_items"]
    left_w = (648 - 14 * (len(left_items) - 1)) / len(left_items)
    for pos, item in enumerate(left_items):
        c.card(92 + pos * (left_w + 14), 246, left_w, 138, *_node(item), accent="spec", title_size=15)
    c.rect(832, 138, 704, 300, fill=t.surface, stroke=t.method, stroke_width=2.5, radius=24, shadow=True, dash="8 5" if spec.data.get("method_external") else None)
    c.text(1184, 178, spec.data["right_title"], 23, 700, t.method)
    c.text(1184, 207, spec.data.get("right_subtitle", "指导如何稳定地执行工程工作"), 13, 400, t.muted)
    right_items = spec.data["right_items"]
    right_w = (648 - 14 * (len(right_items) - 1)) / len(right_items)
    for pos, item in enumerate(right_items):
        c.card(860 + pos * (right_w + 14), 246, right_w, 138, *_node(item), accent="method", title_size=15, dashed=bool(spec.data.get("method_external")))
    c.line(416, 438, 664, 516, t.spec, 2.2, marker="arrow-spec")
    c.line(1184, 438, 936, 516, t.method, 2.2, marker="arrow-harness")
    c.rect(392, 516, 816, 142, fill=t.surface_alt, stroke=t.harness, stroke_width=3, radius=26, shadow=True)
    c.text(800, 554, "仓库级 harness + AI 编码执行器", 24, 700, t.harness)
    c.text(800, 586, spec.data.get("agent", "统一读取规则、规格、当前代码与验证结果"), 14, 500, t.ink)
    c.tag(666, 608, 268, "修改真实文件 · 运行真实命令", accent="agent")
    _draw_repository_strip(c, spec.data["outputs"], y=706, title=spec.data.get("output_title", "全仓同步落地"))
    c.path("M1420 872H1570V587H1212", t.evidence, 2, dash="7 6", marker="arrow-evidence")
    c.text(800, 872, spec.data.get("outcome", "变更与证据回写 OpenSpec、WIKI 和 Git 历史"), 15.5, 650, t.evidence)
    return c.finish()


def draw_lanes(spec: DiagramSpec) -> str:
    c = Canvas(spec)
    t = c.theme
    lanes = spec.data["lanes"]
    c.rect(58, 136, 248, 744, fill=t.harness, radius=24, shadow=True)
    c.text(182, 181, "仓库级 harness", 23, 700, t.background)
    c.text(182, 211, "贯穿每条工程泳道", 13, 500, t.background)
    rail_items = spec.data.get("rail", ["AGENTS.md", "OpenSpec", "仓库 Skills", "质量门禁", "知识回流"])
    for pos, item in enumerate(rail_items):
        c.rect(84, 260 + pos * 105, 196, 64, fill=t.surface, radius=14, opacity=0.96)
        c.text(182, 299 + pos * 105, item, 15, 650, t.harness)
    lane_y = 144
    lane_h = 132
    gap = 14
    for row, lane in enumerate(lanes):
        y = lane_y + row * (lane_h + gap)
        accent = ("spec", "method", "agent", "product", "evidence")[row % 5]
        color = c.accent(accent)
        c.rect(332, y, 1208, lane_h, fill=t.surface, stroke=color, stroke_width=1.9, radius=20, shadow=True)
        c.rect(332, y, 208, lane_h, fill=color, radius=20)
        c.multiline(436, y + lane_h / 2, lane["title"], 18, 700, t.background)
        items = lane["items"]
        item_w = (948 - 12 * (len(items) - 1)) / len(items)
        for pos, item in enumerate(items):
            c.card(564 + pos * (item_w + 12), y + 28, item_w, 76, *_node(item), accent=accent, title_size=14.5)
        c.line(306, y + lane_h / 2, 326, y + lane_h / 2, t.background, 2, marker="arrow-harness")
    c.text(936, 910, spec.data.get("outcome", "任何跨层变更都由同一 harness 协调，避免前后端与规格漂移"), 15.5, 650, t.ink)
    return c.finish()


def draw_loop(spec: DiagramSpec) -> str:
    c = Canvas(spec)
    t = c.theme
    steps = spec.data["steps"]
    count = len(steps)
    selected = []
    for pos in range(count):
        angle = -math.pi / 2 + pos * 2 * math.pi / count
        selected.append((800 + 590 * math.cos(angle) - 110, 510 + 325 * math.sin(angle) - 55))
    for pos in range(count):
        x, y = selected[pos]
        nx, ny = selected[(pos + 1) % count]
        c.line(x + 110, y + 55, nx + 110, ny + 55, t.harness, 2.2, marker="arrow-harness", opacity=0.76)
    c.circle(800, 510, 224, fill=t.surface_alt, stroke=t.harness, stroke_width=3, shadow=True)
    c.circle(800, 510, 184, fill=t.surface, stroke=t.harness, stroke_width=1.5, dash="7 6")
    c.text(800, 450, "持续工程闭环", 14, 600, t.muted)
    c.multiline(800, 510, spec.data.get("center", "仓库级\nharness"), 28, 700, t.harness)
    c.text(800, 581, spec.data.get("center_subtitle", "失败回到代码，知识进入下一轮"), 13.5, 500, t.ink)
    c.tag(690, 604, 220, spec.data.get("tag", "一次变更，一个闭环"), accent="agent")
    accents = ("spec", "spec", "method", "agent", "evidence", "product", "evidence", "harness", "method", "spec")
    for pos, item in enumerate(steps):
        x, y = selected[pos]
        c.card(x, y, 220, 110, *_node(item), accent=accents[pos], title_size=15.5, shadow=True)
        c.circle(x + 22, y + 18, 17, fill=c.accent(accents[pos]))
        c.text(x + 22, y + 23, str(pos + 1), 11, 700, t.background)
    c.text(800, 910, spec.data.get("outcome", "验证、运行和用户反馈都不会散失，而会成为可追踪的仓库记忆"), 15.5, 650, t.ink)
    return c.finish()


def draw_tree(spec: DiagramSpec) -> str:
    c = Canvas(spec)
    t = c.theme
    _draw_harness_bar(c, spec.data["harness"], y=136, height=120)
    c.card(570, 304, 460, 106, spec.data.get("trunk", "AI 编码执行器"), spec.data.get("trunk_subtitle", "按仓库地图跨目录工作"), accent="agent", shadow=True, title_size=23)
    c.line(800, 256, 800, 296, t.harness, 2.5, marker="arrow-harness")
    branches = spec.data["branches"]
    gap = 20
    width = (1448 - gap * (len(branches) - 1)) / len(branches)
    start_x = 76
    c.line(800, 410, 800, 450, t.agent, 2.4)
    c.line(start_x + width / 2, 450, start_x + (len(branches) - 1) * (width + gap) + width / 2, 450, t.agent, 2.4)
    for pos, branch in enumerate(branches):
        x = start_x + pos * (width + gap)
        center = x + width / 2
        accent = ("product", "agent", "spec", "evidence")[pos % 4]
        c.line(center, 450, center, 474, t.agent, 2.1, marker="arrow-agent")
        c.rect(x, 482, width, 300, fill=t.surface, stroke=c.accent(accent), stroke_width=2, radius=20, shadow=True)
        c.text(center, 520, branch["title"], 19, 700, c.accent(accent))
        c.text(center, 545, branch.get("subtitle", ""), 12, 400, t.muted)
        for row, item in enumerate(branch["items"]):
            c.card(x + 20, 566 + row * 64, width - 40, 52, *_node(item), accent=accent, title_size=14)
    c.rect(182, 824, 1236, 62, fill=t.surface_alt, stroke=t.evidence, stroke_width=2, radius=18)
    c.text(800, 851, spec.data.get("roots", "根系：代码、规格、测试、文档和 Git 历史持续供给真实上下文"), 16, 650, t.ink)
    c.text(800, 874, spec.data.get("roots_subtitle", "每一条分支都由同一 harness 约束、实现并验收"), 12.5, 400, t.muted)
    return c.finish()


def draw_matrix(spec: DiagramSpec) -> str:
    c = Canvas(spec)
    t = c.theme
    _draw_harness_bar(c, spec.data["harness"], y=136, height=116)
    rows = spec.data["rows"]
    columns = spec.data["columns"]
    left = 306
    top = 330
    grid_w = 1234
    col_w = grid_w / len(columns)
    row_h = 86
    c.text(178, 292, spec.data.get("row_title", "harness 能力"), 15, 700, t.harness)
    for pos, column in enumerate(columns):
        x = left + pos * col_w
        c.rect(x + 4, 274, col_w - 8, 52, fill=t.surface_alt, stroke=t.product, stroke_width=1.4, radius=12)
        c.multiline(x + col_w / 2, 298, column, 13.5, 650, t.ink)
    labels = spec.data.get("cell_labels", ["约束", "驱动", "同步", "验证", "沉淀"])
    for row, row_name in enumerate(rows):
        y = top + row * row_h
        accent = ("harness", "spec", "method", "agent", "evidence")[row % 5]
        c.rect(60, y + 4, 226, row_h - 8, fill=c.accent(accent), radius=14)
        c.multiline(173, y + row_h / 2, row_name, 15, 700, t.background)
        for col in range(len(columns)):
            x = left + col * col_w
            c.rect(x + 4, y + 4, col_w - 8, row_h - 8, fill=t.surface, stroke=t.line, stroke_width=1.2, radius=12)
            label = labels[(row + col) % len(labels)]
            c.circle(x + col_w / 2, y + 32, 9, fill=c.accent(accent))
            c.text(x + col_w / 2, y + 63, label, 12, 600, t.muted)
    c.text(800, 889, spec.data.get("outcome", "矩阵中的每个交点都代表 harness 对该项目区域的真实工程作用"), 15.5, 650, t.ink)
    return c.finish()


def draw_finale(spec: DiagramSpec) -> str:
    c = Canvas(spec)
    t = c.theme
    c.rect(54, 134, 1492, 770, fill=t.surface_alt, stroke=t.harness, stroke_width=3, radius=34, shadow=True)
    c.rect(82, 164, 1436, 114, fill=t.harness, radius=26)
    c.text(800, 207, "一个仓库级 harness，就能持续 coding 整个项目", 30, 700, t.background)
    c.text(800, 245, "仓库自身携带地图、规程、验收标准、工具入口和工程记忆", 15, 500, t.background)
    stages = spec.data["stages"]
    stage_y = 344
    gap = 18
    width = (1432 - gap * (len(stages) - 1)) / len(stages)
    start_x = 84
    for pos, stage in enumerate(stages):
        x = start_x + pos * (width + gap)
        accent = ("spec", "harness", "agent", "product", "evidence")[pos % 5]
        if pos < len(stages) - 1:
            c.line(x + width, stage_y + 104, x + width + gap - 4, stage_y + 104, t.harness, 2.4, marker="arrow-harness")
        c.card(x, stage_y, width, 208, stage["title"], stage.get("subtitle", ""), accent=accent, title_size=19, shadow=True)
        for row, item in enumerate(stage.get("items", [])):
            c.tag(x + 24, stage_y + 104 + row * 38, width - 48, item, accent=accent)
    modules = spec.data["modules"]
    c.rect(90, 604, 1420, 190, fill=t.surface, stroke=t.product, stroke_width=2.3, radius=24)
    c.text(800, 640, "整个 Agent Py 都是同一套 harness 的可编码工作区", 20, 700, t.product)
    cols = 6
    item_w = 216
    gap_x = 16
    left = 124
    for pos, item in enumerate(modules):
        row, col = divmod(pos, cols)
        c.card(left + col * (item_w + gap_x), 666 + row * 62, item_w, 50, item, accent="product", title_size=13.5)
    c.rect(232, 824, 1136, 48, fill=t.evidence, radius=24, opacity=0.16)
    c.text(800, 855, spec.data.get("outcome", "证据与归档回到 harness，下一次变更从更完整的仓库记忆继续"), 15.5, 700, t.evidence)
    c.path("M1368 848H1570V221H1518", t.evidence, 2.2, dash="7 6", marker="arrow-evidence")
    return c.finish()


DRAWERS = {
    "hub": draw_hub,
    "imagegen": draw_imagegen_hub,
    "boundary": draw_boundary,
    "pipeline": draw_pipeline,
    "pillars": draw_pillars,
    "board": draw_board,
    "dual": draw_dual,
    "lanes": draw_lanes,
    "loop": draw_loop,
    "tree": draw_tree,
    "matrix": draw_matrix,
    "finale": draw_finale,
}


SPECS = (
    DiagramSpec(
        1,
        "01-image2-harness-command-center",
        "image2 总览：一个仓库级 harness，持续 coding 整个项目",
        "需求进入开发控制面，AI 改真实文件、跑真实命令，完整运行链与证据一起回流",
        "imagegen",
        8,
        {
            "stages": [
                ("需求与缺陷", "目标、范围、验收"),
                ("harness 控制面", "规则、规格、方法"),
                ("AI 编码闭环", "读、改、验、修"),
                ("整个仓库", "跨层同步落地"),
                ("验证证据", "测试、运行、归档"),
            ],
            "left_modules": [
                ("体验与契约", "Vue 3 · API / SSE"),
                ("应用与智能", "FastAPI · Chat Agent · AIOps"),
                ("工程与知识", "OpenSpec · docs · 本地门禁"),
            ],
            "right_modules": [
                ("数据与检索", "SQLite · Milvus · BM25L / RRF"),
                ("真实外部系统", "Qwen · MCP · 腾讯 CLS"),
                ("本地运行底座", "JSON 配置 · Compose · 启动脚本"),
            ],
            "runtime": ["用户", "Vue 3", "HTTP / SSE", "FastAPI", "Chat / AIOps", "Qwen / MCP", "SQLite / Milvus"],
            "runtime_note": "回答、引用和诊断证据通过 SSE 返回界面；索引与后台任务状态持久化",
        },
    ),
    DiagramSpec(
        2,
        "02-control-plane-and-runtime-plane",
        "两张网：harness 控制面覆盖真实运行面",
        "开发控制面决定怎样改仓库，产品运行面承载用户请求、模型调用、数据与证据",
        "boundary",
        6,
        {
            "harness": ["AGENTS.md 规则", "OpenSpec 规格", "Skills 方法", "真实仓库上下文", "本地质量门禁"],
            "agent": "AI 编码执行器：沿控制面改动整个运行面",
            "agent_subtitle": "分析影响 → 跨目录修改 → 执行验证 → 依据失败继续修复",
            "columns": [
                {"title": "入口与协议", "subtitle": "用户请求进入系统", "accent": "product", "items": ["Vue 3 四个工作台", "HTTP 同步请求", "SSE 流式事件", "共享错误与类型契约"]},
                {"title": "应用与智能", "subtitle": "FastAPI 组合根", "accent": "agent", "items": ["认证与用户作用域", "LangChain Chat Agent", "LangGraph AIOps", "持久后台任务"]},
                {"title": "数据与外部能力", "subtitle": "全部使用真实边界", "accent": "spec", "items": ["SQLite 业务状态", "Milvus 知识向量", "Qwen 模型", "MCP / 腾讯 CLS"]},
                {"title": "工程证据", "subtitle": "控制面持续读回", "accent": "evidence", "items": ["后端检查与测试", "前端检查与构建", "42 份主规格", "65 个归档变更"]},
            ],
            "feedback": "运行结果、测试失败、规格差异与用户反馈沿证据网回到 harness",
            "feedback_subtitle": "控制面不是运行时服务，却能持续修改、验证并记忆完整运行面",
        },
    ),
    DiagramSpec(
        3,
        "03-one-request-whole-repository",
        "一句需求如何穿透整个仓库",
        "OpenSpec 固化意图，harness 汇集规则与上下文，AI 把同一变更同步落到所有受影响目录",
        "pipeline",
        2,
        {
            "harness": ["AGENTS.md", "OpenSpec", "影响面检索", "仓库 Skills", "真实命令", "历史证据"],
            "steps": [
                ("描述需求", "功能、缺陷或反馈"),
                ("锁定规格", "目标、非目标与验收"),
                ("检索影响面", "代码、契约、配置、文档"),
                ("修改真实文件", "跨前后端与工程目录"),
                ("执行真实命令", "检查、测试、构建"),
                ("修复证据差异", "失败回到实现"),
                ("归档工程记忆", "主规格、WIKI、Git"),
            ],
            "bridge": "同一套 harness 维持需求、代码、契约、数据和验收的一致性",
            "outputs": ["Vue 前端", "FastAPI 后端", "API / SSE 契约", "Agent / AIOps", "存储与检索", "配置与 infra", "测试与文档"],
            "output_title": "一次变更，端到端覆盖整个仓库",
            "evidence": ["OpenSpec 校验", "Ruff / Pyright", "pytest", "前端类型检查", "Vitest", "Vite 构建"],
        },
    ),
    DiagramSpec(
        4,
        "04-five-control-loops",
        "仓库级 harness 的五个控制回路",
        "每个回路都向 AI 提供一种可执行约束，并把偏差送回下一次修改",
        "pillars",
        3,
        {
            "roof": "规则、规格、方法、上下文与证据共同覆盖整个单仓",
            "pillars": [
                ("边界回路", "AGENTS.md"),
                ("意图回路", "OpenSpec"),
                ("动作回路", ".codex/skills"),
                ("上下文回路", "代码 / 规格 / Git"),
                ("证据回路", "本地门禁 / 运行"),
            ],
            "pillar_items": [
                ["目录与技术栈", "配置与密钥", "权限与真实 MCP"],
                ["proposal / design", "delta specs", "tasks / 验收"],
                ["提案与实施", "验证与同步", "归档与 WIKI"],
                ["当前真实实现", "42 份主规格", "65 个归档变更"],
                ["静态检查", "测试与构建", "桌面端运行证据"],
            ],
            "modules": ["Vue 3", "FastAPI", "API 契约", "RAG", "AIOps", "MCP", "SQLite / Milvus", "文档"],
            "foundation": "五个回路不是运行时服务，而是 AI coding 整个仓库的开发控制系统",
        },
    ),
    DiagramSpec(
        5,
        "05-context-and-tool-router",
        "上下文与工具路由器：AI 为什么能看懂整个仓库",
        "harness 按任务汇集最相关的规则、规格、代码和命令，再把证据送回真实仓库",
        "board",
        4,
        {
            "board_label": "仓库级上下文与动作母板",
            "center": "仓库级 harness",
            "center_kicker": "上下文选择 + 动作编排",
            "center_subtitle": "定位影响面 · 选择 Skill · 修改文件 · 执行命令 · 收集证据",
            "center_tag": "任务不同，路由不同；全仓入口不变",
            "modules": [
                ("AGENTS.md", "全仓规则与安全边界"),
                ("OpenSpec", "目标、规格与任务"),
                ("仓库 Skills", "实施、验证、同步、归档"),
                ("代码与契约", "真实当前实现"),
                ("测试与构建", "机器可读失败证据"),
                ("运行与浏览器", "桌面体验证据"),
                ("主规格与 WIKI", "长期工程记忆"),
                ("Git 历史", "变更脉络与当前状态"),
            ],
            "outcome": "harness 不需要把全部仓库塞进一次 Prompt，也能逐层定位并 coding 整个项目",
        },
    ),
    DiagramSpec(
        6,
        "06-openspec-superpowers-gearbox",
        "OpenSpec × Superpowers：做什么与怎么做的变速箱",
        "OpenSpec 是仓库内变更制品；Superpowers 是仓库外 AI 工程方法，二者在执行前汇合",
        "dual",
        7,
        {
            "left_title": "OpenSpec：仓库内定义做什么",
            "left_subtitle": "proposal、design、delta specs、tasks 都随仓库版本化",
            "left_items": [("目标与范围", "为什么做"), ("行为规格", "必须满足什么"), ("设计约束", "如何落到本仓库"), ("任务与验收", "怎样证明完成")],
            "right_title": "Superpowers：仓库外指导怎么做",
            "right_subtitle": "虚线侧车：帮助 AI 澄清、计划、调试和核验，不是产品组件",
            "right_items": [("澄清", "理解真实问题"), ("计划", "拆成可验证步骤"), ("调试", "根据证据定位"), ("核验", "完成前逐项复查")],
            "method_external": True,
            "agent": "做什么与怎么做汇合后，AI 仍受 AGENTS.md 和当前仓库事实约束",
            "outputs": ["前端", "后端", "共享契约", "RAG", "AIOps", "MCP", "基础设施", "文档"],
            "outcome": "OpenSpec 留在仓库成为记忆；Superpowers 只辅助执行；验证证据继续回流",
        },
    ),
    DiagramSpec(
        7,
        "07-evidence-memory-flywheel",
        "证据与记忆飞轮：仓库越 coding 越可理解",
        "每次变更都把规则、规格、测试、运行和归档变成下一轮更完整的上下文",
        "loop",
        1,
        {
            "center": "仓库级\nharness",
            "center_subtitle": "失败不丢失，成功可继承",
            "tag": "一次变更，一圈新记忆",
            "steps": [
                ("接收需求", "目标与非目标"),
                ("建立 OpenSpec", "规格、设计、任务"),
                ("读取当前仓库", "代码、契约、历史"),
                ("跨层 coding", "修改真实文件"),
                ("执行本地门禁", "检查、测试、构建"),
                ("观察运行证据", "API、SSE、桌面体验"),
                ("同步与归档", "主规格、WIKI、归档变更"),
                ("更新 Git 上下文", "下一轮从真实状态继续"),
            ],
            "outcome": "harness 的价值不是一次生成更多代码，而是让整个仓库持续可理解、可修改、可验证",
        },
    ),
    DiagramSpec(
        8,
        "08-repository-cockpit",
        "一处驾驶舱，全仓联动",
        "harness 汇总仓库地图、变更状态、验证结果与工程记忆",
        "board",
        2,
        {
            "board_label": "仓库驾驶舱",
            "center": "AI 编码驾驶舱",
            "center_kicker": "仓库级 harness",
            "center_subtitle": "从同一处观察影响面、修改文件、执行门禁、处理失败",
            "center_tag": "一个目标，多个模块同步联动",
            "modules": [
                ("前端仪表", "61 个源码文件"),
                ("后端仪表", "49 个 Python 源码文件"),
                ("契约仪表", "16 个共享契约源码"),
                ("规格仪表", "42 份主规格"),
                ("后端测试", "32 个测试文件"),
                ("前端测试", "22 个测试文件"),
                ("仓库 Skills", "12 个工作流能力"),
                ("历史变更", "65 个 OpenSpec 归档"),
            ],
            "outcome": "数字不是虚构评分，而是当前仓库可被 harness 读取和利用的真实工程表面",
        },
    ),
    DiagramSpec(
        9,
        "09-harness-motherboard",
        "工程母板：harness 连接所有模块",
        "OpenSpec 是变更输入，代码模块是芯片，验证证据沿反馈线路返回",
        "board",
        5,
        {
            "board_label": "整个仓库的工程母板",
            "center": "仓库级 harness",
            "center_kicker": "中央工程主干",
            "center_subtitle": "一套规则与执行路径，驱动应用、智能、数据和基础设施",
            "center_tag": "变更输入 → 全仓编码 → 证据反馈",
            "modules": [
                ("Vue 3", "工作台与交互"),
                ("FastAPI", "API 与组合根"),
                ("LangChain", "聊天 Agent"),
                ("LangGraph", "AIOps 诊断"),
                ("SQLite", "业务与任务数据"),
                ("Milvus", "知识 chunk 向量"),
                ("MCP / CLS", "真实工具与日志"),
                ("共享契约", "HTTP / SSE / 错误码"),
            ],
            "outcome": "同一 harness 能沿工程线路修改任一芯片，并用跨层测试确认整体仍然连通",
        },
    ),
    DiagramSpec(
        10,
        "10-ai-coding-factory",
        "AI 编码工厂：需求进，完整项目出",
        "仓库级 harness 负责调度每个工位并保存全过程证据",
        "pipeline",
        9,
        {
            "harness": ["规则调度", "OpenSpec 调度", "Skills 调度", "文件操作", "命令执行", "证据收集"],
            "steps": [
                ("需求收敛", "明确目标与边界"),
                ("规格成形", "提案、规格与设计"),
                ("代码装配", "前端与后端实现"),
                ("契约同步", "HTTP / SSE / 错误码"),
                ("测试检验", "单元、组件与契约"),
                ("端上验收", "构建与真实体验"),
                ("文档归档", "主规格与 WIKI"),
            ],
            "bridge": "harness 是调度室：工位不同，工程上下文与质量标准始终一致",
            "outputs": ["Vue 工作台", "FastAPI", "Agent / AIOps", "数据层", "基础设施", "测试", "文档"],
            "output_title": "完整 Agent Py",
        },
    ),
    DiagramSpec(
        11,
        "11-change-metro-map",
        "一次变更的仓库地铁图",
        "OpenSpec 线、代码线、验证线和知识线在仓库级 harness 换乘",
        "lanes",
        3,
        {
            "rail": ["中央换乘站", "AGENTS.md", "OpenSpec", "仓库 Skills", "质量门禁"],
            "lanes": [
                {"title": "OpenSpec 线", "items": ["变更提案", "行为规格", "技术设计", "可执行任务"]},
                {"title": "代码线", "items": ["ChatView.vue", "共享 SSE 契约", "FastAPI stream API", "Chat Agent"]},
                {"title": "验证线", "items": ["Vitest", "契约测试", "pytest", "构建与端上验证"]},
                {"title": "知识线", "items": ["delta spec（差量规格）", "主规格", "WIKI 页面", "Git 历史"]},
                {"title": "运行证据线", "items": ["SSE 帧", "工具审计", "错误反馈", "用户体验"]},
            ],
            "outcome": "一次聊天改动可以穿越前端、契约、后端、测试和文档而不失控",
        },
    ),
    DiagramSpec(
        12,
        "12-change-feedback-loop",
        "读、改、验、归档：仓库变更闭环",
        "失败证据回到代码，设计偏差回到 OpenSpec，完成知识进入下一轮",
        "loop",
        0,
        {
            "center": "仓库级\nharness",
            "center_subtitle": "持续读取真实状态并校正执行",
            "tag": "一次变更，一个闭环",
            "steps": [
                ("读取仓库", "规则、代码与历史"),
                ("理解影响", "确定跨层范围"),
                ("形成计划", "对应 OpenSpec 任务"),
                ("实现代码", "修改真实文件"),
                ("运行测试", "生成机器证据"),
                ("调试修复", "根据失败定位"),
                ("完成验收", "核对规格与体验"),
                ("归档知识", "主规格、WIKI、Git"),
            ],
            "outcome": "闭环让 AI 编码不是一次性生成，而是基于证据持续收敛到可交付结果",
        },
    ),
    DiagramSpec(
        13,
        "13-harness-constraint-tree",
        "harness 约束树：规则生根，项目结果",
        "根系提供真实工程记忆，AI 编码树干把它输送到全仓每条分支",
        "tree",
        1,
        {
            "harness": ["AGENTS.md", "OpenSpec", "仓库 Skills", "代码与 Git", "验证证据"],
            "trunk": "AI 编码执行器",
            "trunk_subtitle": "读取根系，沿真实目录生长完整项目",
            "branches": [
                {"title": "体验枝", "subtitle": "用户可见结果", "items": ["Vue 工作台", "聊天与引用", "知识库", "智能诊断"]},
                {"title": "智能枝", "subtitle": "Agent 与检索", "items": ["LangChain", "LangGraph", "混合 RAG", "MCP 工具"]},
                {"title": "平台枝", "subtitle": "数据与运行", "items": ["FastAPI", "SQLite", "Milvus", "本地启动"]},
                {"title": "证据枝", "subtitle": "验收与知识", "items": ["自动化测试", "类型与代码检查", "OpenSpec 校验", "WIKI 归档"]},
            ],
            "roots": "根系：65 个历史变更、42 份主规格、测试与 Git 历史持续供给上下文",
            "roots_subtitle": "果实：规格一致、测试通过、端上可用、文档可查",
        },
    ),
    DiagramSpec(
        14,
        "14-repository-weaving-matrix",
        "仓库织机：把规则、规格和方法织成代码",
        "经线是 harness 能力，纬线是全仓区域，交点就是可执行工程作用",
        "matrix",
        3,
        {
            "harness": ["规则经线", "规格经线", "方法经线", "上下文经线", "证据经线"],
            "rows": ["AGENTS.md 规则", "OpenSpec 规格", "仓库 Skills", "真实代码上下文", "安全边界", "质量标准"],
            "columns": ["前端", "后端", "共享契约", "Agent", "RAG", "AIOps", "基础设施", "文档"],
            "cell_labels": ["约束", "驱动", "同步", "验证", "沉淀"],
            "outcome": "AI 编码执行器像梭子，在这些交点之间往返，把跨层变更织成一致项目",
        },
    ),
    DiagramSpec(
        15,
        "15-requirement-to-runtime-bridge",
        "从需求岸到运行岸",
        "OpenSpec、仓库规则、工程方法与质量证据共同承载端到端交付",
        "pillars",
        6,
        {
            "roof": "桥面：AI 编码循环把需求安全送达可运行 Agent Py",
            "pillars": [
                ("需求岸", "功能 / 缺陷 / 反馈"),
                ("OpenSpec 桥塔", "目标与验收"),
                ("harness 桥面", "全仓执行"),
                ("质量桥塔", "测试与构建"),
                ("运行岸", "完整项目"),
            ],
            "pillar_items": [
                ["明确问题", "限定范围", "收集约束"],
                ["提案", "规格与设计", "任务"],
                ["读仓库", "跨层编码", "调试收敛"],
                ["机器门禁", "端上验证", "规格核对"],
                ["可运行", "可追踪", "可继续演进"],
            ],
            "modules": ["前端", "后端", "契约", "数据", "RAG", "AIOps", "MCP", "文档"],
            "foundation": "承重索：AGENTS.md · 仓库 Skills · 真实上下文 · 验证证据 · 知识回流",
        },
    ),
    DiagramSpec(
        16,
        "16-repository-security-moat",
        "仓库安全护城河",
        "harness 把禁止事项和权限边界变成每次 AI 编码都必须遵守的全仓规则",
        "boundary",
        4,
        {
            "harness": ["不提交密钥", "前后端项目配置\n不读环境变量", "依赖注入", "真实 MCP / CLS", "user / tenant 隔离"],
            "agent": "守门的仓库级 harness",
            "agent_subtitle": "安全规则覆盖任何新增功能、任何目录和任何数据流",
            "columns": [
                {"title": "身份城堡", "subtitle": "认证与作用域", "accent": "danger", "items": ["注册 / 登录 / 登出", "随机不透明 Bearer 令牌", "密码 Argon2 哈希", "越权返回统一错误"]},
                {"title": "业务城堡", "subtitle": "用户数据边界", "accent": "product", "items": ["聊天与消息", "知识与向量", "AIOps 与证据", "MCP / 审计 / 反馈"]},
                {"title": "集成城堡", "subtitle": "真实外部能力", "accent": "agent", "items": ["Qwen 模型", "腾讯 CLS MCP", "Prometheus / Alertmanager", "失败明确可追踪"]},
                {"title": "配置城堡", "subtitle": "模板与本机配置分治", "accent": "spec", "items": ["提交 *.template.json", "忽略本机 project.json", "禁止真实凭据入库", "配置检查与就绪检查"]},
            ],
            "feedback": "harness 让 AI 能安全改完整个项目，而不是靠每次临时提醒避免事故",
            "feedback_subtitle": "新增能力必须同时带作用域实现、越权测试与配置边界",
        },
    ),
    DiagramSpec(
        17,
        "17-code-config-secret-lanes",
        "代码、配置、密钥三线分治",
        "仓库级 harness 明确哪些内容可提交、哪些由本机读取、哪些交给官方 MCP 进程",
        "lanes",
        9,
        {
            "rail": ["AGENTS.md", "配置规则", "Git 忽略", "测试约束", "安全验收"],
            "lanes": [
                {"title": "可提交代码线", "items": ["Python / Vue 源码", "OpenSpec 与文档", "基础设施配置", "测试与迁移"]},
                {"title": "可提交模板线", "items": ["project.template.json", "user.project.template.json", "无真实密钥", "字段结构可复现"]},
                {"title": "本机配置线", "items": ["project.json", "user.project.json", "Qwen 配置由后端读取", "Git 忽略"]},
                {"title": "CLS 凭据交接线", "items": ["凭据来自本机 JSON", "启动脚本读取", "注入官方 MCP 进程", "不写入应用源码"]},
                {"title": "验证阻断线", "items": ["配置检查", "就绪检查", "敏感字段脱敏", "仓库卫生测试"]},
            ],
            "outcome": "harness 在任何跨层编码中维持同一条秘密边界，阻止凭据误入 Git",
        },
    ),
    DiagramSpec(
        18,
        "18-shared-contract-zipper",
        "共享契约把前后端缝成一个仓库",
        "harness 要求 Vue 与 FastAPI 的 HTTP、SSE、错误码和测试同步演进",
        "dual",
        0,
        {
            "left_title": "Vue 3 体验侧",
            "left_subtitle": "前端真实导入 packages/api-contracts",
            "left_items": [("Vue 页面", "页面交互"), ("Pinia 状态", "状态组装"), ("API 客户端", "HTTP 请求"), ("SSE 客户端", "事件解析")],
            "right_title": "FastAPI 服务侧",
            "right_subtitle": "Pydantic 模型与共享协议保持一致",
            "right_items": [("API 路由", "入口与认证"), ("业务服务", "业务编排"), ("数据访问层", "持久化边界"), ("流式服务", "SSE 编码")],
            "agent": "harness 以共享契约为拉链，同步修改两侧并运行共同验证",
            "outputs": ["认证契约", "聊天契约", "知识契约", "MCP 契约", "后台任务", "错误码", "SSE 事件", "OpenAPI"],
            "output_title": "packages/api-contracts",
            "outcome": "共享契约、前端测试与后端测试共同防止跨层接口漂移",
        },
    ),
    DiagramSpec(
        19,
        "19-full-repository-quality-gates",
        "全仓质量门禁",
        "harness 把规格、代码、类型、测试、构建、文档与端上体验变成可执行证据链",
        "pipeline",
        1,
        {
            "harness": ["选择受影响范围", "执行真实命令", "读取失败信息", "定位根因", "修复后复验", "保存证据"],
            "steps": [
                ("OpenSpec 校验", "openspec validate --all"),
                ("共享契约检查", "类型检查 + 契约测试"),
                ("后端代码检查", "Ruff"),
                ("后端类型检查", "严格 Pyright"),
                ("后端测试", "pytest / pytest-asyncio"),
                ("前端类型与测试", "vue-tsc / Vitest"),
                ("生产构建", "Vite / VitePress"),
                ("人工端上验收", "桌面浏览器真实检查"),
            ],
            "bridge": "任何一道门禁失败，证据都回到 AI 编码循环，而不是被忽略或绕过",
            "outputs": ["规格一致", "共享契约一致", "代码整洁", "类型安全", "行为正确", "前端回归", "可构建", "体验可用"],
            "output_title": "可交付仓库",
            "evidence": ["命令输出", "测试报告", "构建产物", "浏览器证据", "OpenSpec 状态"],
        },
    ),
    DiagramSpec(
        20,
        "20-repository-test-matrix",
        "全仓测试覆盖矩阵",
        "不虚构覆盖率分数，直接展示 harness 如何让不同测试形态作用于核心能力",
        "matrix",
        6,
        {
            "harness": ["测试指南", "真实边界", "失败定位", "回归保护", "完成前验证"],
            "rows": ["认证与权限", "聊天与 SSE", "知识与 RAG", "AIOps 与 MCP", "后台任务", "配置与基础设施"],
            "columns": ["后端单元测试", "契约测试", "集成测试", "前端组件测试", "构建与端上验证"],
            "cell_labels": ["覆盖", "约束", "联调", "回归", "验收"],
            "outcome": "当前真实规模：32 个后端测试文件、22 个前端测试文件、1 个共享契约测试文件",
        },
    ),
    DiagramSpec(
        21,
        "21-runtime-under-harness",
        "运行时全景：harness 在上，项目在下",
        "开发控制面能够修改和验证产品运行面的每一层，但不会混入用户请求链路",
        "board",
        2,
        {
            "board_label": "开发控制面覆盖产品运行面",
            "center": "仓库级 harness",
            "center_kicker": "不进入运行时的工程控制层",
            "center_subtitle": "规则、OpenSpec、Skills 与质量门禁可以触达下面每个真实组件",
            "center_tag": "一套 harness，覆盖全部运行层",
            "modules": [
                ("Vue 3 / Pinia", "四个受保护工作台"),
                ("FastAPI", "HTTP / SSE / 认证"),
                ("LangChain", "流式聊天 Agent"),
                ("LangGraph", "AIOps 诊断图"),
                ("SQLite", "业务、任务、证据、审计"),
                ("Milvus", "知识 chunk 与向量"),
                ("Qwen", "聊天、Embedding、精排"),
                ("MCP / 告警", "CLS 与真实外部系统"),
            ],
            "outcome": "harness 是开发控制面；浏览器、API、Agent、存储与外部系统才是产品运行面",
        },
    ),
    DiagramSpec(
        22,
        "22-four-workspaces-one-harness",
        "四个工作台，一套 harness",
        "聊天、知识库、智能诊断与 MCP 管理共享认证、契约、反馈和工程验证",
        "lanes",
        5,
        {
            "rail": ["AGENTS.md", "共享契约", "用户隔离", "统一错误", "全仓门禁"],
            "lanes": [
                {"title": "/chat 对话", "items": [("对话页面", "ChatView"), ("状态与客户端", "chat 状态与客户端"), "SSE API", "LangChain + 工具"]},
                {"title": "/knowledge 知识", "items": [("知识页面", "KnowledgeView"), "上传与切分预览", "持久索引任务", "SQLite + Milvus"]},
                {"title": "/aiops 诊断", "items": [("诊断页面", "AiopsView"), "告警 REST + 诊断 SSE", "LangGraph", "证据链与报告"]},
                {"title": "/mcp 连接", "items": [("连接页面", "McpView"), "用户级配置", "检查与工具发现", "SSE / Streamable HTTP"]},
                {"title": "共享底座", "items": ["认证与用户作用域", "全局操作反馈", "后台任务", "项目 JSON 配置"]},
            ],
            "outcome": "页面不同、数据流不同，但都由同一仓库级 harness 端到端编码和验收",
        },
    ),
    DiagramSpec(
        23,
        "23-chat-end-to-end-coding",
        "聊天链路由 harness 端到端编码",
        "从 Vue 输入到 LangChain 工具调用，再以共享 SSE 契约逐字返回浏览器",
        "pipeline",
        8,
        {
            "harness": ["聊天规格", "SSE 契约", "权限规则", "Agent 工具边界", "测试", "端上体验"],
            "steps": [
                ("对话页面", "ChatView · 输入、记录与引用"),
                ("状态与客户端", "请求组装与流状态"),
                ("请求内直接 SSE", "认证后直接流式返回"),
                ("聊天服务", "会话、Prompt、记忆"),
                ("LangChain Agent", "自主选择工具"),
                ("Qwen 与工具", "知识 · 时间 · load_skill · MCP"),
                ("SSE 返回", "增量、引用、完成、错误"),
            ],
            "bridge": "聊天不经过持久后台任务；harness 同步修改视图、API、Agent、契约、审计和测试",
            "outputs": ["content.delta", "reasoning.delta", "tool.call", "reference.source", "complete", "error"],
            "output_title": "共享 SSE 事件与前端逐字渲染",
            "evidence": ["聊天测试", "SSE 格式测试", "工具审计", "引用展示", "浏览器体验"],
        },
    ),
    DiagramSpec(
        24,
        "24-knowledge-rag-butterfly",
        "知识库链路由 harness 端到端编码",
        "左翼负责可靠索引，右翼负责权限过滤的混合检索，中轴保持用户隔离",
        "dual",
        3,
        {
            "left_title": "索引翼：文档进入知识库",
            "left_subtitle": "上传、提取、切分、Embedding 与持久任务",
            "left_items": [("Markdown / PDF", "上传与校验"), ("切分策略", "固定 / 标题 / 段落"), ("后台任务", "租约、重试、恢复"), ("Milvus 写入", "分块、向量、权限元数据")],
            "right_title": "检索翼：知识进入回答",
            "right_subtitle": "真实混合召回与可解释精排",
            "right_items": [("向量召回", "Milvus"), ("关键词召回", "BM25L"), ("融合", "RRF · k=60"), ("精排", "Qwen rerank")],
            "agent": "harness 沿 user / tenant 权限中轴，同步编码前端、API、任务、模型、存储与测试",
            "outputs": ["上传界面", "每 2 秒 REST 轮询", "知识 Tool", "权限过滤", "引用详情", "阶段排名", "失败重试", "删除清理"],
            "output_title": "个人知识库端到端能力",
            "outcome": "Milvus 只存知识 chunk 与向量；SQLite 保存文档、任务和业务状态",
        },
    ),
    DiagramSpec(
        25,
        "25-aiops-end-to-end-loop",
        "AIOps 诊断链路由 harness 端到端编码",
        "真实告警、持久任务、LangGraph、CLS 工具、证据链与案例知识形成闭环",
        "loop",
        4,
        {
            "center": "仓库级\nharness",
            "center_subtitle": "同时覆盖 Vue、FastAPI、LangGraph、SQLite 与外部系统",
            "tag": "诊断过程可取消、可恢复、可追溯",
            "steps": [
                ("活跃告警", "Prometheus / Alertmanager"),
                ("持久任务", "SQLite 后台任务"),
                ("规划", "先检索 SOP"),
                ("执行", "调用真实 SearchLog"),
                ("腾讯 CLS", "MCP 返回日志证据"),
                ("再规划", "依据已存证据进入报告"),
                ("报告", "结论关联证据链"),
                ("案例入库", "案例文档存 SQLite · 分块写 Milvus")],
            "outcome": "AIOps SSE 回放持久事件；成功案例又回到个人知识库，为下一次诊断提供依据",
        },
    ),
    DiagramSpec(
        26,
        "26-mcp-real-tool-governance",
        "MCP 真实工具治理全链",
        "harness 让连接管理、工具发现、调用保护、审计和真实 CLS 数据保持一致",
        "pipeline",
        7,
        {
            "harness": ["真实工具规则", "用户级作用域", "连接协议", "超时与重试", "同名保护", "工具审计"],
            "steps": [
                ("用户配置连接", "创建、编辑、启停、删除"),
                ("连接检查", "SSE / Streamable HTTP"),
                ("工具发现", "展示真实工具列表"),
                ("聊天与 AIOps", "共享当前用户连接"),
                ("调用治理", "超时、重试、同名保护"),
                ("审计记录", "参数、摘要、耗时、状态"),
                ("腾讯 CLS", "真实日志 · 当前调用 SearchLog"),
            ],
            "bridge": "红线规则：只使用真实工具和真实数据，不生成虚假日志或不受支持的结论",
            "outputs": ["MCP 页面", "连接数据层", "本地 MCP 客户端", "聊天工具", "AIOps SearchLog", "审计生命周期"],
            "output_title": "从配置到证据的真实工具链",
            "evidence": ["连接结果", "工具列表", "调用状态", "错误信息", "审计记录"],
        },
    ),
    DiagramSpec(
        27,
        "27-durable-job-relay",
        "持久后台任务的接力系统",
        "harness 把 API、SQLite、后台执行器、重试、恢复、SSE 与前端状态编码成一个整体",
        "pipeline",
        2,
        {
            "harness": ["任务规格", "状态契约", "数据访问边界", "并发与租约", "故障语义", "全链测试"],
            "steps": [
                ("API 入队", "文档索引或 AIOps"),
                ("SQLite 持久化", "任务、事件、尝试、租约"),
                ("后台执行器领取", "并发与租约竞争"),
                ("心跳续租", "避免任务被误抢"),
                ("执行工作", "索引或诊断"),
                ("失败控制", "退避重试、超时、取消"),
                ("结果回到界面", "AIOps：SSE · 索引：REST 轮询"),
            ],
            "bridge": "AIOps 与索引任务可重启接续；聊天是请求内直接 SSE，不进入持久后台任务",
            "outputs": ["排队", "执行中", "成功", "失败", "取消", "重试", "恢复"],
            "output_title": "可持久、可恢复的后台执行",
            "evidence": ["租约测试", "重试测试", "取消测试", "事件顺序", "前端状态"],
        },
    ),
    DiagramSpec(
        28,
        "28-user-tenant-isolation",
        "user 与 tenant 隔离贯穿全仓",
        "身份作用域从 API 进入数据访问层、SQLite 与 Milvus，并覆盖所有业务能力",
        "boundary",
        5,
        {
            "harness": ["认证规格", "权限边界", "数据访问约定", "向量过滤", "越权测试"],
            "agent": "harness 强制每个新功能携带权限作用域",
            "agent_subtitle": "实现、契约、数据模型与测试必须同时体现当前用户边界",
            "columns": [
                {"title": "身份入口", "subtitle": "随机 token 与当前用户", "accent": "danger", "items": ["注册 / 登录 / 登出", "浏览器保存原始 Bearer token", "服务端会话只存 token 哈希", "统一未认证错误"]},
                {"title": "业务作用域", "subtitle": "所有记录按 owner 查询", "accent": "product", "items": ["聊天 / 消息 / Prompt / Skill", "知识 / 文档 / 索引任务", "AIOps / 证据 / 报告", "MCP / 审计 / 反馈"]},
                {"title": "数据作用域", "subtitle": "SQLite 与 Milvus 分工", "accent": "agent", "items": ["数据访问加 owner 条件", "Milvus 元数据带 user / tenant", "检索表达式权限过滤", "删除与覆盖同样受控"]},
                {"title": "验证作用域", "subtitle": "跨用户访问必须失败", "accent": "evidence", "items": ["认证 API 测试", "数据访问测试", "向量过滤测试", "工具与诊断权限测试"]},
            ],
            "feedback": "权限不是某个中间件的孤立功能，而是 harness 要求全仓持续满足的工程属性",
            "feedback_subtitle": "任何新增模块都必须同时实现 owner scope 与越权回归测试",
        },
    ),
    DiagramSpec(
        29,
        "29-local-first-topology",
        "本地优先开发拓扑",
        "仓库入口编排本机应用、Docker Compose 基础设施、本地配置与真实外部服务",
        "boundary",
        9,
        {
            "harness": ["start-local.sh / .bat", "本地 JSON 配置", "Alembic 迁移", "进程日志", "就绪与配置检查"],
            "agent": "仓库级 harness 让整个项目可在本机复现",
            "agent_subtitle": "准备依赖、启动基础设施、迁移数据、运行 MCP、后端与前端",
            "columns": [
                {"title": "本机应用", "subtitle": "不进入 Docker Compose", "accent": "product", "items": ["Vue :5173", "FastAPI :8000", "CLS MCP :3000", "SQLite 本地文件"]},
                {"title": "Compose 基础设施", "subtitle": "仅托管五个服务", "accent": "agent", "items": ["Milvus :19530", "etcd", "MinIO", "Attu :8001 / Alertmanager :9093"]},
                {"title": "外部真实服务", "subtitle": "通过项目配置连接", "accent": "spec", "items": ["Qwen / 百炼", "腾讯云 CLS", "可配置 Prometheus", "其他用户级 MCP 服务"]},
                {"title": "工程验证", "subtitle": "启动不是黑盒", "accent": "evidence", "items": ["/health", "/ready", "/config/check", "/metrics 与结构化日志"]},
            ],
            "feedback": "仓库本身携带启动、迁移、配置、基础设施与验证路径",
            "feedback_subtitle": "因此 AI 可以从一个 harness 入口 coding 并复现整个项目",
        },
    ),
    DiagramSpec(
        30,
        "30-one-harness-whole-project",
        "一张图看懂 harness 如何持续完成整个项目",
        "需求进入仓库控制面，AI 跨层编码，完整 Agent Py 交付，证据再回到下一轮",
        "finale",
        8,
        {
            "stages": [
                {"title": "需求", "subtitle": "功能、缺陷、反馈", "items": ["目标与范围", "约束与验收"]},
                {"title": "harness 控制面", "subtitle": "仓库自己的工程系统", "items": ["AGENTS.md", "OpenSpec + Skills"]},
                {"title": "AI 编码闭环", "subtitle": "读、改、验、修", "items": ["真实文件与命令", "跨层同步实现"]},
                {"title": "整个项目", "subtitle": "运行面与工程面", "items": ["应用 + 智能 + 数据", "配置 + 基础设施"]},
                {"title": "证据回流", "subtitle": "让下一次更可靠", "items": ["测试与运行证据", "主规格 + WIKI + Git"]},
            ],
            "modules": [
                "Vue 3 前端", "FastAPI 后端", "共享 API / SSE 契约", "聊天 Agent", "AIOps", "混合 RAG",
                "MCP / CLS", "SQLite / Milvus", "本地 JSON 配置", "Compose 基础设施", "全仓测试", "OpenSpec / 文档",
            ],
            "outcome": "仓库 harness 把整个仓库变成 AI 可理解、可修改、可验证、可持续记忆的工程系统",
        },
    ),
)


def validate_specs() -> None:
    if len(SPECS) != 30:
        raise RuntimeError(f"Expected 30 diagrams, found {len(SPECS)}")
    indices = [spec.index for spec in SPECS]
    if indices != list(range(1, 31)):
        raise RuntimeError(f"Diagram indices must be 1..30, found {indices}")
    slugs = [spec.slug for spec in SPECS]
    if len(slugs) != len(set(slugs)):
        raise RuntimeError("Diagram slugs must be unique")
    unknown = sorted({spec.layout for spec in SPECS} - DRAWERS.keys())
    if unknown:
        raise RuntimeError(f"Unknown layout(s): {unknown}")


def generate_svgs() -> list[Path]:
    validate_specs()
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for spec in SPECS:
        svg = DRAWERS[spec.layout](spec)
        path = SVG_DIR / f"{spec.slug}.svg"
        path.write_text(svg, encoding="utf-8")
        paths.append(path)
    return paths


def render_pngs(svg_paths: list[Path]) -> list[Path]:
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for svg_path in svg_paths:
        png_path = PNG_DIR / f"{svg_path.stem}.png"
        subprocess.run(
            ["sips", "-s", "format", "png", str(svg_path), "--out", str(png_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        paths.append(png_path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--svg-only", action="store_true", help="Generate SVG sources without rendering PNG files")
    args = parser.parse_args()
    svg_paths = generate_svgs()
    png_paths = [] if args.svg_only else render_pngs(svg_paths)
    print(f"generated {len(svg_paths)} SVG files in {SVG_DIR}")
    if not args.svg_only:
        print(f"rendered {len(png_paths)} PNG files in {PNG_DIR}")


if __name__ == "__main__":
    main()
