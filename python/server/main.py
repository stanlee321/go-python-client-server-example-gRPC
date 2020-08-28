import sys
import os
from pathlib import Path

proto_path = os.path.join( str(Path(os.getcwd()).parents[1]), "protos")
sys.path.insert(1, proto_path)

import service_pb2
import service_pb2_grpc

import sys
import time
import os
import grpc


from concurrent import futures

class AddService(service_pb2_grpc.AddServiceServicer):
    
    def Add(self, request, content):
        a = request.a
        b = request.b

        result = a + b

        return service_pb2.Response(result = result)

    def Multiply(self, request, content):
        a = request.a
        b = request.b

        result = a * b

        return service_pb2.Response(result = result)

if __name__ == '__main__':
    port = sys.argv[1] if len(sys.argv) > 1 else 4040
    
    host = '[::]:%s' % port

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    
    keys_dir = os.path.abspath(os.path.join('..', os.pardir, "python", 'keys'))
    
    with open('%s/private.key' % keys_dir, 'rb') as f:
        private_key = f.read()

    with open('%s/cert.pem' % keys_dir, 'rb') as f:
        certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain),))
    #server.add_secure_port(host, server_credentials)
    server.add_insecure_port(host)
    service_pb2_grpc.add_AddServiceServicer_to_server(AddService(), server)
    
    try:
        server.start()
        print('Running Discount service on %s' % host)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)