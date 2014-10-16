"""
This file is part of the flask+d3 Hello World project.
"""

import flask
import argparse
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

from analyser.music_analyser import analyse_wav_file 


app = flask.Flask(__name__)
wav_path = '/tmp/music_analyser/'


@app.route("/")
def index():
    """
    When you request the root path, you'll get the index.html template.

    """
    #print "love"
    #wav_files = [ f for f in os.listdir(wav_path) if os.path.isfile(os.path.join(wav_path, f)) and f.endswith('.wav') ]
    wav_files = []
    return flask.render_template("index.html", wav_files = wav_files)




 


@app.route("/analyse/", methods=["POST","GET"])
def analyse():
    """
    On request, this returns a list of ``ndata`` randomly made data points.

    :param filename: 
        wav file to load

    :returns data:
        A JSON with
          note_names: array of note names
          time_values:  array of time in seconds
          active_notes:  whether note n is detected at time interval t

    """
    #print "hello"
    filename = flask.request.form["filename"] 
    #print filename
       
    payload = analyse_wav_file(os.path.join(wav_path, filename))
    
    return payload
    #return filename


def get_args():
    
    global wav_path
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--wavpath", default=wav_path)
    args = parser.parse_args()
    wav_path = args.wavpath
    
    
    
    

if __name__ == "__main__":
    import os

    port = 8000
    #get_args()
    # Open a web browser pointing at the app.
    #os.system("open http://localhost:{0}".format(port))

    # Set up the development server on port 8000.
    app.debug = True
    app.run(port=port, debug=True)