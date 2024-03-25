import socket

def main():
    #创建一个套接字TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #连接服务器
    client.connect(('10.116.40.73', 6789))
    while(True):
        #输入发送的数据
        data = input("发送的数据为:")
        if data == 'end':
            break
        #发送数据       
        client.send(data.encode('utf-8')) #发送的数据为encode转换为二进制b
    #关闭客户端 
    client.close()

if __name__=="__main__":
    main()
