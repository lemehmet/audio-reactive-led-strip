import json
from time import sleep

CONFIG_FILE = "das-config.json"

import config

def pack():
    return {
        'software_gamma': config.SOFTWARE_GAMMA_CORRECTION,
        'display_fps': config.DISPLAY_FPS,
        'fps': config.FPS,
        'min_freq': config.MIN_FREQUENCY,
        'max_freq': config.MAX_FREQUENCY,
        'n_fft_bins': config.N_PIXELS,
        'n_rolling_history': config.N_ROLLING_HISTORY,
        'min_volume_threshold': config.MIN_SAMPLE_THRESHOLD,
        'selected_visualization': config.SELECTED_VISUALIZATION,
        'force_restart': False,
    }


def unpack(bag, restart_if_needed = True):
    try:
        gamma = bag['software_gamma']
        display_fps = bag['display_fps']
        fps = bag['fps'] if bag['fps'] < config._max_led_FPS else config._max_led_FPS
        minf = bag['min_freq']
        maxf = bag['max_freq']
        bins = bag['n_fft_bins']
        rhist = bag['n_rolling_history']
        mvt = bag['min_volume_threshold']
        vis = bag['selected_visualization']
        force_restart = bag['force_restart']
        if not force_restart:
            force_restart = config.FPS != fps or config.MIN_FREQUENCY != minf or config.MAX_FREQUENCY != maxf or config.N_FFT_BINS != bins or config.N_ROLLING_HISTORY != rhist
        config.DISPLAY_FPS = display_fps
        config.SOFTWARE_GAMMA_CORRECTION = gamma
        config.SELECTED_VISUALIZATION = vis
        config.MIN_SAMPLE_THRESHOLD = mvt
        config.MIN_VOLUME_THRESHOLD = config.MIN_SAMPLE_THRESHOLD / 32767.0
        config.FPS = fps
        config.MIN_FREQUENCY = minf
        config.MAX_FREQUENCY = maxf
        config.N_FFT_BINS = bins
        config.N_ROLLING_HISTORY = rhist
        if restart_if_needed and force_restart:
            #TODO Restart the app somehow
            store()
            print('Restarting')
    except KeyError as err:
        print(f"Unable to load config {err}")
    finally:
        store()

def store():
    with open(CONFIG_FILE, 'w') as outfile:
        json.dump(pack(), outfile)

def load():
    try:
        with open(CONFIG_FILE) as json_file:
            unpack(json.load(json_file), False)
    except:
        print(f"Unable to load {CONFIG_FILE}, loading defaults")

def dummy_loop():
    c = 0
    while True:
        c += 1
        print(f"{c}: FPS: {config.FPS} Gamma: {config.SOFTWARE_GAMMA_CORRECTION} "
               f"Min Freq: {config.MIN_FREQUENCY} Max Freq: {config.MAX_FREQUENCY} "
               f"Bins: {config.N_FFT_BINS} History: {config.N_ROLLING_HISTORY} "
               f"Min Volume: {config.MIN_VOLUME_THRESHOLD}")
        sleep(1)