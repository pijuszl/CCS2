"""H2 interpretability: SHAP on a feature-based interpretable model.

Fits logistic regression and a gradient-boosted classifier on the
feature_table.parquet, evaluates on the test split, then computes SHAP values
for the GBM (TreeExplainer) and logistic (LinearExplainer).

  python -m src.evaluation.interpretability \
        --feature-table data/processed/feature_table.parquet \
        --splits data/processed/splits.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.utils import ensure_dir, get_logger

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _select_features(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    drop = {"id", "label_3class", "source", "source_type"}
    cols = [c for c in df.columns if c not in drop and pd.api.types.is_numeric_dtype(df[c])]
    return df[cols].fillna(df[cols].median(numeric_only=True)), cols


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--feature-table", required=True)
    p.add_argument("--splits", default=None)
    p.add_argument("--out-dir", default=None)
    p.add_argument("--classes", nargs="+", default=["non", "open", "hidden"])
    args = p.parse_args()

    ft_path = Path(args.feature_table) if Path(args.feature_table).is_absolute() else PROJECT_ROOT / args.feature_table
    df = pd.read_parquet(ft_path)
    df = df[df["label_3class"].notna()].reset_index(drop=True)

    if args.splits:
        s = json.loads(Path(args.splits).read_text(encoding="utf-8"))
        train_ids = set(s["train"]); test_ids = set(s["test"])
        train_df = df[df["id"].isin(train_ids)]
        test_df = df[df["id"].isin(test_ids)]
    else:
        from sklearn.model_selection import train_test_split
        train_df, test_df = train_test_split(df, test_size=0.2, stratify=df["label_3class"], random_state=42)

    X_train, feat_cols = _select_features(train_df)
    X_test, _ = _select_features(test_df)
    y_train = train_df["label_3class"].to_numpy()
    y_test = test_df["label_3class"].to_numpy()

    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report
    from sklearn.ensemble import GradientBoostingClassifier

    log.info("Fitting logistic regression on %d features, %d train rows", len(feat_cols), len(X_train))
    lr = LogisticRegression(max_iter=2000, class_weight="balanced")
    lr.fit(X_train, y_train)
    log.info("LR test report:\n%s", classification_report(y_test, lr.predict(X_test), zero_division=0))

    log.info("Fitting GBM ...")
    gbm = GradientBoostingClassifier(random_state=42)
    gbm.fit(X_train, y_train)
    log.info("GBM test report:\n%s", classification_report(y_test, gbm.predict(X_test), zero_division=0))

    out_dir = Path(args.out_dir) if args.out_dir else PROJECT_ROOT / "results" / "figures"
    ensure_dir(out_dir)

    try:
        import shap
        import matplotlib.pyplot as plt

        log.info("SHAP for GBM ...")
        explainer = shap.TreeExplainer(gbm)
        sv = explainer.shap_values(X_test)
        # GradientBoostingClassifier returns a list per class for multiclass.
        if isinstance(sv, list):
            for i, c in enumerate(args.classes):
                fig = plt.figure()
                shap.summary_plot(sv[i], X_test, feature_names=feat_cols, show=False)
                fig.tight_layout()
                fig.savefig(out_dir / f"shap_gbm_{c}.png", dpi=150)
                plt.close(fig)
        else:
            fig = plt.figure()
            shap.summary_plot(sv, X_test, feature_names=feat_cols, show=False)
            fig.tight_layout()
            fig.savefig(out_dir / "shap_gbm.png", dpi=150)
            plt.close(fig)
        log.info("SHAP plots written to %s", out_dir)
    except Exception as e:
        log.warning("SHAP failed (%s); skipping plots", e)

    # Permutation importance as a backup.
    from sklearn.inspection import permutation_importance
    pi = permutation_importance(gbm, X_test, y_test, n_repeats=10, random_state=42, n_jobs=1)
    rows = sorted(zip(feat_cols, pi.importances_mean, pi.importances_std),
                  key=lambda x: -x[1])
    out_path = PROJECT_ROOT / "results" / "tables" / "permutation_importance.csv"
    ensure_dir(out_path.parent)
    pd.DataFrame(rows, columns=["feature", "importance_mean", "importance_std"]).to_csv(out_path, index=False)
    log.info("wrote %s", out_path)


if __name__ == "__main__":
    main()
