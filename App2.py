
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



class FileChoosePopup(Popup):
    load = ObjectProperty()



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

Builder.load_file('main.kv')

class SayHello(App):
    def build(self):
        return MainPanel()



if __name__ == "__main__":
    SayHello().run()
