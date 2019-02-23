# The MIT License (MIT)
#
# Copyright (c) 2019 Melissa LeBlanc-Williams for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_featherwing.gps_featherwing`
====================================================

Helper for using the `Ultimate GPS FeatherWing <https://www.adafruit.com/product/3133>`_.

* Author(s): Melissa LeBlanc-Williams
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_FeatherWing.git"

import busio
import adafruit_gps
from adafruit_featherwing import shared

class GPSFeatherWing:
    """Class representing an `Ultimate GPS FeatherWing
       <https://www.adafruit.com/product/3133>`_.

       Automatically uses the feather's I2C bus."""
    def __init__(self, update_period=1000, baudrate=9600):
        """
        :param int update_period: (Optional) The amount of time in milliseconds between
                                  updates (default=1000)
        :param int baudrate: (Optional) The Serial Connection speed to the GPS (default=9600)
        """
        if not isinstance(update_period, int):
            raise ValueError("Update Frequency should be an integer in milliseconds")
        if update_period < 250:
            raise ValueError("Update Frequency be at least 250 milliseconds")
        timeout = update_period // 1000 + 2
        if timeout < 3:
            timeout = 3

        self._uart = busio.UART(shared.TX, shared.RX, baudrate=baudrate, timeout=timeout)
        self._gps = adafruit_gps.GPS(self._uart, debug=False)
        # Turn on the basic GGA and RMC info
        self._gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        self._gps.send_command(b'PMTK220,{}'.format(update_period))

    def update(self):
        """
        Make sure to call ``gps.update()`` every loop iteration and at least twice
        as fast as data comes from the GPS unit (usually every second).

        :return: Whether it has parsed new data
        :rtype: bool
        """
        return self._gps.update()

    def read(self, size):
        """
        Read the UART for any information that may be on it

        :param int size: The size in bytes of the data to retrieve
        :return: Any data that is on the UART
        :rtype: bytearray
        """
        if isinstance(size, int) and size > 0:
            return self._uart.read(size)
        return None

    def send_command(self, command):
        """
        Send a bytearray command to the GPS module

        :param bytearray command: The command to send
        """
        if isinstance(command, bytearray):
            self._gps.send_command(command)

    @property
    def latitude(self):
        """
        Return the Current Latitude from the GPS
        """
        return self._gps.latitude

    @property
    def longitude(self):
        """
        Return the Current Longitude from the GPS
        """
        return self._gps.longitude

    @property
    def fix_quality(self):
        """
        Return the Fix Quality from the GPS
        """
        return self._gps.fix_quality

    @property
    def has_fix(self):
        """
        Return whether the GPS has a Fix on some satellites
        """
        return self._gps.has_fix

    @property
    def timestamp(self):
        """
        Return the Fix Timestamp as a struct_time
        """
        return self._gps.timestamp_utc

    @property
    def satellites(self):
        """
        Return the Number of Satellites we have a fix on
        """
        return self._gps.satellites

    @property
    def altitude(self):
        """
        Return the Altitude in meters
        """
        return self._gps.altitude_m

    @property
    def speed_knots(self):
        """
        Return the GPS calculated speed in knots
        """
        return self._gps.speed_knots

    @property
    def speed_mph(self):
        """
        Return the GPS calculated speed in Miles per Hour
        """
        return self._gps.speed_knots * 6076 / 5280

    @property
    def speed_kph(self):
        """
        Return the GPS calculated speed in Kilometers per Hour
        """
        return self._gps.speed_knots * 1.852

    @property
    def track_angle(self):
        """
        Return the Tracking angle in degrees
        """
        return self._gps.track_angle_deg

    @property
    def horizontal_dilution(self):
        """
        Return the Horizontal Dilution
        """
        return self._gps.horizontal_dilution

    @property
    def height_geoid(self):
        """
        Return the Height GeoID in  meters
        """
        return self._gps.height_geoid
