from flask import Flask, request, jsonify, render_template
import json
# from flask_socketio import SocketIO, emit

from WoodSolver2 import *

app = Flask(__name__)

@app.route("/")
def session():
    return render_template("input_form.html")

@app.route("/api/solve", methods=['POST'])
def woodsolver():
   
   
    pieces_raw = request.form["pieces"]
    pieces_lis = parse_input(pieces_raw)
    
    options_raw = request.form["options"]
    options_lis = parse_input(options_raw)
    options_lis.sort(reverse=True)

    for piece in pieces_lis: # main input cleaning, conversion to float occurs in parse input method.
        if piece > options_lis[0]: #checks if pieces are too large
            return json.dumps({'status':'OK', 'num_beams': "0", 'solver': "Error: One of your pieces was too large"})
        elif piece <= 0:
            return json.dumps({'status':'OK', 'num_beams': "0", 'solver': "Error: Pieces cannot be zero or negative"})
            
    # print(pieces_lis)
    
    solver = WoodSolver2(pieces_lis, default_beam_length=options_lis[0], alt_beam_length=options_lis[1:])
    printout = solver.convert_to_html()
    return json.dumps({'status':'OK', 'num_beams': solver.num_beams(), 'solver': printout})
    
    
    # default_length = request.form("default_lengths")
def multiply_list(lis):
    val = lis[0]
    for i in lis[1:]: 
        val = val * i
    return val
        

def parse_input(in_string, pieces=True):
    #pieces is passed in to verify that this is being converted to a list of pieces, not a list of options

    in_string = in_string.split(", ")
    outlist = list() 
    for item in in_string:
        # try:
        if "*" in item and pieces: 
            split_lis = [float(num) for num in item.split("*")]
            if pieces:
                multipler = int(multiply_list(split_lis[:-1]))
                for i in range(multipler):
                    outlist.append(float(split_lis[-1]))
            else:
                item = multiply_list([float(num) for num in item.split("*")])
                outlist.append(float(item))
        else:
            outlist.append(float(item))

        # except:
        #     print("invalid input")
    return outlist
            
if __name__ == "__main__":
    app.run(debug=True)
    #  socketio.run(app)