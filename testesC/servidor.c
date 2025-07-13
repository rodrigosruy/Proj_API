#include <czmq.h>

int main() {
    zsock_t *push = zsock_new_push("tcp://localhost:5556"); // Bind to port 5556
    if (!push) {
        printf("Failed to create push socket\n");
        return -1;
    }

    printf("Server is running and sending messages...\n");
    scanf("");
    for (int i = 0; i < 5; i++) {
        char message[50];
        sprintf(message, "Message %d", i + 1);
        zstr_send(push, message);
        printf("Sent: %s\n", message);
        sleep(1); // Wait 1 second between messages
    }

    
    return 0;
}