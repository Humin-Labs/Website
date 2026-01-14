# /opt/Website/cad_app.py
from flask import Flask, send_from_directory, redirect
import os

CAD_STATIC_DIR = os.path.join(os.path.dirname(__file__), "static", "cad")

cad_app = Flask(__name__, static_folder=CAD_STATIC_DIR)

@cad_app.route("/")
def serve_root():
    return send_from_directory(CAD_STATIC_DIR, "index.html")

# Serve any valid CAD asset under /<path>
@cad_app.route("/<path:path>")
def serve_static(path):
    # Remap missing shorthand requests
    redirects = {
        "style.css": "css/toolkit.css",
        "verb.js": "lib/verb.js",
        "moveBody96.png": "img/cad/moveBody96.png",
    }
    if path in redirects:
        path = redirects[path]

    return send_from_directory(CAD_STATIC_DIR, path)

if __name__ == "__main__":
    cad_app.run(host="127.0.0.1", port=5100)
