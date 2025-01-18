from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput 
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder
import re
from dataclasses import dataclass
from functools import partial
from kivy.clock import Clock
from bvat import aw10s,aw10w,aw12s,aw12w

Builder.load_string("""

<Test>:
    id:testview
                    
<Tabs>
    id:tabs
    tab_pos:'bottom_mid'
    do_default_tab: False
    tab_width: root.width/3
        
    TabbedPanelItem:
        #id:listenansicht
        text: 'Autos'
        size_hint: (0.1, 0.1)
        on_state: if self.state=='down' : root.listenansicht()
        StackLayout:
            minimum_height: 32
            size_hint:(1,None)
            orientation:'lr-tb'
            Button :
                text: "+" 
                size_hint: (.33, None)
            Button :
                text: "-" 
                size_hint: (.33, None)
            Button :
                size_hint: (.33, None)
                Image:
                    source: 'pen.png'
                    size: 100,100
                    y: self.parent.y 
                    x: self.parent.x + self.parent.size[0]/2 - self.size[0]/2
            StackLayout:
                id:listenansicht
                orientation: 'lr-tb'
                Auto:
                    id: select
                    text: 'Reno'
                    group: 'auto'
                    state:'down'
                    on_press: root.auto=self
                Auto:
                    text: 'Porsche'
                    group: 'auto'
                    on_press: root.auto=self
                Auto:
                    text: 'Porsche 2'
                    group: 'auto'
                    on_press: root.auto=self
    TabbedPanelItem:
        id: schadensaufnahme
        text: 'Karosserieteile'
        on_state: if self.state=='down' : root.schadensaufnahme()
        Karosserie:
            
    TabbedPanelItem:
        id: tabelle
        text: 'Arbeitsaufwand'
        on_state: if self.state=='down' : root.tabelle()
        StackLayout:
            size_hint:(1,None)
                        
<Karosserie>
    orientation:'lr-tb'
 
""")

def set_( delle,intinput,x):
    if x == '':
        delle.anzahl =0
    else:
        delle.anzahl=int(x)
class IntInput(TextInput):
    pat = re.compile('[^0-9]')
    def insert_text(self, substring,
        from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        return super().insert_text(
            s, from_undo=from_undo)
    def on_focus(
        self, instance, value, *largs):
        if value:
            Clock.schedule_once(
                lambda dt: instance.select_all(),
                    0.1)
        
@dataclass
class delle():
    name: str
    anzahl: int 

@dataclass
class Teil():
    name: str ='name'
    alu:bool=True
    kleben:bool=False 
    dellen:list = list[delle]
    def __post_init__(self):
        self.dellen=[
            delle('10mm',0),
            delle('20mm',0),
            delle('30mm',0),
            delle('40mm',0),
            delle('50mm',0),
            delle('60mm',0),
            delle('70mm',0),
            delle('80mm',0)
            ]
    def set_kleben(self, x, y):
        self.kleben = not self.kleben
    def set_alu(self, x, y):
        self.alu = not self.alu
    
class Auto(ToggleButton):
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.text = kwargs['name']
            kwargs.pop('name')
        super(Auto,self). __init__(**kwargs)
        self.allow_no_selection=False
        self.teile=[
            Teil('Motorhaube'), 
            Teil('Dach') ,
            Teil('Tür v l') 
            ] 
        self.group='auto'
    def on_press(self):
        content = self.parent.parent.parent.parent
        content.auto = self
    
class Karosserie(StackLayout):
    pass
class Schaden(StackLayout):
    def __init__(self, **kwargs):
        self.teil=kwargs['teil']
        kwargs.pop('teil')
        super(Schaden, self).__init__(
                **kwargs)

class Tabs(TabbedPanel):
    auto=Auto() 
    auto_liste=[
                    Auto(name='Tina'), 
                    Auto(name='Andi'), 
                    Auto(name='Erika')
                    ]
    def __init__(self, **kwargs):
        super(Tabs, self).__init__(**kwargs)
        self.auto= self.ids.select
        
    def listenansicht(self):
        content=self.ids.listenansicht
        content.clear_widgets()
        for auto in self.auto_liste:
            content.add_widget(
                auto
            )
    
    def calc(self, teil, x):
        content=self.ids.schadensaufnahme.content
        content.clear_widgets()
        content.add_widget(
            Button(text=teil.name,
            size_hint=(1,.05))) 
        content.add_widget(
            b:=ToggleButton(text='Alu', 
            size_hint=(.5,.05), 
            state="down" if 
                teil.alu else "normal")) 
        b.bind(state=teil.set_alu)
        content.add_widget(
            b:=ToggleButton(
                text='Kleben', size_hint=(.5,.05), 
                state='down' if 
                    teil.kleben else 'normal')) 
        b.bind(state=teil.set_kleben)
        for delle in teil.dellen:
            content.add_widget(
                Button(
                    text=delle.name,
                    size_hint=(.5, .05))) 
            Ii =IntInput(
                text=str(delle.anzahl) ,
                size_hint=(.5, .05))
            Ii.bind(text=partial(set_, delle))
            content.add_widget(Ii)
        content.add_widget(
            Button(text='Fertig', 
            on_press=self.schadensaufnahme,
            size_hint=(1, .1),
            background_color= 
            (0.0, 1.0, 0.0, 1.0))) 

    def schadensaufnahme(self, *args):
        content=self.ids.schadensaufnahme.content
        content.clear_widgets()
        content.add_widget(
            Button(text='Schäden',
            size_hint=(1,.2)))
        for teil in self.auto.teile:
            bt =  Button(
                text=teil.name, size_hint=(1,.1) ) 
            bt.bind(
                on_press=partial(self.calc, teil))
            content.add_widget(bt) 

    def tabelle(self):
        content=self.ids.tabelle.content
        content.clear_widgets()
        content.add_widget(
            Button(text=self.auto.text))
        for teil in self.auto.teile:
            content.add_widget(
                Button(text=teil.name,
                    size_hint=(.5,None)))
            s = sum(x.anzahl for x in teil.dellen)
            a = sum(int((1+x) * teil.dellen[x].anzahl) for x in range(8)) 
            aw = aw12s[round(a/s/10+0.5)](a) if s >0 else 0
            content.add_widget(
                Button(text=str(aw) , 
                size_hint=(.5,None)))
        pass

class Test(BoxLayout):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
        self.tabs=Tabs()
        self.add_widget(self.tabs)

class TabbedPanelApp(App):
    def build(self):
        return Test()


if __name__ == '__main__':
    TabbedPanelApp().run()