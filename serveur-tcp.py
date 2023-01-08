import socket

v_timeout = 20

print("Serveur TCP")
host = socket.gethostbyname(socket.gethostname())
port = int(input("Entrez le port cible sous la forme 8888 :\n"))


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
s.settimeout(v_timeout)

try:
    s.bind((host,port))
except ValueError as message_erreur:
    print(message_erreur)
    exit(1)
s.listen(5)
print('Bind effectué sur '+host+':'+str(port))
#process en attente de connexion du client (s.connect)
try:
    connection, address = s.accept()
except TimeoutError:
    print("Connection timeout")
    exit(1)
print ('le client est ', address)

#le serveur lit le buffer (ou attend si le buffer est vide)
try:
    data = connection.recv(1024)
except TimeoutError:
    print("Connection timeout")
    exit(1)

data=data.decode('utf-8')
print('Message recu : ',data)

connection.sendall(bytes('coucou\n','utf-8'))

connection.close()
s.close()

input("Fin du programme\n ")