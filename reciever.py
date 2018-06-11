from socket import *
import random
import sys

def generate_random():
    return random.random()

def is_corrupted(input_prob, rand_value):
    if input_prob < rand_value:
        return True
    return False

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
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((serverHost, serverPort))
    print('The server is ready to receive')

    # TODO: figure out how to close connection
    while True:
        # TODO: Find out recvfrom port number
        # sentence, clientAddress = serverSocket.recvfrom()

    

if __name__ == '__main__':
    main()


