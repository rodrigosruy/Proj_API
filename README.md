# Sistemas Distribuídos
Murilo Darce Borges Silva - 24.122.031-8  
Nicolas Costa Coppola de Moraes - 22.122.099-9  
Rodrigo Simões Ruy - 24.122.092-0  

# Afazeres
* O projeto deve ser desenvolvido usando qualquer biblioteca de comunicação (e.g., ZeroMQ, gRPC, OpenMPI) e com pelo menos 3 linguagens diferentes (e.g., Python, Java, C, C++, JavaScript ou TypeScript, Go, Rust, Zig, Elixir, Gleam, Erlang...);
* Os processos que postam e/ou enviam mensagens podem ser controlados pelos usuários, ou fazer postagens/troca de mensagens de forma automática; (Python, Java, C).
* O projeto deve executar pelo menos 3 servidores e 5 usuários para testar;
* Para garantir que a sincronização dos relógios está funcionando, os relógios de todos os processos podem sofrer alterações na atualização deles de forma aleatória, podendo ser adiantados ou atrasados em até 1 segundo.
* A documentação do projeto deve conter:
  * Descrição do padrão de mensagem utilizado em todas as partes do projeto.
  * Descrição dos dados enviados nas mensagens.
  * Diagrama mostrando a relação entre os serviços implementados.

  * Portas 5555-5558 para Load Balancer, 5558-5599 para servidores
  
  * Linguagens:
    * Cliente: C/C++
    * Load Balancer: python/[Elixir](https://github.com/mdarce765/SistemasDistribuidos/tree/main/loadbalancer)
    * Servidor: python

  * Tabelas:
    * Posts
      * Usuário que mandou
      * Horário 
      * Conteúdo postado
    * Chats
      * Usuário que mandou
      * Horário
      * Conteudo
    * Seguir (Tabela para correlacionar seguidor e seguido)
      * Seguido
      * Seguidor

  * Load Balancer:
    * Pull: 5555
    * Rep: 5556
    * Pub: 5557
    * Sub: 5558

  * Servidores:
    * Pull
    * Rep
    * Pub
      
  * Mensagens:
    *  Estrutura base: (IP,horariolocal,tipomsg,conteudo)
    *  Tipos de mensagem (tipomsg):
       *  msg (IP,horariolocal,'msg',conversa,usuario,conteudo)
       *  post (IP,horariolocal,'post',conteudo)
       *  seguir (IP,horariolocal,'seguir',conteudo)
       *  verChat (IP,horariolocal,'verChat',conteudo)
       *  repChat (IP,horariolocal,'repChat',conteudo)
       *  repPost (IP,horariolocal,'repPost'conteudo)
       *  rep (IP,horariolocal,'rep',conteudo)
   
# Bibliotecas para os Clientes
Bibliotecas necessárias para rodar o cliente em C:  
Biblioteca CZMQ: https://github.com/zeromq/czmq   
Executável incluído na pasta Grupo64!

Bibliotecas necessárias para rodar o cliente em Java :  
Biblioteca JeroMQ: https://github.com/zeromq/jeromq  
pom.xml incluído na pasta Grupo64!  

Bibliotecas necessárias para rodar o cliente em Python:  
Biblioteca Pyzmq: https://github.com/zeromq/pyzmq  

# Desenhos
## Pull, Push
![image](https://github.com/user-attachments/assets/bacee72d-6d38-4aae-acc0-5c112d32ba95)

## Request, Reply
![image](https://github.com/user-attachments/assets/1eecd3f3-1e91-40b4-874c-25fa799c4e23)

## Publisher, Subscriver
![image](https://github.com/user-attachments/assets/7408570f-8c37-4a81-acf7-6b13f2de46e5)
