package main

import (
	"context"
	"../protos"
	"net"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"

)

type server struct{}

func main(){
	listener, err := net.Listen("tcp", ":4040")

	if err != nil {
		panic(err)
	}

	srv := grpc.NewServer()

	proto.RegisterAddServiceServer(srv, &server{})
	reflection.Register(srv)

	if e:= srv.Serve(listener); e != nil {
		panic(e)
	}
}


func (s *server ) Add(context context.Context, request *proto.Request) (*proto.Response, error){
	var a = request.GetA()
	var b = request.GetB()

	result := a + b

	return &proto.Response{Result: result}, nil
}

func (s *server ) Multiply(context context.Context, request *proto.Request) (*proto.Response, error){
	var a = request.GetA()
	var b = request.GetB()

	result := a * b

	return &proto.Response{Result: result}, nil
}