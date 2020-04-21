#!/usr/bin/python3
from models import storage
from flask import Flask, render_template
app = Flask(__name__)
my_storage = storage.all()


@app.teardown_appcontext
def close_db(error):
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    state_list = []
    for key, vval in my_storage.items():
        if 'State' in key:
            state_list.append(my_storage[key])
    return render_template('7-states_list.html', state_list=state_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
