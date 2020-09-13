import threading
import socket
import pickle
from bitarray import bitarray
d = {'A':bitarray('01000001'),
     'B':bitarray('01000010'),
     'C':bitarray('01000011'),
     'D':bitarray('01000100'),
     'E':bitarray('01000101'),
     'F':bitarray('01000110'),
     'G':bitarray('01000111'),
     'H':bitarray('01001000'),
     'I':bitarray('01001001'),
     'J':bitarray('01001010'),
     'K':bitarray('01001011'),
     'L':bitarray('01001100'),
     'M':bitarray('01001101'),
     'N':bitarray('01001110'),
     'Ñ':bitarray('11010001'),
     'O':bitarray('01001111'),
     'P':bitarray('01010000'),
     'Q':bitarray('01010001'),
     'R':bitarray('01010010'),
     'S':bitarray('01010011'),
     'T':bitarray('01010100'),
     'U':bitarray('01010101'),
     'V':bitarray('01010110'),
     'W':bitarray('01010111'),
     'X':bitarray('01011000'),
     'Y':bitarray('01011001'),
     'Z':bitarray('01011010'),
     'a':bitarray('01100001'),
     'b':bitarray('01100010'),
     'c':bitarray('01100011'),
     'd':bitarray('01100100'),
     'e':bitarray('01100101'),
     'f':bitarray('01100110'),
     'g':bitarray('01100111'),
     'h':bitarray('01101000'),
     'i':bitarray('01101001'),
     'j':bitarray('01101010'),
     'k':bitarray('01101011'),
     'l':bitarray('01101100'),
     'm':bitarray('01101101'),
     'n':bitarray('01101110'),
     'ñ':bitarray('11110001'),
     'o':bitarray('01101111'),
     'p':bitarray('01110000'),
     'q':bitarray('01110001'),
     'r':bitarray('01110010'),
     's':bitarray('01110011'),
     't':bitarray('01110100'),
     'u':bitarray('01110101'),
     'v':bitarray('01110110'),
     'w':bitarray('01110111'),
     'x':bitarray('01111000'),
     'y':bitarray('01111001'),
     'z':bitarray('01111010'),
     '0':bitarray('00000000'),
     '1':bitarray('00000001'),
     '2':bitarray('00000010'),
     '3':bitarray('00000011'),
     '4':bitarray('00000100'),
     '5':bitarray('00000101'),
     '6':bitarray('00000110'),
     '7':bitarray('00000111'),
     '8':bitarray('00001000'),
     '9':bitarray('00001001'),
     'Á':bitarray('11000001'),
     'É':bitarray('11001001'),
     'Í':bitarray('11001101'),
     'Ó':bitarray('11010011'),
     'Ú':bitarray('11011010'),
     'Ü':bitarray('11011100'),
     'á':bitarray('11100001'),
     'é':bitarray('11101001'),
     'í':bitarray('11101101'),
     'ó':bitarray('11110011'),
     'ú':bitarray('11111010'),
     'ü':bitarray('11111100'),
     ' ':bitarray('00100000'),
     '¡':bitarray('10100001'),
     '!':bitarray('00100001'),
     '"':bitarray('00100010'),
     '#':bitarray('00100011'),
     '$':bitarray('00100100'),
     '%':bitarray('00100101'),
     '&':bitarray('00100110'),
     '(':bitarray('00101000'),
     ')':bitarray('00101001'),
     '*':bitarray('00101010'),
     '+':bitarray('00101011'),
     ',':bitarray('00101100'),
     '-':bitarray('00101101'),
     '.':bitarray('00101110'),
     '/':bitarray('00101111'),
     ':':bitarray('00111010'),
     ';':bitarray('00111011'),
     '<':bitarray('00111100'),
     '=':bitarray('00111101'),
     '>':bitarray('00111110'),
     '¿':bitarray('10111111'),
     '?':bitarray('00111111'),
     '@':bitarray('01000000'),
     '[':bitarray('01011011'),
     ']':bitarray('01011101'),
     '^':bitarray('01011110'),
     '_':bitarray('01011111'),
     '{':bitarray('01111011'),
     '|':bitarray('01111100'),
     '}':bitarray('01111101'),
     '~':bitarray('01111110')
     }
HEADERSIZE = 10
typeEncode = 'ascii'

host = '127.0.0.1' #localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []

#mandamos mensaje a todos
def broadcast(message):
    for client in clients:
        client.send(message)

#maneja los mensajes recibidos
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index =  clients.index(client)
            clients.remove(client)
            client.close()
            nickname =  nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode(typeEncode))
            nicknames.remove(nickname)
            break

#aceptamos a los clientes
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode(typeEncode))
        nickname = client.recv(1024).decode(typeEncode)
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        client.send('NICK'.encode(typeEncode))
        client.send('Connected to the server!'.encode(typeEncode))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#con este podemos enviar objetos a otros clientes
def send_obj(conn,o):
    #print("a")
    obj = pickle.dumps(o)
    #print("b")
    obj = bytes(f"{len(obj):<{HEADERSIZE}}", typeEncode) + obj
    #print("c")
    conn.send(obj)
    #print("d")

#con esta funcion podemos recibir objetos que nos manden
def recv_obj(conn):
    obj = conn.recv(1024)
    obj = pickle.loads(obj[HEADERSIZE:])
    return obj


print('Server is listening...')
receive()