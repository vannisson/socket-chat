import socket, threading

def handle_messages(connection: socket.socket):
    
		# Lida com a mensagens recebidas de outras conexões

    while True:
					try:
							# Fica escutando uma mensagem do usuário(client) através do recv()
							msg = connection.recv(1024)

							# Verificando se alguma mensagem foi recebida
							if msg:
									print(msg.decode())

							# Caso nenhuma mensagem seja recebida, a conexão é fechada
							else:
									connection.close()
									break

					# Levanta uma exceção caso tenha ocorrido algum problema
					# de conexão com o servidor
					except Exception as e:
							print(f'Ocorreu algum problema de conexão com o servidor: {e}')
							connection.close()
							break

def client():

    # Realiza a conexão com o servidor
		
		# Servidor rodando localmente
    SERVER_ADDRESS = '127.0.0.1'
		# Porta do servidor
    SERVER_PORT = 12345

    try:
        # Instanciando um socket
        client_socket = socket.socket()
				# Conectando com o servidor
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        # Cria uma thread para lidar com o recebimento e envio de mensagens
        threading.Thread(target=handle_messages, args=[client_socket]).start()

        print('Você foi conectado ao chat!🥳 Que tal mandar uma mensagem?💬')

        # Fica lendo o input do usuário e transforma numa mensagem
        while True:
            new_msg = input()

						# Caso a mensagem seja apenas 'exit' significa que o usuário deseja sair do chat
            if new_msg == 'exit':
                break

            # Converte a mensagem para utf-8
            client_socket.send(new_msg.encode())

        # Fecha a conexão com o servidor depois do usuário digitar exit
        client_socket.close()

		# Levanta uma Exception caso ocorra um erro na conexão do socket do servidor
    except Exception as e:
        print(f'Ocorreu um erro na conexão do socket do servidor {e}')
        client_socket.close()

# Inicia o client
if __name__ == "__main__":
    client()