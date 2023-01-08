import socket

port = int(input("Entrez le port cible sous la forme 8888 :\n"))
v_timeout = 5

# Création du socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(v_timeout)

# Configuration du socket pour pouvoir envoyer des broadcasts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Adresse IP et port de destination du broadcast
destination = ('255.255.255.255', port)

# Envoi du message de broadcast
sock.sendto(b'Message de broadcast !', destination)

print("Broadcast envoyé à " + str(destination))

# Fermeture du socket
sock.close()
input("Fin du programme\n ")