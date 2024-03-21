import socket

target_ip = "127.0.0.1"
target_port = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello, UDP Server!"

sock.sendto(message.encode(), (target_ip, target_port))

sock.close()