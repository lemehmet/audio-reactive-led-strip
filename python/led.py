from __future__ import print_function
from __future__ import division

import platform
import numpy as np
import config
from math import floor

if config.DEVICE == 'pi':
    import board
    import neopixel
    strip = neopixel.NeoPixel(board.D18, config.N_PIXELS, brightness=0.9, auto_write=False, pixel_order=neopixel.GRBW)

_gamma = np.load(config.GAMMA_TABLE_PATH)
"""Gamma lookup table used for nonlinear brightness correction"""

_prev_pixels = np.tile(253, (4, config.N_PIXELS))
"""Pixel values that were most recently displayed on the LED strip"""

pixels = np.tile(1, (4, config.N_PIXELS))
"""Pixel values for the LED strip"""

_is_python_2 = int(platform.python_version_tuple()[0]) == 2


def _update_pi():
    """Writes new LED values to the Raspberry Pi's LED strip

    Raspberry Pi uses the rpi_ws281x to control the LED strip directly.
    This function updates the LED strip with new values.
    """
    global pixels, _prev_pixels
    # Truncate values and cast to integer
    pixels = np.clip(pixels, 0, 255).astype(int)
    # Optional gamma correction
    p = _gamma[pixels] if config.SOFTWARE_GAMMA_CORRECTION else np.copy(pixels)
    # Encode 24-bit LED values in 32 bit integers
    r = p[0][:].astype(int)
    g = p[1][:].astype(int)
    b = p[2][:].astype(int)
    w = p[3][:].astype(int)
    # Update the pixels
    for i in range(config.N_PIXELS):
        # Ignore pixels if they haven't changed (saves bandwidth)
        if np.array_equal(p[:, i], _prev_pixels[:, i]):
            continue
        strip[i] = (r[i] if r[i] < 256 else 255,
                    g[i] if g[i] < 255 else 255,
                    b[i] if b[i] < 255 else 255,
                    w[i] if w[i] < 255 else 255,
                    )
    _prev_pixels = np.copy(p)
    strip.show()

def update():
    if config.DEVICE == 'pi':
        _update_pi()
    else:
        raise ValueError('Invalid device selected')


# Execute this file to run a LED strand test
# If everything is working, you should see a red, green, and blue pixel scroll
# across the LED strip continously
if __name__ == '__main__':
    import time
    # Turn all pixels off
    pixels *= 0
    pixels[0, 0] = 255  # Set 1st pixel red
    pixels[1, 1] = 255  # Set 2nd pixel green
    pixels[2, 2] = 255  # Set 3rd pixel blue
    pixels[3, 3] = 255  # Set 4th pixel white

    pixels[0, 4] = 255
    pixels[1, 4] = 0
    pixels[2, 4] = 0
    pixels[3, 4] = 127

    pixels[0, 5] = 0
    pixels[1, 5] = 255
    pixels[2, 5] = 0
    pixels[3, 5] = 127

    pixels[0, 6] = 0
    pixels[1, 6] = 0
    pixels[2, 6] = 255
    pixels[3, 6] = 127

    pixels[0, 7] = 255
    pixels[1, 7] = 255
    pixels[2, 7] = 255
    pixels[3, 7] = 255

    pixels[0, 8] = 255
    pixels[1, 8] = 255
    pixels[2, 8] = 255
    pixels[3, 8] = 0
    print('Starting LED strand test')
    while True:
        pixels = np.roll(pixels, 1, axis=1)
        update()
        time.sleep(.1)
