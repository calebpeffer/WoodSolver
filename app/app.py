from flask import Flask, request, jsonify, render_template
import json
# from flask_socketio import SocketIO, emit

from WoodSolver2 import *

app = Flask(__name__)

@app.route("/")
def session():
    return render_template("input_form.html")

@app.route("/solve", methods=['POST'])
def woodsolver():
    pieces_raw = request.form["pieces"]
    print(str(pieces_raw))
    pieces_lis = parse_input(pieces_raw)
    print(pieces_lis)
    solver = WoodSolver2(pieces_lis)
    solver.pick_pieces()
    printout = str(solver)
    return json.dumps({'status':'OK', 'teststring':printout})
    
    
    # default_length = request.form("default_lengths")


def parse_input(in_string):
    in_string = in_string.split(", ")
    outlist = list() 
    for item in in_string:
        try:
            outlist.append(int(item))
        except:
            print("invalid input")
    return outlist
            
if __name__ == "__main__":
    app.run(debug=True)
    #  socketio.run(app)