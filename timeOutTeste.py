import time
import threading
import _thread
from tkinter import *
from datetime import datetime, timedelta

testeCpu = 0
relogio = 0


def renderProcess(processos):
    animation = Tk()

    canvas = Canvas(animation, width=800, height=600)
    canvas.pack()
    canvas.create_oval(10, 70, 30, 90, fill=processos[0].process_color)
    canvas.create_oval(10, 10, 30, 30, fill=processos[1].process_color)

    canvas.create_oval(15, 305, 35, 325)
    canvas.create_line(0, 50, 1000, 50)

    canvas.create_rectangle(10, 300, 40, 330)
    canvas.create_rectangle(10, 350, 40, 380)

    animation.update()
    for x in range(1, 120, 5):
        for item in processos:
            if item.state != 1:
                canvas.coords(1, 10, 70, 30, 90)

        canvas.move(1, 5, 0)
        canvas.move(2, 5, 0)
        print('--------------------------------->', canvas.coords(1))
        animation.update()
        time.sleep(1)


class Process:
    def __init__(self, tempo_exec, duracao_io, time_io, process_color, name):
        self.tempo_exec = tempo_exec
        self.duracao_io = duracao_io
        self.time_io = time_io
        self.numero_ios = 0
        self.state = 2
        self.timer = 0
        self.process_color = process_color
        self.name = name
        self.row = 0
        self.tempo_de_fila = 0
        self.start_io = datetime.now()


class Cpu:
    def __init__(self):
        self.busy = 0
        self.sopratermaiscoisa = 'xatuba de mesquita'


# STATE 1 = RODANDO |||| STATE 2 = ESPERA |||| STATE 3 = ENTRADA SAIDA ||||| state 4 = concluido


class Row:
    def __init__(self, tempo_fila):
        self.tempo_fila = tempo_fila


# filas = Row([5,10,15])
filas = [5, 10, 15, 20]

cpu = Cpu()


p1 = Process(20, [5, 5, 3], [3, 8, 15], 'yellow', 'p1')
p2 = Process(25, [2, 6, 4, 3], [3, 7, 12, 18], "blue", 'p2')
threads = []
check_state = 1

processos = [p1, p2]


def fazerIo(pIo):
    pIo.state = 3
    pIo.tempo_de_fila = 0
    pIo.start_io = relogio
    # pIo.start_io = datetime.now()
    # print('terminou')


def escalonarProcesso(ps, cpu):
    if ps[0].state == 2 and cpu.busy == 0:
        print('ESCALONOU PROCESSOa', ps[0].name, 'ESTADO = ', ps[0].state)
        rodarProcesso(ps[0], ps, cpu)
    elif ps[1].state == 2 or cpu.busy == 0:
        print('ESCALONOU PROCESSOb', ps[1].name, 'ESTADO  = ', ps[1].state)
        rodarProcesso(ps[1], ps, cpu)


def rodarProcesso(processo, list_processos, cpu):
    processo.state = 1
    cpu.busy = 1
    if processo.timer == processo.tempo_exec:
        processo.state = 4
        cpu.busy = 0
        return

    for i in range(processo.timer, processo.tempo_exec):
        for x in list_processos:
            if (x.start_io + timedelta(seconds=x.duracao_io[x.numero_ios - 1])) >= datetime.now():

            # if time_io >= datetime.now():
                x.state = 2

        if processo.tempo_de_fila >= filas[processo.row]:
            processo.row = processo.row + 1
            processo.tempo_de_fila = 0
            processo.state = 2
            cpu.busy = 0
            return

        processo.tempo_de_fila = processo.tempo_de_fila + 1
        global relogio
        print('RODANDO PROCESSOx: ', processo.name)
        print('------------->RELOGIO', relogio)
        relogio = relogio + 1

        time.sleep(1)
        processo.timer = processo.timer + 1
        if len(processo.time_io) > processo.numero_ios and processo.time_io[processo.numero_ios] == processo.timer:
            fazerIo(processo)
            processo.numero_ios = processo.numero_ios + 1
            processos.append(processos.pop(0))
            cpu.busy = 0
            return
            
        cpu.busy = 0


def set_process():
    qtd_process = input('Digite a quantidade de processos: ')
    qtd_process = int(qtd_process)
    processos = []

    for i in range(qtd_process):
        tempo_exec = input('Digite o tempo de execução do processo: ')
        duracao_io = input('Digite a duração do IO do processo: ')
        time_io = input('Digite o tempo de IO do processo: ')
        process_color = input('Digite a cor do processo: ')
        name = input('Digite o nome do processo: ')
        processos.append(Process(tempo_exec, duracao_io, time_io, process_color, name))
    # p1 = Process(20, [5, 5, 3], [3, 8, 15], 'yellow', 'p1')
    # p2 = Process(25, [2, 6, 4, 3], [3, 7, 12, 18], "blue", 'p2')    

    for item in processos:
        print(item.name)

def set_rows():
    qtd_rows = input('Digite a quantidade de filas: ')
    rows = []
    for i in range(int(qtd_rows)):
        tempo_fila = input('Digite o tempo de fila: ')
        rows.append(Row(tempo_fila))
    
    for item in rows:
        print(item.tempo_fila)

def menu():
    print('==================================')
    print('Escolha uma opção: ')            
    choice = 0
    choice = input("""
    1. Escolher quantidade de processos
    2. Escolher quantidade de filas
    3. Escalonar Processos
    4. Sair
    """)
    if choice == '1':        
        print(chr(27) + "[2J")
        print('==================================')
        print('Setar quantidade de processos')
        set_process()
        menu()
    elif choice == '2':
        print(chr(27) + "[2J")
        print('==================================')
        print('Setar quantidade de filas')
        set_rows()         
        menu()
    elif choice == '3':
        print(chr(27) + "[2J")
        while p1.state != 4 and p2.state != 4:
            escalonarProcesso(processos,cpu)
    elif choice == '4':
        print(chr(27) + "[2J")
        print('==================================')
        print('Saindo')
        print('==================================')
        sys.exit()
    else:
        menu()
menu()



# threading.Thread(target=escalonarProcesso,
#         args=(processos,)
#     ).start()


# _thread.start_new_thread ( escalonarProcesso, args[, processos] )
# t = threading.Thread(target=escalonarProcesso, args=(processos,))

# threads.append(t)
# t.start()
# t.join()


# print('--------> NUMERO THREADS', threading.active_count())
# renderProcess(processos)

# print(p1.state)
# print(p2.state)
# print('TEMPO EXECUCAO P1 ', p1.tempo_exec)
# print('TEMPO EXECUCAO P2 ', p2.tempo_exec)
