from socket import *
import random
import sys
import time

def rand_arrival_time():
    return random.uniform(0.0, 4.9)

def rand_corrupted():    
    return random.random()

def makepkt(int_val, seq_num, is_ack, is_nack):
    to_encode = [int_val, seq_num, is_ack, is_nack]
    stringify = [str(x) for x in to_encode]
    to_string = ' '.join(stringify)

    return to_string.encode()

def decode_res(res):
    return res.decode().split(' ')

def before_messages(seq_num, resent, int_val, is_ack, is_nack):
    sent_or_resent = 'resent' if resent else 'sent'
    ack =  1 if is_ack else 0
    nack = 1 if is_nack else 0

    print('A packet with sequence number {0} is about to be {1}'.format(seq_num, sent_or_resent))
    print('Packet to send contains: data = {0} seq = {1} ack = {2} nack = {3}'.format(int_val, seq_num, ack, nack))

def uncorrupted_ack_nack(decode_res):
    ack = decode_res[2]
    nack = decode_res[3]

    if ack:
        print('An ACK packet has just been recieved')
    else:
        print('A NACK packet has just been recieved')
    
    print('Packet received contains: data = {0} seq = {1} ack = {2} nack = {3}'.format(decode_res[0], decode_res[1], ack, nack))

def state_msg(seq_num):
    pass


def main():
    try:
        arrival_time_seed = float(sys.argv[1])
        num_packets = float(sys.argv[2])
        corrupted_seed = float(sys.argv[3])
        corruption_prob = float(sys.argv[4])
    except(IndexError) as e:
        print(type(e).__name__, e.args, '\nPlease provide 4 arguments')
        exit

    random.seed(arrival_time_seed)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_port = 2048
    server_name = '127.0.0.1'
    server_port = 50007

    int_val = 1
    seq_num = 0
    is_ack = False
    is_nack = False
    resent = False

    client_socket.connect((server_name, server_port))

    for i in range(int(num_packets)):
        packet = makepkt(int_val, seq_num, is_ack, is_nack)
        before_messages(seq_num, resent, int_val, is_ack, is_nack)
        client_socket.send(packet)
        time.sleep(rand_arrival_time())

        returned_message, server_address = client_socket.recvfrom(2048)
        decoded_res = decode_res(returned_message)
        uncorrupted_ack_nack(decode_res)

        # Packet is corrupted or recieved a nack
        while rand_corrupted() < corruption_prob or bool(decode_res[3]):
            resent = True
            before_messages(seq_num, resent, int_val, is_ack, is_nack)
            client_socket.send(packet)
            returned_message, server_address = client_socket.recvfrom(2048)
            decoded_res = decode_res(returned_message)
            uncorrupted_ack_nack(decode_res)


        resent = False
        int_val += 1
        seq_num = 0 if seq_num == 1 else 1
    
    client_socket.close()
        



if __name__ == '__main__':
    main()