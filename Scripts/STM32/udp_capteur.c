/*
 * upd_capteur.c
 * 
 * Created on: 6 jan 2023
 *      Author : Nicolas Bouchery
 * 
*/

#include "lwip/sys.h"
#include "lwip/sockets.h"
#include <string.h>

#define PORT_UDP_CAPT 9000

//
void udp_capt_task(void){
	int sock, port;
	struct sockaddr_in address;
	struct sockaddr from;
	//struct lwip_sock *socket;

	socklen_t fromlen;
	fromlen=sizeof(from);

	char data_buf[50]; // 1000 erreur ???
	int recv_data;

	 /* create a UDP socket */


	 if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
		 my_printf("erreur sock %d\n\r",sock);
		 while(1);
	 }

	 //vu pour initialiser a 0 ?
	 memset(&from, 0, sizeof(struct sockaddr_in));
	 /* bind to port 5000 at any interface */
	 address.sin_family = AF_INET;
	 address.sin_port = htons(PORT_UDP_CAPT);
	 address.sin_addr.s_addr = INADDR_ANY;

	 if (bind(sock, (struct sockaddr *)&address, sizeof (address)) < 0){
	    return;
	 }


	 while (1){
		 my_printf("attente sur %d\r\n",PORT_UDP_CAPT);

		 recv_data=recvfrom(sock,data_buf,sizeof(data_buf),0,&from,&fromlen);
		 if (recv_data>0){
			 my_printf("data recu :%d   data1:%s\r\n",recv_data,data_buf);

			 if (strcmp(data_buf,"conf\n"))
				 sendto(sock,"temp",4,0,&from,fromlen);

			 port=from.sa_data[0]<<8;
			 port+=from.sa_data[1];
			 //TODO  a tester
			 //port= PP_HTONS((uint16_t *)from.sa_data);

			 my_printf("IPclient :%s   Port Client:%d\r\n",ip4addr_ntoa(&(from.sa_data[2])),port);

			 //TODO : pas de recu si message broadcast
			 sendto(sock,"recu\n\r",6,0,&from,fromlen);
		 }
	 }
}
