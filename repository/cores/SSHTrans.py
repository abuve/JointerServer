from conf.settings import web_conf_path
from conf import settings

import paramiko


class SSHConnection(object):
    def __init__(self, port=settings.ssh_port, username=settings.ssh_username):
        self.port = port
        self.username = username
        self.__key = settings.ssh_key_file
        self.__key_pass = settings.ssh_key_pass
        self.__nginx_conf_path = settings.web_config_nginx_path

    def run(self, host_ip):
        self.connect(host_ip)  # 连接远程服务器
        self.cmd('df')  # 执行df 命令
        self.close()  # 关闭连接

    def push_webconf_files(self, host_ip, s_dir, d_dir):
        self.connect(host_ip)  # 连接远程服务器
        # 删除目录
        self.cmd('/bin/rm -fr %s/*' % d_dir)
        # 上传压缩目录
        self.upload(s_dir, d_dir)
        # 解压缩
        self.cmd('cd %s && /usr/bin/unzip nginx.zip && /bin/rm -f nginx.zip' % d_dir)

        # self.upload("D:/nginx_test", '/tmp/nginx')  # 将本地的db.py文件上传到远端服务器的/tmp/目录下并改名为1.py
        self.close()  # 关闭连接

    def connect(self, host_ip):
        private_key = paramiko.RSAKey.from_private_key_file(self.__key, password=self.__key_pass)
        transport = paramiko.Transport((host_ip, self.port))
        transport.connect(username=self.username, pkey=private_key)

        self.__transport = transport

    def close(self):
        self.__transport.close()

    def upload(self, local_path, target_path):
        print(local_path, target_path)
        try:
            sftp = paramiko.SFTPClient.from_transport(self.__transport)
            sftp.put(local_path, '%s/nginx.zip' % target_path)
        except Exception as e:
            print(Exception, e)

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        return result

def test():

    private_key = paramiko.RSAKey.from_private_key_file(settings.ssh_key_file, password=settings.ssh_key_pass)
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname='192.168.10.231', port=2556, username='snadmin', pkey=private_key)
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command('df')
    # 获取命令结果
    result = stdout.read()
    print(result)
    # 关闭连接
    ssh.close()

if __name__ == '__main__':
    obj = SSHConnection()
    obj.run('118.193.185.33')