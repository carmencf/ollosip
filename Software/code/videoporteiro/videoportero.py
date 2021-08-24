
#VIDEO PORTERO VERSION 20/03/19

from importlib import import_module
#from threading import Thread
import threading
import os
from flask import Flask, render_template, Response

## instalar sudo pip install Flask-HTTPAuth

from flask_httpauth import HTTPBasicAuth

from camera_pi import Camera




import sys
import logging

from subprocess import PIPE, Popen
import re
import RPi.GPIO as GPIO 




#from kivy.app import App

from os import environ






import io
import urllib
#import picamera

import socket






import subprocess

import datetime
import json

import logging
import signal 
import time 


from ctypes import *
import linphone 
import pygame




# from camera_pi import Camera
cctv = Flask(__name__)


auth = HTTPBasicAuth()

users = {
    "megafono1": "proval",
    "susan": "bye",
    "videoportero": "proval"
}




#pygame.event.wait()
#VARIBLES GLOBALES DONDE DEFINIMOS LAS DIFERENRES IPS,PUERTOS DE TODOS LOS TERMINALES Y DISPOSITIVOS
#'''
#
MIEXTENSION=6000
MIEXTENSIONP='p6000'
EXT_USER1=6010
EXT_USER2=6013
EXT_DIRECCION=6002
EXT_XEFATURA=6003
EXT_SECRETARIA=6004
EXT_ELECTRONICA=6005
EXT_LLAMADA_GENERAL=6064



PATHSOUNDS='./sounds/'


IPCENTRALITA='192.168.0.150'
ipcamvideoportero='192.168.0.10'


puertocamvideoportero=6000



USER1='sip:'+str(EXT_USER1)+'@'+str(IPCENTRALITA)
USER2='sip:'+str(EXT_USER2)+'@'+str(IPCENTRALITA)
DIRECCION='sip:'+str(EXT_DIRECCION)+'@'+str(IPCENTRALITA)
XEFATURA='sip:'+str(EXT_XEFATURA)+'@'+str(IPCENTRALITA)
SECRETARIA='sip:'+str(EXT_SECRETARIA)+'@'+str(IPCENTRALITA)
ELECTRONICA='sip:'+str(EXT_ELECTRONICA)+'@'+str(IPCENTRALITA)
whitelist=[USER1,USER2,ELECTRONICA,DIRECCION,XEFATURA,SECRETARIA]


#VARIABLES GLOBALES PRINCIPALMENTE REFERIDAS AL ESTADO DE LAS LLAMADAS DE TELEFONO
registrada=False #variable que indica el estado de registro de la centralita asterix
llamada_entrante=''
llamada_saliente=''
LUZ_ESTADO=0
PUERTA_ESTADO=0
#entradas gpio numero
pulsador=17
#salidas
salida_luz=18
salida_puerta=27






#metodo para saber la ip de nuestro sistema
def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
        sleep(2)
    except: 
        print("Unable to get Hostname and IP") 




class RecibeComando():
    global LUZ_ESTADO
    global PUERTA_ESTADO
    
    def __init__(self):
        #global ipcamara2
        #global puertocamara2        
        
        HOST =ipcamvideoportero# get_Host_name_IP()#ipcamvideoportero#"192.168.1.110"#ipcamara2 
        PORT =puertocamvideoportero #6031#puertocamara2
    
        CONEXIONES = 1
        self.size = 1024
       
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#UDP
        #self.sock.setblocking(0)
        
        
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#STREAM
        try:
            #self.sock.bind((HOST, PORT))
            self.sock.bind((HOST, PORT))
        
            self.conectado = True            
        except:
            #variable donde almacenamos si ha establecido conexion con el puerto
            self.conectato=False
        
        print("SOCKET CREADOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        #self.sock.listen(CONEXIONES)#STREAM
    def start(self):
        self.quit = False
        #self._queue = deque()
        self._thread = threading.Thread(target=self.read_data)
        self._thread.daemon = False
        self._thread.start()    
        
    def stop(self):
        self.quit = True
        self.sock.close()
        self._thread.join()
            
    def read_data(self):  
        logging.info("SOCKET CORRIENDOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        while True:
            self.data, self.addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes #UDP
            #self.client, address = self.sock.accept() #STREAM
            print("Cliente connectado.")#STREAM
            print("SOCKET funcionando")
            
            
            #self.data = self.client.recv(self.size).rstrip() #STREAM
            if not self.data:
                continue
            print("Received command: %s" % self.data)
            if self.data == "ABRE PUERTA":
                print("ABRIENDO PUERTA")
                GPIO.output(27, GPIO.HIGH) 
                self.data=''
                sonidoabrepuerta(self)
                #self.client.send(self.data)
                #self.client.close()
                
            if self.data == "CIERRA PUERTA":
                print("CERRANDO PUERTA")
              
                GPIO.output(27, GPIO.LOW) 
                self.data=''
                #self.client.send(self.data)
                #self.client.close()
                         
            if self.data == "ENCIENDE LUZ":
                
                if (GPIO.input(salida_luz) == GPIO.LOW):
                    GPIO.output(salida_luz, GPIO.HIGH) 
                    self.data=''
                    print("LUZ ENCENDIDA")
                else:
                    GPIO.output(salida_luz, GPIO.LOW) 
                    print("LUZ APAGADA")
                    self.data=''
                
                #logging.info("Client asked server to quit")
                #self.client.send(self.data)
                #self.client.close()
                
               
        #return
    def dato(self,*args):
        return self.data
        

class Phone:

    
    def __init__(self, username='', password='', camera='', snd_capture='', snd_playback=''):
        self.quit = False
        self.pausa=False
        self.quit_when_registered=True
               
        self.whitelist = whitelist
       
        
        #ACTIVAR PARA LA VERSION 3.9.1#####################################################        
        callbacks = {
            'call_state_changed': self.call_state_changed,
            #'registration_state_changed':self.registration_state_changed,
           
        }
        # ####################################################################################
        #Los callbacks se utilizan en linphone para atender las diferentes tareas por si hay una llamada entrante       
        
               
       
       

        # Configure the linphone core
        logging.basicConfig(level=logging.INFO)
        signal.signal(signal.SIGINT, self.signal_handler)
        linphone.set_log_handler(self.log_handler)
        
        #ACTIVAR PARA LA VERSION 3.12.XXX#####################################################
        #self.core = linphone.Factory.get().create_core(callbacks, None, None) 
    
        #ACTIVAR PARA LA VERSION 3.9.1#####################################################        
        self.core = linphone.Core.new(callbacks, None, None)        
        
        
        
        
       
        
        self.core.max_calls = 1
        self.core.mic_enabled=True
        self.core.echo_cancellation_enabled =False
        self.core.echo_limiter_enabled=False
        
        self.core.video_capture_enabled = False
        self.core.video_display_enabled = False
       
        #self.core.ring=str(PATHSOUNDS)+'synth.wav'
        
        self.core.ring_level=100 # EST E PARAMETRO ME AJUSTA EL VOLUMEN DE SALIDA DEL ALTAVOZ SINO LO BAJO AQUI AUNQUE LO BAJE EN LA LLAMADA
                              # CON call.speaker_volume_gain=0.0  PREVALECE ESTE OJO
        
        #self.core.mic_gain_db=15.0
        #MIS VARIABLES
       
        
        logging.info( 'DISPOSITIVOS DE VIDEO ENCONTRADOS:')
        logging.info('%s', self.core.video_devices)
        logging.info( 'CODECS DE VIDEO ENCONTRADOS:')
        #logging.info('%s', self.core.video_codecs)        
        logging.info( 'DISPOSITIVOS DE SONIDO ENCONTRADOS:')
        logging.info('%s', self.core.sound_devices)
        
              
        self.core.capture_device = 'ALSA: USB PnP Sound Device'#snd_capture ALSA: default device
        
        
        self.core.playback_device ='ALSA: default device'
        self.core.video_device = 'V4L2: /dev/video0'
       
        

        self.configure_sip_account(username, password)
      


    def signal_handler(self, signal, frame):
        self.core.terminate_all_calls()
        self.quit = True

    def log_handler(self, level, msg):
        method = getattr(logging, level)
        method(msg)
        
    def registration_state_changed(self, core, proxy, state, message):
        global registrada
        if self.quit_when_registered:
            if state == linphone.RegistrationState.Ok:
            #if linphone.RegistrationState.Ok:
                
                logging.info( 'Registro de cuenta OK')
                logging.info('%s',self.core.proxy_config_list)
                self.core.config.sync()
                self.quit = True
                registrada=True
            #elif state == linphone.RegistrationState.Failed:
            elif linphone.RegistrationState.Failed:
                logging.info( 'Registro de cuenta FALLO')
                print ('Registro de cuenta FALLO: {0}'.format(message))
                self.quit = True   
                registrada=False
        



#FUNCIONES DEL PAQUETE LINPHONE PARA PYTHON
                '''
                linphone.CallState.
                Idle                      Initial call state 
                IncomingReceived          This is a new incoming call 
                OutgoingInit              An outgoing call is started 
                OutgoingProgress          An outgoing call is in progress 
                OutgoingRinging           An outgoing call is ringing at remote end 
                OutgoingEarlyMedia        An outgoing call is proposed early media 
                Connected                 Connected, the call is answered 
                StreamsRunning            The media streams are established and running 
                Pausing                   The call is pausing at the initiative of local end 
                Paused                    The call is paused, remote end has accepted the pause 
                Resuming                  The call is being resumed by local end 
                Refered                   The call is being transfered to another party, resulting in a new outgoing call to follow immediately 
                Error                     The call encountered an error 
                End                       The call ended normally 
                PausedByRemote            The call is paused by remote end 
                UpdatedByRemote           The calls parameters change is requested by remote end, used for example when video is added by remote 
                IncomingEarlyMedia        We are proposing early media to an incoming call 
                Updating                  A call update has been initiated by us 
                Released                  The call object is no more retained by the core 
                EarlyUpdatedByRemote   
                EarlyUpdating   
                
                
                '''




    def call_state_changed(self, core, call, state, message):
        global llamada_entrante
        if state == linphone.CallState.IncomingReceived :
            self.llamada=call
            if call.remote_address.as_string_uri_only() in self.whitelist:
                logging.info('%s',call.remote_address.as_string())
                logging.info( 'LLAMADA ENTRANTE')
                #self.sonido()
                #time.sleep(1.9)
                llamada_entrante=call.remote_address.as_string()
                params = core.create_call_params(call)
                core.accept_call_with_params(call, params)  
                self.core.mic_gain_db=10.0
                call.speaker_volume_gain=100.0  #especifica el volumen de salida del audio de la llamada
                #self.core.ring_level=100
                #call.speaker_volume_gain=8.0  #especifica el volumen de salida del audio de la llamada
                #call.microphone_volume_gain=2.0
            else:
                self.llamada_entrante=False
                core.decline_call(call, linphone.Reason.Declined)
                #llamada_entrante='False'
                #sm.current='VIDEOTELEFONO'
                
                logging.info( 'LLAMADA ENTRANTE RECHAZADA')
                chat_room = core.get_chat_room_from_uri(self.whitelist[0])
                msg = chat_room.create_message(call.remote_address_as_string + ' intento llamar')
                _chat_room.send_chat_message(msg)
                
        if state == linphone.CallState.End:
            logging.info( 'LLAMADA TERMINADA')
   
    def enviardtmf(self,*args):    
        self.current_call.send_dtmf(52)   
        logging.info('TONO DTMF ENVIADO')
   
    def llamada_recibida(self):
        if linphone.CallState.IncomingReceived: 
            return True                
  
 
    
    

    def configure_sip_account(self, username, password):
        # Configure the SIP account
        logging.info( 'CONFIGURANDO CUENTA SIP')
        proxy_cfg = self.core.create_proxy_config()
        
        #proxy_cfg.identity_address = self.core.create_address('sip:{username}@192.168.0.150'.format(username=username))
        
        proxy_cfg.identity_address = self.core.create_address('sip:'+str(username)+'@'+str(IPCENTRALITA))
        proxy_cfg.server_addr = 'sip:'+str(IPCENTRALITA)+':5060;transport=udp'
        proxy_cfg.register_enabled = True
        self.core.add_proxy_config(proxy_cfg)
        #auth_info = self.core.create_auth_info(username, None, password, None, None, '192.168.1.100')
        auth_info = self.core.create_auth_info(username, None, password, None, None, 'asterix')
        self.core.add_auth_info(auth_info)
        logging.info( 'CUENTA REGISTRADA SIP')
  
        '''  
    def run(self):
        while not self.quit:
            self.core.iterate() #ESTE ES EL BUCLE PRINCIPAL DE LINPHONE QUE DEBE SER LLAMADO PERIOICAMENTE. HEMOS FIJADO 20 VECES X S
            time.sleep(0.03)
        
    
            '''
   
        
    def registro(self,*args):
        if self.registrada:
            return True
        else:
            return False
        
    def llamar(self,number):
        self.core.ring_level=100
        params = self.core.create_call_params(None)# None para crear una nueva llamada, recogemos los parametros en params y se los 
                                                   #pasamos a la invitacion de llamada junto con la direccion sip a la que queremos llamar
       
        self.llamada=self.core.invite_with_params('sip:'+str(number)+'@'+str(IPCENTRALITA), params)
        
     
         
        
    def run(self,*args):
        
        while not self.quit:
            
            self.core.iterate() #ESTE ES EL BUCLE PRINCIPAL DE LINPHONE QUE DEBE SER LLAMADO PERIOICAMENTE. HEMOS FIJADO 20 VECES X S
            time.sleep(0.03)
            
      



#Clases e metodos relacionados co servidor mjpeg baseado no framwework flask



@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@cctv.route('/')
@auth.login_required
def index():
    """Video streaming home page."""
    auth.username()
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@cctv.route('/video')
@auth.login_required #el acceso al video requiere autorizacion
def video():
    """Video streaming route. Put this in the src attribute of an img tag."""
    auth.username() #colocamos aqui  para que acceder al video se requiera contrasena
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


class CamaraCctv(object):
    def __init__(self,host,port):
        print(host)
        print(port)
        self.host=host
        self.port=port
        self.thread = threading.Thread(target=self.run)
       
        
  
    def run(self):
        cctv.run(host=self.host,port=self.port,debug=False)#, threaded=True)
    def start(self):
            
            self.thread.start()       
            
            
        
    def stop(self):
        self.thread.join(timeout=1)# para el hilo y espera a que finalice la tarea un maximo de tiempo indicado en timeout


    





 
        
if __name__ == '__main__':
   
    GPIO.setmode(GPIO.BCM)  
    
    GPIO.setup(pulsador, GPIO.IN,pull_up_down=GPIO.PUD_UP) #GPIO17
    GPIO.setup(salida_luz, GPIO.OUT,initial=GPIO.LOW) #GPIO18
    GPIO.setup(salida_puerta, GPIO.OUT,initial=GPIO.LOW) #GPIO18
   
    #Y le damos un valor logico bajo para apagar el LED
    
   
    telefono1 = Phone(username=str(MIEXTENSION), password=str(MIEXTENSIONP), camera='', snd_capture='') #19 diciembre     
    
    def sonidotimbrar(self,*args):
        pygame.init()
        
        pygame.mixer.music.load(str(PATHSOUNDS)+"videoportero.wav")
        pygame.mixer.music.set_volume(0.5)# valores de 0.0 a 1.0
        pygame.mixer.music.play(1)  
        
    def sonidoabrepuerta(self,*args):
        pygame.init()
        
        pygame.mixer.music.load(str(PATHSOUNDS)+"puertaabierta2.wav")
        pygame.mixer.music.set_volume(1.0)# valores de 0.0 a 1.0
        pygame.mixer.music.play(1)                              
        
    def hacerllamada(self,*args):
        sonidotimbrar(self)
        telefono1.llamar(EXT_LLAMADA_GENERAL)
        #telefono1.llamar(EXT_ELECTRONICA)
     
    #GPIO.add_event_detect(pulsador, GPIO.RISING, callback=llamar)   
    GPIO.add_event_detect(pulsador, GPIO.FALLING, callback=hacerllamada)   
        
    
   
    #os.system('sudo mjpg_streamer -i "/usr/local/lib/input_uvc.so -d /dev/video0 -n -y -r 480x270 -f 15" -o "/usr/local/lib/output_http.so -w /usr/local/www -p 8081 -c "videoportero:proval" "&') 
    #os.system('sudo mjpg_streamer -i "/usr/local/lib/input_uvc.so -d /dev/video0 -n -y -r 800x480 -f 15" -o "/usr/local/lib/output_http.so -w /usr/local/www -p 8081 -c "videoportero:proval" "&') 
    
    
        
    comando=RecibeComando()
    comando.start()
    
    servidor=CamaraCctv('',8000)
    print('Sistema funcionando')
    servidor.start()
    print('Servidor de camara iniciado')    
    
 
   
    telefono1.run()