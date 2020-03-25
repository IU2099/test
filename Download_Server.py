import socket
import git
import threading
import time
import re
import os
import shutil
import zipfile #引入zip管理模块
import threading

event = threading.Event()

COD = 'utf-8'
HOST = 'localhost' # 主机ip
# HOST = '119.28.41.16';
PORT = 9090 # 软件端口号
BUFSIZ = 1024
ADDR = (HOST, PORT)
SIZE = 10 

PATH = os.getcwd()
DOWNPATH = PATH + 'download'
print(PATH)

#定义一个函数，递归读取absDir文件夹中所有文件，并塞进zipFile文件中。参数absDir表示文件夹的绝对路径。
def writeAllFileToZip(absDir,zipFile):
    for f in os.listdir(absDir):
        absFile=os.path.join(absDir,f) #子文件的绝对路径
        if os.path.isdir(absFile): #判断是文件夹，继续深度读取。
            relFile=absFile[len(os.getcwd())+1:] #改成相对路径，否则解压zip是/User/xxx开头的文件。
            zipFile.write(relFile) #在zip文件中创建文件夹
            writeAllFileToZip(absFile,zipFile) #递归操作
        else: #判断是普通文件，直接写到zip文件中。
            relFile=absFile[len(os.getcwd())+1:] #改成相对路径
            zipFile.write(relFile)
    return

class Progress(git.remote.RemoteProgress):
    def update(self):
        print (self._cur_line)
    # def update1(self, op_code, cur_count, max_count=None, message=''):
    #     print ('Download(%s, %s, %s, %s)'%(op_code, cur_count, max_count, message))

class download():
    tcp_server_socket = None
    new_socket = None
    ip_port = None

    def __init__(self,host,port):
        # 1. 创建tcp服务端套接字对象
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口号复用，通俗理解程序退出端口号立即释放
        # 1. SOL_SOCKET表示当前套接字
        # 2. SO_REUSEADDR表示复用选项
        # 3. 是否复用，True表示复用
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 2. 绑定端口号, "localhost"： 表示本机， 8989： 端口号
        self.tcp_server_socket.bind((host, port))
        # 3. 设置监听, 128: 表示最大等待的连接个数
        self.tcp_server_socket.listen(128)
        self.start()

    def start(self):
        while True:
            print("服务器启动，监听客户端链接")
            # 4. 等待接受客户的连接请求
            self.new_socket,self.ip_port = self.tcp_server_socket.accept()
            print("链接的客户端:", self.ip_port)
            
            while True:
                try:
                    data = self.new_socket.recv(BUFSIZ) # 读取已链接客户的发送的消息
                except Exception:
                    print("断开的客户端", self.ip_port)
                    break
                if not data:
                    print("断开的客户端", self.ip_port)
                    break
                print("客户端发送的内容:",data.decode(COD))
                # 对二进制数据进行解码
                t = time.strftime("%Y-%m-%d %X") #获取结构化事件戳
                print("时间戳:",t)
                msg = '[%s]:%s' % (t, data.decode(COD))
                self.urlCheck(data.decode(COD))
                self.send(msg) #发送消息给已链接客户端

       
    def close(self):
        # 服务端的套接字关闭，不再提供连接服务
        self.tcp_server_socket.close()

    def send(self,msg):
        # 对字符串进行编码
        data = msg.encode(COD)
        # 发送给客户端的数据
        self.new_socket.send(data)
        # 关闭和客户端通信的socket
        # self.new_socket.close()
        return True

    def gitClone(self,url,callback):
        self.fileName = url[url.rfind('/')+1:url.rfind('.git')]
        path = PATH+'\\git\\'+self.fileName
        if os.path.exists(path) == False:
            print('gitClone Start: ',url)
            clone = git.Repo.clone_from(url,path, progress=Progress())
            print('gitClone End: ',clone)
        print('gitClone is exist:')
        callback()
        return

    def zipDir(self):
        print('压缩 Start: ',self.fileName)
        path = PATH+'\\git\\'+self.fileName

        print('path: ',path)
        # re = shutil.make_archive(dirpath,'zip',DOWNPATH)
        #zipFile=zipfile.ZipFile(dirpath,"w",zipfile.ZIP_DEFLATED) 

        #writeAllFileToZip(DOWNPATH,zipFile)

        print('压缩 End : ',re)
        return

    def urlCheck(self,url):
        pattern = r'github'
        if pattern in url :
            print('github')
            self.gitClone(url,self.zipDir)
        return



if __name__ == '__main__':
    s = download(HOST,PORT)
