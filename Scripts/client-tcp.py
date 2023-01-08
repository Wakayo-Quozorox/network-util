from socket import *

v_timeout = 5

print("Client TCP")
host = input("Entrez l'adresse IP cible sous la forme 192.168.1.20 :\n")
port = int(input("Entrez le port cible sous la forme 8888 :\n"))
message = input("Entrez la donnee a envoyer : ")

s=socket(AF_INET,SOCK_STREAM)
s.settimeout(v_timeout)
try:
    s.connect((host,port))
except TimeoutError:
    print("Pas de serveur en ecoute")
    exit(1)
s.sendall(bytes(message,'utf8'))

try:
    message=s.recv(1024)
except TimeoutError:
    print("Pas de reponse du serveur")
    exit(1)
message=message.decode('utf8')

print("recu : ",message)  

s.close()

input("Fin du programme\n")