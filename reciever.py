from socket import *
import random
import sys

def generate_random():
    return random.random()

def is_corrupted(input_prob, rand_value):
    if rand_value < input_prob:
        return True
    return False

def decode_data(data):
    dec = data.decode().split(' ')
    # print(dec)
    dec = [int(x) for x in dec]
    return dec

def ack_nack_msg(corrupted, int_val, seq_num):
    ack = 0 if corrupted else 1
    nack = 1 if corrupted else 0

    if corrupted:
        print('A NACK is about to be sent')
    else:
        print('An ACK is about to be sent')

    print('Packet to send contains: data = {0} seq = {1} ack = {2} nack = {3}'.format(int_val, seq_num, ack, nack))

def received_msg(vals, duplicate):
    if duplicate:
        print('A duplicate packet with sequence number {0} has been received'.format(vals[1]))
    else:
        print('A packet with sequence number {0} has been received'.format(vals[1]))

    print('Packet received contains: data = {0} seq = {1} ack = {2} nack = {3}'.format(vals[0], vals[1], vals[2], vals[3]))

def received_corrupted():
    print('A corrupted packet has just been received')

def sender_state_msg(corrupted, seq_num):
    seq_num = 0 if seq_num else 1

    if corrupted:
        print('The receiver is moving back to state WAIT FOR {0} FROM BELOW'.format(seq_num))
    else:
        print('The receiver is moving to state WAIT FOR {0} FROM BELOW'.format(seq_num))

def makepkt(int_val, seq_num, is_ack, is_nack):
    to_encode = [int_val, seq_num, is_ack, is_nack]
    stringify = [str(x) for x in to_encode]
    to_string = ' '.join(stringify)

    encoded = to_string.encode()
    # print(encoded)
    return encoded


def main():
    try:
        generator_seed = float(sys.argv[1])
        corrupted_prob = float(sys.argv[2])
    except(IndexError) as e:
        print(type(e).__name__, e.args, '\nPlease provide generator seed and corrupted propability')
        exit

    random.seed(generator_seed)

    serverHost = '127.0.0.1'
    serverPort = 50007
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverHost, serverPort))
    serverSocket.listen(1)
    print('The server is ready to receive')

    int_val = 0
    duplicate = 0
    is_ack = 0
    is_nack = 0
    
    connectionId, addr = serverSocket.accept()

    while True:
        data = connectionId.recv(1024)

        vals = decode_data(data)
        seq_num = vals[1]
        corrupted = is_corrupted(corrupted_prob, generate_random())

        # Send nacks
        while corrupted:
            received_corrupted()
            is_nack = 1
            is_ack = 0
            pkt = makepkt(int_val, seq_num, is_ack, is_nack)
            ack_nack_msg(corrupted, int_val, seq_num)
            connectionId.send(pkt)
            sender_state_msg(corrupted, seq_num)

            data = connectionId.recv(1024)
            vals = decode_data(data)
            corrupted = is_corrupted(corrupted_prob, generate_random())

        # Send an ACK packet
        is_nack = 0
        is_ack = 1
        pkt = makepkt(int_val, seq_num, is_ack, is_nack)
        # print(data)
        ack_nack_msg(corrupted, int_val, seq_num)
        connectionId.send(pkt)
        sender_state_msg(corrupted, seq_num)


    connectionId.close()

if __name__ == '__main__':
    main()


