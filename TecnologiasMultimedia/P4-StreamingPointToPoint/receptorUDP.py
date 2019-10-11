#Importamos la libreria socket.
import socket
import os
import time
import numpy as np
os.system('sudo ntpdate 0.es.pool.ntp.org')

#Indicamos la direccion del servidor.
UDP_IP = "127.0.0.1"
#Indicamos el puerto con el que trabajamos.
UDP_PORT = 5681
UDP_PORT2 = 5682

print "Preparado para recibir datos"
#Abrimos el socket para el envio UDP a traves de una direcion IP.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketPlayer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Indicamos la direccion IP y el puerto a usar al socket.
sock.bind((UDP_IP, UDP_PORT))
socketPlayer.bind(('', 8081))
socketPlayer.listen(1)
print 'Esperando'
conn, addr = socketPlayer.accept()
print 'Conexion establecida con VLC'
sock2.sendto("hola", (UDP_IP, UDP_PORT2))

 
#Mientras no nos llegue un mensaje de fin, seguiremos almacenando lo recibido en nuestro fichero.
#lista = np.empty([128], dtype=str)
lista = [None] * 128
bandera = 0
total = 0
data, addr = sock.recvfrom(2048)
elementos = data.split("----")
conn.sendall(elementos[2])



while True:
	data, addr = sock.recvfrom(2048)
	elementos = data.split("----")
	hora = elementos[1]	
	#Imprime el tiempo que tarda en llegar cada paquete
	print time.time() - float(hora)
	total+=1

	if bandera==1:
		if(lista[total%128]!= None):#Si el paquete no ha llegado, que no lo envie
			conn.sendall(lista[total%128])
	#Almacena cada elemento en su posicion
	lista[long((elementos[0]))%128]=elementos[2] 
	#Esto es para la primera iteracion
	if total == 127:
		bandera=1
lista.sort()	
sock.close()
conn.close()
sock2.close()
socketPlayer.close()