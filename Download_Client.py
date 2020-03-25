import socket

COD = 'utf-8'
HOST = 'localhost' # 主机ip
# HOST = '119.28.41.16';
PORT = 9090 # 软件端口号

class download():
    tcp_server_socket = None
    new_socket = None
    ip_port = None
    recv_data = None
    def __init__(self,host,port):
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.connect((HOST, PORT))
       
        # # 创建TCP套接字
        # tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # # 链接服务器
        # tcp_socket.connect((HOST, PORT))
        # # 获取下载的文件的名字
        # download_file_name = input("请输入要下载的文件名字：")
        # # 将文件名字发送到服务器
        # tcp_socket.send(download_file_name.encode("utf-8"))
        # # 接收文件中的数据
        # recv_data = tcp_socket.recv(1024)
        # if recv_data:
        #     # 保存接收到的数据到一个新的文件中
        #     with open("[新]" + download_file_name, "wb") as f:
        #         f.write(recv_data)
        # # 关闭套接字
        # tcp_socket.close()

    def gitClone(self,url):
        self.tcp_server_socket.send(url.encode("utf-8"))
        while True:
            try:
                data = self.tcp_server_socket.recv(1024)
                print('从服务器收到的内容:',data)
            except Exception:
                print("断开链接")
                break
            if not data:
                break
        self.tcp_server_socket.close()

if __name__ == '__main__':
    go = download(HOST,PORT)
    go.gitClone('https://github.com/IU2099/test.git')
    #go.gitClone('https://github.com/IU2099/Personal.git')