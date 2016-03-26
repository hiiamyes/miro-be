from flask import Flask, jsonify
from flask.ext.cors import CORS

from miro import Miro

app = Flask(__name__)
CORS(app)

@app.route('/<string:sentence>', methods=['GET'])

def get_music(sentence):
    song = Miro(sentence)
    return jsonify(song)

if __name__ == '__main__':
    app.run()
