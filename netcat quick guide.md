# Utilisation de nc.exe

Se placer au meme endroit dans le terminal pour pouvoir utiliser la commande sous windows
Ctrl+c pour quitter le programme

## Lancer un serveur UDP

nc -u -l -p PORTSERVEUR -s IPSERVEUR

## Lancer un client UDP

nc -u IPSERVEUR PORTSERVEUR

## Lancer un serveur TCP

nc -l -p PORTSERVEUR -s IPSERVEUR

## Lancer un client TCP

nc IPSERVEUR PORTSERVEUR
