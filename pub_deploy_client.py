import paramiko,os,pexpect,zipfile,getpass
homefolder=os.path.expanduser("~/")

def addpub(local,server):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server['host'], int(server['port']),server['username'], server['password'])
        ssh.exec_command('unzip ~/pubkey.zip -d ~/pubkey/')
        ssh.exec_command('python ~/pubkey/pub_deploy_server.py')
        #ssh.exec_command('python ~/pubkey/pub_deploy_server.py')
        ssh.exec_command('rm -f ~/pubkey.zip')        
        ssh.exec_command('rm -rf ~/pubkey/')
        os.system('rm -f ~/pubkey.zip')
        ssh.close()
        print 'Your public key has been added to server authorized_keys'
    except paramiko.SSHException, e:
        print e

def uploadpub(local,server):
    srv=zipfile.ZipFile(os.path.expanduser('~/pubkey.zip'),'w')
    temp=__file__.split('/')
    temp[-1]='pub_deploy_server.py'
    serverfile='/'.join(temp)
    srv.write(serverfile,'pub_deploy_server.py')
    srv.write(local['publickey'],'publickey.pub')
    srv.extractall(os.path.expanduser('~/1'))
    srv.close()
    cmd="scp -P %s %s %s@%s:~/" %(server['port'],local['compressfile'],server['username'],server['host'])
    try:
        scp=pexpect.spawn(cmd)  
        i=scp.expect(['password:', 'continue connecting (yes/no)?'],timeout=5)
        if i == 0:
            scp.sendline(server['password'])
        elif i == 1:
            scp.sendline("yes")
            scp.expect(['password:'])  
            scp.sendline(server['password']) 
        scp.expect(pexpect.EOF)
        scp.close()
        print "Trandfer has done"
    except pexpect.TIMEOUT:  
        print 'Connection timeout'  
    except pexpect.EOF:
        print 'Trandfer connection exit'  
        scp.close()  
    except Exception,e:  
        print "Connection close",e
        scp.close()
        
def main():
    local={'known_host':os.path.expanduser("~/.ssh/known_hosts"),
           'compressfile':os.path.expanduser('~/pubkey.zip'),
           'publickey':''}
    server={'host':"115.156.219.152",'port':'22','username':"root",'password':"AP@ssw0rd"}
    while True:
        while True:
            server['host']=raw_input('please input server ip:')
            if not server['host']:
                print 'You do not input ip,please reinput'
                continue     
            else:
                break
        while True:
            server['port']=raw_input('please input server ssh port(default for 22):')
            if not server['port']:
                server['port']='22'
            break
        while True:
            server['username']=raw_input('please input login username:')
            if not server['username']:
                print 'You do not input username,please reinput'
                continue     
            else:
                break        
        while True:
            server['password']=getpass.getpass('please input login password:')
            if not server['password']:
                print 'You do not input password,please reinput'
                continue     
            else:
                break     
        while True:
            if local['publickey']:
                break
            else:
                local['publickey']=raw_input('please input where your public key is(absolute path):')
                if not local['publickey']:
                    print 'You do not input you public file,please reinput'
                    continue
                else:
                    break
        uploadpub(local,server)
        addpub(local,server)
        goon=raw_input("Do you have other server to deploy public key('y'or 'n'):")
        if goon=='n' or goon=='N':
            print('Thanks for using,see you next time')
            break
main()