
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

import pandas as pd
import seaborn as sns

from MemProgrammer import MemProgrammer
import plyer
import numpy as np
class FileChoosePopup(Popup):
    load = ObjectProperty(None)
    
    def __init__(self,**kwargs):
        #execute the normal __init__ from the parent
        super().__init__(**kwargs)
        self.ids.filechooser.path = os.getcwd()

class FigurePopup(Popup):
    path = ObjectProperty(None)
    file_path = ObjectProperty(None)
    def __init__(self,**kwargs):
        #execute the normal __init__ from the parent
        super().__init__(**kwargs)
        self.plot()
        
        
    def plot(self):
        data = pd.read_csv(self.file_path)
        print(self.file_path)

        data.columns = ["Time", "Pulses", "Tests",'R','isSucces','dt_Ron',
                        'Amp_Ron', 'q', 'E_memristor', 'State']

        temp_data = data[data["isSucces"]==True].groupby(by="Pulses").count()
        plt.figure(figsize=(10,5))
        sns.barplot( x=temp_data.index, y="R", data=temp_data)
        plt.xlabel("$No.\ of\ Pulses$", fontsize=15)
        plt.ylabel("Number of successful tests to $R_{on}$ state ", fontsize=15)
        plt.grid(True)
        
        box = self.ids.Ploting_box
        box.clear_widgets()
        self.figure = plt.gcf()
        box.add_widget(FigureCanvasKivyAgg(  self.figure))

        
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
        if not os.path.isdir(self.file_path):
            self.ids.FilePath.color = "red"
            self.ids.FilePath.text = "Nie wybrano ścieżki"
        else:
            print("Hello World")
            self.directory = self.ids.FilePath.text
            self.Amp_On = round(self.ids.AmpOn.value,1)
            self.dt_Ron = self.ids.dtOn.value/1000.
            self.max_tests = int(self.ids.max_test.text)
            self.max_pulses = int(self.ids.max_pulses.text)
            
            print(self.Amp_On)
            #print(self.ids.pos_hint)
            programmer = MemProgrammer(device_name = "myDAQ1",fs_acq=10000. , N = 10000,r = 4.7, states_limit= (4, 50))
            self.measure_file = programmer.setting_Ron_measurment(n_mem=1,Amp_On=self.Amp_On, Amp_Off=-1.5, dt_On=self.dt_Ron, dt_Off=0.1,
                                        max_tests=self.max_tests, max_pulses=self.max_pulses, saving=True,directory=self.directory)
            programmer.closing()
            self.ids.plot.disabled = False
            




    def make_file(self):
        file = f"Programowanie_Ron_wyniki_AmpOn={self.Amp_On}_dtOn={self.dt_Ron}.csv"
        string = "Timestamp,No. pulses, No. Test,R,Succes,dt_Ron,Amp_RonR,q,E_memristor,State\n"
        self.file = os.path.join(self.directory, file)
        
        with open(self.file, "w") as f:
            f.write(string)
            print("Operacja udana")

    def open_popup_plot(self):
        self.plot_popup = FigurePopup(path = self.file_path, file_path = self.measure_file)
        self.plot_popup.open()
        
        



Builder.load_file('main.kv')

class SayHello(App):
    def build(self):
        return MainPanel()


if __name__ == "__main__":
    SayHello().run()
