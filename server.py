import socket, threading

# Array para manter salvo as conexões
connections = []

def handle_client(connection: socket.socket, address: str):
    
	# Obtém a conexão do usuário para continuar recebendo e enviando suas mensagens.
      
  while True:
			try:
				# Fica escutando uma mensagem do usuário(client) através do recv()
				msg = connection.recv(1024)

				# Verificando se alguma mensagem foi recebida
				if msg:
						# Monta a mensagem no seguinte formato "De {IP} : {Port} - {Mensagem}"
						new_msg = f'De {address[0]}:{address[1]} - {msg.decode()}'

						# Imprime no console do Servidor a mensagem acima
						print(new_msg)
						
						# Transmite a mensagem para as conexões armazenadas no array de conexões
						broadcast(new_msg, connection)
				
				# Caso nenhuma mensagem seja recebida, a conexão é fechada
				else:
						close_connection(connection)
						break
			
			# Levanta uma Exception caso a conexão dê alguma problema 
			except Exception as e:
						print(f'Ocorreu um erro na conexão com o client: {e}')
						close_connection(connection)
						break

        
def broadcast(message: str, connection: socket.socket):
    
		# Transmite a mensagem para todas as conexões do array de conexões

    # Loop passando por todas as conexões
    for client in connections:
        # Verifica se a conexão é a que enviou a mensagem
        if client != connection:
            try:
                # Envia a mensagem para a o client
                client.send(message.encode())

            # Levanta uma Exception para caso o socket tenha falhado ou morrido
            except Exception as e:
                print('Error while broadcasting the message: {e}')
                close_connection(client)


def close_connection(conn: socket.socket):
    
		# Fecha uma conexão

    # Verifica se a conexão está no array de conexões
    if conn in connections:
        conn.close()
        connections.remove(conn)


def server():

    # Lida com as conexões utilizando threads

		# Definindo a porta do servidor
    SERVER_PORT = 12345
    
    try:
        # Cria o server com a porta definida acima
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', SERVER_PORT))
				# Definindo o máximo de conexões que o servidor suporta, nesse caso 4
        server_socket.listen(4)

        print('Servidor iniciado!💬')
        
        while True:

            # Aceita a conexão de clients
            socket_connection, address = server_socket.accept()
            # Adiciona a conexão o array de conexões
            connections.append(socket_connection)
						# Inicia uma thread para lidar com a conexão com o cliente, receber suas mensagens
						# e enviá-las para as outras conexão do array de conexões
            threading.Thread(target=handle_client, args=[socket_connection, address]).start()

		# Levanta uma Exception para caso ocorra algum problema na criação de uma instância de socket
    except Exception as e:
        print(f'Um erro ocorreu durante a criação de uma instância de socket: {e}')
    finally:
        # Finally é um bloco que sempre será executado, não importa se o bloco try gera um erro ou não
				# Com isso fechamos todas as conexões para garantir que não ocorra nenhum problema
        if len(connections) > 0:
            for conn in connections:
                close_connection(conn)

        server_socket.close()

# Inicia o servidor
if __name__ == "__main__":
    server()