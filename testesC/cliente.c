#include <czmq.h>
#include <string.h>

void limparInput(){
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}
int main() {
    zsock_t *clientPush = zsock_new_push("tcp://localhost:5555");
    zsock_t *clientReq = zsock_new_req("tcp://localhost:5556");
    zsock_t *clientSub = zsock_new_sub("tcp://localhost:5557",NULL);
    int horarioLocal = 1;
    
    char address[50] = "localhost:boapergunta";

    if (!clientPush || !clientReq || !clientSub) {
        printf("Algum dos socket explodiu!\n");
        return -1;
    }

    printf("entrou!1\n");
    char usr1[50];
    printf("Nome usr1:\n");
    scanf("%s",&usr1);
    while(true){
        int esc;
        horarioLocal++;
        printf("Sair(0) Push(1) Req(2) Posts(3) Chat(4): ");
        scanf("%d",&esc);
        switch (esc){
            case 0:
                return 0;
                break;
            case 1:
                printf("PUSH!\n");
                zstr_send(clientPush,"address,6534,mensagem,adoro muito tudo isso :)");
                break;
            
            case 2:
                printf("REQ!\n");
                zstr_send(clientReq,"address,7263,testando,mkasd");
                printf("%s\n",zstr_recv(clientReq));
                break;
            case 3: //POSTS!
                printf("Voltar(0) ou Postar(1) ou Ver Posts(2) ou Seguir Usuario(3): ");
                scanf("%d",&esc);
                switch(esc){
                    case 0:{
                        break;
                    }
                    case 1:{ //Postar
                        char msg[500];
                        char push[500];
                        limparInput();
                        printf("Digite oque quer mandar (Vazio sai!):\n");

                        fgets(msg,sizeof(msg),stdin);
                        msg[strcspn(msg, "\n")] = '\0';

                        
                        if (strlen(msg) == 0) {
                            break; 
                        }
                        sprintf(push,"%s,%d,post,%s,%s",address,horarioLocal,usr1,msg);
                        printf("%s\n",push);
                        zstr_send(clientPush,push);
                        break;

                    }
                    case 2:{ //Ver Posts
                        char request[500];
                        sprintf(request,"%s,%d,verPost,%s",address,horarioLocal,usr1);
                        zstr_send(clientReq,request);
                        printf("%s\n",zstr_recv(clientReq));
                        break;
                        
                    }
                    case 3:{ //Seguir
                        char msg[500];
                        char push[500];
                        printf("Usuario que deseja seguir: ");
                        scanf("%s",&msg);
                        sprintf(push,"%s,%d,seguir,%s,%s",address,horarioLocal,usr1,msg);
                        zstr_send(clientPush,push);
                        break;
                    }
                        
                }
                break;
            case 4: { //CHAT!
                char conversa[100];
                char aux[50];
               
                char usr2[50];
                
                strcpy(aux,usr1);
                printf("%s\n",usr1);
                printf("Nome usr2:\n");
                scanf("%s",&usr2);
                printf("%s\n",usr2);
                    
                if(strcmp(usr1,usr2) >0){
                    sprintf(conversa,"%s_%s",usr2,usr1);
                        
                }
                else{
                    sprintf(conversa,"%s_%s",usr1,usr2);
                }
                strcpy(usr1,aux);
                printf("%s\n",conversa); //print debug
                char request[250];
                sprintf(request,"%s,%d,reqChat,%s",address,horarioLocal,conversa);
                printf("%s\n",request); //print debug 
                zstr_send(clientReq,request);
                printf("%s\n",zstr_recv(clientReq)); //print chat inicial!
                zsock_set_subscribe(clientSub,conversa);
                limparInput();
                while (true){
                    char msg[500];
                    char aux[500];
                    printf("Digite oque quer mandar (Vazio sai!):\n");

                    fgets(msg,sizeof(msg),stdin);
                    msg[strcspn(msg, "\n")] = '\0';

                    
                    if (strlen(msg) == 0) {
                        break; 
                    }
                    sprintf(aux,"%s,%d,msg,%s,%s,%s",address,horarioLocal,conversa,usr1,msg);
                    printf("%s\n",aux); //print debug
                    zstr_send(clientPush,aux);
                    printf("%s\n",zstr_recv(clientSub)); //print chat Sub
                    
                    


                    
                
                    
                
                    
                }
                zsock_set_unsubscribe(clientSub,conversa);
                break;
            }
        }
    }
    
    
    
    
    
    


    

    
    return 0;
}