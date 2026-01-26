import unittest
import yaml
from wireviz.wireviz import parse
# We will import the function to be tested after we modify app.py,
# but for now we can just use the logic or try to import it if we mock things.
# Since app.py has GUI code, importing it might trigger Tkinter.
# `app.py` has `if __name__ == '__main__': Application()` but top level imports like `tkinter` might be an issue in headless.
# However, `wireviz_gui` imports `tkinter` at top level.
# I will try to import `normalize_connections` from `wireviz_gui.app`.
# If that fails due to display, I might need to mock sys.modules or use xvfb (not available).
# But standard tkinter usually allows import if DISPLAY is unset, just not root creation? No, it might fail on `import tkinter`.
# Let's check `tests/test_dialog_integration.py` mentioned in memory.

# Memory says: "The file tests/test_dialog_integration.py contains integration tests for dialog classes ... utilizing unittest.mock to patch tkinter components for headless testing."
# So I should check that file.


class TestIssueRepro(unittest.TestCase):
    def test_parse_user_yaml(self):
        # This test is expected to fail before fixes are applied
        # I'll define the YAML here
        yaml_content = """
metadata:
  title: Sol-Ark 15K Battery Storage System
connectors:
  Battery_Rack:
    type: 6-Slot Server Rack
    pincount: 3
    pinlabels: [POS, NEG, CHASSIS]
  Industrial_Switch:
    type: 800A 1500V DC Disconnect
    pincount: 2
    pinlabels: [SW_IN, SW_OUT]
  Pos_Distribution_Bus:
    type: Blue Sea 2104 PowerBar (Positive)
    pincount: 3
    pinlabels: [FROM_SW, TO_F1, TO_F2]
  Neg_Distribution_Bus:
    type: Blue Sea PowerBar (Negative)
    pincount: 3
    pinlabels: [FROM_SHUNT, TO_INV1, TO_INV2]
  Class_T_Fuse_1:
    type: 400A Fuse Block
    pincount: 2
    pinlabels: [F1_IN, F1_OUT]
  Class_T_Fuse_2:
    type: 400A Fuse Block
    pincount: 2
    pinlabels: [F2_IN, F2_OUT]
  SmartShunt:
    type: Victron 500A Shunt
    pincount: 2
    pinlabels: [BATT_NEG, LOAD_NEG]
  Sol_Ark_15K:
    type: Hybrid Inverter
    pincount: 6
    pinlabels:
      [BAT1_POS, BAT1_NEG, BAT2_POS, BAT2_NEG, CHASSIS, GND_LUG]
  Chassis_Ground_Bus:
    type: Copper Ground Bar
    pincount: 4
    pinlabels: [RACK, INVERTER, HUB_BOX, EARTH]
  Ground_Rod:
    type: 8ft Copper Earth Rod
    pincount: 1
    pinlabels: [EARTH]
cables:
  Trunk_Pos:
    gauge: 4/0 AWG
    wirecount: 1
    colors: [RD]
    category: Power
  Jumper_SW_Bus:
    gauge: 4/0 AWG
    wirecount: 1
    colors: [RD]
    category: Power
  Trunk_Neg:
    gauge: 4/0 AWG
    wirecount: 1
    colors: [BK]
    category: Power
  Shunt_To_NegBus:
    gauge: 4/0 AWG
    wirecount: 1
    colors: [BK]
    category: Power
  Chassis_Bond:
    gauge: 6 AWG
    wirecount: 1
    colors: [GN]
    category: Ground
  Earth_Ground:
    gauge: 4 AWG
    wirecount: 1
    colors: [GN]
    category: Ground
  Bus_To_Fuse1_Pos:
    gauge: 4/0 AWG
    wirecount: 1
    colors: [RD]
    label: "POS BUS → FUSE1"
    category: Power
  Fuse1_To_INV1_Pos:
    gauge: 4/0 AWG
    wirecount: 1
    colors: [RD]
    label: "FUSE1 → INV BAT1+"
    category: Power
  Bus_To_Fuse2_Pos:
    gauge: 4/0 AWG
    wirecount: 1
    colors: [RD]
    label: "POS BUS → FUSE2"
    category: Power
  Fuse2_To_INV2_Pos:
    gauge: 4/0 AWG
    wirecount: 1
    colors: [RD]
    label: "FUSE2 → INV BAT2+"
    category: Power
  NegBus_To_INV1:
    gauge: 4/0 AWG
    wirecount: 1
    colors: [BK]
    label: "NEG BUS → INV BAT1−"
    category: Power
  NegBus_To_INV2:
    gauge: 4/0 AWG
    wirecount: 1
    colors: [BK]
    label: "NEG BUS → INV BAT2−"
    category: Power
connections:
  # ---------- Positive Power ----------
  - Battery_Rack.POS:
      - Industrial_Switch.SW_IN: Trunk_Pos
  - Industrial_Switch.SW_OUT:
      - Pos_Distribution_Bus.FROM_SW: Jumper_SW_Bus
  - Pos_Distribution_Bus.TO_F1:
      - Class_T_Fuse_1.F1_IN: Bus_To_Fuse1_Pos
  - Class_T_Fuse_1.F1_OUT:
      - Sol_Ark_15K.BAT1_POS: Fuse1_To_INV1_Pos
  - Pos_Distribution_Bus.TO_F2:
      - Class_T_Fuse_2.F2_IN: Bus_To_Fuse2_Pos
  - Class_T_Fuse_2.F2_OUT:
      - Sol_Ark_15K.BAT2_POS: Fuse2_To_INV2_Pos
  # ---------- Negative Power ----------
  - Battery_Rack.NEG:
      - SmartShunt.BATT_NEG: Trunk_Neg
  - SmartShunt.LOAD_NEG:
      - Neg_Distribution_Bus.FROM_SHUNT: Shunt_To_NegBus
  - Neg_Distribution_Bus.TO_INV1:
      - Sol_Ark_15K.BAT1_NEG: NegBus_To_INV1
  - Neg_Distribution_Bus.TO_INV2:
      - Sol_Ark_15K.BAT2_NEG: NegBus_To_INV2
  # ---------- Chassis / Earth Ground ----------
  - Battery_Rack.CHASSIS:
      - Chassis_Ground_Bus.RACK: Chassis_Bond
  - Sol_Ark_15K.CHASSIS:
      - Chassis_Ground_Bus.INVERTER: Chassis_Bond
  - Chassis_Ground_Bus.EARTH:
      - Ground_Rod.EARTH: Earth_Ground
"""
        # Load yaml
        data = yaml.safe_load(yaml_content)

        # We need to import the preprocessing function from app.py
        # But for this test to be useful before we edit app.py, we can't really import the *new* logic.
        # So we just try to parse using wireviz and expect it to fail.
        # Or we can verify that app.normalize_connections (current) FAILS to produce valid output.

        try:
            from wireviz_gui.app import normalize_connections
        except ImportError:
            # Fallback if headless
            import sys
            from unittest.mock import MagicMock

            sys.modules["tkinter"] = MagicMock()
            sys.modules["tkinter.ttk"] = MagicMock()
            sys.modules["tkinter.filedialog"] = MagicMock()
            sys.modules["tkinter.messagebox"] = MagicMock()
            from wireviz_gui.app import normalize_connections

        normalized_data = normalize_connections(data)

        # With current implementation, this should fail at parse step
        try:
            parse(inp=normalized_data, return_types=("harness",))
        except Exception as e:
            # We expect failure currently
            print(f"Caught expected error: {e}")
            raise e


if __name__ == "__main__":
    unittest.main()
