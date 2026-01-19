EXAMPLES = {
    "Demo 01": """connectors:
  X1:
    type: D-Sub
    subtype: female
    pinlabels: [DCD, RX, TX, DTR, GND, DSR, RTS, CTS, RI]
  X2:
    type: Molex KK 254
    subtype: female
    pinlabels: [GND, RX, TX]

cables:
  W1:
    gauge: 0.25 mm2
    length: 0.2
    color_code: DIN
    wirecount: 3
    shield: true

connections:
  -
    - X1: [5,2,3]
    - W1: [1,2,3]
    - X2: [1,3,2]
  -
    - X1: 5
    - W1: s
""",
    "Demo 02": """metadata:
  title: WireViz Demo 2
  pn: WV-DEMO-02

  authors:
    Created:
      name: D. Rojas
      date: 2020-05-20
    Approved:
      name: D. Rojas
      date: 2020-05-20

  revisions:
    A:
      name: D. Rojas
      date: 2020-10-17
      changelog: WireViz 0.2 release

  template:
    name: din-6771
    sheetsize: A3

templates: # defining templates to be used later on
  - &molex_f
    type: Molex KK 254
    subtype: female
  - &con_i2c
    pinlabels: [GND, +5V, SCL, SDA]
  - &wire_i2c
    category: bundle
    gauge: 0.14 mm2
    colors: [BK, RD, YE, GN]

connectors:
  X1:
    <<: *molex_f # copying items from the template
    pinlabels: [GND, +5V, SCL, SDA, MISO, MOSI, SCK, N/C]
  X2:
    <<: *molex_f
    <<: *con_i2c # it is possible to copy from more than one template
  X3:
    <<: *molex_f
    <<: *con_i2c
  X4:
    <<: *molex_f
    pinlabels: [GND, +12V, MISO, MOSI, SCK]
  F:
    style: simple
    type: Crimp ferrule
    subtype: 0.25 mm²
    color: YE

cables:
  W1:
    <<: *wire_i2c
    length: 0.2
    show_equiv: true
  W2:
    <<: *wire_i2c
    length: 0.4
    show_equiv: true
  W3:
    category: bundle
    gauge: 0.14 mm2
    length: 0.3
    colors: [BK, BU, OG, VT]
    show_equiv: true
  W4:
    gauge: 0.25 mm2
    length: 0.3
    colors: [BK, RD]
    show_equiv: true

connections:
  -
    - X1: [1-4]
    - W1: [1-4]
    - X2: [1-4]
  -
    - X1: [1-4]
    - W2: [1-4]
    - X3: [1-4]
  -
    - X1: [1,5-7]
    - W3: [1-4]
    - X4: [1,3-5]
  -
    - F.
    - W4: [1,2]
    - X4: [1,2]
""",
    "Example 01": """connectors:
  X1:
    type: Molex KK 254 # more information
    subtype: female
    pinlabels: [GND, VCC, RX, TX] # pincount is implicit in pinout
  X2:
    type: Molex KK 254
    subtype: female
    pinlabels: [GND, VCC, RX, TX]

cables:
  W1:
    color_code: IEC # auto-color wires based on a standard
    wirecount: 4 # need to specify number of wires explicitly when using a color code
    gauge: 0.25 mm2 # also accepts AWG as unit
    show_equiv: true # auto-calculate AWG equivalent from metric gauge
    length: 0.2 # length in m
    shield: true
    type: Serial

connections:
  -
    - X1: [1-4]
    - W1: [1-4]
    - X2: [1,2,4,3] # crossover
  - # connection from connector pin to wire shielding
    - X1: 1
    - W1: s
""",
    "Example 02": """connectors:
  X1: &boo
    type: Molex Micro-Fit
    subtype: male
    pinlabels: [GND, VCC]
  X2: &con_power_f # define template
    type: Molex Micro-Fit
    subtype: female
    pinlabels: [GND, VCC]
  X3:
    <<: *con_power_f # create from template
  X4:
    <<: *con_power_f # create from template

cables:
  W1: &wire_power # define template
    colors: [BK, RD] # number of wires implicit in color list
    gauge: 0.25 # assume mm2 if no gauge unit is specified
    show_equiv: true
    length: 0.2
  W2:
    <<: *wire_power # create from template
  W3:
    <<: *wire_power # create from template
    gauge: 20 awg

connections:
  -
    - X1: [1-2]
    - W1: [1-2]
    - X2: [1-2]
  -
    - X1: [1-2]
    - W2: [1-2]
    - X3: [1-2]
  -
    - X1: [1-2]
    - W3: [1-2]
    - X4: [1-2]
""",
    "Example 03": """connectors:
  X1: &boo
    type: Molex Micro-Fit
    subtype: male
    pinlabels: [GND, VCC]
  X2: &con_power_f
    type: Molex Micro-Fit
    subtype: female
    pinlabels: [GND, VCC]
  X3:
    <<: *con_power_f
  X4:
    <<: *con_power_f

cables:
  W1:
    category: bundle # bundles are routed together, but more loosely than normal cables
    wirecount: 6
    colors: [BK, RD] # if number of items in color list is less than wirecount, loop colors
    gauge: 0.25 mm2
    show_equiv: true
    length: 0.2

connections:
  -
    - X1: [1-2]
    - W1: [1-2]
    - X2: [1-2]
  -
    - X1: [1-2]
    - W1: [3,4]
    - X3: [1-2]
  -
    - X1: [1-2]
    - W1: [5,6]
    - X4: [1-2]
""",
    "Example 04": """cables:
  W1:
    gauge: 0.25 mm2
    show_equiv: true
    length: 0.2
    color_code: IEC
    wirecount: 6
    category: bundle

connectors:
  F:
    style: simple
    type: Crimp ferrule

connections:
  -
    - F.
    - W1: [1-6]
    - F.
""",
    "Example 05": """# daisy chain, variant 1
templates:
  - &template_con
    type: '<a href="https://www.molex.com/molex/products/family/kk_254_rpc_connector_system">Molex KK 254</a>'
    subtype: female
    pinlabels: [GND, VCC, SCL, SDA]
  - &template_wire
    gauge: 0.25 mm2
    length: 0.2
    colors: [PK, TQ, YE, VT]
    category: bundle
    type: I2C

connectors:
  X1:
    <<: *template_con
  X2:
    <<: *template_con
  X3:
    <<: *template_con

cables:
  W1:
    <<: *template_wire
  W2:
    <<: *template_wire

connections:
  -
    - X1: [1-4]
    - W1: [1-4]
    - X2: [1-4]
  -
    - X2: [1-4]
    - W2: [1-4]
    - X3: [1-4]
""",
    "Example 06": """# daisy chain, variant 2
templates:
  - &template_con
    type: Molex KK 254
    subtype: female
    pinlabels: [GND, VCC, SCL, SDA]
  - &template_wire
    gauge: 0.25 mm2
    length: 0.2
    colors: [PK, TQ, YE, VT]
    category: bundle

connectors:
  X1:
    <<: *template_con
  X2:
    <<: *template_con
  X3:
    <<: *template_con
  X4:
    <<: *template_con
  X5:
    <<: *template_con
  X6:
    <<: *template_con

cables:
  W1:
    <<: *template_wire
  W2:
    <<: *template_wire
  W3:
    <<: *template_wire
  W4:
    <<: *template_wire
  W5:
    <<: *template_wire

connections:
  -
    - X1: [1-4]
    - W1: [1-4]
    - X2: [1-4]
  -
    - X3: [1-4]
    - W2: [1-4]
    - X2: [1-4]
  -
    - X3: [1-4]
    - W3: [1-4]
    - X4: [1-4]
  -
    - X5: [1-4]
    - W4: [1-4]
    - X4: [1-4]
  -
    - X5: [1-4]
    - W5: [1-4]
    - X6: [1-4]
""",
    "Example 07": """# contributed by @elliotmr

connectors:
  X1:
    type: TE 776164-1
    subtype: female
    hide_disconnected_pins: True
    pincount: 35
    notes: Unconnected pins are not shown

  X2:
    type: D-Sub
    subtype: female
    pincount: 9
    hide_disconnected_pins: True
    notes: Unconnected pins are not shown

cables:
  C1:
    wirecount: 2
    gauge: 20 AWG
    colors: [YE, GN]
    length: 1

connections:
  -
    - X1: [5,6]
    - C1: [1,2]
    - X2: [7,2]
""",
    "Example 08": """# contributed by @cocide
# and later extended to include images

connectors:
  Key:
    type: Phone Connector
    subtype: male 3.5
    pins: [T, R, S]
    pinlabels: [Dot, Dash, Ground]
    show_pincount: false
    # image:
    #   src: resources/stereo-phone-plug-TRS.png
    #   caption: Tip, Ring, and Sleeve

cables:
  W1:
    gauge: 24 AWG
    length: 0.2
    color: BK  # Cable jacket color
    color_code: DIN
    wirecount: 3
    shield: SN  # Matching the shield color in the image
    # image:
    #   src: resources/cable-WH+BN+GN+shield.png
    #   height: 70  # Scale the image size slightly down
    #   caption: Cross-section

connections:
  -
    - Key: [S,R,T]
    - W1: [WH,BN,GN]
  -
    - Key: S
    - W1: s
""",
    "Example 09": """# contributed by @kimmoli

connectors:
  X1:
    type: D-Sub
    subtype: male
    pincount: 25
    pins: [1,14,3,16,5,18,7,20,9,22,11,24,13]
    pinlabels: [ SENSE_P_1, SENSE_N_1, SENSE_P_2, SENSE_N_2, SENSE_P_3, SENSE_N_3, SENSE_P_4,SENSE_N_4, SENSE_P_5, SENSE_N_5, SENSE_P_6, SENSE_N_6, GND ]
  X2:
    type: F48
    subtype: female
    pincount: 48
    pins: [ z2,b2,d2,z4,b4,d4,z6,b6,d6,z8,b8,d8,z10,b10,d10,z12,b12,d12,z14,b14,d14,z16,b16,d16,z18,b18,d18,z20,b20,d20,z22,b22,d22,z24,b24,d24,z26,b26,d26,z28,b28,d28,z30,b30,d30,z32,b32,d32 ]

cables:
  W1:
    gauge: 0.25 mm2
    length: 0.2
    color_code: DIN
    wirecount: 12
    shield: true

connections:
  -
    - X1: [1,14,3,16,5,18,7,20,9,22,11,24]
    - W1: [2,1,4,3,6,5,8,7,10,9,12,11]
    - X2: [d4,z2,d10,z8,d16,z14,d20,z18,d26,z24,d32,z30]
  -
    - X1: 13
    - W1: s
""",
    "Example 10": """# Example 7: Crossover Cable
connectors:
  X1:
    type: Stewart Connector SS-37000-002
    subtype: male
    pinlabels: [DA+,DA-,DB+,DC+,DC-,DB-,DD+,DD-] # pincount is implicit in pinout
  X2:
    type: Stewart Connector SS-37000-002
    subtype: male
    pinlabels: [DB+,DB-,DA+,DD+,DD-,DA-,DC+,DC-]

cables:
  W1:
    color_code: T568A # auto-color wires based on a standard
    wirecount: 8 # need to specify number of wires explicitly when using a color code
    gauge: 24 AWG # also accepts AWG as unit
    length: 1 # length in m
    shield: false
    type: CAT5e

connections:
  - - X1: [1-8]
    - W1: [1-8]
    - X2: [3,6,1,7,8,2,4,5] # crossover
""",
    "Example 11": """# based on @stmaxed's example in #134

connectors:
  X1: &X
    type: Screw connector
    subtype: male
    color: GN
    pincount: 4
    pinlabels: [A, B, C, D]
  F:
    style: simple
    type: Ferrule
    color: GY

cables:
  W:
    color: BK
    colors: [BK, WH, BU, BN]

connections:
  -  # ferrules + connector X1
    - W.W1: [1-4]
    - F.
    - -->
    - X1: [1-4]
""",
    "Example 12": """# based on @MSBGit's example in #134

connectors:
  X1: &dupont
    type: Dupont 2.54mm
    subtype: male
    pincount: 5
    color: BK
  X2:
    <<: *dupont
    subtype: female

cables:
  W:
    category: bundle
    colors: [RD, BK, BU, GN]
    length: 0.2

connections:
  -
    - W.W1: [1-4]
    - X1: [1-4]
    - ==>
    - X2: [1-4]
    - W.W2: [1-4]
""",
    "Example 13": """# based on @formatc1702's example in #184

connectors:
  X:
    pincount: 4
    pinlabels: [A, B, C, D]
  F:
    style: simple
    type: ferrule

cables:
  C:
    wirecount: 4
    color_code: DIN

connections:
  -
    - X.X1: [1-4]
    - C.C1: [1-4]
    - [F.F1, F.F2, F.F3, F.F4]  # generate new instances of F and assign designators
    - C.C2: [1-4]
    - X.X2: [1-4]
  -
    - [F1, F2, F3, F4]  # use previously assigned designators
    - C.C3: [1-4]
    - X.X3: [1-4]
""",
    "Example 14": """connectors:
  JSTMALE: &JST_SM  # use generic names here, assign designators at generation time
    type: JST SM
    subtype: male
    pincount: 4
    pinlabels: [A, B, C, D]
  JSTFEMALE:
    <<: *JST_SM  # easily create JSTMALE's matching connector
    subtype: female
  X4:  # this connector is only used once, use fixed designator here already
    type: Screw terminal connector
    pincount: 4
    color: GN
    pinlabels: [W, X, Y, Z]
  S:
    style: simple
    type: Splice
    color: CU
  F:
    style: simple
    type: Ferrule
    color: GY


cables:
  CABLE:
    wirecount: 4
    color_code: DIN
    length: 0.1
  WIRE:
    wirecount: 1
    colors: [BK]
    length: 0.1

connections:
  -
    - JSTMALE.X1: [4-1]   # use `.` syntax to generate a new instance of JSTMALE, named X1
    - CABLE.W1: [1-4]     # same syntax for cables
    - [S., S., S.S1, S.]  # splice W1 and W2 together; only wire #3 needs a user-defined designator
    - CABLE.W2: [1-4]
    - S.                  # test shorthand, auto-get required number of ferrules from context
    - CABLE.W21: [1-4]
    - JSTFEMALE.X2: [1-4]
    - <=>                 # mate X2 and X3
    - JSTMALE.X3: [1-4]
    - CABLE.W3: [1-4]
    - [F., F., F., F.]
    - -->                 # insert ferrules into screw terminal connector
    - X4: [2,1,4,3]       # X4 does not require auto-generation, thus no `.` syntax here
  -
    - S1: [1]             # reuse previously generated splice
                          # TODO: Make it work with `- F1` only, making pin 1 is implied
    - WIRE.: [1]          # We don't care about a simple wire's designator, auto-generate please!
                          # TODO: Make it work with `- W.W4: 1`, dropping the need for `[]`
    - X2: [4]
""",
}
