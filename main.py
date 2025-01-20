from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput 
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
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
        text: 'Autos'
        size_hint: (0.1, 0.1)
        on_state: if self.state=='down' : root.listenansicht()
        StackLayout:
            id:startansicht 
            size_hint:(1,1)
            orientation:'lr-tb'
                
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
            size_hint:(1,1)

<Karosserie>
    orientation:'lr-tb'

<EditButton>
    size_hint: (1/3, None)
    # on_press: root.parent.edit(auto=root.auto)
    Image:
        source: 'pen.png'
        size: self.parent.height*0.7,self.parent.height*0.7
        y: self.parent.y + self.parent.size[1]/2 - self.size[1]/2
        x: self.parent.x + self.parent.size[0]/2 - self.size[0]/2
""")
def set_aw10(y, x):
    y.aw10 = x
def set_anzahl( delle,intinput,x):
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
    def __init__(self, aw10= True, **kwargs):
        if 'name' in kwargs:
            self.text = kwargs['name']
            kwargs.pop('name')
        super(Auto,self). __init__(**kwargs)
        self.allow_no_selection=False
        self.teile=[
            Teil('Motorhaube'), 
            Teil('Dach'),
            Teil('Tür vorne links'), 
            Teil('Tür vorne rechts'),
            Teil('Tür hinten links'),
            Teil('Tür hinten rechts'), 
            Teil('Kofferraum'),
            ] 
        self.group='auto'
        self.size_hint = 1,.05
        self.aw10= aw10
    def on_press(self):
        content = self.parent.parent.parent
        content.auto = self
    def set_name(self,textinput, value):
        self.text= value
    
class EditButton(Button):
    pass
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
        self.auto= self.auto_liste[0]
        self.auto.state='down'
        
    def listenansicht(self, *args):
        content=self.ids.startansicht
        content.clear_widgets()
        content.add_widget(
            b:=Button(text='+',
            size_hint=(1/3,.1), 
            background_color=( 0,1, 0)))
        b.bind(on_press= self.edit)
        content.add_widget(
            b:=Button(text='-',
            size_hint=(1/3,.1), 
            background_color=( 1,0, 0)))
        b.bind(on_press= self.delete)
        content.add_widget(
            b:=EditButton(size_hint=(1/3,.1)))
        b.bind(on_press= partial(self.edit,new = False))
        for auto in self.auto_liste:
            content.add_widget(auto)
    def edit(self, button ,new=True):
        auto=Auto() if new else self.auto
        content=self.ids.startansicht
        content.clear_widgets() 
        content.add_widget(
            Button(text='Name', 
            size_hint=( .5,.1))) 
        content.add_widget(
            t:=TextInput(size_hint=(.5,.1),
                multiline=False,text=auto.text)) 
        t.bind(text=auto.set_name)
        content.add_widget(
            s:=ToggleButton(text='10 AW', 
            size_hint=( .5,.1),group='aw', 
            state='down')) 
        content.add_widget(
            ToggleButton(text='12 AW', 
            size_hint=( .5,.1),group='aw'))  
        content.add_widget(
            b:=Button(text='Fertig',
            size_hint=(.5,.1), 
            background_color=(0, 1,0)))
        b.bind(on_press= partial(self.add_Auto,auto))
        content.add_widget(
            b:=Button(text='Abbrechen',
            size_hint=(.5,.1), 
            background_color=( 1,0, 0)))
        b.bind(on_press= self.listenansicht)
    def add_Auto(self, auto ,Button):
        if auto in self.auto_liste:
            self.listenansicht()
        else:
            self.auto.state= 'normal'
            self.auto = auto
            self.auto_liste.append(auto)
            auto.state='down'
            self.listenansicht()
    def delete(self, button):
        content=self.ids.startansicht
        content.clear_widgets()
        content.add_widget(
            Label(text='Möchtest du das Auto wirklich löschen? ', 
            size_hint=( 1,.1)))  
        content.add_widget(
            b:=Button(text='Ja',
            size_hint=(.5,.1), 
            background_color=(0, 1,0)))
        b.bind(on_press= self.delete_auto)
        content.add_widget(
            b:=Button(text='Nein',
            size_hint=(.5,.1), 
            background_color=(1, 0,0))) 
        b.bind(on_press= self.listenansicht)
    def delete_auto(self,button):
        self.auto_liste.remove(self.auto)
        if len(self.auto_liste)<=0:
            self.auto_liste.append(Auto(name='Beispielauto'))
        self.auto = self.auto_liste[0]
        self.auto.state='down'
        self.listenansicht()
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
            Ii.bind(text=partial(set_anzahl, delle))
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
            Button(text=self.auto.text,
            size_hint=(1,.2)))
        content.add_widget(
            Label(text='Teil',
            size_hint=(.5,.1)))
        content.add_widget(
            Label(text='AW',
            size_hint=(.5,.1)))
        for teil in self.auto.teile:
            s = sum(x.anzahl for x in teil.dellen)
            a = sum(int((1+x) * teil.dellen[x].anzahl) for x in range(8)) 
            aw = aw12s[round(a/s/10+0.5)](a) if s >0 else 0
            if aw ==0:
                continue
            content.add_widget(
                Button(text=teil.name,
                    size_hint=(.5,.1)))
            content.add_widget(
                Button(text=str(aw) , 
                size_hint=(.5,.1)))
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