import socket
import threading

running = threading.Event()

# Timeout set pour ne pas provoquer de boucles infinies à la fermeture du programme
v_timeout_udp = 20
v_timeout_tcp = 20

print("Serveur Multi TCP/UDP")

# on recupere automatiquement l'adresse IP de la machine (peut planter si plusieurs reseaux en meme temps)
host = socket.gethostbyname(socket.gethostname())
# décommenter pour mettre l'adresse manuellement (mais ça marchera pas)
#host = '192.168.1.20'
print("Le serveur se lancera sur l'addresse hote "+host)
# On entre les ports à la main pour plus de fluidité
port_tcp = int(input("Entrez le port cible TCP sous la forme 8888 :\n"))
port_udp = int(input("Entrez le port cible UDP sous la forme 8888 :\n"))

# Si c'est toujours les même ports à entrer, les régler ici
# port_tcp = 8888
# port_udp = 8888

# thread pour chaque connexion TCP qui arrive 
def handleClient_tcp(connection):
    data=''
    while data!='exit':
        data=connection.recv(1024)
        data=data.decode('utf-8')
        print(data)
        if not data: break
        connection.send(bytes('recu','utf-8'))
    connection.close()

# Fonction pour lancer le serveur TCP
def lancer_serveur_tcp():
    # Création du socket TCP
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.settimeout(v_timeout_tcp)
    
    try:
        # Liaison du socket à une adresse IP et un port
        sock_tcp.bind((host, port_tcp))
        # Mise en écoute du socket
        sock_tcp.listen()
        print("Le serveur TCP est en écoute sur le port "+str(port_tcp)+"...")
    except ValueError as message :
        print(message)
        exit(1)

    # Boucle infinie pour traiter les connexions entrantes
    while running.is_set():
        # Acceptation d'une connexion entrante
        try:
            conn, addr = sock_tcp.accept()
        # Les timmeout servent juste à quitter le programme à la fin puisque
        # les connexions ne sont pas interrompues
        except TimeoutError:
            print("Timeout TCP\n")
            conn = None
        if conn is not None:
            print("Connexion TCP établie avec " + str(addr))
            tcp_client=threading.Thread(target=handleClient_tcp,args=(conn,))
            tcp_client.start()
    sock_tcp.close()

# Fonction pour lancer le serveur UDP
def lancer_serveur_udp():
    # Création du socket UDP
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.settimeout(v_timeout_udp)

    # Liaison du socket à une adresse IP et un port
    sock_udp.bind((host, port_udp))
    
    print("Le serveur UDP est en écoute sur le port "+str(port_udp)+"...")
    
    # Boucle infinie pour traiter les données entrantes
    while running.is_set():
        # Réception de données
        try:
            data, addr = sock_udp.recvfrom(1024)
        # Les timmeout servent juste à quitter le programme à la fin puisque
        # les connexions ne sont pas interrompues
        except TimeoutError:
            print("Timeout UDP")
            data = None
        if data is not None:
            data=data.decode('utf-8')
            print("Données reçues de " + str(addr) + " : " + str(data))
        
            # Envoi de données au client
            sock_udp.sendto(bytes('Donnees recues !','utf-8'), addr)
    sock_udp.close()

# Création des threads
thread_tcp = threading.Thread(target=lancer_serveur_tcp)
thread_udp = threading.Thread(target=lancer_serveur_udp)


# Démarrage des threads
running.set()
thread_tcp.start()
thread_udp.start()

# Pour fermer le serveur quand on veut
message = ""
while( message != 'exit'):
    message = input("Entrez \"exit\" pour fermer le serveur\n")
    print('Vous avez entré : ',message)

print('En attente de la fermeture des serveurs (devrait prendre maximum '+str(max(v_timeout_udp,v_timeout_tcp))+'s)\n')

running.clear()

thread_udp.join()
thread_tcp.join()

exit()