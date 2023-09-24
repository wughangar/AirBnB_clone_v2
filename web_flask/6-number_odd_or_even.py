#!/usr/bin/python3
"""
6. Odd or even?
"""

import re
from flask import Flask
from flask import render_template, abort
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


@app.route('/number/<int:n>', strict_slashes=False)
def is_int(n):
    """
    check if n is an int
    """
    if isinstance(n, int):
        return f"{n} is a number"
    else:
        return "Not a valid integer"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    render template function
    """
    if isinstance(n, int):
        return render_template('5-number_template.html', n=n)
    else:
        abort(404)


@app.route('/number_template/<int:n>', strict_slashes=False)
def odd_even(n):
    """
    function to check if its odd or even
    """
    if isinstance(n, int):
        ans = "even" if n % 2 == 0 else "odd"
        return (render_template('6-number_odd_or_even.html', n=n, ans=ans))
    else:
        abort(404)


if __name__ == '__main__':
    """
    start the aplication on port 5000
    """
    app.run(host='0.0.0.0', port=5000)
