"""
One command to launch the prototype:

    python run.py

Then open http://127.0.0.1:5050
(We avoid port 5000 because macOS uses it for AirPlay Receiver.)
"""
import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5050"))
    app.run(host="127.0.0.1", port=port, debug=True)
