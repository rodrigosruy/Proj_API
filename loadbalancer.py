import zmq
import threading
import time
ctx = zmq.Context()
LBReq= ctx.socket(zmq.REQ)
LBRep= ctx.socket(zmq.REP)
LBPull= ctx.socket(zmq.PULL)
LBPush = ctx.socket(zmq.PUSH)
LBSub = ctx.socket(zmq.SUB)
LBPub = ctx.instance().socket(zmq.PUB)

poller = zmq.Poller()
poller.register(LBRep,zmq.POLLIN)
poller.register(LBPull,zmq.POLLIN)
poller.register(LBSub,zmq.POLLIN)
    

def checarUso():
    ctx = zmq.Context()
    
    servidores = []
    for x in range(5559,5600,2):
        try:
            socketTeste = ctx.socket(zmq.PUSH)
            socketTeste.bind(f"tcp://*:{x}")
            socketTeste.close()
        except:
            socketTeste.close()
            servidores.append([x,x+1])
    return servidores

LBPull.bind("tcp://*:5555")
LBRep.bind("tcp://*:5556")
LBPub.bind("tcp://*:5557")
LBSub.bind("tcp://*:5558")
LBSub.subscribe("")




print(checarUso())
ultimoUsado = -1
while True:
    portas = dict(poller.poll())
    if portas.get(LBPull) == zmq.POLLIN:
        recv = LBPull.recv_string()
        print(f"push recebido {recv}")
        servidoresDisp = checarUso()
        ultimoUsado = (ultimoUsado+1)%len(servidoresDisp)
        stringServ = f"tcp://localhost:{servidoresDisp[ultimoUsado][0]}"
        LBPush.connect(stringServ)
        LBPush.send_string(recv)
        print(f"push mandado {recv}")
        LBPush.disconnect(stringServ)
    if portas.get(LBRep) == zmq.POLLIN:
        recv = LBRep.recv_string()
        print(f"Req recebido {recv}")
        servidoresDisp = checarUso()
        ultimoUsado = (ultimoUsado+1)%len(servidoresDisp)
        stringServ = f"tcp://localhost:{servidoresDisp[ultimoUsado][1]}"
        LBReq.connect(stringServ)
        LBReq.send_string(recv)
        print(f"Req mandado {recv}")
        recv = LBReq.recv_string()
        print(f"Rep Recebido {recv}")
        LBRep.send_string(recv)
        print(f"Rep mandado {recv}")
        LBReq.disconnect(stringServ)
    if portas.get(LBSub) == zmq.POLLIN:
        msg = LBSub.recv_string()
        print(f"pub recebido {msg}")
        LBPub.send_string(msg)
        print(f"pub mandado {msg}")

    
    







