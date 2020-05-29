import os
from datetime import datetime
from flask import Flask, render_template, make_response

app = Flask(__name__)


def get_app_debug_info():
    cfg_items = {k: v for k, v in os.environ.items()}
    cfg_items['datetime'] = datetime.now().isoformat()
    return cfg_items


@app.route('/')
def welcome():
    return {
        'msg': 'Hello World! This is a simple Python app using Flask! But wait there is more!',
        'endpoints': ['/', '/ping', '/debug', '/debug/ui']
    }


@app.route('/ping')
def ping():
    return {'msg': 'pong!'}


@app.route('/debug', methods=['GET'])
def debug():
    cfg_items = get_app_debug_info()
    response = make_response(cfg_items, 200)

    # Enable CORS: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    response.headers['Access-Control-Allow-Origin'] = '*'  # allow all domains for now
    response.headers['Access-Control-Allow-Methods'] = "GET"

    return response


@app.route('/debug/ui', methods=['GET'])
def debug_ui():
    cfg_map = get_app_debug_info()
    # sort items by key
    cfg_items = sorted([{'k': k, 'v': v} for k, v in cfg_map.items()], key=lambda x: x['k'].upper())
    return render_template('debug.html', cfg_items=cfg_items, title='Hello Python Debug!')


@app.errorhandler(404)
def not_found(e):
    return {'err': 'Not found!'}, 404


if __name__ == '__main__':
    port = os.environ.get('PORT', 5001)
    app.run(debug=True, host='0.0.0.0', port=port)
