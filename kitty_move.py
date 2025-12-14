import board
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

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


def move_legs(legs, top_angle, bottom_angle):
    for servos, invert in LEGS[legs]:
        if invert:
            servos[0].angle = 180 - top_angle
            servos[1].angle = 180 - bottom_angle
        else:
            servos[0].angle = top_angle
            servos[1].angle = bottom_angle
