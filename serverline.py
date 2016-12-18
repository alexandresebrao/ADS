import simpy
import random

# Constantes
NUM_SERVERS = 2
RANDOM_SEED = 42
SIM_TIME = 200

# Variaveis
server_in_use = 0
clients = 0
line = []
time_in_line = []
time_in_server = []
clients_server = {}
clients_server[0] = 0
clients_server[1] = 0
avarage_time_create_process = []

# Popular listas
# De acordo com a tabela
time_between_arrival = []

for i in range(35):
    time_between_arrival.append(random.randint(0, 5))
for i in range(19):
    time_between_arrival.append(random.randint(5, 10))
for i in range(19):
    time_between_arrival.append(random.randint(10, 15))
for i in range(13):
    time_between_arrival.append(random.randint(15, 20))
for i in range(3):
    time_between_arrival.append(random.randint(20, 25))
for i in range(7):
    time_between_arrival.append(random.randint(25, 30))
for i in range(1):
    time_between_arrival.append(random.randint(30, 35))
for i in range(2):
    time_between_arrival.append(random.randint(35, 40))
for i in range(1):
    time_between_arrival.append(random.randint(40, 45))

server1_service_time = []

for i in range(6):
    server1_service_time.append(9.5)
for i in range(5):
    server1_service_time.append(10)
for i in range(23):
    server1_service_time.append(10.5)
for i in range(20):
    server1_service_time.append(11)
for i in range(21):
    server1_service_time.append(11.5)
for i in range(12):
    server1_service_time.append(12)
for i in range(9):
    server1_service_time.append(12.5)
for i in range(2):
    server1_service_time.append(13)
for i in range(1):
    server1_service_time.append(13.5)

server2_service_time = []

for i in range(5):
    server2_service_time.append(9.5)
for i in range(4):
    server2_service_time.append(10)
for i in range(15):
    server2_service_time.append(10.5)
for i in range(16):
    server2_service_time.append(11)
for i in range(23):
    server2_service_time.append(11.5)
for i in range(20):
    server2_service_time.append(12)
for i in range(10):
    server2_service_time.append(12.5)
for i in range(5):
    server2_service_time.append(13)
for i in range(2):
    server2_service_time.append(13.5)


class Server(object):
    def __init__(self, env, num_servers):
        self.env = env
        self.machine = simpy.Resource(env, num_servers)
        self.serverTime = 1

    def do(self, process):
        yield self.env.timeout(self.serverTime)
        print("procss %s left." % process)


def service(env, name, server, line, time_in_line, clients_server,
            server_in_use, time_in_server, servidor1_service_time,
            servidor2_service_time):
    line.append(len(server.machine.queue))
    print('%s arrives at the server at %.2f.' % (name, env.now))
    process_in_line = env.now
    with server.machine.request() as request:
            yield request

            if server_in_use:
                print("%s gonna use server 1" % name)
                server.serverTime = random.choice(servidor1_service_time)
                server_in_use = 0
                clients_server[0] += 1

            else:
                print("%s gonna use server 2" % name)
                server.serverTime = random.choice(servidor2_service_time)
                server_in_use = 1
                clients_server[1] += 1

            print('%s enters the server at %.2f.' % (name, env.now))
            # saves when the service is processed by the server
            process_out_line = env.now
            # calculate how long the service waiter for being processed
            time_in_line.append(process_out_line - process_in_line)
            # Process being processed
            print('%s will stay %d seconds on server' % (name,
                                                         server.serverTime))
            yield env.process(server.do(name))
            # saves when the service leaves the server
            process_out_server = env.now
            # calculate how long the service stayed in ther server
            time_in_server.append(process_out_server - process_in_line)
            print('%s leaves the server at %.2f.' % (name, env.now))


def setup(env, nun_server, time_between_arrival, avarage_time_create_process,
          clients, server1_service_time, server2_service_time, clients_server):
    # Create the environment
    environment = Server(env, nun_server)
    i = 0
    # Create more process while the simulation is running
    while True:
        # Time to create a new service
        time = random.choice(time_between_arrival)
        avarage_time_create_process.append(time)
        print('Next service will be created in %d seconds' % time)
        yield env.timeout(time)
        clients += 1
        env.process(service(env, 'process %d' % i, environment, line,
                            time_in_line, clients_server, server_in_use,
                            time_in_server, server1_service_time,
                            server2_service_time))
        i += 1


# Setup and start the simulation
random.seed(RANDOM_SEED)  # This helps reproducing the results
# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_SERVERS, time_between_arrival,
                  avarage_time_create_process, clients, server1_service_time,
                  server2_service_time, clients_server))
# Execute!
env.run(until=SIM_TIME)


# Answering the questions:
valores = 0
for value in line:
    valores += value
media_de_clients = valores/len(line)

valores = 0
for value in time_in_line:
    valores += value
media_de_tempo_fila = valores/len(time_in_line)

valores = 0
for value in time_in_server:
    valores += value
media_de_tempo_servidor = valores/len(time_in_server)

valores = 0
for value in avarage_time_create_process:
    valores += value
media_para_criar_processo = value/len(avarage_time_create_process)

# clients_server_1 = round(clients_server[0], 2)/round(clients, 2) * 100
# clients_server_2 = round(clients_server[1], 2)/round(clients, 2) * 100

print("\n\n\n")
print("Respostas para as perguntas")
print("\n\n\n")
print("O numero final de processos: %i" % clients)
print("Numero Médio de Clientes %s" % media_de_clients)
print("Tempo Medio de um Cliente na Fila: %i" % media_de_tempo_fila)
print("Tempo Medio no Sistema: %i" % media_de_tempo_servidor)
print("Tempo Medio para criar um processo: %i" % media_para_criar_processo)
# print("porcentagem de clientes no servidor 1: %f" % round(clients_server_1, 2))
# print("porcentagem de clientes no servidor 2: %f" % round(clients_server_2, 2))
