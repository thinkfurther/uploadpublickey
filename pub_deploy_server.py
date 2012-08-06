import os
if not os.path.exists(os.path.expanduser('~/.ssh/')):
    os.system('mkdir ~/.ssh')
if os.path.isfile(os.path.expanduser('~/.ssh/authorized_keys')):
    clientkeyfile=open(os.path.expanduser('~/pubkey.pub'))
    clientkey=clientkeyfile.read()
    authkeyfile=open(os.path.expanduser('~/.ssh/authorized_keys'))
    found=0
    for authkey in authkeyfile:
        if authkey==clientkey:
            found=1
            break
        else:
            found=0
    if found==0:
        os.system('cat ~/pubkey.pub >> ~/.ssh/authorized_keys')
else:
    os.system('cat ~/pubkey.pub > ~/.ssh/authorized_keys')

os.system('chmod 0700 ~/.ssh')
os.system('chmod 0600 ~/.ssh/authorized_keys')    