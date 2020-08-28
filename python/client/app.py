import sys
import os
from pathlib import Path

proto_path = os.path.join( str(Path(os.getcwd()).parents[1]), "protos")
sys.path.insert(1, proto_path)



from flask import Flask
from flask import jsonify
app = Flask(__name__)

import grpc

import service_pb2
import service_pb2_grpc

def obj_to_dict(obj):return obj.__dict__

@app.route('/add/<a>/<b>')
def add(a,b):
    print("Start service")
    try:
        channel = grpc.insecure_channel('localhost:4040')
        stub = service_pb2_grpc.AddServiceStub(channel)

        req  = service_pb2.Request(a=int(a), b = int(b))

        response = stub.Add( req )

        return jsonify({
            "result": response.result,
        })

    except Exception as e:
        print(e)
        return e

@app.route('/multiply/<a>/<b>')
def multiply(a,b):
    try:
        channel = grpc.insecure_channel('localhost:4040')
        stub = service_pb2_grpc.AddServiceStub(channel)

        req  = service_pb2.Request(a=int(a), b = int(b))

        response  = stub.Multiply(req)

        return jsonify({
            "result": response.result,
        })
    except Exception as e:
        print(e)
        return e

if __name__ == '__main__':
    app.run()