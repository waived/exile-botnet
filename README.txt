██████████████████      ██  ██████  ██      ██  ██████      ██████████████
█████████████████  ████████  ██   █████  ████  ██████  ███████████████████
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓▓▓▓    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒   ▒  ▒▒▒▒▒▒  ▒▒▒▒  ▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
░░░░░░░░░░░░░░      ░░   ░░░░░  ░░      ░░      ░░      ░░░░░░░░░░░░░░░░░░
──────────────────────────────────────────────────────────────────────────
                                  ABOUT
──────────────────────────────────────────────────────────────────────────
Program: Exile Botnet (server + client) / Proof-of-Concept
Server version: 3.0
Client version: 19.0

Languages: Python 3.11.9
           Shell BASH/SH

Tested on: KaOS amd64 minimal-2024
           Kali Linux 2024.1
           Ubuntu 24.01
           Microsoft Windows 11 (Version 23H2)
           
C2 communication method: TCP sockets
           
Effected platforms: Linux/Unix environments
           
Author: Waived
──────────────────────────────────────────────────────────────────────────
                               CAPABILITIES 
──────────────────────────────────────────────────────────────────────────

--- Denial-of-Service
    ExileBot weilds a total of fourteen different attack vectors, based on
    standard UDP, TCP, and the HTTP protocol.
    
--- Binary Loader
    Exile also acts as a loader, where C, PY, SH, and ELF files can be
    loaded and executed on the client machines.
    
--- C2 manipulation
    Like any bot/loader, Exile's C2 infrastructure allows for TCP connection
    manipulation: termination of connections, refreshing of connections, and
    disconnection from TCP connections. Additionally, ExileBot provides the
    option to update the current running client with a more recent build. 
    
--- Self-replication
    Once a client/s are connected to the C2, at the command of the botmaster,
    said client/s can then begin scanning the internet for hosts that are
    running SSH and Telnet services. Via password spraying of commonly used
    credentials, ExileBot attempts to hijack a session and inject a copy of
    the client onto said machines. This allows for Exile to gain a wider scope
    of connected machines.
    
--- Anti-viral manuvers
    Exile makes use of a BotKiller, or routine that will check for suspicious
    processes that are known to belong to other Bots, Loaders, Vertexes, etc.
    
──────────────────────────────────────────────────────────────────────────
                             ATTACK FUNCTIONS 
──────────────────────────────────────────────────────────────────────────
--- UDP: 
    Standard junk flood via UDP. Dynamic data buffer with non-fixed length.

--- TCP:
    Standard junk flood via TCP. Dynamic data buffer with non-fixed length.

--- RHEX:
    UDP flood using random hexadecimal values. Dynamic data buffer with non-
    fixed length. Effective against some OVH-based services.
    
--- HTTPBYPASS:
    An HTTP-GET flood that implements proxification per each request. HTTP
    headers such as User-agent, Referer, and URI query are randomized. 
    Effective against CDNs, WAFs, and other reverse-proxy implementations.
    
--- HOLD:
    Much like the 'Xerxes' attack, a HOLD flood will open a series of TCP
    sockets. After the user-specified delay has passed, a null byte '\x00'
    will be send through the sockets to keep them alive. If used against
    single thread-based socket spawning services such Apache Tomcat, 
    Microsoft IIS, dhttpd Dart, etc, one machine can take a server down.
    However, HTTP services such as NGINX can manage this quite well. In
    terms of a botnet, will several hundred if not several thousand clients
    requesting socket-connections all at once, even such service can be
    crippled. Effectivity in lies on the amount of clients connected to Exile.
    
--- RECOIL:
    Originally taken from NewEraCracker's LOIC HiveMind edition, the ReCoil
    flood is a slow-download attack via HTTP. The botmaster will find a site
    that is hosting a relatively large file. Once the download on the client
    machine has started, each byte is streamed to the client over the TCP
    socket very slowly. The botmaster will specify the delay in seconds before
    receiving the next byte in the sequence. Alike the HOLD flood, the more
    clients acting against the specific file will yield a greater ability to
    paralyze the target.
    
--- STDHEX:
    Modeled off of the well known STD.c attack, and STD packet via UDP, using
    hexadecimal values will be send to the target. The data-buffer in each
    UDP packet will not exceed 50 bytes, however this method is a PPS dependent
    flood, where the volume to requests are hurled at the target in a rapid
    succession.
    
--- QUAKE3:
    A UDP-based attack that effects Quake V3 gaming servers. Each packet makes
    use of QUAKE3 query vulnerabilities.
    
--- HTTP:
    Standard HTTP flood with user-agent randomization and keep-alive headers.
    TCP socket responsible for sending the HTTP headers will remain open until
    forcibly closed by the endpoint. Upon closure, more sockets are spawned 
    until duration is complete or cancelled by the botmaster.
    
--- FIVE-M:
    A UDP-based attack that effects GTA-V (Grand Theft Auto 5) modding game-
    servers. Each packet makes use of FIVE-M query vulnerabilities.
    
--- HTTPHEX:
    An HTTP-GET flood that appends junk hexadecimal payloads at the end of
    each HTTP request. User-agent randomization and keep-alive headers are
    sent.
    
--- TLS:
    This attack attempts to exhaust SSL/TLS slates on HTTPS protected
    websites. It begins the TLS encryption process, then drops the connection
    and quickly spawns a new TLS agreement. This process is done repeatedily
    over the same TCP socket until forcibly closed by the endpoint. Upon 
    closure, more sockets are spawned until duration is complete or cancelled
    by the botmaster. 
    
--- VSE:
    This UDP-based attack manipulates the VSE (Value Source Engine) protocol
    on game-servers ran by the gaming platform Steam. Each packet makes use 
    of VSE query vulnerabilities.
    
--- TS3:
    This UDP-based attack manipulates the TS3 (Team Speak Ver3.0) protocol
    on TS3-servers. Each packet makes use of TS3 query vulnerabilities.
──────────────────────────────────────────────────────────────────────────
                             NOTABLE FEATURES 
──────────────────────────────────────────────────────────────────────────
SERVER:
=======
Clear:
Simply put, this command will clear the terminal environment of Exile to
allow for a more clear working interface.

Goodbye:
This command was designed to eliminate the <CTRL+C> abort feature in
Python and to safely power-down the TCP Listener and other currently
running routines.  

V&:
The V& ("vanned") command is a panic feature. Once executed, Exile
will terminate all client connection via the "uninstall" command.
It also will self terminate (via BASH) by deleting the active
server.py script.

Be careful! There is no confirmation when processing this request!

=======
CLIENT:
=======

Resurrection:
Upon execution, the client will locate the Linux/Unix CronTab (if supported)
and will (via BASH) add itself to the CronTab. Per every reboot, Exile will
reconnect to the C2.

Connection management:
Exile will take commands from the C2 in regards to the active TCP connection
running on the machine. At any given point, the client wields the ability
to either restart the connection to the C2, drop it entirely, or "uninstall"
which not only drops the connection but (via BASH) will self-destruct the client
script entirely.

Verbose output:
Since ExileBot serves as a POC and for the purpose of dev-testing, the client
will output verbose information after connecting/reconnection to the C2 and
when processing commands.

SERVER:
=======
    
──────────────────────────────────────────────────────────────────────────
                           KNOWN BUGS / ISSUES
──────────────────────────────────────────────────────────────────────────
ExileBot aims to make multi-platform Linux/Unix use smooth and compatible
with as many systems as possible. It is possible that due to certain system
limitations or lack of permissions, ExileBot is unable properly process a
command. At any point be sure to leave a bug report!

Keyboard Interrupt:
Whereas the 'disconnect' command from the C2 functions flawlessly, using the
keyboard interrupt <CTRL+C> maybe yeild an interrupt-error when breaking. This
doesn't necessarily need handeled since the client should run silently on the
infected machine without hinderance.

Disconnect:
Because of certain activity during data transversal, taking the 'disconnect' 
command from the C2 may not exit immediately. The TCP socket may hang for
up to another 30 seconds before exiting. This is more of a performance issue
rather than an actual bug.

Anything else that may arise during execution of ExileBot that does not
work correctly, please leave a bug report.

──────────────────────────────────────────────────────────────────────────
                              AUTHOR'S NOTES
──────────────────────────────────────────────────────────────────────────
Python is an interpreted language, NOT compiled! This means two things:

    1) Since Python is interpreted, it is slower than other compiled
       languages like C, Delphi, GoLang, etc. It may not be as suitable
       in the field for this reason alone.
       
    2) Because ExileBot is not compiled, the server/client can simply be
       opened up/viewed. There is no ability to hide the C2 connections
       within the code. This may requires some level of third-party
       obfuscation.

Additionally, there is no level of encryption/encoding between the server
and clients. Having encryption would be a beneficial feature to have when
conducing illicit activities. I felt no reason to include such a feature.

──────────────────────────────────────────────────────────────────────────
                              LEGAL STATEMENT
──────────────────────────────────────────────────────────────────────────
By downloading, modifying, redistributing, and/or executing ExileBot, the
user agrees to the contained LEGAL.txt statement found in this repository.

I, Waived, the creator, take no legal responsibility for unlawful actions
caused/stemming from this program. Use responsibly and ethically!
