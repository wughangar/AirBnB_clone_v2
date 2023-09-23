#!/usr/bin/python3
"""
3. Python is cool!
"""

import re
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def display_hello():
    """
    function to display text
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """
    function to diapky hbnb
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def text_display(text):
    """
    displays text after replacing _ with spaces
    """
    final_text = re.sub('_', ' ', text)
    return f'C {final_text}'


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """
    displays python text
    """
    final_text = re.sub('_', ' ', text)
    return f'Python {final_text}'


if __name__ == '__main__':
    """
    start the aplication on port 5000
    """
    app.run(host='0.0.0.0', port=5000)
