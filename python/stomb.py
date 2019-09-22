import json
import os
from math import floor
from time import sleep

from visualization import select_new_visualization

import config

def unpack(running_config, bag, restart_if_needed=True):
    try:
        gamma = bag['SOFTWARE_GAMMA_CORRECTION']
        display_fps = bag['DISPLAY_FPS']
        fps = bag['FPS'] if bag['FPS'] < running_config['_max_led_FPS'] else running_config['_max_led_FPS']
        minf = bag['MIN_FREQUENCY']
        maxf = bag['MAX_FREQUENCY']
        bins = bag['N_FFT_BINS']
        rhist = bag['N_ROLLING_HISTORY']
        mvt = bag['MIN_VOLUME_THRESHOLD']
        vis = bag['SELECTED_VISUALIZATION']
        pscale = bag['POWER_SCALE']
        force_restart = bag['force_restart']
        if vis == -2:
            # Just send the current values back, don't update anything
            return
        elif vis == -4:
            # Reset config and restart
            running_config.remove()
            # TODO: Restart
            os._exit(0)
        if not force_restart:
            force_restart = running_config['FPS'] != fps or running_config['MIN_FREQUENCY'] != minf or running_config['MAX_FREQUENCY'] != maxf or running_config['N_FFT_BINS'] != bins or running_config['N_ROLLING_HISTORY'] != rhist
        running_config['DISPLAY_FPS'] = display_fps
        running_config['SOFTWARE_GAMMA_CORRECTION'] = gamma
        running_config['MIN_VOLUME_THRESHOLD'] = mvt
        running_config['MIN_SAMPLE_THRESHOLD'] = floor(running_config['MIN_VOLUME_THRESHOLD'] * 32767.0)
        running_config['FPS'] = fps
        running_config['MIN_FREQUENCY'] = minf
        running_config['MAX_FREQUENCY'] = maxf
        running_config['N_FFT_BINS'] = bins
        running_config['N_ROLLING_HISTORY'] = rhist
        running_config['POWER_SCALE'] = pscale
        if vis >= 0:
            select_new_visualization(running_config, vis)
            running_config.store()
        # elif vis == -1:
        #     # Only store, don't change visualization
        elif vis == -3:
            # Store and restart
            force_restart = True
        if restart_if_needed and force_restart:
            running_config.store()
            # TODO Restart the app somehow
            os._exit(0)
            print('Restarting')
    except KeyError as err:
        print(f"Unable to load config {err}")
    finally:
        running_config.store()



def dummy_loop():
    c = 0
    while True:
        c += 1
        print(f"{c}: FPS: {running_config['FPS']} Gamma: {running_config['SOFTWARE_GAMMA_CORRECTION']} "
              f"Min Freq: {running_config['MIN_FREQUENCY']} Max Freq: {running_config['MAX_FREQUENCY']} "
              f"Bins: {running_config['N_FFT_BINS']} History: {running_config['N_ROLLING_HISTORY']} "
              f"Min Volume: {running_config['MIN_VOLUME_THRESHOLD']}")
        sleep(1)
