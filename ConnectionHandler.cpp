#include <string.h>
#include <iostream>
#include <sys/socket.h>
#include <sys/types.h>
#include <pthread.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <uuid.h>

typedef struct _TurnData{
    // TKTK - data fields required to summarize and validate a turn
}TurnData;

class ConnectionHandler {
    public:
        sockaddr_in AddrInfo;
        uuid_t GameSessionId;
        bool EndTurn(){

        }
}