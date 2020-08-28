.PHONY: protos
.PHONY: protos_python

protos:
	protoc -I protos/ protos/service.proto --go_out=plugins=grpc:protos/

protos_python:
	python -m grpc_tools.protoc -I=protos/ --python_out=protos/ --grpc_python_out=protos/ protos/service.proto