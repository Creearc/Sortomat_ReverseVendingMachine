from flask import Flask, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

state = 'normal'
out = ''
manual = False
aluminium = False

@app.route('/get_state', methods=['GET'])
def get_state():
  global state
  if request.method == 'GET':
    return state

@app.route('/set_state', methods=['POST'])
def set_state():
  global state
  if request.method == 'POST':
    data = request.data
    state = json.loads(data)['state']
    print(state)
    return 'ok'

@app.route('/get_out', methods=['GET'])
def get_out():
  global out
  if request.method == 'GET':
    return out

@app.route('/set_out', methods=['POST'])
def set_out():
  global out
  if request.method == 'POST':
    data = request.data
    out = json.loads(data)['out']
    print(out)
    return 'ok'

@app.route('/get_manual', methods=['GET'])
def get_manual():
  global manual
  if request.method == 'GET':
    return str(manual)

@app.route('/set_manual', methods=['POST'])
def set_manual():
  global manual
  if request.method == 'POST':
    data = request.data
    manual = json.loads(data)['manual'] == 'True'
    print(manual)
    return 'ok'

@app.route('/get_aluminium', methods=['GET'])
def get_aluminium():
  global aluminium
  if request.method == 'GET':
    return str(aluminium)

@app.route('/set_aluminium', methods=['POST'])
def set_aluminium():
  global aluminium
  if request.method == 'POST':
    data = request.data
    aluminium = json.loads(data)['aluminium'] == 'True'
    print(aluminium)
    return 'ok'
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000, debug=True)
