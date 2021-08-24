from __future__ import division

from kivy.lang import Builder
from kivy.properties import NumericProperty,StringProperty, ListProperty, AliasProperty, \
    BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.image import Image
#from kivy.uix.slider import Slider
from kivy.uix.behaviors import ButtonBehavior
class VolumenRect(Widget):
    
    color = ListProperty([0.8, 0.0, 0.0, 1])
    valor = NumericProperty(10)  # value: app.mm.state.time_position or 0 posicion time position
    ocultar_volumen=BooleanProperty(True)
    imagen=StringProperty('')
    
    maximo = NumericProperty(1)   # max: app.mm.current.duration or 0 duracion
    overflow = BooleanProperty(False)
    ####################fernando
    _locked = False
   
    valor_buscar = NumericProperty(0)  # value: app.mm.state.time_position or 0 posicion
    cached_value_buscar = NumericProperty(0) 
    posi_x= NumericProperty(0) 
    posi_y= NumericProperty(0) 
    posi_seek= NumericProperty(0) 
    posi_max=NumericProperty(0) 
    



    def _get_progress(self):
        if not self.maximo:
            return 0
        if not self.overflow and self.valor > self.maximo:
            return 1
        #print(self.value / self.max)
        return self.valor / self.maximo

    def _set_progress(self, progress):
        self.valor = progress * self.maximo

    progress = AliasProperty(_get_progress, _set_progress, bind=['valor', 'maximo'])
    
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        self.posi_x=touch.x
        self.posi_x-=self.x
        self.posi_y=touch.y
        self.posi_y-=self.y        
        #self.progress=(self.posi_x/self.width)
        self.progress=(self.posi_y/self.height)    
        
        #return self.posi_seek
   
    def on_touch_move(self, touch, *args):
        if not self.collide_point(*touch.pos):
            return
        self.posi_x=touch.x
        self.posi_x-=self.x
        self.posi_y=touch.y
        self.posi_y-=self.y           
        #self.progress=(self.posi_x/self.width)  
        self.progress=(self.posi_y/self.height)     

    def on_touch_up(self, touch, *args):
        if not self.collide_point(*touch.pos):
            return
        self.valor_buscar=(self.posi_y/self.height)*self.maximo
        #self.valor_buscar=(self.posi_x/self.width)*self.maximo
        

    def anima_volumen(self, instance):
        
        # creamos un obxeto animado. Este obxeto pode ser empregado
        # en calquera widget
        # += e secuencial, mentras que &= executase en paralelo
        if self.ocultar_volumen:
            #animation = Animation(pos=(600, 0), t='out_bounce')
            animation = Animation(opacity=1,duration=0.2,t='out_quad')
            #animation+= Animation(pos=(0, 0), t='out_bounce')
            self.ocultar_volumen=False
        else:
            #animation= Animation(pos=(800, 0), t='out_bounce')
            animation = Animation(opacity=0,duration=0.2, t='out_quad')
            self.ocultar_volumen=True
        #animation &= Animation(size=(500, 500))
        #animation += Animation(size=(100, 50))

        # apply the animation on the button, passed in the "instance" argument
        # Notice that default 'click' animation (changing the button
        # color while the mouse is down) is unchanged.
        animation.start(instance)            
Builder.load_string('''
<MiImagen@ButtonBehavior+Image>
    allow_stretch: False
<ImageButton@ButtonBehavior+Image>:  
    allow_stretch: False
<VolumenRect>:
    
    BoxLayout:
        size_hint:None,None
        orientation:'vertical'
        size:root.size
        pos:root.pos
        
        BoxLayout:
            id:voll
            canvas.before:
                Color:
                    rgba: root.color
                Rectangle:
                    
                    pos: root.pos
                    size: root.width , root.height*root.progress
         
        
            
''')
