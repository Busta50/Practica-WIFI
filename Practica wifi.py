import network
import socket
import time
import urequests

#Recuerden colocar las credenciales de la red donde harán la prueba
ssid = 'Desconocido_2.4'
password = 'ZG7SRn64DN'

#Creamos una presentación HTML basica para mostrar datos
html = """<!DOCTYPE html>
<html>
    <head>
    <style>
        h1 {text-align: center;}
        p {text-align: center;}
        div {text-align: center;}
    </style>
    <title>Sistemas programables</title> </head>
    <body> <h1>Jesus Arturo Bustamante Garces</h1>
    <h1>Practicas de WiFi para dias SIN laboratorio</h1>
    <a href="https://es.cooltext.com"><img src="https://images.cooltext.com/5626350.png" width="570" height="92" alt="Jesus Bustamante" /></a>
        <p>%s</p>
    </body>
</html>
"""

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

connectCount = 0



max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Conectando...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('Error al conectarse a la red')
else:
    print('Conectado')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

#Para obtener la hora, usamos la API IDTIME
r = urequests.get('http://worldtimeapi.org/api/ip')
result = str(r.content)
startTime = result[int(result.find("datetime")) + 11:30 + result.find("datetime")]


print('Start Time', startTime)
print('listening on', addr)

# Mediante esta instruccion nos muestra quien o quienes estan conectados
while True:
    try:
        cl, addr = s.accept()
        clientIP = addr[0]
        print('Conectado, con IP:', clientIP)
        request = cl.recv(1024)
        request = str(request)
        connectCount += 1
        countText = "This site has been accessed " + str(connectCount) + " time since " + startTime

        response = html % countText

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')