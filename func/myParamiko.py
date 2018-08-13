# coding:utf8
# import paramiko

class myParamikoClass():

    def __init__(self,password=None,port=22,*,username,hostname):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.conn(hostname,port,username,password)

    def conn(self,hostname,port,username,password):
        if password:
            self.ssh.connect(hostname=hostname,port=port,username=username)
        else:
            self.ssh.connect(hostname=hostname,port=port,username=username,password=password)

    def execute(self,cmd):
        stdin,stdout,stderr = self.ssh.exec_command(cmd)
        result = stdout.read()
        print(str(result,encoding='utf8'))

    def download(self,remote_path,local_path):
        sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        sftp.get(remote_path,local_path)

    def upload(self,local_path,target_path):
        sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        sftp.put(local_path,target_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ssh.close()


if __name__ == "__main__":
    import sys
    print(sys.argv)
    # with myParamikoClass(username="hdfs",hostname="47.98.99.192") as mp:
    #     mp.execute("ls")
    #     mp.download("~/xw/1_sample.py","k.py")
    # # coding:utf8
    # from datetime import datetime
    # import subprocess
    # cmd = "scp -r hdfs@47.98.99.192:/home/hdfs/hdfs_dir/sale_predict/xgboost/train_{0} ~/hdfs_dir/xgboost/".format(str(datetime.now())[:10].replace("-",""))
    # print cmd
    # #p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # retcode = subprocess.call(cmd,shell=True)
    # print retcode
    # ssh = myParamikoWithFileClass(username="hdfs",hostname="10.10.10.121")
    # ssh.connect()
    # ssh.execute("ls")
    # # ssh.download("~/xw/1_sample.py","./")
    # ssh.close()