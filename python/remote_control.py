import threading

import config
from flask import Flask, jsonify, request
from stomb import dummy_loop, pack, load, unpack

app = Flask(__name__)


@app.route('/api/v1/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        payload = request.get_json(force=True)
        unpack(payload)
    return pack()


def remote_control():
    app.run(host="127.0.0.1", port=8080, debug=True, use_reloader=False)

if __name__ == "__main__":
    load()
    t = threading.Thread(target=dummy_loop)
    t.start()
    remote_control()
    t.join()
