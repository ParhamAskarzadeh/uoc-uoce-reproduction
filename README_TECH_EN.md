# Technical Run Guide (Step-by-Step)

This guide explains how to run the project on CPU without modifying the original repository.

## 1) Project Structure
- `project/original_repo`: untouched copy of the official repository
- `project/experiments`: reproduction + improvement scripts
- `project/demo`: demo notebook
- `project/requirements.txt`: optional dependencies

## 2) Prerequisites
- Python 3.11+ (tested with Python 3.12)
- No external packages are required for the default reproduction and demo.
- For full component-level evaluation, install `pandas` and `numpy`.

## 3) (Optional) Install Dependencies
If you have internet access:
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r project/requirements.txt
```

## 4) Reproduce a Result (Mandatory)
This runs the official evaluation code for tuple-level exact match:
```bash
python3 project/experiments/reproduce_tuple_em.py
```
Output is saved to `project/experiments/baseline_results.json`.

## 5) Run the Improvement
This applies a small but meaningful fix to entity/category parsing:
```bash
python3 project/experiments/entity_category_fix_eval.py
```
Output is saved to `project/experiments/improved_results.json`.

## 6) Run the Demo Notebook
Notebook path: `project/demo/uoc_demo.ipynb`

Inside the notebook you will see:
- baseline results (no improvement)
- improved results (with fix)
- a simple chart output
- dataset-based sample output
- free-form input using a CPU-only rule-based extractor

## 7) CPU-Only Input/Output Script
A minimal script that reads a CSV with a `text` column and writes UOCE-like outputs:
```bash
python3 project/experiments/run_rule_based_inference.py \
  project/experiments/sample_input.csv \
  project/experiments/sample_output.csv
```
More details: `project/experiments/input_output_README_FA.md`

## 8) Notes
- The original repository remains unchanged.
- The rule-based inference is a lightweight demo (not a real model).
