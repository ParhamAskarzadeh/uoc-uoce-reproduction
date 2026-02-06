from __future__ import annotations

import json
import sys
import types
from pathlib import Path

if 'pandas' not in sys.modules:
    sys.modules['pandas'] = types.ModuleType('pandas')
if 'numpy' not in sys.modules:
    sys.modules['numpy'] = types.ModuleType('numpy')

REPO_ROOT = Path(__file__).resolve().parents[1] / "original_repo"
sys.path.append(str(REPO_ROOT))

from result_replication_src.mvp_eval import ProcMvpRes  # noqa: E402


def split_entcat(entcat: str) -> list[str]:
    parts = entcat.split(" ")
    if len(parts) == 1:
        return [parts[0], "general"]
    if len(parts) == 2:
        return parts
    return [parts[0], " ".join(parts[1:])]


def calc_tup_em_acos_fixed(records: list[dict], mode: str = "aste") -> tuple[float, float, float]:
    mode_index = {
        "aste": [2, 3, 4],
        "acos": [0, 1, 2, 3, 4],
    }
    incl = mode_index[mode]
    tp = 0
    n_pred = 0
    n_gold = 0

    for rec in records:
        gold_labs = []
        pred_labs = []
        for gentcat, gasp, gpol, gop in rec["gold"]:
            entcat = split_entcat(gentcat)
            gold_labs.append([*entcat, gasp, gpol, gop])
        for pentcat, pasp, ppol, pop in rec["pred"]:
            entcat = split_entcat(pentcat)
            pred_labs.append([*entcat, pasp, ppol, pop])

        gold = set(["-".join([x for i, x in enumerate(rx) if i in incl]) for rx in gold_labs])
        pred = set(["-".join([x for i, x in enumerate(rx) if i in incl]) for rx in pred_labs])

        tp += len(gold.intersection(pred))
        n_pred += len(pred)
        n_gold += len(gold)

    precision = tp / n_pred if n_pred else 0.0
    recall = tp / n_gold if n_gold else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return precision, recall, f1


def main() -> None:
    mvp_file = REPO_ROOT / "final_result/acos-comparison/ours24_mvp.json"
    gold_file = REPO_ROOT / "final_result/gold_annotations_fin_3.csv"

    mvp = ProcMvpRes(str(mvp_file), str(gold_file))

    base_p, base_r, base_f1 = mvp.calc_tup_em_acos(mode="aste")

    records = json.loads(mvp_file.read_text(encoding="utf-8"))
    fix_p, fix_r, fix_f1 = calc_tup_em_acos_fixed(records, mode="aste")

    results = {
        "baseline": {"precision": base_p, "recall": base_r, "f1": base_f1},
        "fixed_entcat": {"precision": fix_p, "recall": fix_r, "f1": fix_f1},
    }

    out_path = Path(__file__).with_name("improved_results.json")
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
