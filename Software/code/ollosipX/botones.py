from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior,ToggleButtonBehavior
from kivy.animation import Animation




from kivy.properties import StringProperty,ListProperty,BooleanProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.lang import Builder

class IconBoton(Button):
    icono=StringProperty(" ")


Builder.load_string("""
<IconBoton>:
    canvas:
        Rectangle:
            
            pos: self.center
            size: self.size
            source:self.icono
""")

class IconButton(Button):
    def __init__(self,imagen,texto='', **kwargs):
        super( IconButton, self).__init__(**kwargs)    #con super heredamos de la clase screen todos los atributos de esta   
        
        #imagen=StringProperty()
        self.background_color=[1,0.5,0,0] # cambiamos el color de fondo del background del boton para que quede transparente y solo se vea el  
                                         #icono para ello ponemos el Alpha Blending a 0 [R,G,B,A]
        
        if self.size:
            self.size_hint=(None,None)                               
        capa=BoxLayout(size_hint=self.size_hint,size=self.size, pos=self.pos,orientation='vertical')       
        icono=Image( source= imagen, size_hint=self.size_hint,size=self.size, pos=self.pos)           
        capa.add_widget(icono)       
        capa.add_widget(Label(text=texto,font_size=18,halign='left',color=[1,1,0.6,0.8]))
        self.add_widget(capa)



class BotonI(Button): # pasamos la ( pos, size,imagen='imagen.ext')


    def __init__(self, imagen,trasparencia=1, **kwargs):
        super( BotonI, self).__init__(**kwargs)    #con super heredamos de la clase screen todos los atributos de esta   
        
        self.background_color=[0.5,0.5,0.5,trasparencia]
        if self.size:
            self.size_hint=(None,None)               
        ca1=BoxLayout(size_hint=self.size_hint,size=self.size, pos=self.pos,orientation='vertical')         
        imagen=Image(source=imagen,size_hint=self.size_hint,size=self.size, pos=self.pos)      
        ca1.add_widget(imagen) 
        self.add_widget(ca1)    


class BotonLed(Button): # pasamos la ( pos, size,imagen='imagen.ext')

    imaxe=StringProperty()
    def __init__(self, imagen, **kwargs):
        super( BotonLed, self).__init__(**kwargs)    #con super heredamos de la clase screen todos los atributos de esta   
        self.size_hint=(None, None)   #deshabilito el ocupar el boton toda la capa a la que se anade y se tiene encuenta el size
        self.imaxe=imagen
                 
        
Builder.load_string("""

<BotonLed>: 
    
    Image:   
        size_hint_x:None
        width: root.width*0.2
        center_x:root.x+30
        center_y:root.y+25
        source:root.imaxe
        allow_stretch: True
""")

        




class BotonColor(ToggleButton,Image):
  
    background_color_down = ListProperty([1, 0, 0, 1])
    background_color_normal = ListProperty([0.25, 0.25, 0.25, 1])

    def __init__(self,imagen, **kwargs):
        super(BotonColor, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = self.background_color_normal
        self.size_hint=(None, None)   #deshabilito el ocupar el boton toda la capa a la que se anade y se tiene encuenta el size
       
        img=Image(source=imagen)
        img.center=self.center
     
        self.add_widget(img)     
    
    def on_state(self, widget, value):
        if value == 'down':
            self.background_color = self.background_color_down
        else:
            self.background_color = self.background_color_normal



class BotonColour(ToggleButtonBehavior,Image):
    """
    Button with a possibility to change the color on on_press (similar to background_down in normal Button widget)
    """
    imagen=StringProperty('')
    background_color_down = ListProperty([1, 0, 0, 1])
    background_color_normal = ListProperty([0.25, 0.25, 0.25, 1])
    parpadeo=BooleanProperty(False)
    animation = Animation(opacity=1,duration=0.2,t='out_quad')
    animation+= Animation(opacity=0,duration=0.2, t='out_quad')
   
   
    def on_state(self, widget, value):
        if value == 'down':
            self.background_color = self.background_color_down
            self.parpadeo=True
            #self.flash(self)
        else:
            self.background_color = self.background_color_normal
            self.parpadeo=False
            #self.flash(self)
    
    
    
    
    def flash(self, instance):
        
        
        
        # creamos un obxeto animado. Este obxeto pode ser empregado
        # en calquera widget
        # += e secuencial, mentras que &= executase en paralelo
      
            #animation = Animation(pos=(600, 0), t='out_bounce')
        
       
        #animation &= Animation(size=(500, 500))
        #animation += Animation(size=(100, 50))

       
        
        if self.parpadeo:
            
            animation2 = Animation(size_hint=(0.6, 0.7),duration=0.15)   
            animation2.start(instance)  
            self.animation.start(instance)  
            self.animation.repeat=True
           
            self.parpadeo=True
        else:
            self.animation.repeat=False
            self.animation.stop(instance) 
            
            
            animation2 = Animation(size_hint=(0, 0),duration=0.15)   
            animation2.start(instance)  
            self.parpadeo=False    

class BotonLedToggle(ToggleButton): # pasamos la ( pos, size,imagen='imagen.ext')

    imaxe=StringProperty()
    def __init__(self, imagen, **kwargs):
        super( BotonLedToggle, self).__init__(**kwargs)    #con super heredamos de la clase screen todos los atributos de esta   
        self.size_hint=(None, None)   #deshabilito el ocupar el boton toda la capa a la que se anade y asi se tiene encuenta el size
        
        self.imaxe=imagen
        #img=Image(source=imaxe)
        #img.center_x=self.x+25
        #img.center_y=self.y+25
        #self.add_widget(img) 
        
    
        #self.background_color=(1,0.8,1,0.4)      
        
Builder.load_string("""

<BotonLedToggle>: 
    
    Image:             
        size_hint_x:None
        width: root.width*0.2
        #height:self.height*0.2 
        center_x:root.x+30
        center_y:root.y+25
        source:root.imaxe
        allow_stretch: True
    
""")