from socket import *
import random
import sys
import time

def rand_arrival_time(rand):
    return rand.uniform(0.0, 4.9)

def rand_corrupted(rand):    
    return rand.random()

def makepkt(int_val, seq_num, is_ack, is_nack):
    to_encode = [int_val, seq_num, is_ack, is_nack]
    stringify = [str(x) for x in to_encode]
    to_string = ' '.join(stringify)

    return to_string.encode()

def decode_res(res):
    dec = res.decode().split(' ')
    dec = [int(x) for x in dec]
    return dec

def before_messages(seq_num, resent, int_val, is_ack, is_nack):
    sent_or_resent = 'resent' if resent else 'sent'

    print('A packet with sequence number {0} is about to be {1}'.format(seq_num, sent_or_resent))
    print('Packet to send contains: data = {0} seq = {1} ack = {2} nack = {3}'.format(int_val, seq_num, is_ack, is_nack))

def uncorrupted_ack_nack(decoded):
    ack = decoded[2]
    nack = decoded[3]

    if ack:
        print('An ACK packet has just been recieved')
    else:
        print('A NACK packet has just been recieved')
    
    print('Packet received contains: data = {0} seq = {1} ack = {2} nack = {3}'.format(decoded[0], decoded[1], ack, nack))


def main():
    try:
        arrival_time_seed = float(sys.argv[1])
        num_packets = float(sys.argv[2])
        corrupted_seed = float(sys.argv[3])
        corruption_prob = float(sys.argv[4])
    except(IndexError) as e:
        print(type(e).__name__, e.args, '\nPlease provide 4 arguments')
        exit


    rand_arrival = random.Random()
    rand_corrupt = random.Random()
    rand_arrival.seed(arrival_time_seed)
    rand_corrupt.seed(corrupted_seed)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_port = 2048
    server_name = '127.0.0.1'
    server_port = 50007

    int_val = 1
    seq_num = 0
    is_ack = 0
    is_nack = 0
    resent = 0

    client_socket.connect((server_name, server_port))

    for i in range(int(num_packets)):
        packet = makepkt(int_val, seq_num, is_ack, is_nack)
        before_messages(seq_num, resent, int_val, is_ack, is_nack)
        client_socket.send(packet)
        time.sleep(rand_arrival_time(rand_arrival))

        print('The sender is moving to state WAIT FOR ACK OR NACK')
        returned_message, server_address = client_socket.recvfrom(2048)
        decoded = decode_res(returned_message)
        uncorrupted_ack_nack(decoded)

        # Packet is corrupted or recieved a nack
        while  (rand_corrupted(rand_corrupt) < corruption_prob or decoded[3]):
            print('The sender is moving back to state WAIT FOR CALL {0} FROM ABOVE'.format(seq_num))
            resent = True
            before_messages(seq_num, resent, int_val, is_ack, is_nack)
            client_socket.send(packet)
            time.sleep(rand_arrival_time(rand_arrival))
            print('The sender is moving to state WAIT FOR ACK OR NACK')

            returned_message, server_address = client_socket.recvfrom(2048)
            decoded = decode_res(returned_message)
            uncorrupted_ack_nack(decoded)


        resent = False
        int_val += 1
        seq_num = 0 if seq_num else 1
        print('The sender is moving to state WAIT FOR CALL {0} FROM ABOVE'.format(seq_num))
    
    client_socket.close()
        

if __name__ == '__main__':
    main()