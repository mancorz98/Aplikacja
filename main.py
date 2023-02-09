
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooser
import tkinter as tk
from tkinter import filedialog
import easygui
import kivy

class SayHello(App):
    def build(self):
        #returns a window object with all it's widgets
        self.window = FloatLayout()
        self.window.cols = 4
        self.window.rows = 50
        self.window.size_hint = (0.8,0.97)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # image widget
        self.LogoAGH = Image(source="agh_znak_negatyw_bez_nazwy.jpg",
        pos_hint= {"left": 0, "top":1},
        size_hint= (0.4, 0.2)
        )
        self.window.add_widget(self.LogoAGH)
        # label widget
        self.greeting = Label(
                        text= "Program do programowania memrystora",
                        pos_hint = {"center_x": 0.5, "top": 1},
                        size_hint = (0.2, 0.2)
                        )
        self.window.add_widget(self.greeting)

        self.LogoSamogloski = Image(source="logo-prawie-biale-tlo.png",
                                    pos_hint= {"right": 1, "top":1},
                                    size_hint= (0.2, 0.2))


        self.window.add_widget(self.LogoSamogloski)



        # text input widge
        self.sciezka = TextInput(
                    multiline= False,
                    padding_y= (20,20),
                    size_hint= (0.5, 0.1),
                    pos_hint= {"center_x": 0.8, "center_y":0.6}
                    )
        
        self.window.add_widget(self.sciezka)

        # button widget
        self.button = Button(
                      text= "Wybierz folder zapisu",
                      size_hint= (0.5,0.1),
                      bold= True,
                      background_color ='white',
                      pos_hint= {"center_x": 0.2, "center_y":0.6}
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )


        self.button2 = Button(
                      text= "GREET",
                      size_hint= (0.2,0.2),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )


        self.button.bind(on_press=self.callback_path)
        self.window.add_widget(self.button)


        self.window.add_widget(self.button2)
        
        from kivy.uix.popup import Popup

        self.popup = Popup(title='Test popup',
        content=FileChooser(),
        size_hint=(None, None), size=(400, 400))



        return self.window

    def callback_path(self, instance):
        self.popup.open()

# run Say Hello App Calss

class Filechooser(BoxLayout):
    def select(self, *args):
        try: self.label.text = args[1][0]
        except: pass
 
# Create the App class
class FileApp(App):
    def build(self):
        return Filechooser()

if __name__ == "__main__":
    SayHello().run()
