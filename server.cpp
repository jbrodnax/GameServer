#include <iostream>
#include <netdb.h>
#include <netinet/in.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <pthread.h>
#include <unistd.h>
#include <fcntl.h>
#include <arpa/inet.h>
#include <fstream>
#include <string>
#include <cstring>
#include <signal.h>

/* Server TCP port*/
#define PORT 8080

/* Max concurrent connections */
#define CONNS 32

/* Max number of backlogged connections */
#define BACKLOG 5

typedef struct _ConnectionThread{
    bool isActive;
    pthread_t conn_thread;
}ConnectionThread;

typedef struct _ConnectionReq{
    int fd;
    socklen_t addrlen;
    sockaddr_in addr;
} ConnectionReq;

sockaddr_in _serveraddr;

/* Array of pointers to Connection structs*/
ConnectionThread connectionList[CONNS];
int listenfd = -1;

void *new_connection(void* arg){
    ConnectionReq* req = (ConnectionReq*)arg;
    char buff[1048] = {0};
    ssize_t n = 0;

    while(1){
        n = recv(req->fd, buff, sizeof(buff) - 1, 0);
        if (n < 1){
            std::cout << "Connection closed by client (probably).\n";
            break;
        }
        std::cout << "Thread: Received message: \n"
                  << buff << "\n";
        memset(buff, 0, sizeof(buff));
    }
    std::cout << "Thread is returning.\n";
    return (void*)req;
}

void cleanup(){
    // TKTK - instruct each thread to close it's connection and return
    // TKTK - wait for threads to return
}

void sig_handler(int signo){
    if (signo == SIGINT){
        std::cout << "Shutting down server...\n";
        // TKTK - call cleanup() or set break condition?
        close(listenfd);
        exit(1);
    }
}

/* Find the first available slot in the connection list. Null if full.*/
ConnectionThread *find_available(){
    int i = 0;
    ConnectionThread *ct = NULL;

    for (i = 0; i < CONNS; i++){
        ct = &connectionList[i];
        if (ct->isActive == false)
            return ct;
    }

    return NULL;
}

/* Start listening for incoming connections and spin-up a new thread for each. */
void start_listening(){
    ConnectionThread *ct = NULL;
    sockaddr_in serveraddr;
    sockaddr_in clientaddr;
    socklen_t addrlen = sizeof(clientaddr);
    int connfd = -1;

    memset(&serveraddr, 0, sizeof(serveraddr));
    memset(&clientaddr, 0, sizeof(clientaddr));

    memcpy(&serveraddr, &_serveraddr, sizeof(serveraddr));

    if ((listen(listenfd, BACKLOG)) != 0){
        std::cout << "Failed to listen on socket.\n";
        return;
    }

    std::cout << "Server is now listening for new connections...\n";

    while(1){
        if ((connfd = accept(listenfd, (sockaddr*)&clientaddr, &addrlen)) < 0){
            std::cout << "Client connection failed.\n";
        }else{
            std::cout << "Client connection accepted.\n";
        }

        if ((ct = find_available()) == NULL){
            std::cout << "No available slots in connection list.\n";
            continue;
        }

        ConnectionReq *req = new ConnectionReq;
        memset(req, 0, sizeof(ConnectionReq));

        req->addrlen = addrlen;
        req->fd = connfd;
        memcpy(&req->addr, &clientaddr, addrlen);

        ct->isActive = true;
        pthread_create(&ct->conn_thread, NULL, new_connection, (void *)req);
    }
}

/* Create and bind to a socket. */
bool init_server(){
    int i = 0;
    ConnectionThread *ct = NULL;

    /* Create Socket */
    if ((listenfd = socket(AF_INET, SOCK_STREAM, 0)) == -1){
        std::cout << "Socket creation failed.\n";
        return false;
    }

    int optval = 1;
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, (const void *)&optval, sizeof(int));

    std::cout << "Socket successfully created.\n";

    memset(&_serveraddr, 0, sizeof(_serveraddr));
    _serveraddr.sin_family = AF_INET;
    _serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
    _serveraddr.sin_port = htons(PORT);

    /* Bind the address to the socket */
    if (bind(listenfd, (sockaddr*)&_serveraddr, sizeof(_serveraddr)) != 0){
        std::cout << "Failed to bind to socket.\n";
        return false;
    }

    std::cout << "Successfully bound to socket.\n";

    /* Init connection list */
    for (i = 0; i < CONNS; i++){
        ct = &connectionList[i];
        ct->isActive = false;
        ct->conn_thread = 0;
    }

    return true;
}

int main(int argc, char **argv){

    if (init_server() == false){
        exit(1);
    }

    signal(SIGINT, sig_handler);
    start_listening();
    return 0;
}