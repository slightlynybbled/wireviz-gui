import yaml
from wireviz.wireviz import parse

yaml_string = """
connectors:
  X1:
    type: D-Sub
    subtype: female
    pinlabels: [DCD, RX, TX, DTR, GND, DSR, RTS, CTS, RI]
  X2:
    type: Molex KK 254
    subtype: female
    pinlabels: [GND, RX, TX]

mates:
  -
    - X1
    - ==>
    - X2
"""

try:
    harness = parse(inp=yaml_string, return_types='harness')
    print("Successfully parsed harness.")
    print(harness)
except Exception as e:
    print(f"Error parsing harness: {e}")
