

#from os import environ
#environ['SDL_VIDEO_ALLOW_SCREENSAVER']='1'
#from kivy.config import Config
#Config.set('graphics', 'fullscreen', 'auto')
#Config.set('graphics', 'allow_screensaver', '0')

import kivy
from kivy.config import ConfigParser
from kivy.config import Config
from kivy.core.image import Image as CoreImage
config = ConfigParser()
config.read('ollosip.ini')
#'dock'            activa o teclado na parte inferior
#systemandmulti   activa o teclado nunha venta flotante que podemos mover
Config.set('kivy', 'keyboard_mode', 'systemanddock') 
from kivy.app import App
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.effectwidget import EffectWidget
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.animation import AnimationTransition
from kivy.properties import StringProperty,BooleanProperty,NumericProperty,ListProperty,ObjectProperty,DictProperty
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from collections import deque
from kivy.uix.settings import SettingsWithTabbedPanel,SettingsWithSpinner,SettingsWithSidebar
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle,Line
from kivy.uix.behaviors import ButtonBehavior,ToggleButtonBehavior
from kivy.uix.image import Image as kivyImage 
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import Screen, ScreenManager,WipeTransition,FadeTransition,FallOutTransition,RiseInTransition,SwapTransition

from kivy.uix.textinput import TextInput
from kivy.uix.settings import Settings 
from kivy.lang import Builder 
import os
import re

import fileinput
import threading
from threading import Thread
import io
import urllib
import struct
import datetime
import signal 
import socket

from ctypes import *
from functools import partial 

import linphone 
from digitalclock import DigitalClock
from volumen_rect import VolumenRect

from botones import BotonColor,BotonI,BotonLed,IconBoton,IconButton,BotonLedToggle

#VARIBLES GLOBALES DONDE DEFINIMOS LAS DIFERENRES IPS,PUERTOS DE TODOS LOS TERMINALES Y DISPOSITIVOS
#'''

EXT_USER1=6010
EXT_USER2=6013
EXT_DIRECCION=6002
EXT_XEFATURA=6003
EXT_SECRETARIA=6004
EXT_ELECTRONICA=6005
EXT_VIDEOPORTERO=6000#config.get('videoportero', 'extension')#6000

MIEXTENSION=config.get('terminal', 'extension')#6005
MIEXTENSIONP=str(config.get('terminal', 'clave'))#'p6005'

IPCENTRALITA=str(config.get('terminal', 'ipbx')) #'192.168.0.150'  #IES PROVAL
PATH='./imaxes/'
PATHSOUNDS='./sons/'
PATHVIDEO='./VIDEOS/'


#'192.168.0.12' #ethernet .22 capturamos la ip de ollosip.ini y lo convertimos a string para
#que pueda ser utilizado por el programa, puesto que tiene que ser tipo string
ipelectronica=str(config.get('sistema', 'ip'))
                                               
                

MIIP=ipelectronica
USER2='sip:'+str(EXT_USER2)+'@'+str(IPCENTRALITA)
USER1='sip:'+str(EXT_USER1)+'@'+str(IPCENTRALITA)
DIRECCION='sip:'+str(EXT_DIRECCION)+'@'+str(IPCENTRALITA)
XEFATURA='sip:'+str(EXT_XEFATURA)+'@'+str(IPCENTRALITA)
SECRETARIA='sip:'+str(EXT_SECRETARIA)+'@'+str(IPCENTRALITA)
ELECTRONICA='sip:'+str(EXT_ELECTRONICA)+'@'+str(IPCENTRALITA)
ENTRADA_PRINCIPAL='sip:'+str(EXT_VIDEOPORTERO)+'@'+str(IPCENTRALITA)

#colocamos as direccions das que a clase phone aceptara chamadas, o resto seran rexeitadas
whitelist=[ENTRADA_PRINCIPAL] 

#VARIABLES GLOBALES PRINCIPALMENTE REFERIDAS AL ESTADO DE LAS LLAMADAS DE TELEFONO
llamada_entrante=''
llamada_in=False
llamada_saliente=''
videollamada_saliente=''
llamada_extension=0
nivel_sonido_telefono=50
SCREEN_ACTIVA='OLLOSIP'
CCTV_ZOOM=1
volumen_sistema=50.0
volumen_microfono=10.0


class SonidoClick():
    sound = SoundLoader.load(str(PATHSOUNDS)+'timbre_portal.wav')
      
    def __init__(self,son):
       
        self.sonido=son 
       
       
        
       
    def click(self):
        if self.sound:
            sound.volume=0.6      
            Clock.schedule_once(partial(self.suena,self.sound))
           
        return True
    def suena(self,sonido,*args):
        try:
            sonido.play()
            return
        except:
            pass
        #self.sound.stop()        

""" 
#ESTA CLASE NOS SIRVE PARA ENVIAR COMANDOS DE CONTROL, PARA ACITVAR SONIDOS EN EL MEGAFONO 
COMO PARA ABRIR LA PUERTA Y ENCENDER LA LUZ DEL VIDEOPORTERO MEDIANTE EL EMPLEO DE UN 
SOCKET UPD.ACTUA EN MODO CLIENTE. EL SERDIDOR SE INSTALARA EN LOS ALTAVOCES Y EN LA 
UNIDAD EXTERIOR DEL VIDEOPORTERO IP

"""

class EnviaComando():
        
    def __init__(self,ip,puerto):
        BUFSIZE=1024
        self.ip=ip
        self.puerto=puerto
        self.client_socket =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
           
    def envia(self,comando):    
       
        direccion=(self.ip,self.puerto)
        try:
            self.client_socket.sendto(comando ,direccion)
        except:
            return False
       
        


    
            






class DisplayCctv(Image): #SEVER
   
    url = StringProperty()  
    hora=StringProperty()
   # pantalla=ObjectProperty(source='./imaxes/novideo600.png' )
    def __init__(self, **kwargs):
        
        #con super heredamos de la clase screen todos los atributos de esta
        super( DisplayCctv, self).__init__(**kwargs)   
        self._image_buffer = None
        self.cctv_no=Image( source='./imaxes/novideo600.png') #str(PATH)+
    def on_press(self, *args):
        pass
    
    def start(self):
        
        self.quit = False
       
        self._thread = threading.Thread(target=self.read_stream)
        self._thread.daemon = True
        self._thread.start()
       
       
        Clock.schedule_interval(self.update_image, 1 / 32)

    def stop(self):
        self.quit = True
        
        Clock.unschedule(self.update_image)
       
    def read_queue(self):
        pass

    def read_stream(self):
        try:
            #print(self.url)
            self._image_buffer =self.cctv_no
            stream = urllib.urlopen(self.url)
        except:# IOError as e:
            #se non se logra conectar coa camara devolve unha imaxe fixa que indique
            #que non hai video na camara
            self._image_buffer =self.cctv_no
          
            self.stop()#self.quit=True
            return  False
        
        bytes = b''
       
       
        while  not self.quit:    
           
            bytes+=stream.read(1024)
            #caracteres que indican el inicio de un nuevo frame jpeg
            a = bytes.find('\xff\xd8')
            #caracteres que indican el final de un nuevo frame jpeg
            b = bytes.find('\xff\xd9')
            #comprobomas que hemos capturado los dos indicadores, se los sacamos y ya tenemos
            #el frame jpeg completo
            if a != -1 and b != -1: 
                jpg = bytes[a:b + 2] 
                bytes = bytes[b + 2:]
                #comvertimos el frame en un objeto similar a un fichero, pero en memoria
                #( en python el objeto es io.BytesIO)
                data = io.BytesIO(jpg) 
                #creamos una imagen con los datos del frame almacenado en memoria
                self._image_buffer=CoreImage(data,ext="jpeg",nocache=True,scale=0.1) 
             
                
              
   
   
    def update_image(self, *args):
        
        im = None
        im = self._image_buffer
                        
       
        #actualizamos la hora al mismo tiempo que la imagen, en caso contrario la fecvha 
        #y hora se sobreimpresiona so unha vez
        
        # con esto le sacamos los tres ultimos caracteres del string
        self.hora= str(datetime.datetime.now())[:-3] 
        
        self._image_buffer = None        
        if im is not None:
            
            
            self.texture = im.texture
            self.texture_size = im.texture.size
          

 ########### fin clase DisplayCctv    
 
 
class CamaraCctv(ButtonBehavior,AnchorLayout):
    nombre=StringProperty()
    h=StringProperty()
    url = StringProperty()
    #print(url)       
    def on_press(self, *args):
        pass        
    def start(self):
        self.ids.camara.start()
    def stop(self):
        self.ids.camara.stop()    
    def actualiza_hora(self,*args):
        self.h=self.ids.camara.hora
        #print(self.ids.camara.height)
        #print(self.ids.camara.texture.x)
        
Builder.load_string("""
    
<CamaraCctv>:    
# con anchor_x e anchor_y conseguimos que los widgets que se coloquen 
#dentro de la capa anchor layout se situen en la posicion que queramos 
#en este caso arrriba a la izquierda
    anchor_x:'center'
    anchor_y:'top'     
    
    DisplayCctv: 
        id:camara
        texture:self.texture      
        url:root.url       
        on_hora:root.actualiza_hora(args[0])            

    BoxLayout:  
        orientation:'horizontal'
        pos_hint:None,None
        size_hint:0.9,0.2       
        pos:0,10
                        
        Label:
            size_hint:1,0.4        
            markup:True
            text:root.nombre
            font_size:self.width*0.1
            halign:'center'
            color:0.5,0.5,0.5,1
        Label:            
            size_hint:1,0.4
            font_size:self.width*0.065
            text:root.h
            halign:'left'       
        
""")
    
       

class Phone(EventDispatcher):
    volumen_altavoz=NumericProperty(25.0)
    
    def __init__(self, username='', password='', camera='', snd_capture='', snd_playback='',**kwargs):
        
        
        #REGISTRAMOS LOS EVENTOS CREADOS CON NUESTROS NOMBRES QUE LUEGO UTILIZAMOS 
        #EN EL RESTO DE LAS SCREENS CON KIVY
        self.register_event_type('on_registrar') 
        self.register_event_type('on_noregistrado') 
        self.register_event_type('on_llamada_entrante') 
        self.register_event_type('on_llamada_terminada') 
        self.register_event_type('on_llamada_atendida') 
        super(Phone, self).__init__(**kwargs)    
        
        self.quit = BooleanProperty(False)        
        self.quit_when_registered=False       
        self.pausa=False
        self.whitelist = whitelist
        
        #ACTIVAR PARA LA VERSION 3.9.1#####################################################        
        self.callbacks = {
            'global_state_changed': self.global_state_changed,
            'call_state_changed': self.call_state_changed,
            'registration_state_changed':self.registration_state_changed,           
        }
        # #################################################################################
        #Los callbacks se utilizan en linphone para atender las diferentes tareas 
        #por si hay una llamada entrante       

        # Configure the linphone core
       
        signal.signal(signal.SIGINT, self.signal_handler)
       
        #ACTIVAR PARA LA VERSION 3.9.1#####################################################        
        self.core = linphone.Core.new(self.callbacks, None, None)     
        
        self.registrada=False
        self.core.max_calls = 1      
        self.core.echo_cancellation_enabled =False
        self.core.video_capture_enabled = False
        self.core.video_display_enabled = False        
     
        self.core.capture_device = 'ALSA: USB PnP Sound Device'
        self.core.playback_device ='ALSA: default device'
        self.core.ringer_device='default device'
        self.core.video_device = 'V4L2: /dev/video0'
        
        self.core.ring=str(PATHSOUNDS)+'timbre_portal.wav'#'synth.wav'
        self.core.ring_level=0
        self.core.mic_gain_db=5.0
        #MIS VARIABLES
        self.llamada_entrante=False
        self.configure_sip_account(username, password)

    def signal_handler(self, signal, frame):
        self.core.terminate_all_calls()
        self.quit = True   
    
    def global_state_changed(*args, **kwargs):
        pass
    
        #print("global_state_changed: %r %r" % (args, kwargs))   
    
    
    def registration_state_changed(self, core,proxy,state, message):
        global registrada
        if self.quit_when_registered:
            if state == linphone.RegistrationState.Ok:
                
                #print( 'Registro de cuenta OK')
                #print('%s',self.core.proxy_config_list)
                self.core.config.sync()
                self.quit = True
                registrada=True
                self.dispatch('on_registrar')
            
            elif linphone.RegistrationState.Failed:
                #print( 'Registro de cuenta FALLO')
                #print ('Registro de cuenta FALLO: {0}'.format(message))
                self.dispatch('on_noregistrado')
                self.quit = True   
                registrada=False
        



                """
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
                Refered                   The call is being transfered to another party, 
                                        resulting in a new outgoing call to follow immediately 
                Error                     The call encountered an error 
                End                       The call ended normally 
                PausedByRemote            The call is paused by remote end 
                UpdatedByRemote           The calls parameters change is requested by remote end, 
                                          used for example when video is added by remote 
                IncomingEarlyMedia        We are proposing early media to an incoming call 
                Updating                  A call update has been initiated by us 
                Released                  The call object is no more retained by the core 
                EarlyUpdatedByRemote   
                EarlyUpdating   
                
                
                """




    def call_state_changed(self, core, call, state, message):
        global llamada_entrante
        global llamada_extension
        global llamada_in
        if state == linphone.CallState.IncomingReceived :
            self.llamada=call
            if call.remote_address.as_string_uri_only() in self.whitelist:               
                llamada_entrante=call.remote_address.as_string()
                llamada_extension=re.search(r'\d+',llamada_entrante).group()
                #pasamos el string a numero de extension               
                llamada_extension=int(llamada_extension)
                #extraemos de la direccion del que llama     
                #print( llamada_extension)
                self.dispatch('on_llamada_entrante')               
                llamada_in=True             
               
            else:
                llamada_in=False
                core.decline_call(call, linphone.Reason.Declined)                
                self.dispatch('on_llamada_terminada')               
                logging.info( 'LLAMADA ENTRANTE RECHAZADA')
                chat_room = core.get_chat_room_from_uri(self.whitelist[0])
                msg = chat_room.create_message(call.remote_address_as_string + ' intento llamar')
                chat_room.send_chat_message(msg)
                
        if state == linphone.CallState.End:           
            self.dispatch('on_llamada_terminada')
            llamada_in=False           
            
        if state== linphone.CallState.Connected:
            self.dispatch('on_llamada_atendida')
           
            
    def enviardtmf(self,*args):    
        self.current_call.send_dtmf(52)   
        logging.info('TONO DTMF ENVIADO')
   
    def llamada_recibida(self):
        if linphone.CallState.IncomingReceived: 
            return True                
  
   ## FUNCION PARA COGER LA LLAMADA CUANDO PULSAMOS EL BOTON DE DESCOLGAR   
    
    def on_registrar(self, *args): 
        pass     
    def on_noregistrado(self, *args): 
        pass         
    def on_llamada_entrante(self, *args): 
        pass   
    
    def on_llamada_terminada(self, *args): 
        pass     
    def on_llamada_atendida(self, *args): 
        pass  
    def on_volumen_altavoz(self,*args):
        volumen_sistema= self.volumen_altavoz
        if llamada_in==True:
            #se ai unha chamada en curso actualiza o volumen de saida do audio da chamada
            self.llamada.speaker_volume_gain=volumen_sistema  
        #print(volumen_sistema)
        
        
    def descolgar(self,*args):
        global volumen_sistema
        if llamada_in==True:
           
            params = self.core.create_call_params(self.llamada)    
            self.core.accept_call_with_params(self.llamada, params)
            #especifica el volumen de salida del audio de la llamada         
            self.llamada.speaker_volume_gain=volumen_sistema  
            
        
    def colgar(self,*args):
        llamada_in=False       
        self.core.terminate_all_calls()
      
     
        
    def llamar(self,number):
        
        # None para crear una nueva llamada, recogemos los parametros en params y se los 
        #pasamos a la invitacion de llamada junto con la direccion sip a la que queremos llamar        
        params = self.core.create_call_params(None)       
        self.llamada=self.core.invite_with_params('sip:'+str(number)+'@'+str(IPCENTRALITA), params)      
       
        
    def pausar(self,*args):       
        self.core.play_file=(str(PATHSOUNDS)+'synth.wav')
        if self.pausa:
            self.pausa=False           
            self.core.resume_call(self.llamada)           
        else:                   
            self.core.pause_call(self.llamada)
            self.pausa=True
               
        
        

    def configure_sip_account(self, username, password):
        # Configure the SIP account
        self.quit_when_registered=True
        #print( 'CONFIGURANDO CUENTA SIP')
        self.proxy_cfg = self.core.create_proxy_config()        
        self.proxy_cfg.identity_address = self.core.create_address('sip:'+str(username)+'@'+str(IPCENTRALITA))
        self.proxy_cfg.server_addr = 'sip:'+str(IPCENTRALITA)+':5060;transport=udp'
        self.proxy_cfg.register_enabled = True
        self.core.add_proxy_config(self.proxy_cfg)       
        auth_info = self.core.create_auth_info(username, None, password, None, None, 'asterix')
        self.core.add_auth_info(auth_info)
        #print( 'CUENTA REGISTRADA SIP')  
       
        
    def eliminar_registro(self, username, password):
        self.proxy_cfg.edit()
        self.configure_sip_account(username, password)      
        
    def activar_registro(self):
        self.proxy_cfg.done()        
        
    def mute(self):
        global nivel_sonido_telefono
        self.core.ring_level=0
        
    def un_mute(self):
        self.core.ring_level=nivel_sonido_telefono       
        
    def registro(self,*args):
        if self.registrada:
            return True
        else:
            return False
        
    #ESTE ES EL BUCLE PRINCIPAL DE LINPHONE QUE DEBE SER LLAMADO PERIOICAMENTE. 
    #HEMOS FIJADO 11 VECES X S       
    def run(self,*args):      
        self.core.iterate()       
            
            
    def start(self):
        Clock.schedule_interval(self.run, 1 / 11)

   
   
  



class MjpegCCtv(ButtonBehavior,Image):

    url = StringProperty()
    cctv_no=Image( source='./imaxes/novideo600.png')
   
    def on_press(self, *args):
        pass
    
    def start(self):
        self.quit = False
        self._queue = deque()
        self._thread = threading.Thread(target=self.read_stream)       
        self._thread.start()       
        self._image_buffer = None
        Clock.schedule_interval(self.update_image, 1 / 30)

    def stop(self):
        self.quit = True       
        Clock.unschedule(self.update_image)
        
    def read_queue(self):
        pass    
     
    
    def read_stream(self):
        try:
            self._image_buffer =self.cctv_no
            stream = urllib.urlopen(self.url)
        except:
            self._image_buffer =self.cctv_no
            self.quit=True 
        
        bytes = ''        
        while  not self.quit:             
            bytes+=stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]               
                data = io.BytesIO(jpg)
                im = CoreImage(data,ext="jpeg",nocache=True,scale=0.5)                
                self._image_buffer = im              
        return  

    def update_image(self, *args):
        im = None
        im = self._image_buffer
        self._image_buffer = None       
        if im is not None:
            self.texture = im.texture
            self.texture_size = im.texture.size
   
 

#CONTROL DE VIDEOPORTERO   
    
class Videoportero_screen(Screen):   
   
    def __init__(self, **kwargs):
        #con super heredamos de la clase screen todos los atributos de esta
        super( Videoportero_screen, self).__init__(**kwargs)    
       
        global volumen_microfono
        global volumen_altavoz
        IPVIDEOPORTEROEXT=config.get('videoportero', 'ipvideoportero')        
        PORTOVIDEOPORTERO=config.get('videoportero', 'puerto')
        #print(IPVIDEOPORTEROEXT)        
        capa= BoxLayout(size_hint=(None,None),size=(800, 480),orientation='vertical')       
        with capa.canvas.before:
            rect = Rectangle(source=str(PATH)+'fondo41.png',size=capa.size, pos=capa.pos)
            
        capa.opacity=1
        #debe ser FloatLayout para que el widget BotonLed funcione
        capa2= FloatLayout(size_hint=(None,None),size=(800, 440),pos=(0,0))        
        capa1=RelativeLayout(pos_hint_x=None,size_hint_x=None,size=(800, 40),pos=(0,440))
        self.capacamara=BoxLayout(size_hint=(None,None),size=(490, 400),pos=(5,60))
        
        with capa1.canvas.before:
           
            Color(0.15,0.15,15,0.1)
            self.r1=Rectangle(size=capa1.size, pos=capa1.pos)           
        
        atras=BotonI( imagen=str(PATH)+'casa_white.png',size_hint_x=0.1,pos=(750,0),size=(35,35),trasparencia=0.2)        
        self.imagencon = Image( source=str(PATH)+'load3.gif',size_hint_x=None,pos=(10,0),opacity=0.2)
        self.imagencon.anim_delay=0    
        self.textocon = Label(text='Conectando',bold = True,font_size=18,color=[1,1,1,1],size_hint_x=None,pos=(90,0))      
        reloj=DigitalClock(size_hint_x=0.3, pos=(500,0),font_size=24, style='cool', halign='right', valign='middle')     
      
        capa1.add_widget(self.imagencon)
        capa1.add_widget(self.textocon)       
        capa1.add_widget(reloj)   
        capa1.add_widget(atras)   
        #CAPA PARA INFO,RELOJ ETC COLOCADA EN LA PARTE SUPERIOR DE LA PANTALLA
        capa.add_widget(capa1)
        
       
        self.CAM1=BotonLedToggle(pos=(600,300),size=(200,100),imagen=str(PATH)+'camara_white.png',text='',opacity=0.7)        
        self.ABRIR=BotonLed(pos=(600,200),size=(200,100),imagen=str(PATH)+'chave2.png',text='',opacity=0.7,group='zona')  
        self.LUZ=BotonLed(pos=(600,100),size=(200,100),imagen=str(PATH)+'luz_white.png',text='',opacity=0.7,group='zona')       
        self.MUTE=BotonLedToggle(pos=(600,0),size=(200,100),imagen=str(PATH)+'mute_white.png',text='',opacity=0.7,group='zona',state="down") 
        self.HABLAR=BotonColor(pos=(500,0),size=(100,400),imagen=str(PATH)+'micro_white.png',text=' ',opacity=0.4)      
      
        capa2.add_widget(self.MUTE)
        capa2.add_widget(self.LUZ)
        capa2.add_widget(self.ABRIR)
        capa2.add_widget(self.HABLAR)     
        capa2.add_widget(self.CAM1)       
      
        self.camaraip= MjpegCCtv(url='http://videoportero:proval@'+str(IPVIDEOPORTEROEXT)+':'+str(PORTOVIDEOPORTERO)+'/?action=stream') 
        self.ImagenVideo = Image( source=str(PATH)+'novideoip.png')
        self.micamara=self.ImagenVideo
        
        self.capacamara.add_widget(self.micamara)
        capa2.add_widget(self.capacamara)       
        capacontroles=BoxLayout(orientation='horizontal',size_hint=(None,None),size=(500, 40),pos=(0,0)) 
        self.Imic=Image( source=str(PATH)+'Mic32.png',size_hint=(None,1),pos=(0,0))
        
        self.volumeMic = Slider(value=volumen_microfono,pos=(0,40),value_track=True, 
                                value_track_color=[0, 0, 1, 0.5],
                                value_track_width=3,border_horizontal= [0, 10, 0, 10],cursor_size=(16,20),
                                orientation='horizontal',min=0, max =15)
        self.volumeMic.bind(value=self.volumen_mic)
        
        self.Ialtavoz=Image( source=str(PATH)+'speaker32.png',size_hint=(None,1),pos=(0,0))
        self.volumeAltavoz = Slider(value=volumen_microfono,pos=(0,40),value_track=True,
                                    value_track_color=[0, 0, 1, 0.5],value_track_width=3,
                                    border_horizontal= [0, 10, 0, 10],cursor_size=(16,20),
                                    orientation='horizontal',min=0, max =100)
        self.volumeAltavoz.bind(value=self.volumen_altavoz)      
    
        capacontroles.add_widget(self.Imic)   
        capacontroles.add_widget(self.volumeMic) 
        capacontroles.add_widget(self.Ialtavoz)    
        capacontroles.add_widget(self.volumeAltavoz)   
        capa2.add_widget(capacontroles)        
        
        capa.add_widget(capa2) #EL RESTO DE LA PANTALLA[] 
        
        telefono1.start()        
        #empleamos el evento creado on_registrar en la clase Phone
        telefono1.bind(on_registrar=self.registrado) 
        #empleamos el evento creado on_registrar en la clase Phone 
        telefono1.bind(on_noregistrado=self.noregistrado)    
       
        #anado la capa que contiene todos los widgets creados al propio ,self, screen Principal_screen
        self.add_widget(capa) 
           
        atras.bind(on_press=self.cambio)    
        self.CAM1.bind(on_press=self.controlcamara)
        self.MUTE.bind(on_press=self.control_mute)
        self.HABLAR.bind(on_release=self.descolgar)
        self.LUZ.bind(on_press=self.control_luz)
        self.ABRIR.bind(on_press=self.abrir)
        self.ABRIR.bind(on_release=self.cerrar)       
        
        self.comando=EnviaComando(str(IPVIDEOPORTEROEXT),EXT_VIDEOPORTERO)
        #self.sonido=SonidoClick('timbre_portal.wav')
       
        
        #CONTROL DE VIDEOPORTERO
   
    def volumen_mic(self,*args):       
        telefono1.core.mic_gain_db= self.volumeMic.value   
        volumen_microfono=self.volumeMic.value  
        
    def volumen_altavoz(self,*args):    
        telefono1.core.ring_level= int(self.volumeAltavoz.value)#cambia el volumen del ring del linphone
        volumen_altavoz=self.volumeAltavoz.value   
          
    
    def descolgar(self,*args):
        global llamada_in
        #EN ESTE CASO SE ENTRA EN EL MENU CUANDO ALGUIEN TIMBRA      
        if llamada_in:                 
            if self.HABLAR.state=="down":
                telefono1.descolgar()    
            else:    
                telefono1.colgar()                
                self.desactivacamara()
                #se va a la screen con nombre OLLOSIP 
                self.manager.current = SCREEN_ACTIVA
        #EN ESTE OTRO CASO ES CUANDO ENTRAMOS DESDE EL MENU PRINCIPAL SIN LA EXISTENCIA 
        #DE LLAMADA AL VIDEOPORTERO
        else: 
            if self.HABLAR.state=="down":
                    telefono1.llamar(EXT_VIDEOPORTERO)  
            else:    
                telefono1.colgar()                 
                self.desactivacamara()
    #CONTROL DE VIDEOPORTERO        
    def control_mute(self,*args):
        if self.MUTE.state=='normal':
            self.MUTE.imaxe=str(PATH)+'mute_off.png'
            telefono1.mute()#core.ring_level=0          
            volumen_altavoz=0
            
        else:
            telefono1.un_mute()
            self.MUTE.imaxe=str(PATH)+'mute_white.png'       
        
        pass
    def control_luz(self,*args):
       
       
        
        self.comando.envia('ENCIENDE LUZ')
        
        
    def abrir(self,*args):
        self.comando.envia('ABRE PUERTA')
    def cerrar(self,*args):
        self.comando.envia('CIERRA PUERTA')       
    
    def controlcamara(self,*args):
        if self.CAM1.state=="down":
            self.activacamara()
        else:
            self.desactivacamara()
           
    def activacamara(self,*args):
        self.CAM1.state="down"
        self.capacamara.remove_widget(self.micamara) 
        self.camaraip.start()
        self.micamara=self.camaraip
        self.capacamara.add_widget(self.micamara)    
        #self.sonido.click()
            
    def desactivacamara(self,*args):  
        self.CAM1.state="normal"
        self.capacamara.remove_widget(self.micamara) 
        self.camaraip.stop()
        self.micamara=self.ImagenVideo
        self.capacamara.add_widget(self.micamara)            
     
     
     #CONTROL DE VIDEOPORTERO   
        
    def registrado(self,*args):
        self.imagencon.source=str(PATH)+'ledverde18.png'
        self.textocon.text='Conectado'   
        
    def noregistrado(self,*args):
        self.imagencon.source=str(PATH)+'load3.gif'            
        self.textocon.text='Conectando'        
    
    # este metodo es llamado cada vez que SALIMOS en esta pantalla FORMA 
    #PARTE DE LOS METODOS DEL SCREEN MAGAGER 
    def on_leave(self): 
        #NOS ASEGURAMOS DE APAGAR EL MICROFONO EN EL CASO DE SALIR DE LA PANTALLA
        self.HABLAR.state="normal" 
        telefono1.colgar()
        self.comando.envia('CIERRA PUERTA')       
        self.CAM1.state="normal"
        self.camaraip.stop()
       
    #CONTROL DE VIDEOPORTERO    
    def on_enter(self):
        global llamada_entrante
        global llamada_in  
        
        if llamada_in:  
            self.activacamara()
         
    def cambio(self,*args):
        self.manager.current = 'OLLOSIP' #se va a la screen con nombre OLLOSIP       
#CONTROL DE VIDEOPORTERO
    
    


class Camara_screen(Screen):
    
    url=StringProperty()   
    nombre=StringProperty('')    
   

      
  
Builder.load_string("""

<Camara_screen>:
   
    on_enter:self.ids.camzoom.start() 
    on_leave:self.ids.camzoom.stop() 
    CamaraCctv:
        id:camzoom
        nombre:root.nombre#app.sm.get_screen('CCTV').camara_nombre
       
        ##accedemos a la variable camara_zoon de la clase Cctv_screen donde asignamos 
        #la camara que queremos ver en zoom en esta clase
        ##para ello usamos el metodo get_screen para acceder a otra clase screen desde esta
        url: root.url 
        on_press:root.manager.current= 'CCTV' 
    
""")

  
         
        
class Cctv_screen(Screen):
    #declaramos una lista property donde tendremos las url de las camaras de seguridad.
    #En el caso de que cambiemos la ip automaticamente se actualizara en nuestro codigo 
    #kv mas abajo
    
   
    numero_de_camaras=NumericProperty(4)
    lista_camaras=ListProperty(['','','','','','','','','',''])
    uno=''
    camara_url= StringProperty()
    camara_nombre= StringProperty()
    ocultar_menu=BooleanProperty(True)
  
    nomecam2= StringProperty()
    nomecam3= StringProperty()
    nomecam4= StringProperty()
    nomecam5= StringProperty()
    nomecam6= StringProperty()   
    nomecam7= StringProperty()
    nomecam8= StringProperty()
    nomecam9= StringProperty()    
   
    
    
   
    
    def on_config(self):
        pass
    
  

    def configcamaras(self,config,none,section,key,value):  
        if (section == "camaras"):
            if key=='nomecam1':
                self.nomecam1=value
    
    
    # creamos un diccionario llamado camara donde almacenamos la url y el nombre 
    #de la camara que queramos poner a pantalla
    #completa cuando pulsemos en una de ellas 
    
    def __init__(self, **kwargs):
        #con super heredamos de la clase screen todos los atributos de esta
        super( Cctv_screen, self).__init__(**kwargs)   
        
        self.nomecam1= StringProperty()
        self.configuracion_camaras()
        
        self.lista_camaras[1]='http://'+str(self.usercam1)+':'+str(self.clave1)+'@'+str(self.ipcamara1)+':'+str(self.porto1)+'/video' 
        self.lista_camaras[2]='http://'+str(self.usercam2)+':'+str(self.clave2)+'@'+str(self.ipcamara2)+':'+str(self.porto2)+'/video' 
        self.lista_camaras[3]='http://'+str(self.usercam3)+':'+str(self.clave3)+'@'+str(self.ipcamara3)+':'+str(self.porto3)+'/video' 
        self.lista_camaras[4]='http://'+str(self.usercam4)+':'+str(self.clave4)+'@'+str(self.ipcamara4)+':'+str(self.porto4)+'/video' 
        self.lista_camaras[5]='http://'+str(self.usercam5)+':'+str(self.clave5)+'@'+str(self.ipcamara5)+':'+str(self.porto5)+'/video' 
        self.lista_camaras[6]='http://'+str(self.usercam6)+':'+str(self.clave6)+'@'+str(self.ipcamara6)+':'+str(self.porto6)+'/video' 
        self.lista_camaras[7]='http://'+str(self.usercam7)+':'+str(self.clave7)+'@'+str(self.ipcamara7)+':'+str(self.porto7)+'/video' 
        self.lista_camaras[8]='http://'+str(self.usercam8)+':'+str(self.clave8)+'@'+str(self.ipcamara8)+':'+str(self.porto8)+'/video' 
        self.lista_camaras[9]='http://'+str(self.usercam9)+':'+str(self.clave9)+'@'+str(self.ipcamara9)+':'+str(self.porto9)+'/video'         
  
    def on_nomecam1(self,*args):
        pass
      
    def configuracion_camaras(self,*args):
        
        #lemos de novo o arquivo por se houbo algun cambio na configuracion
        config.read('ollosip.ini')      
        
        self.ipcamara1=config.get('camaras', 'ipcam1')
        self.porto1 = config.get('camaras', 'porto1')
        self.usercam1 = config.get('camaras', 'usercam1')
        self.clave1 = config.get('camaras', 'clave1')
        self.oncam1 = config.get('camaras', 'oncam1')   
        self.nomecam1=config.get('camaras', 'nomecam1')      
        #print(self.nomecam1)
   
        self.ipcamara2=config.get('camaras', 'ipcam2')
        self.porto2 = config.get('camaras', 'porto2')
        self.usercam2 = config.get('camaras', 'usercam2')
        self.clave2 = config.get('camaras', 'clave2')
        self.oncam2 = config.get('camaras', 'oncam2')   
        self.nomecam2=config.get('camaras', 'nomecam2')  
    
        self.ipcamara3=config.get('camaras', 'ipcam3')
        self.porto3 = config.get('camaras', 'porto3')
        self.usercam3 = config.get('camaras', 'usercam3')
        self.clave3 = config.get('camaras', 'clave3')
        self.oncam3 = config.get('camaras', 'oncam3')    
        self.nomecam3=config.get('camaras', 'nomecam3')   
    
        self.ipcamara4=config.get('camaras', 'ipcam4')
        self.porto4 = config.get('camaras', 'porto4')
        self.usercam4 = config.get('camaras', 'usercam4')
        self.clave4 = config.get('camaras', 'clave4')
        self.oncam4 = config.get('camaras', 'oncam4')    
        self.nomecam4=config.get('camaras', 'nomecam4')   
    
        self.ipcamara5=config.get('camaras', 'ipcam5')
        self.porto5 = config.get('camaras', 'porto5')
        self.usercam5 = config.get('camaras', 'usercam5')
        self.clave5 = config.get('camaras', 'clave5')
        self.oncam5 = config.get('camaras', 'oncam5')    
        self.nomecam5=config.get('camaras', 'nomecam5')   
    
        self.ipcamara6=config.get('camaras', 'ipcam6')
        self.porto6 = config.get('camaras', 'porto6')
        self.usercam6 = config.get('camaras', 'usercam6')
        self.clave6 = config.get('camaras', 'clave6')
        self.oncam6 = config.get('camaras', 'oncam6')    
        self.nomecam6=config.get('camaras', 'nomecam6')   
    
        self.ipcamara7=config.get('camaras', 'ipcam7')
        self.porto7 = config.get('camaras', 'porto7')
        self.usercam7 = config.get('camaras', 'usercam7')
        self.clave7 = config.get('camaras', 'clave7')
        self.oncam7 = config.get('camaras', 'oncam7')    
        self.nomecam7=config.get('camaras', 'nomecam7')   
    
        self.ipcamara8=config.get('camaras', 'ipcam8')
        self.porto8 = config.get('camaras', 'porto8')
        self.usercam8 = config.get('camaras', 'usercam8')
        self.clave8 = config.get('camaras', 'clave8')
        self.oncam8 = config.get('camaras', 'oncam8')    
        self.nomecam8=config.get('camaras', 'nomecam8')   
    
        self.ipcamara9=config.get('camaras', 'ipcam9')
        self.porto9 = config.get('camaras', 'porto9')
        self.usercam9 = config.get('camaras', 'usercam9')
        self.clave9 = config.get('camaras', 'clave9')
        self.oncam9 = config.get('camaras', 'oncam9')    
        self.nomecam9=config.get('camaras', 'nomecam9')       
        
    def on_numero_de_camaras(self,*args):
       
        if self.numero_de_camaras==4:
            self.camaras_9off()
            self.camaras_4()
        else:
            self.camaras_4off()
            self.camaras_9()
        pass
   
    
    def on_enter(self):
        self.configuracion_camaras()
       
        if self.numero_de_camaras==4:
            self.camaras_4(self)
        else:
            self.camaras_9(self)        
       
        
    def on_leave(self):
        if self.numero_de_camaras==4:
            self.camaras_4off()
        else:
            self.camaras_9off()
        
      
    def camaras_4(self,*args):
        self.ids.camarascctv.clear_widgets()
        self.ids.camarascctv.cols=2
        self.ids.camarascctv.row=2
        
        self.camara1=CamaraCctv(url=self.lista_camaras[1],nombre=self.nomecam1)
        self.ids.camarascctv.add_widget(self.camara1)
        self.camara1.bind(on_press=partial(self.camara_zoom,self.camara1.nombre,self.camara1.url))
        self.camara1.start()
        
        self.camara2=CamaraCctv(url=self.lista_camaras[2],nombre=self.nomecam2)
        self.ids.camarascctv.add_widget(self.camara2)
        self.camara2.bind(on_press=partial(self.camara_zoom,self.camara2.nombre,self.camara2.url))
        
        self.camara3=CamaraCctv(url=self.lista_camaras[3],nombre=self.nomecam3)
        self.ids.camarascctv.add_widget(self.camara3)
        self.camara3.bind(on_press=partial(self.camara_zoom,self.camara3.nombre,self.camara3.url))
    
        self.camara4=CamaraCctv(url=self.lista_camaras[4],nombre=self.nomecam4)
        self.ids.camarascctv.add_widget(self.camara4)
        self.camara4.bind(on_press=partial(self.camara_zoom,self.camara4.nombre,self.camara4.url))        
        self.camaras_4on()   
    def camaras_9(self,*args):
        
        self.ids.camarascctv.clear_widgets()
        self.ids.camarascctv.cols=3
        self.ids.camarascctv.row=3       
        self.camara1=CamaraCctv(url=self.lista_camaras[1],nombre=self.nomecam1)
        self.ids.camarascctv.add_widget(self.camara1)
        self.camara1.bind(on_press=partial(self.camara_zoom,self.camara1.nombre,self.camara1.url))
    
        self.camara2=CamaraCctv(url=self.lista_camaras[2],nombre=self.nomecam2)
        self.ids.camarascctv.add_widget(self.camara2)
        self.camara2.bind(on_press=partial(self.camara_zoom,self.camara2.nombre,self.camara2.url))
    
        self.camara3=CamaraCctv(url=self.lista_camaras[3],nombre=self.nomecam3)
        self.ids.camarascctv.add_widget(self.camara3)
        self.camara3.bind(on_press=partial(self.camara_zoom,self.camara3.nombre,self.camara3.url))
    
        self.camara4=CamaraCctv(url=self.lista_camaras[4],nombre=self.nomecam4)
        self.ids.camarascctv.add_widget(self.camara4)
        self.camara4.bind(on_press=partial(self.camara_zoom,self.camara4.nombre,self.camara4.url))       
        
        self.camara5=CamaraCctv(url=self.lista_camaras[5],nombre=self.nomecam5)
        self.ids.camarascctv.add_widget(self.camara5)
        self.camara5.bind(on_press=partial(self.camara_zoom,self.camara5.nombre,self.camara5.url))
    
        self.camara6=CamaraCctv(url=self.lista_camaras[6],nombre=self.nomecam6)
        self.ids.camarascctv.add_widget(self.camara6)
        self.camara6.bind(on_press=partial(self.camara_zoom,self.camara6.nombre,self.camara6.url))
    
        self.camara7=CamaraCctv(url=self.lista_camaras[7],nombre=self.nomecam7)
        self.ids.camarascctv.add_widget(self.camara7)
        self.camara7.bind(on_press=partial(self.camara_zoom,self.camara7.nombre,self.camara7.url))
    
        self.camara8=CamaraCctv(url=self.lista_camaras[8],nombre=self.nomecam8)
        self.ids.camarascctv.add_widget(self.camara8)
        self.camara8.bind(on_press=partial(self.camara_zoom,self.camara8.nombre,self.camara8.url))          
        
        self.camara9=CamaraCctv(url=self.lista_camaras[9],nombre=self.nomecam9)
        self.ids.camarascctv.add_widget(self.camara9)
        self.camara9.bind(on_press=partial(self.camara_zoom,self.camara9.nombre,self.camara9.url))                
        self.camaras_9on()
    def camaras_4on(self,*args):
        
        self.camara1.start()
        self.camara2.start()
        self.camara3.start()
        self.camara4.start()
    def camaras_9on(self,*args):
        self.camara1.start()
        self.camara2.start()
        self.camara3.start()
        self.camara4.start()     
        self.camara5.start()
        self.camara6.start()
        self.camara7.start()
        self.camara8.start()        
        self.camara9.start()        
                       
        
    
    def camaras_4off(self,*args):
       
        self.camara1.stop()
        self.camara2.stop()
        self.camara3.stop()
        self.camara4.stop()    
        
    def camaras_9off(self,*args):
        self.camara1.stop()
        self.camara2.stop()
        self.camara3.stop()
        self.camara4.stop()      
        self.camara5.stop()
        self.camara6.stop()
        self.camara7.stop()
        self.camara8.stop()    
        self.camara9.stop() 
      
           
    def camara_zoom(self,nome,url,comodin):
        # cambiamos el valor de las propiedades url y nombre de la "screen" VIDEOCAMARA     
        self.manager.get_screen('VIDEOCAMARA').url=url 
        self.manager.get_screen('VIDEOCAMARA').nombre=nome    
        self.manager.current='VIDEOCAMARA'
     
    def graba(self,*args):
        pass
    def animate(self, instance):
        
        # creamos un obxeto animado. Este obxeto pode ser empregado
        # en calquera widget
        # += e secuencial, mentras que &= executase en paralelo
        if self.ocultar_menu:           
            animation = Animation(size_hint=(0.3, 1), t='out_expo')          
            self.ocultar_menu=False
        else:          
            animation = Animation(size_hint=(0, 1), t='out_expo')
            self.ocultar_menu=True      
        animation.start(instance)    
     
Builder.load_string("""
<ImageButton@ButtonBehavior+Image>  
    allow_stretch: False
    pos_hint: {'center_x': 0.1, 'center_y': 0.5}
    size: self.texture_size
<Cctv_screen>:
  
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size       
            source:'./imaxes/fondo12.png'          
    
    BoxLayout:
        id:camaras
        orientation: 'vertical'
        ##spacing: 5

        BoxLayout:
            size_hint:1,0.08
            orientation: 'vertical'
            canvas.before:
                Color:
                    rgba:0.1,0.1,0.1,0.5
                Rectangle:
                    pos: self.pos
                    size: self.size      
            BoxLayout:
                id:botones
                orientation:'horizontal'
                size_hint:0.3,0.2
                pos_hint:{'right': 1}
                
                ImageButton:
                    size_hint_y:0.7
                    opacity:0.8                     
                    source:'./imaxes/cctv4_white.png'## if self.state=="down" else 'playlist_add_black.png'     
                    on_press: root.numero_de_camaras=4
               
                ImageButton:
                    size_hint_y:0.7
                    opacity:0.8                      
                    source:'./imaxes/cctv9_white.png'## if self.state=="down" else 'playlist_add_black.png'     
                    on_press: root.numero_de_camaras=9
                   
                ImageButton:
                    size_hint_y:0.7
                    opacity:0.6                      
                    source:'./imaxes/casa_white.png'## if self.state=="down" else 'playlist_add_black.png'     
                    on_press: root.manager.current='OLLOSIP'#root.cambio()
                  
                ImageButton:               
                    opacity:0.6                      
                    source:'./imaxes/menu_white.png'## if self.state=="down" else 'playlist_add_black.png' 
                    #neste punto chammos o menu de configuracion das opcions das camaras(pendente de desenrolo)
                    #on_press: root.animate(root.ids.menu)       
            
        GridLayout:
            id:camarascctv
            size_hint_y:0.9
            cols:2
            row:2
            disabled:False if root.ocultar_menu==True else True 
            #comprobamos si o menu desplegable esta activado, si e asi bloqueamos
            #todos os widgets que colgan desta capa gridlayout    
    BoxLayout:
        id:menu
        orientation:'vertical'
        size_hint:0,1 
        canvas.before:
            Color:
                rgba:0.1,0.1,0.05,0.7
            Rectangle:
                pos: self.pos
                size: self.size 
        
        ScrollView:   
           
            BoxLayout:
                size_hint:1,None#dp(10) ##separacion en pixeles entre os elementos que componen o menu
                size:100,10                
                height:800                
                orientation:'vertical'
               
                ImageButton:
                    size_hint:0.3,1
                    opacity:0.6                      
                    source:'./imaxes/cctv.png'## if self.state=="down" else 'playlist_add_black.png'     
                    #funcion pendente de desenrolo
                    #on_press: root.graba(self)
                Label:  
                    text:'pruebas'        
          
                ImageButton:
                    size_hint:0.3,1
                    opacity:0.6                      
                    source:'./imaxes/cctv.png'## if self.state=="down" else 'playlist_add_black.png' 
                    #funcion pendente de desenrolo
                    #on_press: root.graba(self)
                    
                ImageButton:
                    size_hint:0.3,1
                    opacity:0.6                      
                    source:'./imaxes/cctv.png'## if self.state=="down" else 'playlist_add_black.png' 
                    #funcion pendente de desenrolo
                    #on_press: root.graba(self)
          
                ImageButton:
                    size_hint:0.3,1
                    opacity:0.6                      
                    source:'./imaxes/cctv.png'## if self.state=="down" else 'playlist_add_black.png'   
                    #funcion pendente de desenrolo
                    #on_press: root.graba(self)  

                ImageButton:
                    size_hint:0.3,1
                    opacity:0.6                      
                    source:'./imaxes/cctv.png'## if self.state=="down" else 'playlist_add_black.png'  
                    #funcion pendente de desenrolo
                    #on_press: root.graba(self)

        
""")
     


       
class Principal_screen(Screen):
    
    def __init__(self, **kwargs):
        #con super heredamos de la clase screen todos los atributos de esta
        super( Principal_screen, self).__init__(**kwargs)    
        SCREEN_ACTIVA= 'OLLOSIP'
        self.size=(800,480)  
        self.imagenfondo = Image(source=str(PATH)+'fondo5.jpg')      
        capa_fondo=FloatLayout(size_hint=(1,1))         
        capa_botones= FloatLayout(size_hint=(None,None),size=(800, 460),pos=(0,0)) 
        capa_info=RelativeLayout(size_hint=(None,None),size=(800, 40),pos=(0,440)) 
        with capa_info.canvas.before:           
            Color(0,0,1,1)
            rect = Rectangle(size=capa_info.size, pos=capa_info.pos)  
    
        capa_test=BoxLayout(size_hint=(None,None),size=(200,20),pos=(0,19))
        b1=Button(size_hint=(0.5,1),text='B1')
        b2=Button(size_hint=(0.5,1),text='B2')
        capa_test.add_widget(b1) 
        capa_test.add_widget(b2) 
        
        capa_test2=BoxLayout(size_hint=(None,None),size=(200,20))
        b3=Button(size_hint=(0.5,1),text='B3')
        b4=Button(size_hint=(0.5,1),text='B4')
        capa_test2.add_widget(b3) 
        capa_test2.add_widget(b4)              
      
        
        reloj=DigitalClock(size_hint_x=0.3, pos=(510,0),font_size=34, style='cool', halign='right', valign='middle')
        boton_settings= IconButton(pos=(760,0),imagen=str(PATH)+'menu_white.png',size=(40,40))       
        boton_megafonia= IconButton(pos=(50,120),imagen=str(PATH)+'megafonia90.png',texto='MEGAFONIA' ,size=(140,140))
        boton_cctv= IconButton(pos=(320,220),imagen=str(PATH)+'cctv90.png',texto='CCTV' ,size=(140,140))        
        boton_videoip= IconButton(pos=(610,120),imagen=str(PATH)+'porteroip90.png',texto='VIDEOIP' ,size=(140,140)) 
       
        #OJO SI EL NOMBRE DE LA IMAGEN
       
        #OJO SI EL NOMBRE DE LA IMAGEN
        #EMPIEZA POR V DA ERROR AL LEERLA, HABRa QUE ESTUDIAR EL PORQUe     
        
        capa_botones.add_widget(boton_videoip)        
        capa_botones.add_widget(boton_megafonia)
        capa_botones.add_widget(boton_cctv)        
        capa_info.add_widget(boton_settings) 
        capa_info.add_widget(reloj)         
        capa_fondo.opacity=1
        capa_botones.opacity=1
        capa_info.opacity=1 
        
        capa_fondo.add_widget(self.imagenfondo)
        capa_fondo.add_widget(capa_info)
        capa_fondo.add_widget(capa_botones)        
        self.add_widget(capa_fondo)      
             
        boton_cctv.bind(on_release=self.cambiocctv)      
        boton_megafonia.bind(on_release=self.cambiomegafonia)
        boton_videoip.bind(on_release=self.cambiovideoportero)      
        boton_settings.bind(on_press=self.configuracion)
        
    def configuracion (self,*args):
              
        config = ConfigParser()

        config.read('ollosip.ini')        
        self.configuracion =SettingsWithSidebar()# Settings()       
        self.configuracion.add_json_panel('Configuracion Ollosip', config, 'settings_ollosip.json')        
        self.add_widget(self.configuracion)
        self.configuracion.bind(on_close=self.cerrarconfig)
        self.configuracion.bind(on_config_change=self.configcambio)      
      
    #   debemos introcucir como parametro none al ser llamado desde el evento on_cofig_change   
    def configcambio(self,config,none,section,key,value):   
        global MIEXTENSION   
        global MIEXTENSIONP
        global IPCENTRALITA
        #  si fuese redefinido y utilizado dentro del metodo App sobraria
        
        #print("Config: %s / %s -> %s" % (section, key, value)) 
        if (section == "sistema"):
            if key=='ip':
                self.cambia_ip_sistema(value) 
                
        if (section == "sistema"):
            if key=='pe':
                self.cambia_gateway_sistema(value)  
                
        if (section == "terminal"):
                if key=='extension':
                    MIEXTENSION=value
                    telefono1.configure_sip_account(str(MIEXTENSION), str(MIEXTENSIONP))
                    #print(value)
                if key=='clave':
                    MIEXTENSIONP=str(value) 
                    #telefono1.start()
                if key=='ipbx':
                    
                    IPCENTRALITA=str(value) 
                    telefono1.configure_sip_account(username=str(MIEXTENSION), password=str(MIEXTENSIONP))
                    #print(value)
                
               
     
    def cambia_ip_sistema(self,value,*args):
        #Este metodo nos permite cambiar la ip del sistema editando el fichero de la rpi dhcpcd.conf
        #recibe como parametro la ip modificada desde la pantalla de configuracion
        indice=0       
        texto="inform"
        nuevotexto="inform "+str(value)+"\n"
        #print (value)
        x=fileinput.input(files="/etc/dhcpcd.conf", inplace=1)       
        for line in x:
            if texto in line:
                line=nuevotexto
            print line,
        x.close       
        os.system("sudo ifconfig wlan0 down")    
        os.system("sudo ifconfig wlan0 up")    
        os.system("sudo ifconfig eth0 down")    
        os.system("sudo ifconfig eth0 up")            
        
    def cambia_gateway_sistema(self,value,*args):
        #Este metodo nos permite cambiar la ip del sistema editando el fichero de la rpi dhcpcd.conf
        #recibe como parametro la ip modificada desde la pantalla de configuracion
        indice=0
        texto="static routers="
        #print (value)
        nuevotexto="static routers="+str(value)+"\n"
        x=fileinput.input(files="/etc/dhcpcd.conf", inplace=1)
        for line in x:
            if texto in line:
                line=nuevotexto
            print line,
        x.close                    
        os.system("sudo ifconfig wlan0 down")      
        os.system("sudo ifconfig wlan0 up")

    def cerrarconfig(self,*args):
        self.remove_widget(self.configuracion)
    
    def cambiovideoportero(self,*args):
        self.manager.current = 'VIDEOIP' #se va a la screen con nombre MUSICA    
        SCREEN_ACTIVA= 'VIDEOIP'
    def cambiomegafonia(self,*args):
        self.manager.current = 'MEGAFONIA' #se va a la screen con nombre MUSICA 
        SCREEN_ACTIVA= 'MEGAFONIA'
    def cambiocctv(self,*args):
        self.manager.current = 'CCTV' #se va a la screen con nombre VIDEOTELEFONO   
        SCREEN_ACTIVA= 'CCTV'

 




class Rectangulo(Widget):
    ancho=NumericProperty(1)
    color=ListProperty([1,1,1,1])    
  
Builder.load_string("""
<Rectangulo>:
    canvas:
        Color:
            rgba:root.color
        Line:
            width:root.ancho
            #rectangle: (self.x-10,self.y-10,self.width+10,self.height+40)
            rectangle: (self.x,self.y,self.width,self.height)
""")





class Megafonia_screen(Screen):
    
    ocultar_volumen=BooleanProperty(True)
    animando=BooleanProperty(False)
    def __init__(self, **kwargs):
        #con super heredamos de la clase screen todos los atributos de esta
        super( Megafonia_screen, self).__init__(**kwargs)   
        self.interr=BooleanProperty(False)  
        #self.ipcamara1="192.168.0.17"
        
   
                
        
    def actualiza_volumen_microfono(self,valor):
      
        telefono1.core.mic_gain_db=valor
        
    
    def activa_microfono(self,*args):
        EXTENSION=0
        #llamada general a todos los altavoces
        if self.ids.E5.state=="down":
            EXTENSION=6060
            
        elif self.ids.E4.state=="down":   
            EXTENSION=6064            
        elif self.ids.E3.state=="down":   
            EXTENSION=6063
        elif self.ids.E2.state=="down":   
            EXTENSION=6031
        elif self.ids.E1.state=="down":   
            EXTENSION=6030
        #logging.info('%s', EXTENSION)
        if self.ids.microfono.state=="down":
            telefono1.llamar(EXTENSION)
        else:
            telefono1.colgar()
    
    
    # este metodo es llamado cada vez que SALIMOS en esta pantalla FORMA PARTE 
    #DE LOS METODOS DEL SCREEN MAGAGER
    def on_leave(self): 
        #NOS ASEGURAMOS DE APAGAR EL MICROFONO EN EL CASO DE SALIR DE LA PANTALLA
        self.ids.microfono.state="normal" 
        self.ids.microfono.parpadeo=False 
        self.animando=True
        self.animate(self.ids.altofalantes)
        self.ids.microfono.flash(self.ids.activado)
        telefono1.colgar()
    
    def anima_volumen(self, instance):
        
        # creamos un obxeto animado. Este obxeto pode ser empregado
        # en calquera widget
        # += e secuencial, mentras que &= executase en paralelo
        if self.ocultar_volumen:
           
            animation = Animation(opacity=1,duration=0.9,t='out_quad')
           
            self.ocultar_volumen=False
           
        else:
          
            animation = Animation(opacity=0,duration=0.6, t='out_quad')
            self.ocultar_volumen=True
       
        animation.start(instance)        
        
    

    
    
    # creamos un obxeto animado. Este obxeto pode ser empregado
    # en calquera widget
    # += e secuencial, mentras que &= executase en paralelo    
    
    def animate(self, instance):
        
        
        
     
      
            
        animation = Animation(opacity=1,duration=0.2,t='out_quad')
        animation+= Animation(opacity=0,duration=0.2, t='out_quad')
          
        #animation.repeat=True
        
        if self.animando==False:
            animation.repeat=True
            animation.start(instance)    
            self.animando=True
        else:
            
            
            self.animando=False
            instance.opacity=0
            animation.cancel_all(instance) 
            
            






            
    
Builder.load_string("""
<ImageButton@ButtonBehavior+Image>  
    allow_stretch: False
    #pos_hint: {'center_x': 0.1, 'center_y': 0.5}
    #size: self.texture_size
    
<BotonLed2@ToggleButton+Image>:
    #pos_hint: {'center_x': 0.4, 'center_y': 0.5}
    
    font_size:self.width*0.1
    text_size:self.size
    valihaling:'left'
    text:self.text

        
    
    #size: self.texture_size



<Megafonia_screen>:
    
    on_leave:self.ids.microfono.flash(root.ids.activado)
  
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size       
            source:'./imaxes/fondo32.png'
    
               
    
    BoxLayout:
        id:camaras
        size_hint:1,1
        orientation: 'vertical'

        BoxLayout:
            size_hint:1,0.1
            orientation: 'vertical'
            canvas.before:
                Color:
                    rgba:0.1,0.1,0.1,0.8
                Rectangle:
                    pos: self.pos
                    size: self.size       
                        
            BoxLayout:
                id:botones
                orientation:'horizontal'
                 #fijamos el tamano de la box en x e y, es el espacio que dejamos para los botones
                size_hint:0.28,1                        
                pos_hint:{'right': 1.03}        
                
                DigitalClock:
                   
                    font_size:self.width*0.25
                    style:'cool'                   
                    valign:'middle'
                    
                ImageButton:                   
                    size_hint_y:0.6
                    opacity:0.6                      
                    source:'./imaxes/casa_white.png'
                    on_press: root.manager.current='OLLOSIP'
                      
                ImageButton:                         
                    
                    opacity:0.6                      
                    source:'./imaxes/menu_white.png'
                    #on_press: root.animate(root.ids.menu)
        
        
        BoxLayout:
            orientation:'horizontal'
            size_hint:1,1         
            
            
            FloatLayout:
                
                #pos_hint:{'center_x': 0.8,'center_y':0.5}
                orientation:'vertical'
                size_hint:0.1,0.8
                Label:
                    id:altofalantes
                    opacity:0                   
                    markup:True
                    pos_hint:{'x': 1.6,'center_y':1.2}
                    font_size:self.width*0.4
                    text:'Altofalantes activados'
                
                VolumenRect: 
                    id:volumen
                    size_hint:0.4,0.9
                    pos_hint:{'center_x': 0.5,'center_y':0.65}
                    imagen:'./imaxes/mic_white.png'      
                    opacity:0
                    color: (1, 1, 1, 0.9)                    
                    maximo: 15
                    on_valor:root.actualiza_volumen_microfono(self.valor)
                    
                BoxLayout:
                    size_hint:1,0.2
                    pos_hint:{'center_y':0.1,'center_x':0.5}
                    ImageButton:                   
                        pos:root.pos
                        size_hint:0.15,0.35
                        source:'./imaxes/mic_white.png'
                        on_press:root.anima_volumen(root.ids.volumen) 
                        
            
            AnchorLayout:
                orientation:'vertical'
                size_hint:0.6,0.6                
                pos_hint:{'center_x': 0.5,'center_y':0.5}
                
                BotonColour:
                    id:microfono
                    size_hint:0.6,0.6
                    pos_hint:self.pos_hint                                       
                    opacity:1                    
                    source:'./imaxes/mic1.png'
                    on_press: root.activa_microfono(),self.flash(root.ids.activado),root.animate(root.ids.altofalantes)
                   
                
                Rectangulo: 
                    id:activado
                    ancho:3
                    color:1,1,1,1
                    size_hint:0.6,0.7
                    pos_hint:self.pos_hint
                    
                
            BoxLayout:
                orientation:'vertical'
                size_hint:0.2,1
                pos_hint:self.pos_hint
                BotonLed2:
                    id:E5
                    source:'./imaxes/megafonoverde24.png'
                    text:'TODAS AS ZONAS'
                    opacity:0.4
                    group:'zona'
            
            BoxLayout:
                orientation:'vertical'
                size_hint:0.3,1
                pos_hint:self.pos_hint
                
                
                BotonLed2:
                    id:E1                   
                    source:'./imaxes/megafonoverde24.png'
                    text:'ZONA1'
                    opacity:0.3
                    #group:'zona'
                    #on_press:root.activa_microfono()
                
                BotonLed2:
                    id:E2
                    #size_hint_y:0.2
                    source:'./imaxes/megafonoverde24.png'
                    text:'ZONA2'
                    opacity:0.3    
                    #group:'zona'
                
                BotonLed2:
                    id:E3
                    #size_hint_y:0.2
                    source:'./imaxes/megafonoverde24.png'
                    text:'ZONA3'
                    opacity:0.3  
                    #group:'zona'
                
                BotonLed2:
                    id:E4
                    #size_hint_y:0.2
                    source:'./imaxes/megafonoverde24.png'
                    text:'ZONA4'
                    opacity:0.3    
                    #group:'zona'
""")        
        
        
    



telefono1 = Phone(username=str(MIEXTENSION), password=str(MIEXTENSIONP), camera='', snd_capture='')
# =================
#   Aplicacion principal App
# =================
class OllosipApp(App):
    
    
    
    def build(self):       
      
        self.sm = ScreenManager()
        self.sm.transition=FadeTransition()#RiseInTransition()
        self.sm.add_widget(Principal_screen(name='OLLOSIP'))
        self.sm.add_widget(Cctv_screen(name='CCTV'))      
        self.sm.add_widget(Videoportero_screen(name='VIDEOIP'))
        self.sm.add_widget(Megafonia_screen(name='MEGAFONIA'))      
        self.sm.add_widget(Camara_screen(name='VIDEOCAMARA'))        
        self.sm.current = "OLLOSIP"
        #empleamos el evento creado on_registrar en la clase Phone
        telefono1.bind(on_llamada_entrante=self.llamada_entrando)        
                  
        return self.sm        
   
   
              
    def llamada_entrando(self,*args):
        if llamada_extension==EXT_VIDEOPORTERO:
            self.sm.current = "VIDEOIP"        
        
if __name__ == '__main__':
    OllosipApp().run()
