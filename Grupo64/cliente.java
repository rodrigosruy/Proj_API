package grupo;
import org.zeromq.SocketType;
import org.zeromq.ZMQ;
import org.zeromq.ZContext;
import org.zeromq.ZMQ.Socket;
import java.util.Scanner;  
import java.util.Arrays;

public class cliente
{
    public static void main(String[] args) throws Exception
    {
        try (ZContext context = new ZContext()) {
            // Socket to talk to clients
            Scanner scanner = new Scanner(System.in);  
            Socket clientPush = context.createSocket(SocketType.PUSH);
            Socket clientReq = context.createSocket(SocketType.REQ);
            Socket clientSub = context.createSocket(SocketType.SUB);
            clientReq.connect("tcp://localhost:5556");
            clientPush.connect("tcp://localhost:5555");
            clientSub.connect("tcp://localhost:5557");
            if (clientPush == null || clientReq == null || clientSub == null){
                System.out.println("ALGUMA DAS CONEXOES NAO DEU CERTO!");
                

            }
            int horarioLocal = 1;
            Thread.sleep(1000); //wait para ter certeza que tudo carrega a tempo (sim, isso era um problema)
            System.out.println("Insira seu usuario:");
            String usr1 = scanner.nextLine();
            
            while(true){
                System.out.println("Sair(0) ou Push(1) ou REQ(2) ou Post(3) ou Chat(4)");
                horarioLocal++;

                int resp = scanner.nextInt();
                scanner.nextLine();

                if (resp == 0){
                    break;
                }
                else if(resp == 1){
                    String msgPush = "End," + String.valueOf(horarioLocal)+",Tipo,Conteudo";

                    clientPush.send(msgPush.getBytes(ZMQ.CHARSET),0);
                }
                else if (resp == 2){
                    String msgReq = "End," + String.valueOf(horarioLocal) + ",Tipo,Conteudo";
                    clientReq.send(msgReq.getBytes(ZMQ.CHARSET),0);
                    String recv = clientReq.recvStr();
                    System.out.println(recv);
                }
                else if (resp == 3){ //post
                    System.out.println("Postar(1) ou Ver Posts(2) ou Seguir(3)");
                    int resp2 = scanner.nextInt();
                    scanner.nextLine();
                    if (resp2 == 1){
                        System.out.println("Mensagem do post:");
                        String msgPostar =  scanner.nextLine();
                        msgPostar = "End," + String.valueOf(horarioLocal) + ",post,"+ usr1 + "," + msgPostar;
                        clientPush.send(msgPostar.getBytes(ZMQ.CHARSET),0);


                    }
                    else if (resp2 == 2){
                        String msgPosts = "End," + String.valueOf(horarioLocal) + ",verPost," + usr1;
                        clientReq.send(msgPosts.getBytes(ZMQ.CHARSET),0);
                        System.out.println(clientReq.recvStr()); 

                    }
                    else if (resp2 == 3){
                        System.out.println("Quem deseja seguir: ");
                        String msgSeguir = scanner.nextLine();
                        msgSeguir = "End," + String.valueOf(horarioLocal) + ",seguir," + usr1 + "," + msgSeguir;
                        clientPush.send(msgSeguir.getBytes(ZMQ.CHARSET),0);


                    }

                }
                else if (resp == 4){ //chat
                    System.out.println("Insira quem deseja conversar com:");
                    String usr2 = scanner.nextLine();
                    String[] users = {usr1,usr2};
                    Arrays.sort(users);
                    String conversa = users[0] + "_" + users[1];
                    System.out.println(conversa); //print debug
                    clientSub.subscribe(conversa);
                    String reqChat = "End," + String.valueOf(horarioLocal) + ",reqChat," + conversa;
                    clientReq.send(reqChat.getBytes(ZMQ.CHARSET),0);
                    System.out.println(clientReq.recvStr());
                    while(true){
                        System.out.println("Digite a mensagem (EXIT para sair): ");
                        String mensagem = scanner.nextLine();
                        if (mensagem.equals("EXIT")){
                            break;
                        }
                        mensagem = "End," + String.valueOf(horarioLocal) + ",msg," + conversa + "," + usr1 + "," + mensagem ;
                        System.out.println(mensagem); //print debug

                        clientPush.send(mensagem.getBytes(ZMQ.CHARSET),0);
                        System.out.println(clientSub.recvStr());


                        
                        
                    }
                    clientSub.unsubscribe(conversa);


                }



                
            }
           
            
            
            
        }
    }
}