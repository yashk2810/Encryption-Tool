import os
import sys
from stat import *
from Crypto.Cipher import AES
import os
from Crypto.Protocol.KDF import PBKDF2


def traversetree(top, callback):
    # returns a LIST of files or directories present
    # in the path (in this case 'top')
    dirs = os.listdir(top)
    for files in dirs:
        pathname = os.path.join(top, files)
        # print pathname
        mode = os.stat(pathname)[ST_MODE]

        if S_ISDIR(mode):
            traversetree(pathname, callback)    # It's a directory, recurse into it

        elif S_ISREG(mode):             # It's a file, call the callback function
            key = 'secret message asecret message a'

            # Encryption part
            if sys.argv[1] == '-e':
                print "Encrypting..\n"
                iv = os.urandom(16)
                mode = AES.MODE_CBC
                encryptor = AES.new(key, mode, IV=iv)
                bs = AES.block_size

                f = open(pathname, 'r')
                block = f.read(1024*bs)
                if len(block) % bs != 0:
                    length = 16 - (len(block) % 16)
                    block += '*' * length  # or block+=' '*length
                fw = open(pathname, 'w')
                fw.write(iv+encryptor.encrypt(block))

            # Decryption part

            if sys.argv[1] == '-d':
                print "Decrypting"
                fr=open(pathname,'r')
                chunk=fr.read(1024*16)
                key='secret message a'
                iv = chunk[:16]
                mode = AES.MODE_CBC
                decryptor = AES.new(key, mode, IV=iv)
                fw1=open(pathname,'w')
                #fw1.write(decryptor.decrypt(chunk[16:]))
                original=decryptor.decrypt(chunk[16:])
                fw1.write(original.replace('*',''))

            # the callback function will call 
            # the visitfile function
            callback(pathname)   
        else:
            print "Skipping %s" % (pathname)


def visitfile(file):
    print file

traversetree(sys.argv[2], visitfile)
