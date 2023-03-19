# SPDX-FileCopyrightText: Copyright (c) 2023 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
AD9833_ADSR_FeatherWing_sweep.py 2023-03-19 version 3.0.0

Fixed or swept frequency generator example. Update "initial parameters"
section for required functionality.

Uses optional AD5245 digital potentiometer for output level control.

Tested with Adafruit Feather M4 Express and CircuitPython 8.0.3
"""

import time
import board
import cedargrove_ad5245
import cedargrove_ad9833

try:
    digi_pot = cedargrove_ad5245.AD5245(address=0x2C)
    digi_pot.shutdown()  # mute the output before instantiating wave_gen
    digi_pot_connected = True
except RuntimeError as e:
    print("AD5245 digital potentiometer not connected.")
    digi_pot_connected = False

wave_gen = cedargrove_ad9833.AD9833(spi=board.SPI(), select=board.D6)

print("AD9833_ADSR_FeatherWing_sweep_v03.py")

# Setup Parameters
FREQUENCY_START = 20  # fixed or sweep starting frequency (Hz)
FREQUENCY_END = 21000  # sweep ending frequency (Hz)
FREQUENCY_STEP = 10  # sweep frequency step size (Hz)
PERIODS_PER_STEP = 3  # number of waveform periods to hold (non-linear mode)
SWEEP_MODE = "non-linear"  # fixed (10ms per step) or non-linear sweep hold timing
FREQUENCY_MODE = "sweep"  # fixed or sweep frequency
WAVE_TYPE = "sine"  # sine, triangle, or square waveform
AMPLITUDE = 1.0  # normalized potentiometer value (0 to 1.0)

DEBUG = True

if DEBUG:
    print("begin:", FREQUENCY_START, "  end:", FREQUENCY_END, "  incr:", FREQUENCY_STEP)
    print("periods per step:", PERIODS_PER_STEP)
    print(
        "sweep mode:",
        SWEEP_MODE,
        "  freq mode:",
        FREQUENCY_MODE,
        "  wave type:",
        WAVE_TYPE,
    )
    time.sleep(1)

while True:
    print("reset")
    wave_gen.reset()
    wave_gen.WAVE_TYPE = WAVE_TYPE
    print("start")
    wave_gen.start()
    if digi_pot_connected:
        digi_pot.normalized_wiper = AMPLITUDE

    if FREQUENCY_MODE == "sweep":
        wave_gen.start()

        for i in range(FREQUENCY_START, FREQUENCY_END, FREQUENCY_STEP):
            if DEBUG:
                print("sweep: frequency =", i)
            wave_gen.wave_freq = i

            if SWEEP_MODE == "non-linear":
                time.sleep(
                    PERIODS_PER_STEP * (1 / i)
                )  # pause for x periods at the specified frequency
            else:
                time.sleep(0.010)  # 10msec fixed hold time per step
    else:
        # output a fixed frequency for 10 seconds
        if DEBUG:
            print("fixed: frequency =", FREQUENCY_START)
        wave_gen.wave_freq = FREQUENCY_START
        wave_gen.start()
        time.sleep(10)  # 10sec fixed hold time

    if digi_pot_connected:
        digi_pot.shutdown()  # mute the output
    print("stop")
    wave_gen.stop()  # stop wave generator

    time.sleep(2)  # wait a second then do it all over again
