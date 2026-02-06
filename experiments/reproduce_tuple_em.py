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

from result_replication_src.mvp_eval import ProcMvpRes
from result_replication_src.gen_nat_scl_eval import ProcGenSclNatRes


def main() -> None:
    mvp_file = REPO_ROOT / "final_result/acos-comparison/ours24_mvp.json"
    gen_file = REPO_ROOT / "final_result/acos-comparison/ours24_gen_scl_nat2.json"
    map_file = REPO_ROOT / "final_result/mappings_for_comparison/gen_sch_nat/gen_sch_nat_map.json"
    gold_file = REPO_ROOT / "final_result/gold_annotations_fin_3.csv"

    mvp = ProcMvpRes(str(mvp_file), str(gold_file))
    gen = ProcGenSclNatRes(str(gen_file), str(gold_file), str(map_file))

    results = {
        "mvp": {},
        "gen_scl_nat": {},
    }
    for mode in ["aste", "acos"]:
        p, r, f1 = mvp.calc_tup_em_acos(mode=mode)
        results["mvp"][mode] = {"precision": p, "recall": r, "f1": f1}

        p, r, f1 = gen.calc_tup_em_acos(mode=mode)
        results["gen_scl_nat"][mode] = {"precision": p, "recall": r, "f1": f1}

    out_path = Path(__file__).with_name("baseline_results.json")
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
