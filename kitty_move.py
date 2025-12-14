import board
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import json
import os

i2c = board.I2C()
pca = PCA9685(i2c)
pca.frequency = 50

S0 = servo.Servo(pca.channels[0], min_pulse=550, max_pulse=2400)
S1 = servo.Servo(pca.channels[1], min_pulse=550, max_pulse=2400)
S2 = servo.Servo(pca.channels[2], min_pulse=600, max_pulse=2500)
S3 = servo.Servo(pca.channels[3], min_pulse=550, max_pulse=2400)
S4 = servo.Servo(pca.channels[4], min_pulse=500, max_pulse=2500)
S5 = servo.Servo(pca.channels[5], min_pulse=500, max_pulse=2500)
S6 = servo.Servo(pca.channels[6], min_pulse=500, max_pulse=2500)
S7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2500)

# Leg mappings
#
# Each leg is described by a top joint angle, bottom joint angle,
# and if the angles should be inverted or not.
#
# 0 degrees is pointing straight forward, 180 is straight back.
LEGS = {
    'f': [
        ([S0, S4], False),
        ([S1, S5], True)
    ],
    'fl': [([S0, S4], False)],
    'fr': [([S1, S5], True)],
    'b': [
        ([S3, S7], False),
        ([S2, S6], True)
    ],
    'bl': [([S3, S7], False)],
    'br': [([S2, S6], True)],
    'l': [
        ([S0, S4], False),
        ([S3, S7], False)
    ],
    'r': [
        ([S1, S5], True),
        ([S2, S6], True)
    ],
    'all': [
        ([S0, S4], False),
        ([S1, S5], True),
        ([S3, S7], False),
        ([S2, S6], True)
    ]
}

# Calibration offsets for each leg joint
# Format: {leg_joint: offset}
# e.g., 'fl_top': -5 means front-left top joint needs -5 degrees
OFFSETS = {
    'fl_top': 0,
    'fl_bottom': 0,
    'fr_top': 0,
    'fr_bottom': 0,
    'bl_top': 0,
    'bl_bottom': 0,
    'br_top': 0,
    'br_bottom': 0,
}

CALIBRATION_FILE = 'calibration.json'


def _get_leg_name(servos):
    """Get the leg name from servo objects."""
    # Map servo pairs to leg names
    servo_to_leg = {
        (S0, S4): 'fl',
        (S1, S5): 'fr',
        (S3, S7): 'bl',
        (S2, S6): 'br',
    }
    return servo_to_leg.get(tuple(servos), None)


def move_legs(legs, top_angle, bottom_angle):
    """Move legs with calibration offsets applied."""
    for servos, invert in LEGS[legs]:
        # Get the leg name to look up offsets
        leg_name = _get_leg_name(servos)

        # Apply offsets if we have a specific leg
        if leg_name:
            top_offset = OFFSETS.get(f'{leg_name}_top', 0)
            bottom_offset = OFFSETS.get(f'{leg_name}_bottom', 0)
            adjusted_top = top_angle + top_offset
            adjusted_bottom = bottom_angle + bottom_offset
        else:
            adjusted_top = top_angle
            adjusted_bottom = bottom_angle

        # Clamp to valid range
        adjusted_top = max(0, min(180, adjusted_top))
        adjusted_bottom = max(0, min(180, adjusted_bottom))

        if invert:
            servos[0].angle = 180 - adjusted_top
            servos[1].angle = 180 - adjusted_bottom
        else:
            servos[0].angle = adjusted_top
            servos[1].angle = adjusted_bottom


def set_leg_offset(leg, joint_type, offset):
    """Set the calibration offset for a specific leg joint."""
    key = f'{leg}_{joint_type}'
    if key in OFFSETS:
        OFFSETS[key] = offset


def save_offsets():
    """Save calibration offsets to a JSON file."""
    with open(CALIBRATION_FILE, 'w') as f:
        json.dump(OFFSETS, f, indent=2)


def load_offsets():
    """Load calibration offsets from a JSON file."""
    global OFFSETS
    if os.path.exists(CALIBRATION_FILE):
        try:
            with open(CALIBRATION_FILE, 'r') as f:
                loaded = json.load(f)
                OFFSETS.update(loaded)
            print(f"Loaded calibration from {CALIBRATION_FILE}")
        except Exception as e:
            print(f"Error loading calibration: {e}")
    else:
        print("No calibration file found. Using default offsets.")
