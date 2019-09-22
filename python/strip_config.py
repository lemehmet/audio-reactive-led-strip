import json
import os
import traceback

CONFIG_FILE = "das-config.json"

N_PIXELS = 288
MIN_SAMPLE_THRESHOLD = 0

DEFAULT_CONFIG = {
    'DEVICE': 'pi',
    'INPUT_DEVICE_INDEX': 1,
    'LED_PIN': 18,
    'LED_FREQ_HZ': 800000,
    'LED_DMA': 5,
    'BRIGHTNESS': 255,
    'LED_INVERT': True,
    'SOFTWARE_GAMMA_CORRECTION': True,
    'USE_GUI': False,
    'DISPLAY_FPS': True,
    'N_PIXELS': N_PIXELS,
    'GAMMA_TABLE_PATH': os.path.join(os.path.dirname(__file__), 'gamma_table.npy'),
    'MIC_RATE': 48000,
    'FPS': 40,
    '_max_led_FPS': int(((N_PIXELS * 30e-6) + 50e-6) ** -1.0),
    'MIN_FREQUENCY': 200,
    'MAX_FREQUENCY': 4200,
    'N_FFT_BINS': 144,
    'N_ROLLING_HISTORY': 2,
    'MIN_SAMPLE_THRESHOLD': MIN_SAMPLE_THRESHOLD,
    'MIN_VOLUME_THRESHOLD': MIN_SAMPLE_THRESHOLD / 32767.0,
    'SELECTED_VISUALIZATION': 0,
    'POWER_SCALE': 1.0,
}
