import threading
import traceback

from flask import Flask, jsonify, request
from stomb import dummy_loop, pack, load, unpack

app = Flask(__name__)


@app.route('/api/v1/config', methods=['GET', 'POST'])
def config():
    print(f"Handling config {request.method}")
    try:
        if request.method == 'POST':
            payload = request.get_json(force=True)
            print(f"Got a set config: {payload}")
            unpack(payload)
        return pack()
    except Exception as e:
        print(traceback.format_exc())
    except:
        print("Unexpected error:", sys.exc_info()[0])
    return None


def control_loop():
    print("Starting config server.")
    app.run(host="127.0.0.1", port=8080, debug=True, use_reloader=False)

if __name__ == "__main__":
    load()
    t = threading.Thread(target=dummy_loop)
    t.start()
    control_loop()
    t.join()
