#!/usr/bin/python3
"""
0. Hello Flask!
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def display_hello():
    """
    function to display text
    """
    return 'Hello HBNB!'


if __name__ == '__main__':
    """
    start the aplication on port 5000
    """
    app.run(host='0.0.0.0', port=5000)
