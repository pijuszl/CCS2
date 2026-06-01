"""Smoke: each loader returns >=1 row of the common schema on the real corpora."""
from pathlib import Path

import pytest

from src.data import load_existing as L

ROOT = Path(__file__).resolve().parents[1]
DATASETS = ROOT / "datasets"

COMMON_COLS = {"id", "text", "image_path", "source", "source_type",
               "native_label", "native_meta", "group_key"}


@pytest.mark.skipif(not (DATASETS / "HALT-PROP").exists(), reason="HALT-PROP not present")
def test_load_halt_prop():
    df = L.load_halt_prop(DATASETS)
    assert len(df) > 0
    assert COMMON_COLS.issubset(set(df.columns))
    assert df["source"].iloc[0] == "halt-prop"


@pytest.mark.skipif(not (DATASETS / "DIGIRES").exists(), reason="DIGIRES not present")
def test_load_digires():
    df = L.load_digires(DATASETS)
    assert len(df) > 0
    assert COMMON_COLS.issubset(set(df.columns))
    assert set(df["native_label"].unique()) <= {"reliable", "unreliable"}


@pytest.mark.skipif(not (DATASETS / "LITUND").exists(), reason="LITUND not present")
def test_load_litund():
    df = L.load_litund(DATASETS)
    assert len(df) > 0
    assert COMMON_COLS.issubset(set(df.columns))
    assert set(df["native_label"].unique()) <= {"unreliable", "lrt"}
