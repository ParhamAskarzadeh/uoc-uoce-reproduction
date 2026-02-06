from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

POS_WORDS = {"good", "great", "excellent", "amazing", "love", "loved", "like", "liked", "fantastic", "wonderful", "best", "awesome"}
NEG_WORDS = {"bad", "poor", "awful", "terrible", "hate", "hated", "worst", "boring", "disappointed", "slow", "dirty"}
INTENSIFIERS = {"very", "really", "so", "extremely", "super"}
ASPECT_KEYWORDS = {
    "battery": ("battery", "operational_performance", "laptop"),
    "screen": ("screen", "display", "laptop"),
    "keyboard": ("keyboard", "operational_performance", "laptop"),
    "service": ("service", "service", "restaurant"),
    "food": ("food", "food_and_beverage", "restaurant"),
    "price": ("price", "price", "general"),
    "ambience": ("ambience", "ambience", "restaurant"),
    "clean": ("cleanliness", "hygiene", "restaurant"),
}


def rule_based_extract(sentence: str) -> dict:
    text = sentence.lower()
    polarity = "neutral"
    expr = "N/A"
    intensity = "average"

    words = re.findall(r"[a-zA-Z]+", text)
    for i, w in enumerate(words):
        if w in POS_WORDS:
            polarity = "positive"
            expr = w
            if i > 0 and words[i - 1] in INTENSIFIERS:
                expr = words[i - 1] + " " + w
                intensity = "strong"
            break
        if w in NEG_WORDS:
            polarity = "negative"
            expr = w
            if i > 0 and words[i - 1] in INTENSIFIERS:
                expr = words[i - 1] + " " + w
                intensity = "strong"
            break

    aspect_term, aspect_category, target_entity = "N/A", "general", "general"
    for k, (a, c, e) in ASPECT_KEYWORDS.items():
        if k in text:
            aspect_term, aspect_category, target_entity = a, c, e
            break

    return {
        "aspect_term": aspect_term,
        "sentiment_expression": expr,
        "target_entity": target_entity,
        "aspect_category": aspect_category,
        "sentiment_polarity": polarity,
        "sentiment_intensity": intensity,
        "opinion_holder_span": "N/A",
        "opinion_holder_entity": "author",
        "opinion_qualifier": "N/A",
        "opinion_reason": "N/A",
    }


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python3 run_rule_based_inference.py input.csv output.csv")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    rows = []
    with in_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    out_rows = []
    for i, row in enumerate(rows, start=1):
        text = row.get("text", "")
        pred = rule_based_extract(text)
        out_rows.append({
            "id": f"u-{i}",
            "raw_text": text,
            **pred,
        })

    header = [
        "id",
        "raw_text",
        "aspect_term",
        "sentiment_expression",
        "target_entity",
        "aspect_category",
        "sentiment_polarity",
        "opinion_holder_span",
        "opinion_holder_entity",
        "sentiment_intensity",
        "opinion_qualifier",
        "opinion_reason",
    ]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Wrote {len(out_rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
