#!/usr/bin/env python3
"""
标书评价加权评分计算与等级判定脚本
"""

import json
import sys
from typing import Dict, Optional


# 维度权重配置
DIMENSION_WEIGHTS = {
    "科学设计合理性": 0.25,
    "统计学方法适用性": 0.20,
    "创新性与转化潜力": 0.20,
    "预算编制合理性": 0.15,
    "时间安排可行性": 0.10,
    "撰写规范性": 0.10,
}

# 等级划分阈值
GRADE_THRESHOLDS = [
    (9.0, "优秀", "可直接提交"),
    (7.5, "良好", "小幅修改后可提交"),
    (6.0, "中等", "需实质性修改"),
    (4.0, "较差", "需大幅重写"),
    (0.0, "不合格", "建议重新构思"),
]


def calculate_total_score(scores: Dict[str, float]) -> float:
    """计算加权总分"""
    total = 0.0
    for dim, weight in DIMENSION_WEIGHTS.items():
        if dim in scores:
            total += scores[dim] * weight
        else:
            print(f"警告：缺少维度 '{dim}' 的评分，按 0 分计算", file=sys.stderr)
    return round(total, 2)


def determine_grade(total_score: float) -> tuple:
    """根据总分判定等级"""
    for threshold, grade_name, grade_desc in GRADE_THRESHOLDS:
        if total_score >= threshold:
            return grade_name, grade_desc
    return "不合格", "建议重新构思"


def calculate_weighted_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """计算各维度加权得分"""
    weighted = {}
    for dim, score in scores.items():
        weight = DIMENSION_WEIGHTS.get(dim, 0)
        weighted[f"{dim}（加权）"] = round(score * weight, 2)
    return weighted


def determine_dimension_grade(score: float) -> str:
    """判定单个维度等级"""
    for threshold, grade_name, _ in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade_name
    return "不合格"


def generate_score_summary(scores: Dict[str, float]) -> dict:
    """生成完整的评分摘要"""
    total = calculate_total_score(scores)
    grade_name, grade_desc = determine_grade(total)
    weighted = calculate_weighted_scores(scores)

    dimension_details = {}
    for dim, score in scores.items():
        dimension_details[dim] = {
            "原始得分": score,
            "权重": DIMENSION_WEIGHTS.get(dim, 0),
            "加权得分": round(score * DIMENSION_WEIGHTS.get(dim, 0), 2),
            "等级": determine_dimension_grade(score),
        }

    return {
        "加权总分": total,
        "等级": grade_name,
        "等级说明": grade_desc,
        "维度详情": dimension_details,
        "加权得分": weighted,
    }


def main():
    """命令行入口：接受 JSON 格式的评分数据"""
    if len(sys.argv) > 1:
        # 从文件读取
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            scores = json.load(f)
    else:
        # 从标准输入读取
        data = sys.stdin.read()
        if not data.strip():
            print("用法：python score_calculator.py [scores.json]", file=sys.stderr)
            print("或通过管道传入 JSON 数据", file=sys.stderr)
            sys.exit(1)
        scores = json.loads(data)

    result = generate_score_summary(scores)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
