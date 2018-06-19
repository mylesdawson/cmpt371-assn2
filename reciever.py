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
    data = data.decode()

    # int_val, seq_num, is_ack, is_nack
    data = data.split(' ')
    print(data)
    return data


def main():
    try:
        generator_seed = sys.argv[1]
        corrupted_prob = sys.argv[2]
    except(IndexError) as e:
        print(type(e).__name__, e.args, '\nPlease provide generator seed and corrupted propability')
        exit

    random.seed(generator_seed)

    serverHost = '127.0.0.1'
    serverPort = 50007
    # Create a socket that can communicate with ipv4 addresses (AF_INET) using UDP (SOCK_DGRAM)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverHost, serverPort))
    serverSocket.listen(1)
    print('The server is ready to receive')

    # TODO: figure out how to close connection
    while True:
        # TODO: Find out recvfrom port number
        data, clientAddress = serverSocket.accept()

        vals = decode_data(data)
        is_corrupted = is_corrupted(corrupted_prob, generate_random())

    

if __name__ == '__main__':
    main()


