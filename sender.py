from socket import *
import random
import sys
import time


'''simulate random arrival time of packets.  When a packet is sent, 
the send is followed immediately by a call to this random number generator.  The pseudo 
random number returned will be interpreted as the delay in seconds before the next 
packet will be generated.'''
def rand_arrival_time():
    return random.uniform(0.0, 4.9)

'''used to determine if an ACK and NACK that has just arrived 
has been corrupted.  This instance of the pseudo random number generator random 
should generate uniformly distributed pseudo random numbers between [0.0 and 1.0).  
If the number generated is less that the input value of the probability that an ACK or NACK 
packet has been be corrupted, then the ACK or NACK packet that has just arrived will be 
considered to be corrupted.'''
def rand_corrupted():
    return random.random


def main():
    try:
        arrival_time_seed = sys.argv[1]
        num_packets = sys.argv[2]
        corrupted_seed = sys.argv[3]
        corruption_prob = sys.argv[4]
    except(IndexError) as e:
        print(type(e).__name__, e.args, '\nPlease provide 4 arguments')
        exit

    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_port = 2048
    server_name = '127.0.0.1'
    server_port = 50007

    # Send 4 packets (filler for now)
    packet_list = [0, 0, 0, 0]

    # TODO: figure out how ACK and NACK work with packets and sockets
    
    for item in packet_list:
        client_socket.sendto(item, (server_name, server_port))
        time.sleep(rand_arrival_time()) 
        
        returned_message, server_address = client_socket.recvfrom(2048)

    client_socket.close()


if __name == '__main__':
    main()