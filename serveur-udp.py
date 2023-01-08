import socket

v_timeout = 20

print("Serveur UDP")

# on recupere automatiquement l'adresse IP de la machine (peut planter si plusieurs reseaux en meme temps)
host = socket.gethostbyname(socket.gethostname())
port = int(input("Entrez le port cible sous la forme 8888 :\n"))

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(v_timeout)

print("serveur démarré")
#le serveur se met en écoute
try:
    s.bind((host,port))
except ValueError as message_erreur:
    print(message_erreur)
    exit(1)
print("bind effectué sur "+host+':'+str(port)+", en attente de réception")

try:
    data,addr=s.recvfrom(1024)
except TimeoutError:
    print("Connexion Timeout")
    exit(1)
data=data.decode('utf-8')
print("recu : ",data)

s.sendto(bytes('Bien recu !','utf-8'),addr)

s.close()

input("Fin du programme\n ")
