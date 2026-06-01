"""Group-aware split must produce zero group overlap across train/val/test."""
import numpy as np
import pandas as pd

from src.data.split import _make_groups, _stratified_group_split


def _toy(n=120, n_groups=24, seed=0):
    rng = np.random.default_rng(seed)
    groups = [f"g{i}" for i in range(n_groups)]
    labels = ["non", "open", "hidden"]
    rows = []
    for i in range(n):
        g = groups[i % n_groups]
        lab = labels[i % 3]
        rows.append({"id": f"id{i}", "source": "fake", "group_key": g, "label_3class": lab})
    return pd.DataFrame(rows)


def test_no_group_overlap():
    df = _toy()
    rest_idx, test_idx = _stratified_group_split(df, frac=0.2, seed=1)
    rest = df.iloc[rest_idx].reset_index(drop=True)
    train_idx, val_idx = _stratified_group_split(rest, frac=0.15 / 0.8, seed=2)
    train = rest.iloc[train_idx]
    val = rest.iloc[val_idx]
    test = df.iloc[test_idx]
    g_train = set(_make_groups(train))
    g_val = set(_make_groups(val))
    g_test = set(_make_groups(test))
    assert not (g_train & g_val)
    assert not (g_train & g_test)
    assert not (g_val & g_test)
    # All three splits cover all classes (with 120/24 and balanced).
    assert set(train["label_3class"].unique()) == {"non", "open", "hidden"}
