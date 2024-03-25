import socket

#先开服务器

#创建一个套接字
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#绑定IP和端口号
server.bind(('10.116.40.73', 6789))
#开始监听，绑定最大连接数
server.listen(5)

while(True):
    client_socket, client_addr = server.accept()
    print('一个新的客户端到来%s' %str(client_addr))
    while(True):
        #接收client的数据 b
        data = client_socket.recv(1024)
        if data:
            print('recevied: %s' %data.decode('utf-8'))
        else:
            break
    print("本次服务完毕\n等待新的客户端连接\n-------")
    client_socket.close()
server.close()
