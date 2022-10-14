Introduction
============




.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/CedarGroveStudios/CircuitPython_AD9833/workflows/Build%20CI/badge.svg
    :target: https://github.com/CedarGroveStudios/CircuitPython_AD9833/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

A CircuitPython driver for the AD9833 Programmable Waveform Generator.

.. image:: https://github.com/CedarGroveStudios/CircuitPython_AD9833/blob/master/media/DSC05796_combo.jpg


The AD9833 is a programmable waveform generator that produces sine, square, and
triangular waveform output from 0 MHz to 12.5MHz with 28-bit frequency resolution. The
CircuitPython SPI driver controls the waveform generator's frequency, phase, and
waveshape.

The Cedar Grove AD9833 Precision Waveform Generator and AD9833 ADSR Precision
Waveform Generator FeatherWings provide all the support circuitry for the
AD9833. The ADSR (Attack, Decay, Sustain, Release) version incorporates the
AD5245 digital potentiometer to provide output amplitude control.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install cedargrove_ad9833

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

    # insert code here

``ad9833_simpletest.py`` and other examples can be found in the ``examples`` folder.

Documentation
=============
`AD9833 CircuitPython Driver API Class Description <https://github.com/CedarGroveStudios/CircuitPython_AD9833/blob/master/media/pseudo_readthedocs_cedargrove_ad9833.pdf>`_

`CedarGrove AD9833 Precision Waveform Generator FeatherWing OSH Park Project <https://oshpark.com/shared_projects/al6aPN0u>`_

.. image:: https://github.com/CedarGroveStudios/CircuitPython_AD9833/blob/master/media/Waveform_Generator_closeup.png

`CedarGrove AD9833 ADSR Precision Waveform Generator FeatherWing OSH Park Project <https://oshpark.com/shared_projects/RoKf63De>`_

.. image:: https://github.com/CedarGroveStudios/CircuitPython_AD9833/blob/master/media/Waveform_Gen_ADSR_close.png


For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_AD9833/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
