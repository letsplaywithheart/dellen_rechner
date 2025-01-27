import pickle
from kivy.app import App
from kivy.metrics import dp
from kivy.graphics import Color
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
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
from bvat import aw10s, aw10w, aw12s, aw12w
from kivy.core.window import Window

Builder.load_string(
    """

<Tabs>
    id:tabs
    tab_pos:'bottom_mid'
    do_default_tab: False
    tab_width: root.width/3
        
    TabbedPanelItem:
        text: 'Autos'
        size_hint: (0.1, 0.1)
        on_state: if self.state=='down' : root.startansicht()
        StackLayout:
            id:startansicht 
            size_hint:(1,1)
            orientation:'lr-tb'
                
    TabbedPanelItem:
        text: 'Hagel'
        on_state: if self.state=='down' : root.schadensaufnahme()
        StackLayout:
            id:hagel
            orientation: 'lr-tb'
            size_hint:(1,1)
            
#    TabbedPanelItem:
#        id: tabelle
#        text: 'Foto'
#        on_state: if self.state=='down' : root.aw_tabelle()
#        StackLayout:
#            size_hint:(1,1)

<EditButton>
    size_hint: (1/3, None)
    # on_press: root.parent.edit_auto(auto=root.auto)
    Image:
        source: 'pen.png'
        size: self.parent.height*0.7,self.parent.height*0.7
        y: self.parent.y + self.parent.size[1]/2 - self.size[1]/2
        x: self.parent.x + self.parent.size[0]/2 - self.size[0]/2
"""
)

# Window.softinput_mode = "pan"


@dataclass
class delle:
    name: str
    anzahl: int

    def set_anzahl(self, initinput, x):
        if x == "":
            self.anzahl = 0
        else:
            self.anzahl = int(x)

    def incr_anzahl(self, Ii, bt):
        self.anzahl = self.anzahl + 1
        Ii.text = str(self.anzahl)

    def decr_anzahl(self, Ii, bt):
        if self.anzahl > 0:
            self.anzahl = self.anzahl - 1
            Ii.text = str(self.anzahl)


@dataclass
class Teil:
    name: str = "name"
    alu: bool = False
    kleben: bool = False
    press: bool = False
    tauschen: bool = False
    dellen: list = list[delle]
    senkrecht: bool = False
    aw10: bool = True

    def __post_init__(self):
        self.dellen = [
            delle("10mm", 0),
            delle("20mm", 0),
            delle("30mm", 0),
            delle("40mm", 0),
            delle("50mm", 0),
            delle("60mm", 0),
            delle("70mm", 0),
            delle("80mm", 0),
        ]

    def set_kleben(self, x, y):
        self.kleben = not self.kleben

    def set_alu(self, x, y):
        self.alu = not self.alu

    def set_tauschen(self, x, y):
        self.tauschen = not self.tauschen

    def set_press(self, x, y):
        self.press = not self.press


class Auto:
    def __init__(self, aw10=True, **kwargs):
        self.text = "Auto"
        if "name" in kwargs:
            self.text = kwargs["name"]
            kwargs.pop("name")
        self.allow_no_selection = False
        self.teile = [
            Teil("Motorhaube"),
            Teil("Dach"),
            Teil("A Säule links"),
            Teil("A Säule rechts"),
            Teil("Tür vorne links", senkrecht=True),
            Teil("Tür vorne rechts", senkrecht=True),
            Teil("Tür hinten links", senkrecht=True),
            Teil("Tür hinten rechts", senkrecht=True),
            Teil("Kotflügel vorne links", senkrecht=True),
            Teil("Kotflügel vorne rechts", senkrecht=True),
            Teil("Kotflügel hinten links", senkrecht=True),
            Teil("Kotflügel hinten rechts", senkrecht=True),
            Teil("Heckklappe oben"),
            Teil("Heckklappe unten", senkrecht=True),
        ]
        self.aw10 = aw10
        self.state = "normal"

    def set_name(self, textinput, value):
        self.text = value

    def set_aw10(self, button, value):
        self.aw10 = not self.aw10
        for teil in self.teile:
            teil.aw10 = self.aw10


class EditButton(Button):
    pass


class IntInput(TextInput):
    pat = re.compile("[^0-9]")

    def __init__(self, **kwargs):
        super(IntInput, self).__init__(**kwargs)
        self.font_size = self.size[1] * 0.6
        self.halign = "center"
        self.align = "center"

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, "", substring)
        return super().insert_text(s, from_undo=from_undo)

    def on_focus(self, instance, value, *largs):
        Clock.schedule_once(lambda dt: instance.select_all(), 0.1)


class Tabs(TabbedPanel):
    auto = Auto()
    auto_liste = [Auto(name="Tina"), Auto(name="Andi"), Auto(name="Erika")]

    def __init__(self, **kwargs):
        super(Tabs, self).__init__(**kwargs)
        with open("auto_liste", "ab+") as file:
            file.seek(0)
            temp = file.read()
            if len(temp) > 0:
                file.seek(0)
                self.auto_liste = pickle.load(file)
        for auto in self.auto_liste:
            auto.state = "normal"
        self.auto = self.auto_liste[0]
        self.auto.state = "down"

    def save(self):
        with open("auto_liste", "wb") as file:
            pickle.dump(self.auto_liste, file)

    def set_auto(self, button, value):
        self.auto.state = "normal"
        self.auto = button.auto
        self.auto.state = "down"

    def edit_auto(self, button, new=True):
        auto = Auto() if new else self.auto
        content = self.ids.startansicht
        content.clear_widgets()
        content.add_widget(Button(text="Name / VIN", size_hint=(0.5, 0.1)))
        content.add_widget(
            t := TextInput(size_hint=(0.5, 0.1), multiline=False, text=auto.text)
        )
        t.bind(text=auto.set_name)
        Clock.schedule_once(lambda dt: setattr(t, 'focus', True), 0.1)
        if new:
            Clock.schedule_once(lambda dt: t.select_all(), 0.1)
        content.add_widget(
            s := ToggleButton(
                text="10 AW",
                size_hint=(0.5, 0.1),
                group="aw",
                state="down" if auto.aw10 else "normal",
                allow_no_selection=False
            )
        )
        s.bind(state=self.auto.set_aw10)
        content.add_widget(
            ToggleButton(
                text="12 AW",
                size_hint=(0.5, 0.1),
                group="aw",
                state="down" if not auto.aw10 else "normal",
                allow_no_selection=False
            )
        )
        content.add_widget(
            b := Button(text="Fertig", size_hint=(0.5, 0.1), background_color=(0, 1, 0))
        )
        b.bind(on_press=partial(self.add_Auto, auto))
        content.add_widget(
            b := Button(
                text="Abbrechen", size_hint=(0.5, 0.1), background_color=(1, 0, 0)
            )
        )
        b.bind(on_press=self.startansicht)

    def add_Auto(self, auto, Button):
        if auto in self.auto_liste:
            self.startansicht()
        else:
            self.auto.state = "normal"
            self.auto = auto
            self.auto_liste.insert(0, auto)
            auto.state = "down"
            self.startansicht()

    def delete_abfrage(self, button):
        content = self.ids.startansicht
        content.clear_widgets()
        content.add_widget(
            Label(text="Möchtest du das Auto wirklich löschen? ", size_hint=(1, 0.1))
        )
        content.add_widget(
            b := Button(text="Ja", size_hint=(0.5, 0.1), background_color=(0, 1, 0))
        )
        b.bind(on_press=self.delete_auto)
        content.add_widget(
            b := Button(text="Nein", size_hint=(0.5, 0.1), background_color=(1, 0, 0))
        )
        b.bind(on_press=self.startansicht)

    def delete_auto(self, button):
        self.auto_liste.remove(self.auto)
        if len(self.auto_liste) <= 0:
            self.auto_liste.append(Auto(name="Beispielauto"))
        self.auto = self.auto_liste[0]
        self.auto.state = "down"
        self.startansicht()

    def dellen_aufnehmen(self, teil, x):
        content = self.ids.hagel
        content.clear_widgets()
        height = 0.08
        content.add_widget(
            Button(
                text=self.auto.text,
                on_press=self.schadensaufnahme,
                size_hint=(1, 0.1),
                background_color=(0.0, 1, 0.0),
            )
        )
        content.add_widget(
            Button(
                text=teil.name, on_press=self.schadensaufnahme, size_hint=(1, height)
            )
        )
        content.add_widget(
            b := ToggleButton(
                text="Alu",
                size_hint=(0.25, height),
                state="down" if teil.alu else "normal",
            )
        )
        b.bind(state=teil.set_alu)
        content.add_widget(
            b := ToggleButton(
                text="Kleben",
                size_hint=(0.25, height),
                state="down" if teil.kleben else "normal",
            )
        )
        b.bind(state=teil.set_kleben)
        content.add_widget(
            b := ToggleButton(
                text="Drücken",
                size_hint=(0.25, height),
                state="down" if teil.press else "normal",
            )
        )
        b.bind(state=teil.set_press)
        content.add_widget(
            b := ToggleButton(
                text="Tauschen",
                size_hint=(0.25, height),
                state="down" if teil.tauschen else "normal",
            )
        )
        b.bind(state=teil.set_tauschen)
        for delle in teil.dellen:
            content.add_widget(bt := Button(text=delle.name, size_hint=(0.3, height)))
            Ii = IntInput(text=str(delle.anzahl), size_hint=(0.3, height))
            Ii.bind(text=delle.set_anzahl)
            content.add_widget(bt := Button(text="-", size_hint=(0.2, height)))
            bt.bind(on_press=partial(delle.decr_anzahl, Ii))
            content.add_widget(Ii)
            content.add_widget(bt := Button(text="+", size_hint=(0.2, height)))
            bt.bind(on_press=partial(delle.incr_anzahl, Ii))
        content.add_widget(
            Button(
                text="Fertig",
                on_press=self.schadensaufnahme,
                size_hint=(1, 0.1),
                background_color=(0.0, 1.0, 0.0, 1.0),
            )
        )

    def startansicht(self, *args):
        self.save()
        content = self.ids.startansicht
        content.clear_widgets()
        content.add_widget(
            b := Button(text="+", size_hint=(1 / 3, 0.1), background_color=(0, 1, 0))
        )
        b.bind(on_press=self.edit_auto)
        content.add_widget(
            b := Button(text="-", size_hint=(1 / 3, 0.1), background_color=(1, 0, 0))
        )
        b.bind(on_press=self.delete_abfrage)
        content.add_widget(b := EditButton(size_hint=(1 / 3, 0.1)))
        b.bind(on_press=partial(self.edit_auto, new=False))
        content.add_widget(ti:=TextInput(hint_text="Suche", size_hint=(1, 0.05)))
        ti.bind(text=self.list_renew)
        content.add_widget(
            scv:= ScrollView(do_scroll_x=False, size_hint=(1, 1))
        )
        self.startansicht_bl=BoxLayout(orientation = 'vertical', size_hint=(1,None),size=(0,0))
        scv.add_widget(self.startansicht_bl)
        self.list_renew(None,'')

    def list_renew(self,textinput, value):
        self.startansicht_bl.height=0
        self.startansicht_bl.clear_widgets()
        for auto in self.auto_liste:
            if value.lower() in auto.text.lower():
                self.startansicht_bl.add_widget(
                    b := ToggleButton(
                        text=auto.text,
                        size_hint=(1, 0.05),
                        group="auto",
                        allow_no_selection=False,
                        state=auto.state,
                    )
                )
                b.auto = auto
                b.bind(state=self.set_auto)
                self.startansicht_bl.height += dp(40)

    def schadensaufnahme(self, *args):
        self.save()
        content = self.ids.hagel
        content.clear_widgets()
        content.add_widget(
            Button(
                text=self.auto.text,
                size_hint=(0.7, 0.1),
                background_color=(0.0, 0.6, 0.0),
            )
        )
        content.add_widget(
            bt_sum := Button(
                text=self.auto.text,
                size_hint=(0.3, 0.1),
                background_color=(1.0, 0, 0.0),
            )
        )
        bt_sum.canvas.add(Color(rgba=(1, 0, 0)))
        content.add_widget(
            bt_name := Label(
                text="Teil",
                size_hint=(0.45, None),
                size=(0, Window.size[1] * 0.05),
            )
        )
        content.add_widget(
            bt_aw := Label(
                text="Gr",
                size_hint=(0.1, None),
                size=(0, Window.size[1] * 0.05),
            )
        )
        content.add_widget(
            bt_aw := Label(
                text="Anzahl",
                size_hint=(0.1, None),
                size=(0, Window.size[1] * 0.05),
            )
        )
        content.add_widget(
            bt_aw := Label(
                text="Extra",
                size_hint=(0.2, None),
                size=(0, Window.size[1] * 0.05),
            )
        )
        content.add_widget(
            bt_aw := Label(
                text="AW",
                size_hint=(0.15, None),
                size=(0, Window.size[1] * 0.05),
            )
        )

        content.add_widget(
            scv := ScrollView(
                do_scroll_x=False,
                size_hint=(1, None),
                size=(0, Window.size[1] * 0.9 - dp(40)),
            )
        )
        scv.add_widget(stl := StackLayout(size_hint=(1, None)))
        summe = 0
        teile_gr_0 = 0
        finish = 13 if self.auto.aw10 else 15.5
        for teil in self.auto.teile:
            extra = BoxLayout(
                orientation="vertical",
                size_hint=(0.2, None),
                size=(0, Window.size[1] * 0.1),
            )
            s = sum(x.anzahl for x in teil.dellen)
            a = sum(int((1 + x) * teil.dellen[x].anzahl) for x in range(8))
            if teil.aw10:
                y = aw10s if teil.senkrecht else aw10w
            else:
                y = aw12s if teil.senkrecht else aw12w
            # print(f"a {a} s {s}")
            # print(round(a / s - 1)) if s > 0 else 0
            aw = y[round(a / s - 1)](s) if s > 0 else 0
            # print(f"aw {aw}") if s > 0 else 0
            if teil.alu:
                aw = aw * 1.25
                extra.add_widget(Button(text="Alu",background_color=(0,0,10)))
            if teil.kleben:
                aw = aw * 1.4
                extra.add_widget(Button(text="Kleben",background_color=(1,1,0)))
            if teil.press:
                aw = aw * 0.6
                extra.add_widget(Button(text="Drücken",background_color=(1,0,0)))
            # print(f"aw {aw}") if s > 0 else 0
            # print(f"aw {aw}") if s > 0 else 0
            stl.add_widget(
                bt_name := Button(
                    text=teil.name, size_hint=(1, None), size=(0, Window.size[1] * 0.1)
                )
            )
            stl.add_widget(
                bt := Button(
                    text=str(10 * round(a / s + 0.5)) if s > 0 else "0",
                    size_hint=(0.1, None),
                    size=(0, Window.size[1] * 0.1),
                )
            )
            bt.bind(on_press=partial(self.dellen_aufnehmen, teil))
            stl.add_widget(
                bt := Button(
                    text=str(s), size_hint=(0.1, None), size=(0, Window.size[1] * 0.1)
                )
            )
            bt.bind(on_press=partial(self.dellen_aufnehmen, teil))
            stl.add_widget(extra)
            stl.height = stl.height + bt_name.height
            bt_name.bind(on_press=partial(self.dellen_aufnehmen, teil))
            if aw > 0:
                stl.add_widget(
                    bt_aw := Button(
                        text=str(round(aw, 1)),
                        size_hint=(0.15, None),
                        size=(0, Window.size[1] * 0.1),
                    )
                )
                bt_aw.bind(on_press=partial(self.dellen_aufnehmen, teil))

                summe += aw
                teile_gr_0 += 1
            bt_name.size_hint_x = 0.45
        bt_sum.text = str(round(summe, 1))
        if teile_gr_0 > 0:
            stl.add_widget(
                bt := Button(
                    text="Rüstzeit",
                    size_hint=(0.45, None),
                    size=(0, Window.size[1] * 0.1),
                ),
                index=len(stl.children),
            )
            stl.add_widget(
                bt := Label(
                    text="", size_hint=(0.4, None), size=(0, Window.size[1] * 0.1)
                ),
                index=len(stl.children) - 1,
            )
            stl.add_widget(
                bt := Button(
                    text=str(6 if self.auto.aw10 else 7),
                    size_hint=(0.15, None),
                    size=(0, Window.size[1] * 0.1),
                ),
                index=len(stl.children) - 2,
            )
            stl.add_widget(
                bt := Button(
                    text="Finish",
                    size_hint=(0.45, None),
                    size=(0, Window.size[1] * 0.1),
                ),
                index=len(stl.children) - 3,
            )
            stl.add_widget(
                bt := Label(
                    text="", size_hint=(0.4, None), size=(0, Window.size[1] * 0.1)
                ),
                index=len(stl.children) - 4,
            )
            if teile_gr_0 > 5:
                finish = 13 if self.auto.aw10 else 15.5
            else:
                finish = teile_gr_0 * (2.5 if self.auto.aw10 else 3)

            stl.add_widget(
                bt := Button(
                    text=str(finish),
                    size_hint=(0.15, None),
                    size=(0, Window.size[1] * 0.1),
                ),
                index=len(stl.children) - 5,
            )
            stl.height = stl.height + bt_name.height

    def aw_tabelle(self):
        self.save()
        content = self.ids.tabelle.content
        content.clear_widgets()


class Test(BoxLayout):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
        self.tabs = Tabs()
        self.add_widget(self.tabs)


class TabbedPanelApp(App):
    def build(self):
        return Test()


if __name__ == "__main__":
    TabbedPanelApp().run()
