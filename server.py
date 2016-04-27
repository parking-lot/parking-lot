from pb_simulation import *
from time import sleep
from flask import Flask, redirect
from sys import exit

app = Flask(__name__, static_url_path='')

time = 0
sim = Simulation()
sim.load_map_from_file("walls.old")
sim.setOutputFileName("walls.log")

@app.route('/')
def index():
    return redirect("visualizer.html", code=302)

@app.route('/enter/<entrance>/<goal>/<pref>/')
def enter(entrance, goal, pref):
    return str(sim.addCars(int(entrance), int(goal), int(pref)))

@app.route('/directions/<id>/')
def directions(id):
    return str(sim.carDirections(int(id)))

@app.route('/leave/<id>/')
def leave(id):
    return str(sim.requestToLeave(int(id)))

@app.route('/test')
def test():
    return 'ok'

@app.route('/stop')
def stop():
    sim.sanitizeOutputFile()
    sim.closeOutputFile()
    return 'ok'

@app.route('/beat')
def beat():
    sim.advanceTimeStep()
    sim.output()

if __name__ == '__main__':
    app.debug = True
    app.run(host='stingray')
