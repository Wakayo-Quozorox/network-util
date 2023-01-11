/*
 * tcp_capteur.c
 * 
 * Created on: 6 jan 2023
 *      Author : Nicolas Bouchery
 * 
*/

#include "lwip/sys.h"
#include "lwip/sockets.h"
#include <string.h>

#define PORT_TCP_CAPT 9000

void tcp_capt_task(void)
{
    char data_buf[50];
    char mac_addr[18] = {0};
    sprintf(mac_addr,"%x:",MAC_ADDR0);
    sprintf(mac_addr+3,"%x:",MAC_ADDR1);
    sprintf(mac_addr+6,"%x:",MAC_ADDR2);
    sprintf(mac_addr+9,"%x:",MAC_ADDR3);
    sprintf(mac_addr+12,"%x:",MAC_ADDR4);
    sprintf(mac_addr+15,"%x\0",MAC_ADDR5);
    char* reception_ok = "Recu!\0";
    
    // Définir une socket TCP
    int sock, new_conn, size;
    struct sockaddr_in address, remote_host;

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) 
    {
        my_printf("erreur sock %d\n\r",sock);
        while(1);
    }

    // Dans le doute on initialise à 0 comme le prof
    memset(&remote_host, 0, sizeof(struct sockaddr_in));

    // Se mettre en mode écoute
    address.sin_family = AF_INET;
    address.sin_port = htons(PORT_TCP_CAPT);
    address.sin_addr.s_addr = INADDR_ANY;

    if (bind(sock, (struct sockaddr *)&address, sizeof (address)) < 0)
    {
        return;
    }

    /* listen for incoming connections (TCP listen backlog = 5) */
    listen(sock, 5);
    
    size = sizeof(remote_host);

    // Traiter les demandes de connection
    while(1)
    {
        new_conn = accept(sock, (struct sockaddr *)&remote_host, (socklen_t *)&size);
        
        if (read(new_conn, data_buf, sizeof(data_buf)) < 0)   // Peut planter
            my_printf("erreur lecture data tcp\n\r");
        
        // On teste le message de broadcast
        if (strncmp(data_buf,"cid?\n",5)==0)
            write(new_conn,mac_addr,18);    // TODO : improve
        write(new_conn,reception_ok,6);
        close(new_conn);
    }
}
