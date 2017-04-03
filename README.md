# telnet-bruteforce

Installation:

~: sudo pip install -r requirements 
                                                                 
usage: 

    python TelnetScanner.py -t 300

    python TelnetScanner.py -f listip -t 300

Scan default telnet with random ip or a list of ips

optional arguments:

      -h, --help  show this help message and exit

TelnetScanner:

    Options for TelnetScanner

          -t THREAD   number of threads
          
          -f FILE     list ip
  
  
 read result:
 
     ~: tail -f data.log

     ~: cat data.log | grep INFO

