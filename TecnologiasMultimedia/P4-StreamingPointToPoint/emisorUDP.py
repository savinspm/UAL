# Importamos las librerias que vamos a usar
 
import socket
import sys  
import time 
import os
#Nos conectamos a el servidor 0.es.pool.ntp.org para sincronizar nuestro reloj con el receptor.
os.system('sudo ntpdate 0.es.pool.ntp.org')
# Declaramos las siguientes variables donde tenemos la informacion de los puertos a usar
# y la direccion IP del receptor UDP.
# UDP_PORT lo usamos para enviar chunks al receptor.
# UDP_PORT2 lo usamos para recibir un hola del receptor indicandonos que esta listo para recibir.
UDP_IP = '127.0.0.1'
UDP_PORT = 5681
UDP_PORT2 = 5682


# La funcion autoIncrement hace uso de la variable global rec y su funcion es incrementar una variable
# de tipo string en 1 cada vez que hes llamada; ej. Primera vez devuelve 000; Segunda vez devuelve 001
rec=0
def autoIncrement():	
	global rec
	pStart = 1 #adjust start value, if req'd 
	pInterval = 1 #adjust interval value, if req'd
	if (rec == 0): 
		rec = pStart 
	else: 
		rec = rec + pInterval 
	return str(rec).zfill(7)#El fichero puede ser como maximo 9,9 GB.
# Intentamos abrir el socket para la comunicacion streaming con el VLC que esta emitiendo.
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Fallo al conectar al socket del player'
    sys.exit()
print 'Socket creado'
# Declaramos las variables que usaremos para la conexion con el VLC que esta emitiendo. 
hostSource = ''
portSource = 8080
channelSource = ''
# Localizamos la direccion remota del reproductor. 
try:
    remote_ip = socket.gethostbyname(hostSource)
except socket.gaierror:
    #could not resolve
    print 'No es posible conectarse al host'
    sys.exit()
 
# Establecemos la conexion con el servidor VLC.
s.connect((remote_ip , portSource))
print 'Socket connectado al Reproductor VLC'
# Usamos el sock2 para recibir el hola del receptor indicando que esta listo.
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.bind((UDP_IP, UDP_PORT2))
data, addr = sock2.recvfrom(1024)
# Guardamos en message el mensaje que enviaremos al Servidor VLC.
message = 'GET /' + channelSource + ' HTTP/1.1\r\n\r\n'

#Nos preparamos para enviar
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Enviamos la solicitud HTTP al servidor VLC para que comience a enviarnos chunks
s.sendall(message)
print "Enviando datos via UDP a la direccion: " + UDP_IP

while True: 
	try :
	    # Recibimos un chunk del servidor VLC.
	    reply = s.recv(1024)
		# Enviamos el chunk recibido de VLC al receptor UDP añadiendo el identificador
		# y una estampa de tiempo.
	    sock.sendto(autoIncrement()+"----" + str(time.time())+"----"+reply , (UDP_IP, UDP_PORT))
	except socket.error:
	    #Send failed
	    print 'Mensaje no enviado'
	    sys.exit()
    #Now receive data
# Cerramos los sockets usados.
s.close()
sock.close()
sock.close()
sock2.close()
print 'Fichero enviado'


