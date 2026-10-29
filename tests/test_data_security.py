"""Offline tests for the CAN (ROAD) and V2X (VeReMi Extension) parsers.

The fixtures are short excerpts in the exact formats of the published files:
ROAD ``candump -l`` logs with ``capture_metadata.json`` entries, and VeReMi Extension
``traceJSON`` receiver logs (one JSON object per line).
"""
import json

import numpy as np
import pytest

from avsafety import data as D

pd = pytest.importorskip("pandas")

# ROAD: three genuine frames, then an injected max-speedometer frame on 0x0D0 (byte 5 = 0xFF)
CANDUMP = """(1000000000.000000) can0 20E#4E2003A0C63F8FFF
(1000000000.000002) can0 522#DF7FD0007F08001C
(1000000000.001001) can0 0D0#427504646C018700
(1000000000.011001) can0 0D0#4275046489FF6E00
(1000000000.012000) can0 6E0#0233
(1000000000.021001) can0 0D0#427504646D018800
"""
META_SPEEDO = {"injection_id": "0xd0", "injection_data_str": "XXXXXXXXXXFFXXXX",
               "injection_interval": [0.005, 0.020], "modified": False}
META_FUZZ = {"injection_id": "XXX", "injection_data_str": "FFFFFFFFFFFFFFFF",
             "injection_interval": [0.0, 1.0], "modified": False}


def test_parse_candump_columns_and_bytes():
    df = D.parse_candump(CANDUMP)
    assert list(df.columns[:4]) == ["t", "can_id", "dlc", "data"]
    assert len(df) == 6 and df["t"].iloc[0] == 0.0
    assert df["t"].iloc[3] == pytest.approx(0.011001, abs=1e-6)
    assert df["can_id"].tolist() == [0x20E, 0x522, 0x0D0, 0x0D0, 0x6E0, 0x0D0]
    assert df["dlc"].tolist() == [8, 8, 8, 8, 2, 8]
    assert df.loc[3, "b5"] == 0xFF and df.loc[0, "b7"] == 0xFF
    assert df.loc[4, "b0"] == 0x02 and df.loc[4, "b1"] == 0x33 and df.loc[4, "b2"] == 0   # short frame is zero-padded


def test_parse_candump_rejects_garbage():
    with pytest.raises(ValueError):
        D.parse_candump("not a candump line\n")


def test_road_label_targeted_injection_with_wildcards():
    df = D.parse_candump(CANDUMP)
    lab = D.road_label(df, META_SPEEDO)
    assert lab.tolist() == [0, 0, 0, 1, 0, 0]   # only the 0x0D0 frame with byte 5 = FF inside the interval


def test_road_label_fuzzing_any_identifier_and_no_injection():
    df = D.parse_candump(CANDUMP + "(1000000000.030000) can0 0AB#FFFFFFFFFFFFFFFF\n")
    assert D.road_label(df, META_FUZZ).tolist() == [0, 0, 0, 0, 0, 0, 1]
    assert D.road_label(df, {"injection_interval": None, "injection_data_str": None}).sum() == 0


def test_road_attack_family_names():
    assert D._road_family("ambient_dyno_drive_basic_short") == "none"
    assert D._road_family("fuzzing_attack_2") == "fuzzing"
    assert D._road_family("max_speedometer_attack_1") == "targeted injection"
    assert D._road_family("max_engine_coolant_temp_attack_masquerade") == "masquerade"
    assert "ROAD" in D.LICENCES and "CC BY 4.0" in D.attribution("ROAD")


# VeReMi Extension: one own GNSS fix (type 2) and two received BSMs (type 3)
TRACE = "\n".join(json.dumps(m) for m in [
    {"type": 2, "rcvTime": 54004.0, "pos": [1313.99, 1007.62, 0.0], "pos_noise": [4.36, 4.83, 0.0],
     "spd": [0.0, 0.0, 0.0], "spd_noise": [0.0, 0.0, 0.0], "acl": [6.4e-5, 6.4e-5, 0.0],
     "acl_noise": [0.002, 0.002, 0.0], "hed": [-0.536, -0.844, 0.0], "hed_noise": [7.93, 7.93, 0.0]},
    {"type": 3, "rcvTime": 54004.0166, "sendTime": 54004.0166, "sender": 6027, "senderPseudo": 1060275,
     "messageID": 12205597, "pos": [1237.19, 976.54, 0.0], "pos_noise": [3.70, 3.61, 0.0],
     "spd": [-12.02, -0.21, 0.0], "spd_noise": [0.03, 0.0005, 0.0], "acl": [-1.67, -0.03, 0.0],
     "acl_noise": [0.0046, 0.0027, 0.0], "hed": [-0.99986, -0.01685, 0.0], "hed_noise": [22.86, 7.02, 0.0]},
    {"type": 3, "rcvTime": 54004.3158, "sendTime": 54004.3158, "sender": 6015, "senderPseudo": 1060155,
     "messageID": 12206253, "pos": [1209.77, 826.86, 0.0], "pos_noise": [3.42, 3.56, 0.0],
     "spd": [-13.84, -3.56, 0.0], "spd_noise": [-0.006, -0.0016, 0.0], "acl": [-2.08, -0.54, 0.0],
     "acl_noise": [0.001, 0.0003, 0.0], "hed": [-0.98940, -0.14524, 0.0], "hed_noise": [69.5, 3.1, 0.0]},
]) + "\n"


def test_parse_veremi_trace():
    df = D.parse_veremi_trace(TRACE, receiver=6039)
    assert df["type"].tolist() == [2, 3, 3] and (df["receiver"] == 6039).all()
    assert df["sender"].tolist() == [-1, 6027, 6015]
    assert np.isnan(df["send_time"].iloc[0]) and df["send_time"].iloc[1] == pytest.approx(54004.0166)
    assert df["pos_x"].iloc[1] == pytest.approx(1237.19) and df["spd_y"].iloc[2] == pytest.approx(-3.56)
    assert df["hed_x"].iloc[1] ** 2 + df["hed_y"].iloc[1] ** 2 == pytest.approx(1.0, abs=1e-3)


def test_veremi_trace_filename_pattern_and_attack_codes():
    m = D._TRACE.search("VeReMi_54000_57600_2022-9-11_18:8:38/traceJSON-6033-6031-A1-54004-15.json")
    assert m.group(1) == "6033" and m.group(3) == "1"     # vehicle id (= 'sender' in BSMs), attacker type
    assert D.VEREMI_ATTACKS[0] == "Genuine" and D.VEREMI_ATTACKS[2] == "ConstPosOffset"
    assert D.VEREMI_ATTACKS[13] == "DoS" and len(D.VEREMI_ATTACKS) == 20
    assert "CC BY 4.0" in D.attribution("VeReMi Extension")
    with pytest.raises(ValueError):
        D.veremi("NoSuchAttack")


@pytest.mark.skipif(not __import__("os").environ.get("AVSAFETY_NETWORK"), reason="set AVSAFETY_NETWORK=1 to download")
def test_loaders_network():
    fz = D.can_ids("fuzzing_attack_3")
    assert fz["label"].sum() > 0 and set(fz["attack"]) == {"fuzzing"}
    v = D.veremi("ConstPos", hour=1, n_receivers=2)
    assert {2, 3} <= set(v["type"]) and (v["attacker_type"] >= -1).all()
