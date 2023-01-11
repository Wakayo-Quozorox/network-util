import socket
from time import time

port = int(input("Entrez le port cible sous la forme 8888 :\n"))
v_timeout = 5

# Création du socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(v_timeout)

# Configuration du socket pour pouvoir envoyer des broadcasts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Adresse IP et port de destination du broadcast
# Attention visiblement 255.255.255.255 ne fonctionne pas avec windows
destination = ('192.168.2.255', port)

# Envoi du message de broadcast
sock.sendto(bytes("Message de broadcast !",'utf-8'), destination)

print("Broadcast envoyé à " + str(destination))

# Boucle de 5 seconde pour récupérer des données de plusieurs clients
t_end = time() + 5
data_received = False
while time() < t_end:
    try:
        data, addr = sock.recvfrom(1024)
    except ValueError as message_error:
        print(message_error)
    except TimeoutError:
        if data_received is not True:
            print("Pas de reponse du serveur")
        data = None
    if data is not None:
        data_received = True
        data = data.decode("utf-8")
        print("Data received : ",data)

# Fermeture du socket
sock.close()
input("Fin du programme\n ")