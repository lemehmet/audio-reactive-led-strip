import os
import threading
from math import floor

from flask import Flask, request, abort
from stomb import dummy_loop, unpack

app = Flask(__name__)
running_config = None

@app.route('/api/v1/config', methods=['GET', 'POST'])
def config():
    if running_config is None:
        return abort(500, "Config is not usable")
    if request.method == 'POST':
        payload = request.get_json(force=True)
        print(f"Setting config: {payload}")
        unpack(running_config=running_config, bag=payload)
    print(f"Returning current config: {running_config.get_all()}")
    return running_config.get_all()


def control_loop(config_instance):
    print("Starting config server.")
    global running_config
    running_config = config_instance
    app.run(host="127.0.0.1", port=8080, debug=True, use_reloader=False)

if __name__ == "__main__":
    t = threading.Thread(target=dummy_loop)
    t.start()
    control_loop()
    t.join()
