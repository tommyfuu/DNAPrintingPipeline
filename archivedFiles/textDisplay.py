from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


Builder.load_string('''
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Add New Staff'
            on_press: root.manager.current = 'add_staff'
        Button:
            text: 'View Staff Profile'
        Button:
            text: 'Salary report'

<Add_new_staff>:
    nam: str(name_input)
    job: job_input
    GridLayout:
        cols: 2
        Label:
            text: 'Name'
        TextInput:
            id: name_input
            multiline: False
        Label:
            text: 'Job'
        TextInput:
            id: job_input
        Label:
            text: 'Salary'
        TextInput:
        Label:
            text: 'Date of Joining'
        TextInput:
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
        Button:
            text: 'Save'
            on_press: app.save(name_input.text, job_input.text)
''')


class MenuScreen(Screen):
    pass

class Add_new_staff(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(Add_new_staff(name='add_staff'))

class TestApp(App):
    def build(self):
        return sm

    def save(self, name, job):
        fob = open('c:/test.txt','w')
        fob.write(name + "\n")
        fob.write(job)
        fob.close()    

if __name__ == '__main__':
    TestApp().run()