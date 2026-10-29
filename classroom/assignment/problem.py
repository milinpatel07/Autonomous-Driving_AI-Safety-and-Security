"""Problem set 1: rating the AEB item (functional safety, cybersecurity, SOTIF).

Instructors: change the parameters below each term; the grading tests and the reference
answers are computed from them with the course toolkit, so nothing else needs editing.
Students: read the questions here and write your answers in answers.py.
"""

# Q1 (03-02 HARA). An AEB malfunction is rated with these classes. Which ASIL results?
Q1_S, Q1_E, Q1_C = "S3", "E3", "C3"

# Q2 (03-02 / 03-04). Decompose the ASIL of Q1 onto two redundant elements (ISO notation, e.g. "X(C)").

# Q3 (03-03 FMEDA). Compute SPFM and LFM (fractions) of this camera FMEDA (rates in FIT).
Q3_FMEDA = [
    {"rate": 30, "dc": 0.99, "dc_latent": 0.90},   # image sensor, frame-loss monitor
    {"rate": 12, "dc": 0.90, "dc_latent": 0.60},   # supply, voltage monitor
    {"rate": 8, "safe": True},                     # stuck pixels, justified safe fault
    {"rate": 1, "spf": True},                      # oscillator, no mechanism
]

# Q4 (05-02 TARA). Attack potential and feasibility of a path with these factors (Annex G.2 labels):
Q4_FACTORS = ("<=1 month", "expert", "restricted", "easy", "specialized")

# Q5 (05-02 TARA). Risk value for this impact, with the feasibility you found in Q4.
Q5_IMPACT = "Severe"

# Q6 (05-01 / 05-02). CAL of the goal for this impact and attack vector (Annex E example).
Q6_IMPACT, Q6_VECTOR = "Major", "Network"

# Q7 (04-05 RSS). Minimum safe longitudinal distance in metres (speeds given in km/h).
Q7_V_REAR_KMH, Q7_V_FRONT_KMH = 90, 60
Q7_PARAMS = {"rho": 0.8, "a_max_accel": 2.0, "b_min_brake": 4.0, "b_max_brake": 8.0}

# Q8 (04-01 SOTIF). Hours of operation needed to show a hazardous-event rate below Q8_RATE per hour
# at Q8_CONFIDENCE, when Q8_EVENTS events are observed.
Q8_RATE, Q8_CONFIDENCE, Q8_EVENTS = 1e-6, 0.95, 0
