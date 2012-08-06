import paramiko,os,getpass,time

def addpub(local,server):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server['host'], int(server['port']),server['username'], server['password'])
        ssh.exec_command('python ~/pub_deploy_server.py')
        time.sleep(0.1)
        ssh.exec_command('rm -f ~/pubkey.pub')
        ssh.exec_command('rm -f ~/pub_deploy_server.py')
        ssh.close()
        print 'Your public key has been added to senrver authorized_keys'
    except paramiko.SSHException, e:
        print e

def uploadpub(local,server):
    transport=paramiko.Transport((server['host'],int(server['port'])))
    transport.connect(username=server['username'],password=server['password'])
    sftp=paramiko.SFTPClient.from_transport(transport)
    remotefile1=''.join(['/home/',server['username'],'/','pubkey.pub'])
    localfile1=local['publickey']
    sftp.put(localfile1,remotefile1)
    remotefile2=''.join(['/home/',server['username'],'/','pub_deploy_server.py'])
    temp=__file__.split('/')
    temp[-1]='pub_deploy_server.py'
    serverfile='/'.join(temp)
    localfile2=serverfile
    sftp.put(localfile2,remotefile2)
    sftp.close() 
    transport.close()
    print "Trandfer has done"

def infoinput(local,server):
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
    return (local,server)
    
def main():
    local={'known_host':os.path.expanduser("~/.ssh/known_hosts"),
           'compressfile':os.path.expanduser('~/pubkey.zip'),
           'publickey':''}
    server={'host':"",'port':'','username':"",'password':""}
    while True:
        local,server=infoinput(local,server)
        uploadpub(local,server)
        addpub(local,server)
        goon=raw_input("Do you have other server to deploy public key('y'or 'n'):")
        if goon=='n' or goon=='N':
            print('Thanks for using,see you next time')
            break
main()