"""Smoke: label mapping is deterministic and exhaustive on a fixture."""
import json

import pandas as pd

from src.data.map_labels import map_corpus

MAPPING = {
    "overt": ["loaded-language", "wavingTheFlag"],
    "subtle": ["doubt", "whataboutism"],
    "ambiguous_is_propaganda_values": ["Unclear", "nonDeterminable", "propagandaCitation"],
}


def _row(**kw):
    base = {"id": "x", "text": "t", "image_path": None,
            "source": "halt-prop", "source_type": "unknown",
            "native_label": "", "native_meta": "{}", "group_key": "g"}
    base.update(kw)
    return base


def test_halt_prop_no_is_non():
    df = pd.DataFrame([_row(native_label="no")])
    out = map_corpus(df, "halt-prop", MAPPING)
    assert out["label_3class"].iloc[0] == "non"


def test_halt_prop_yes_overt_is_open():
    techs = json.dumps([{"technique": "loaded-language"}])
    df = pd.DataFrame([_row(native_label="yes",
                            native_meta=json.dumps({"techniques": techs}))])
    out = map_corpus(df, "halt-prop", MAPPING)
    assert out["label_3class"].iloc[0] == "open"


def test_halt_prop_yes_subtle_is_hidden():
    techs = json.dumps([{"technique": "doubt"}])
    df = pd.DataFrame([_row(native_label="yes",
                            native_meta=json.dumps({"techniques": techs}))])
    out = map_corpus(df, "halt-prop", MAPPING)
    assert out["label_3class"].iloc[0] == "hidden"


def test_halt_prop_ambiguous_is_dropped():
    df = pd.DataFrame([_row(native_label="Unclear")])
    out = map_corpus(df, "halt-prop", MAPPING)
    assert out["label_3class"].iloc[0] is None


def test_digires():
    df = pd.DataFrame([
        _row(source="digires", native_label="reliable"),
        _row(source="digires", native_label="unreliable"),
    ])
    out = map_corpus(df, "digires", MAPPING)
    assert out["label_3class"].tolist() == ["non", "hidden"]


def test_litund():
    df = pd.DataFrame([
        _row(source="litund", native_label="lrt"),
        _row(source="litund", native_label="unreliable"),
    ])
    out = map_corpus(df, "litund", MAPPING)
    assert out["label_3class"].tolist() == ["non", "hidden"]
    assert out["needs_review"].tolist() == [False, True]
