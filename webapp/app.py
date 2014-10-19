

import flask
import argparse
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

from analyser.music_analyser import analyse_wav_url 


app = flask.Flask(__name__)



@app.route("/")
def index():
    """
    When you request the root path, you'll get the index.html template.

    """
    
    default_url = 'https://s3-eu-west-1.amazonaws.com/music-analysis/rise like a phoenix beginning.wav'
    return flask.render_template("index.html", default_url = default_url)




 


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
    try:
        url = flask.request.form["url"]
        
        if not url.startswith("http://") and not url.startswith("https://")  :
            raise Exception('Invalid URL, url start with http/https required')
        #print url
        #payload = '{}'
        payload = analyse_wav_url(url, 1024*1024)
        
        return payload
    except:
        flask.abort(400)
        pass
    



    
    
    
    

if __name__ == "__main__":
    import os

    port = 8000
    
    app.debug = True
    app.run(port=port, debug=True)