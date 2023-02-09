
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooser
import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
import os


class FileChoosePopup(Popup):
    load = ObjectProperty(None)




class MainPanel(FloatLayout):
    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)

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

    def startMeasure(self):
        self.directory = self.ids.FilePath.text
        self.Amp_On = round(self.ids.AmpOn.value)
        self.dt_Ron = self.ids.dtOn.value/1000
        print(self.Amp_On)
        self.make_file()

    def make_file(self):
        file = f"Programowanie_Ron_wyniki_AmpOn={self.Amp_On}_dtOn={self.dt_Ron}.csv"
        string = "Timestamp,No. pulses, No. Test,R,Succes,dt_Ron,Amp_RonR,q,E_memristor,State\n"
        self.file = os.path.join(self.directory, file)
        
        with open(self.file, "w") as f:
            f.write(string)
            print("Operacja udana")




Builder.load_file('main.kv')

class SayHello(App):
    def build(self):
        return MainPanel()



if __name__ == "__main__":
    SayHello().run()
