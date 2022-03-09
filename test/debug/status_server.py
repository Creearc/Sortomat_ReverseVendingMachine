from flask import Flask, request, redirect, url_for, jsonify
import json
import requests
import os

app = Flask(__name__)

@app.route('/status', methods=['POST'])
def question_page():
  if request.method == 'POST':
    data = request.data
    info = json.loads(data)['status']
    print(info)
    if len(info.split(':')) == 6:
      filename = '{}.eye'.format(info.replace(':', '@'))
      if os.path.isfile(filename):
        f = open(filename, 'r')
        answer = f.read()
        f.close()
      else:
        f = open(filename, 'w')
        f.write('1')
        f.close()
        answer = 1
        
    return jsonify({'status' : answer})

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=56088, debug=True)
