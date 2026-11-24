#!/usr/bin/env python3
"""
Automated 3NF CSV Integrity Validator for JUPAS 2027 Calculator.
Checks programmes.csv, programme_weights.csv, admissions_history.csv,
institutions.csv, grade_scales.csv, and subjects.csv for:
  - Missing required columns or duplicate primary keys
  - Broken foreign keys (institution_id, jupas_code, subject_code, scale_id)
  - Invalid numeric weights, bonus weights, or grade levels
  - Malformed compulsory_electives syntax
"""

import os
import sys
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.isdir(DATA_DIR):
    DATA_DIR = "data"

VALID_GRADES = {"5**", "5*", "5", "4", "3", "2", "1", "U", "A"}
VALID_FORMULAS = {"BEST_5", "BEST_6", "3C2X", "4C2X"}

errors = []
warnings = []


def load_csv(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        errors.append(f"Missing required CSV file: {path}")
        return pd.DataFrame()
    return pd.read_csv(path, dtype=str).fillna("")


def main():
    insts = load_csv("institutions.csv")
    scales = load_csv("grade_scales.csv")
    subjs = load_csv("subjects.csv")
    progs = load_csv("programmes.csv")
    weights = load_csv("programme_weights.csv")
    hist = load_csv("admissions_history.csv")

    if errors:
        for e in errors:
            print(f"[ERROR] {e}")
        sys.exit(1)

    valid_inst_ids = set(insts["institution_id"].str.strip())
    valid_scale_ids = set(scales["scale_id"].str.strip())
    valid_subj_codes = set(subjs["subject_code"].str.strip())

    # 1. Check programmes.csv
    req_prog_cols = [
        "jupas_code", "institution_id", "faculty", "programme_name",
        "formula_type", "scale_override_id", "bonus_extra_elective_weight"
    ]
    for col in req_prog_cols:
        if col not in progs.columns:
            errors.append(f"programmes.csv missing required column: {col}")

    if progs["jupas_code"].duplicated().any():
        dups = progs[progs["jupas_code"].duplicated()]["jupas_code"].tolist()
        errors.append(f"programmes.csv has duplicate jupas_code(s): {dups}")

    valid_jupas_codes = set()
    for idx, row in progs.iterrows():
        line = idx + 2
        code = row["jupas_code"].strip()
        if not code:
            errors.append(f"programmes.csv line {line}: empty jupas_code")
            continue
        valid_jupas_codes.add(code)

        inst_id = row["institution_id"].strip()
        if inst_id not in valid_inst_ids:
            errors.append(f"programmes.csv line {line} ({code}): unknown institution_id '{inst_id}'")

        formula = row["formula_type"].strip()
        if formula not in VALID_FORMULAS:
            errors.append(f"programmes.csv line {line} ({code}): invalid formula_type '{formula}'")

        scale_ov = row["scale_override_id"].strip()
        if scale_ov and scale_ov not in valid_scale_ids:
            errors.append(f"programmes.csv line {line} ({code}): unknown scale_override_id '{scale_ov}'")

        bonus_str = row["bonus_extra_elective_weight"].strip()
        if bonus_str:
            try:
                val = float(bonus_str)
                if val < 0 or val > 3.0:
                    errors.append(f"programmes.csv line {line} ({code}): out-of-range bonus_extra_elective_weight '{bonus_str}'")
            except ValueError:
                errors.append(f"programmes.csv line {line} ({code}): non-numeric bonus_extra_elective_weight '{bonus_str}'")

        # Check compulsory_electives syntax if present
        if "compulsory_electives" in progs.columns and row["compulsory_electives"].strip():
            for grp in row["compulsory_electives"].strip().split(";"):
                if ":" not in grp:
                    errors.append(f"programmes.csv line {line} ({code}): malformed compulsory_electives '{grp}' (expected SUBJ:LVL)")
                    continue
                subj_part, lvl_part = grp.split(":", 1)
                if lvl_part.strip() not in VALID_GRADES:
                    errors.append(f"programmes.csv line {line} ({code}): invalid level '{lvl_part}' in compulsory_electives")
                for sc in subj_part.split("|"):
                    if sc.strip() not in valid_subj_codes:
                        errors.append(f"programmes.csv line {line} ({code}): unknown subject '{sc.strip()}' in compulsory_electives")

    # 2. Check programme_weights.csv
    for idx, row in weights.iterrows():
        line = idx + 2
        code = row["jupas_code"].strip()
        subj = row["subject_code"].strip()
        w_str = row["weight"].strip()
        min_g = row.get("min_grade", "").strip()

        if code not in valid_jupas_codes:
            errors.append(f"programme_weights.csv line {line}: unknown jupas_code '{code}'")
        if subj not in valid_subj_codes:
            errors.append(f"programme_weights.csv line {line} ({code}): unknown subject_code '{subj}'")
        try:
            w_val = float(w_str)
            if w_val <= 0 or w_val > 15.0:
                errors.append(f"programme_weights.csv line {line} ({code}, {subj}): suspicious weight '{w_str}'")
        except ValueError:
            errors.append(f"programme_weights.csv line {line} ({code}, {subj}): invalid non-numeric weight '{w_str}'")

        if min_g and min_g not in VALID_GRADES:
            errors.append(f"programme_weights.csv line {line} ({code}, {subj}): invalid min_grade '{min_g}'")

    # 3. Check admissions_history.csv
    for idx, row in hist.iterrows():
        line = idx + 2
        code = row["jupas_code"].strip()
        if code not in valid_jupas_codes:
            errors.append(f"admissions_history.csv line {line}: unknown jupas_code '{code}'")
        for col in ["score_uq", "score_median", "score_lq"]:
            val_str = row.get(col, "").strip()
            if val_str:
                try:
                    v = float(val_str)
                    if v < 0 or v > 450:
                        warnings.append(f"admissions_history.csv line {line} ({code}): unusual {col}='{val_str}'")
                except ValueError:
                    errors.append(f"admissions_history.csv line {line} ({code}): non-numeric {col}='{val_str}'")

    print(f"Checked {len(progs)} programmes, {len(weights)} weight rules, {len(hist)} history rows.")
    for w in warnings:
        print(f"[WARN] {w}")
    if errors:
        for e in errors:
            print(f"[ERROR] {e}")
        print(f"Validation FAILED with {len(errors)} error(s).")
        sys.exit(1)

    print("Validation PASSED with 0 errors.")


if __name__ == "__main__":
    main()
