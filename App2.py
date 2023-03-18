
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooser

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
import os
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import _osx_support
from kivy.clock import Clock

import numpy as np
class FileChoosePopup(Popup):
    load = ObjectProperty(None)
    
    def __init__(self,**kwargs):
        #execute the normal __init__ from the parent
        super().__init__(**kwargs)
        self.ids.filechooser = os.getcwd()

class FigurePopup(Popup):
    load = ObjectProperty(None)
    path = ObjectProperty(None)
    def __init__(self,**kwargs):
        #execute the normal __init__ from the parent
        super().__init__(**kwargs)
        Clock.schedule_interval(self.on_start,1)
        
        
    def plot(self):
        signal = [7, 89.6, 45.-56.34]

        signal = np.array(signal)

        # this will plot the signal on graph
        plt.plot(signal)
        # setting x label
        plt.xlabel('Time(s)')

        # setting y label
        plt.ylabel('signal (norm)')
        plt.grid(True, color='lightgray')
        plt.show()
        
    def on_start(self,*args):
        signal = [7, 89.6, 45., -56.34]

        signal = np.array(signal)

        # this will plot the signal on graph
        plt.hist(signal,color='blue')
        # setting x label
        plt.xlabel('Time(s)')

        # setting y label
        plt.ylabel('signal (norm)')
        plt.grid(True, color='lightgray')

        # adding plot to kivy boxlayout
        box = self.ids.Ploting_box
        box.clear_widgets()
        self.figure = plt.gcf()
        box.add_widget(FigureCanvasKivyAgg(  self.figure))
    
    def save(self):
        path = os.path.join(self.path, 'signal.pdf')
        self.figure.savefig(path)
    


class MainPanel(FloatLayout):
    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)
    plot_popup = ObjectProperty(None)

    def open_popup(self):
        self.the_popup = FileChoosePopup(load = self.load)
        self.the_popup.open()

    def load(self, selection):
        self.file_path = str(selection)
        self.the_popup.dismiss()
        print(self.file_path)

        # check for non-empty list i.e. file selected
        if self.file_path:
            self.ids.FilePath.text = self.file_path
            self.ids.FilePath.color = "white"

    def startMeasure(self):
        print("Hello World")
        self.directory = self.ids.FilePath.text
        self.Amp_On = round(self.ids.AmpOn.value,1)
        self.dt_Ron = self.ids.dtOn.value/1000.
        print(self.Amp_On)
        #print(self.ids.pos_hint)
        
        if os.path.isdir(self.directory):
            self.make_file()
        else:
            self.ids.FilePath.color = "red"
            self.ids.FilePath.text = "Nie wybrano ścieżki"



    def make_file(self):
        file = f"Programowanie_Ron_wyniki_AmpOn={self.Amp_On}_dtOn={self.dt_Ron}.csv"
        string = "Timestamp,No. pulses, No. Test,R,Succes,dt_Ron,Amp_RonR,q,E_memristor,State\n"
        self.file = os.path.join(self.directory, file)
        
        with open(self.file, "w") as f:
            f.write(string)
            print("Operacja udana")

    def open_popup_plot(self):
        self.plot_popup = FigurePopup(path = self.file_path)
        self.plot_popup.open()
        
        
        
        




Builder.load_file('main.kv')

class SayHello(App):
    def build(self):
        return MainPanel()


if __name__ == "__main__":
    SayHello().run()
