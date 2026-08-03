#!/usr/bin/env python3
"""
标书评价雷达图生成模板
使用 matplotlib 生成六维度雷达图
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import os
import sys
import json

# 尝试加载中文字体
def get_chinese_font():
    """自动检测可用的中文字体"""
    candidates = [
        "SimHei", "Microsoft YaHei", "WenQuanYi Micro Hei",
        "Noto Sans CJK SC", "Source Han Sans SC", "Arial Unicode MS",
        "PingFang SC", "STHeiti",
    ]
    available = set(f.name for f in FontProperties().get_fontlist() if hasattr(f, "name"))
    for font in candidates:
        if font in available:
            return font
    return None


def create_radar_chart(
    scores: dict,
    output_path: str = "radar_chart.png",
    title: str = "标书六维度评价雷达图",
):
    """
    生成六维度雷达图

    Parameters:
    scores: {维度名称: 得分} 的字典
    output_path: 输出图片路径
    title: 图表标题
    """
    categories = list(scores.keys())
    values = list(scores.values())
    N = len(categories)

    # 闭合雷达图
    values += values[:1]
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # 创建图形
    chinese_font = get_chinese_font()
    if chinese_font:
        plt.rcParams["font.family"] = chinese_font
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#1e1e1e")
    ax.set_facecolor("#1e1e1e")

    # 绘制评分区域
    ax.fill(angles, values, color="#4ecdc4", alpha=0.25)
    ax.plot(angles, values, color="#4ecdc4", linewidth=2, marker="o", markersize=8)

    # 设置刻度
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, color="white", fontsize=12, fontweight="bold")

    # 设置 y 轴
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], color="gray", fontsize=9)
    ax.set_rlabel_position(30)

    # 添加参考线
    for level in [5, 7.5]:
        ax.plot(
            np.linspace(0, 2 * np.pi, 100),
            [level] * 100,
            color="gray",
            linestyle="--",
            linewidth=0.5,
            alpha=0.5,
        )

    # 添加数值标注
    for angle, value in zip(angles[:-1], values[:-1]):
        ax.annotate(
            f"{value:.1f}",
            xy=(angle, value),
            xytext=(5, 5),
            textcoords="offset points",
            color="#4ecdc4",
            fontsize=11,
            fontweight="bold",
        )

    # 标题
    ax.set_title(title, color="white", fontsize=16, fontweight="bold", pad=25)

    # 图例
    ax.legend(
        ["本标书"],
        loc="upper right",
        bbox_to_anchor=(1.3, 1.1),
        facecolor="#2d2d2d",
        edgecolor="gray",
        labelcolor="white",
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="#1e1e1e")
    plt.close()
    print(f"雷达图已保存至: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("用法: python radar_chart_template.py <scores.json> [output_path]")
        print("scores.json 格式: {\"维度1\": 8.5, \"维度2\": 7.0, ...}")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        scores = json.load(f)

    output_path = sys.argv[2] if len(sys.argv) > 2 else "radar_chart.png"
    create_radar_chart(scores, output_path)


if __name__ == "__main__":
    main()
