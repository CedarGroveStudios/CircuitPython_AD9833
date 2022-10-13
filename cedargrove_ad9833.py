# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`cedargrove_ad9833`
================================================================================

A CircuitPython driver for the AD9833 Programmable Waveform Generator.

* Author(s): JG

Implementation Notes
--------------------

**Hardware:**

* Cedar Grove Studios AD9833 Precision Waveform Generator FeatherWing
* Cedar Grove Studios AD9833 ADSR Precision Waveform Generator FeatherWing

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

import board
import busio
import digitalio
from adafruit_bus_device.spi_device import SPIDevice

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/CircuitPython_AD9833.git"


# pylint: disable=too-many-instance-attributes
class AD9833:
    """The driver class for the AD9833 Programmable Waveform Generator.

    The AD9833 is a programmable waveform generator that produces sine, square,
    and triangular waveform output from 0 MHz to 12.5MHz with 28-bit frequency
    resolution. The CircuitPython class sets the waveform generator's frequency,
    phase, and waveshape properties as well as providing methods for
    resetting, starting, pausing, and stopping the generator."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        wave_freq=440,
        wave_phase=0,
        wave_type="sine",
        select="D6",
        m_clock=25000000,
    ):
        """Initialize SPI bus interconnect, derive chip select pin (to allow
        multiple class instances), and create the SPIDevice instance. During
        intialization, the generator is reset and placed in the pause state.

        :param int wave_freq: The 28-bit waveform frequency in Hz ranging from
        0 to 2 ** 28. Practical maximum is 12.5MHz (one-half the master clock
          frequency). Defaults to 440.
        :param int wave_phase: The waveform phase offset in 2π Rad // 4096.
          Defaults to 0.
        :param str wave_type: The "sine", "triangle", or "square" waveshape.
          Defaults to "sine".
        :param str select: The AD9833 chip select pin designation. Defaults to "D6".
        :param int m_clock: Master clock frequency in Hz. Defaults to 25MHz.
        """

        self._spi = busio.SPI(board.SCK, MOSI=board.MOSI)  # Define SPI bus
        self._cs = digitalio.DigitalInOut(getattr(board, select))
        self._device = SPIDevice(
            self._spi, self._cs, baudrate=5000000, polarity=1, phase=0
        )

        self._wave_freq = wave_freq
        self._wave_phase = wave_phase
        self._wave_type = wave_type
        self._m_clock = m_clock  # Master clock frequency

        # Initiate register pointers
        self._freq_reg = 0  # FREQ0
        self._phase_reg = 0  # PHASE0

        self._pause = True
        self._reset = True

        # Reset the device
        self.reset()

        # Set the master clock frequency
        self._m_clock = m_clock

    @property
    def wave_freq(self):
        """The wave generator's floating or integer output frequency value."""
        return self._wave_freq

    @wave_freq.setter
    def wave_freq(self, new_wave_freq=440):
        """:param int new_wave_freq: The waveform frequency in Hz.
        Defaults to 440."""
        self._wave_freq = new_wave_freq
        self._wave_freq = max(self._wave_freq, 0)
        self._wave_freq = min(self._wave_freq, self._m_clock // 2)
        self._update_freq_register(self._wave_freq)

    @property
    def wave_phase(self):
        """The wave generator's integer output phase value."""
        return self._wave_phase

    @wave_phase.setter
    def wave_phase(self, new_wave_phase=0):
        """:param int new_wave_phase: The waveform phase offset.
        Defaults to 0."""
        self._wave_phase = int(new_wave_phase)
        self._wave_phase = max(self._wave_phase, 0)
        self._wave_phase = min(self._wave_phase, 4095)
        self._update_phase_register(self._wave_phase)

    @property
    def wave_type(self):
        """The wave generator's string waveform type value."""
        return self._wave_type

    @wave_type.setter
    def wave_type(self, new_wave_type="sine"):
        """:param str new_wave_type: The waveform type. Defaults to 'sine'."""
        self._wave_type = new_wave_type
        if self._wave_type not in ("triangle", "square", "sine"):
            # Default to sine in type isn't valid
            self._wave_type = "sine"
        self._update_control_register()

    def pause(self):
        """Pause the wave generator and freeze the output at the latest voltage
        level by stopping the internal clock.
        """
        self._pause = True  # Set the pause bit
        self._update_control_register()

    def start(self):
        """Start the wave generator with current register contents, register
        selection and wave mode setting.
        """
        self._reset = False  # Clear the reset bit
        self._pause = False  # Clear the clock disable bit
        self._update_control_register()

    def stop(self):
        """Stop the wave generator and reset the output to the midpoint
        voltage level.
        """
        self._reset = True  # Sets the reset bit
        self._pause = True  # Set the pause bit
        self._update_control_register()

    def reset(self):
        """Stop and reset the waveform generator. Pause the master clock.
        Update all registers with default values. Set sine wave mode. Clear the
        reset mode but keep the master clock paused.
        """
        # Reset control register contents, pause, and put device in reset state
        self._reset = True
        self._pause = True
        self._freq_reg = 0
        self._phase_reg = 0
        self._wave_type = "sine"
        self._update_control_register()

        # While reset, zero the frequency and phase registers
        self._update_freq_register(new_freq=0, register=0)
        self._update_freq_register(new_freq=0, register=1)
        self._update_phase_register(new_phase=0, register=0)
        self._update_phase_register(new_phase=0, register=1)

        # Take the waveform generator out of reset state, master clock still paused
        self._reset = False
        self._update_control_register()

    def _send_data(self, data):
        """Send a 16-bit word through SPI bus as two 8-bit bytes.
        :param int data: The 16-bit data value to write to the SPI device.
        """
        data &= 0xFFFF
        tx_msb = data >> 8
        tx_lsb = data & 0xFF

        with self._device:
            self._spi.write(bytes([tx_msb, tx_lsb]))

    def _update_control_register(self):
        """Construct the control register contents per existing local parameters
        then send the new control register word to the waveform generator.
        """
        # Set default control register mask value (sine wave mode)
        control_reg = 0x2000

        if self._reset:
            # Set the reset bit
            control_reg |= 0x0100

        if self._pause:
            # Disable master clock bit
            control_reg |= 0x0080

        control_reg |= self._freq_reg << 11  # Frequency register select bit
        control_reg |= self._phase_reg << 10  # Phase register select bit

        if self._wave_type == "triangle":
            # Set triangle mode
            control_reg |= 0x0002

        if self._wave_type == "square":
            # Set square mode
            control_reg |= 0x0028

        self._send_data(control_reg)

    def _update_freq_register(self, new_freq, register=None):
        """Load inactive register with new frequency value then set the
        register active in order to avoid partial frequency changes. Writes to
        specified register if != None.

        :param int new_freq: The new frequency value.
        :param union(int, None) register: The register for the new value; FREG0
        or FREG1. Selects the non-active register if register == None.
        """
        self._wave_freq = new_freq

        if register is None:
            # Automatically toggle to use the inactive register
            self._freq_reg = int(not self._freq_reg)
        else:
            self._freq_reg = register

        freq_word = int(round(float(self._wave_freq * pow(2, 28)) / self._m_clock))

        # Split frequency word into two 14-bit parts; MSB and LSB
        freq_msb = (freq_word & 0xFFFC000) >> 14
        freq_lsb = freq_word & 0x3FFF

        if self._freq_reg == 0:
            # bit-or freq register 0 select (DB15 = 0, DB14 = 1)
            freq_lsb |= 0x4000
            freq_msb |= 0x4000
        else:
            # bit-or freq register 1 select (DB15 = 1, DB14 = 0)
            freq_lsb |= 0x8000
            freq_msb |= 0x8000

        self._send_data(freq_lsb)  # Load new LSB into inactive register
        self._send_data(freq_msb)  # Load new MSB into inactive register

        self._update_control_register()

    def _update_phase_register(self, new_phase, register=None):
        """Load inactive register with new phase value then set the
        register active in order to to avoid partial phase changes. Writes to
        specified register if != None.

        :param int new_freq: The new phase value.
        :param union(int, None) register: The register for the new value; PHASE0
        or PHASE1. Selects the non-active register if register == None.
        """
        self._wave_phase = new_phase

        if register is None:
            # Automatically toggle to use the inactive register
            self._phase_reg = int(not self._phase_reg)
        else:
            self._phase_reg = register

        if self._phase_reg == 0:
            # bit-or phase register 0 select (DB15=1, DB14=1, DB13=0)
            self._wave_phase |= 0xC000
        else:
            # bit-or phase register 1 select (DB15=1, DB14=1, DB13=1)
            self._wave_phase |= 0xE000

        self._send_data(self._wave_phase)

        self._update_control_register()
