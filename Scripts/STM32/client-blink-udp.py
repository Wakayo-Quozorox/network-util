from socket import *
import threading
from time import sleep

running = threading.Event()

host = input("Entrez l'adresse IP cible sous la forme 192.168.1.20 :\n")
#port = int(input("Entrez le port cible sous la forme 8888 :\n"))
port = 6000
message = input("Entrez la donnee string a envoyer : ")
v_timeout = 5
v_loop_delay = float(input("Entrez la periode de clignotement : "))

def loop():
    s=socket(AF_INET,SOCK_DGRAM)
    s.settimeout(v_timeout)
    while running.is_set():
        s.sendto(bytes(message,'utf8'),(host,port))
        sleep(v_loop_delay)
    s.close()

thread = threading.Thread(target=loop)

running.set()
thread.start()

message_cmd = ""
while( message_cmd != 'exit'):
    message_cmd = input("Entrez \"exit\" pour fermer le serveur\n")
    print('Vous avez entré : ',message_cmd)

print("En attente de l'arret du thread")
running.clear()
thread.join()

input("Fin du programme\n ")