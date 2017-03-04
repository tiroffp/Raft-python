import socket
import json
import pickle
import uuid

from messages import *

class client(object):
    cnt = 0
    def __init__(self):
        client.cnt = client.cnt+1
        self.id = client.cnt
        self.num_of_reply = 0 

    def buyTickets(self, port, buy_msg, uuid):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = Request(buy_msg, uuid)
        s.sendto(pickle.dumps(msg), ("", port))
        while 1:
            reply, addr = s.recvfrom(1024)
            if reply != '':
                self.num_of_reply += 1
                print(reply)
            if self.num_of_reply == 2:
                break
        s.close()

    def show_state(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = Request('show')
        s.sendto(pickle.dumps(msg),("",port))
        while 1:
            reply, addr = s.recvfrom(1024)
            if reply != '':
                print 'Pool Size', reply
                break

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)
    ports = config['AddressBooks']
    num_ports = len(ports)
    while True:
        customer = client()
        server_id = input('Which datacenter do you want to connect to? 1-%d: ' % num_ports )
        request = raw_input('How can we help you? --')
        if request == 'show':
            customer.show_state(ports[server_id - 1])
        else:
            uuid_ = uuid.uuid1()
            customer.buyTickets(ports[server_id - 1], request, uuid_)

if __name__ == '__main__':
    main()