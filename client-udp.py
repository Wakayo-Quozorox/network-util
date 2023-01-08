from socket import *

host = input("Entrez l'adresse IP cible sous la forme 192.168.1.20 :\n")
port = int(input("Entrez le port cible sous la forme 8888 :\n"))
v_timeout = 5

s=socket(AF_INET,SOCK_DGRAM)
s.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
s.settimeout(v_timeout)

message = input("Entrez la donnee string a envoyer : ")

s.sendto(bytes(message,'utf8'),(host,port))

try:    
    data,addr=s.recvfrom(1024)
except TimeoutError:
    print("Pas de retour du serveur")
    exit(1)
data=data.decode('utf-8')
print("recu : ",data)

s.close()
input("Fin du programme\n ")