import zmq
import ast
import random
## import msgpack
ctx = zmq.Context()
clientReq= ctx.socket(zmq.REQ)
clientPull= ctx.socket(zmq.PULL)
clientPush = ctx.socket(zmq.PUSH)
clientSub = ctx.socket(zmq.SUB) ##montar um pollin para sub!!
portacliente = 5600
##clientEnd = f"tcp://localhost:{portacliente}" ##endereco do cliente
clientReq.connect("tcp://localhost:5556") ##endereco do Rep do load balancer (por agora serv)
## clientPull.bind(f"tcp://*:{portacliente}") ##endereco do pull do cliente
clientPush.connect("tcp://localhost:5555") #endereco do Pull do load balancer (por agora serv)
clientSub.connect("tcp://localhost:5557")
#estrutura da mensagem (ip de quem mandou,horarioLocal,tipo,conteudo)
horarioLocal = 0
def aumentarTempo():
    global horarioLocal
    horarioLocal += random.randint(1,10)
while True:
    try:
        clientPull.bind(f"tcp://*:{portacliente}")
        clientEnd = f"tcp://localhost:{portacliente}" ##endereco do cliente
        print(f"Bind na porta {portacliente}")
        break
    except:
        if (portacliente <= 6000):
            portacliente += 1
        else:
            raise("FUDEU! Porta muito alta >= 6000!")
        

class mensagem:
    def __init__(self,recv):
        conteudo = recv.split(",")
        self.end = conteudo[0]
        self.horarioRecv = int(conteudo[1])
        self.tipoRecv = conteudo[2]
        self.conteudoRecv = conteudo[3]

        format_aux = recv.split("[")
        
        self.conteudoRecvLIST = ast.literal_eval("[" + format_aux[1])
        # print(self.conteudoRecv)
        # print(self.conteudoRecvLIST)
        # print(type(self.conteudoRecvLIST))
        if self.tipoRecv == "msg":
            self.conversa = conteudo[4] ##conversa da qual 
            self.usuario = conteudo[5]
            self.conteudoMsg = conteudo[6]
        
usuario = input("Insira o seu usuario: ")
while True:
    esc = int(input("Sair(0) Push(1) ou RepReq (2) ou Chat(3) ou Posts(4)? "))
    
    
    if esc == 0:
        break
    if esc == 1:
        conteudo = input("Mensagem a ser mandada: ")
        clientPush.send_string(f"{clientEnd},{horarioLocal},teste,{conteudo}")
        aumentarTempo()
    elif esc == 2:
        conteudo = input("Mensagem a ser mandada: ")
        clientReq.send_string(f"{clientEnd},{horarioLocal},req,{conteudo}")
        aumentarTempo()
        recv = clientReq.recv_string()
        print(recv)
    elif esc == 3:
        
        usuarioEsc = input("Insira usuario com o qual quer conversar: ")
       
        alfabet = sorted([usuario,usuarioEsc])
        conversa = f"{alfabet[0]}_{alfabet[1]}"
        ## Checar se existe TABLE com este nome
        clientReq.send_string(f"{clientEnd},{horarioLocal},reqChat,{conversa}") ##solicita o historico
        aumentarTempo()
        recv = clientReq.recv_string() ##adquire o historico
        msg = mensagem(recv)
        clientSub.subscribe(conversa)
        # print(f'esc 2: {msg.conteudoRecvLIST}')
        extracted_items = [item[0] for item in msg.conteudoRecvLIST]
        # print(f"extracted {extracted_items}")
        for item in extracted_items:
            print(item)
        
        while True: ##transformar isso em algo rodando paralelo, para o chat conseguir atualizar enquanto esta sendo digitado
            dialogo = input("Diz (EXIT para sair): ")
            if dialogo == "EXIT":
                break
            clientPush.send_string(f"{clientEnd},{horarioLocal},msg,{conversa},{usuario},{dialogo}")
            aumentarTempo()
            # print(f'dialogo: {clientSub.recv_string()}')
            aux = clientSub.recv_string()
            res = aux.split('\n')
            # print(f'1 {res[0]} 2 {res[1]}')
            historico = ast.literal_eval(res[1])
            # print(type(historico))
            print(historico)
            # extracted_items = [item[0] for item in historico]
            # print(f"extracted {extracted_items}")
            for item in historico: 
                # print(type(item))
                print(item[0])
            # print(dialogo)

        clientSub.unsubscribe(conversa)
        
    elif esc == 4:
        escPost = int(input("Postar(0) ou Ver Posts(1) ou Seguir Usuario(2)? "))
        if escPost == 0:
            conteudoPost = input("Digite oque quer postar: ")
            clientPush.send_string(f"{clientEnd},{horarioLocal},post,{usuario},{conteudoPost}")
            aumentarTempo()
        elif escPost == 1:
            clientReq.send_string(f"{clientEnd},{horarioLocal},verPost,{usuario}")
            aumentarTempo()
            recv = clientReq.recv_string()
            msg = mensagem(recv)
            # print(f'{recv}')
            # extracted_items = [item[0] for item in msg.conteudoRecvLIST]
            # print(f"extracted {extracted_items}")
            print('Posts recentes:')
            for item in msg.conteudoRecvLIST:
                # print(f'ver post printloop: {item}')
                print(f'{item[2]}')
            print('\n')

        elif escPost == 2:
            usuarioASeguir = input("Deseja seguir quem? ")
            clientPush.send_string(f"{clientEnd},{horarioLocal},seguir,{usuario},{usuarioASeguir}")
            aumentarTempo()

        
        
    
    



