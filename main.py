from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from server import check_login_password, get_coin_quint, pay_for_water
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
import time

TOKEN = ""


class EntryPanel(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        self.label1 = Label(
            size_hint=(0.8, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            text="Добро пожаловать \n на окно авторизации",
            font_size="30dp",
            color="black",
            halign="center"
        )
        self.layout.add_widget(self.label1)

        self.input1 = TextInput(
            size_hint=(0.6, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            hint_text="Имя пользователя",
            font_size="20dp",
            multiline=False,
            write_tab=False
        )
        self.layout.add_widget(self.input1)

        self.input2 = TextInput(
            size_hint=(0.6, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.49},
            hint_text="Пароль",
            font_size="20dp",
            multiline=False,
            password=True,
            write_tab=False
        )
        self.layout.add_widget(self.input2)

        self.btn = Button(
            size_hint=(0.6, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            text="Войти",
            on_release=self.event_but
        )
        self.layout.add_widget(self.btn)

        self.label2 = Label(
            size_hint=(0.5, 0.1),
            pos_hint={"center_x": 0.3, "center_y": 0.4},
            text="Запомнить меня",
            font_size="15dp",
            color="black",
        )
        self.layout.add_widget(self.label2)

        self.check = CheckBox(
            size_hint=(0.1, 0.1),
            pos_hint={"center_x": 0.55, "center_y": 0.4},
            active=False,
            color=[0, 0, 0, 1]
        )
        self.layout.add_widget(self.check)

        self.label3 = Label(
            size_hint=(0.1, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            text="",
            font_size="20dp",
            color="black"
        )
        self.layout.add_widget(self.label3)
        self.add_widget(self.layout)

    def event_but(self, rub):
        login, password = self.input1.text, self.input2.text
        if login == "" or password == "":
            self.status_label(3)
        else:
            self.status_label(5)
            answer = check_login_password(login, password)
            self.status_label(answer[0])
            if answer[0] == 4:
                global TOKEN
                TOKEN = answer[1]
                self.main_page()

    def status_label(self, value):
        print(value == 5)
        if value == 0:
            self.label3.text = "Ошибка времени запроса"
            self.label3.color = "red"
        elif value == 1:
            self.label3.text = "Неверный логин"
            self.label3.color = "red"
        elif value == 2:
            self.label3.text = "Неверный пароль"
            self.label3.color = "red"
        elif value == 3:
            self.label3.text = "Введите свой логин и пароль"
            self.label3.color = "black"
        elif value == 4:
            self.label3.text = "OK"
            self.label3.color = "green"
        elif value == 5:
            self.label3.text = "Загрузка"
            self.label3.color = "black"

    def main_page(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'mainpanel'


class MainPanel(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.label1 = Label(
            size_hint=(0.8, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.85},
            text="Личный кабинет",
            font_size="30dp",
            color="black",
            halign="center"
        )
        self.layout.add_widget(self.label1)
        self.label2 = Label(
            size_hint=(0.2, 0.2),
            pos_hint={"center_x": 0.3, "center_y": 0.75},
            text="0",
            font_size="30dp",
            color="black",
            halign="center"
        )
        self.layout.add_widget(self.label2)
        self.update_coins()

        self.btn = Button(
            size_hint=(0.3, 0.06),
            pos_hint={"center_x": 0.3, "center_y": 0.62},
            text="Обновить",
            on_release=self.update_coins
        )
        self.layout.add_widget(self.btn)
        self.image = Image(
            source="data/images/coin.jpeg",
            size_hint_x=0.2,
            pos_hint={"center_x": 0.6, "center_y": 0.75},
            allow_stretch=True
        )
        self.layout.add_widget(self.image)

        self.input1 = TextInput(
            size_hint=(0.8, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            hint_text="Сколько заплатить за воду",
            font_size="20dp",
            multiline=False,
            write_tab=False
        )
        self.layout.add_widget(self.input1)

        self.btn1 = Button(
            size_hint=(0.3, 0.06),
            pos_hint={"center_x": 0.3, "center_y": 0.4},
            text="Заплатить",
            on_release=self.pay_for_water
        )
        self.layout.add_widget(self.btn1)
        self.label3 = Label(
            size_hint=(0.8, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            text="",
            font_size="30dp",
            color="black",
            halign="center"
        )
        self.layout.add_widget(self.label3)

        self.btn2 = Button(
            size_hint=(0.5, 0.06),
            pos_hint={"center_x": 0.3, "center_y": 0.2},
            text="Выйти из аккаунта",
            on_release=self.entry_page
        )
        self.layout.add_widget(self.btn2)

        self.add_widget(self.layout)



    def update_coins(self, *args):
        self.now_coins = get_coin_quint(TOKEN)
        self.label2.text = str(self.now_coins)

    def pay_for_water(self, *args):
        self.coins_for_water = self.input1.text
        try:
            self.int_coins_for_water = int(self.coins_for_water)
            if not self.int_coins_for_water:
                self.label3.text = "Введите число больше 0"
            elif self.int_coins_for_water > self.now_coins:
                self.label3.text = "Недостаточно монет"
            else:
                pay_for_water(TOKEN, self.int_coins_for_water)
                self.update_coins()
                self.input1.text = ""
                self.label3.text = "Оплачено"
        except Exception:
            self.label3.text = "Введите число"
        pass

    def entry_page(self, *args):
        global TOKEN
        TOKEN = ""
        self.manager.transition.direction = 'right'
        self.manager.current = 'entrypanel'



class MyApp(App):
    def build(self):
        Window.size = (400, 800)
        Window.clearcolor = (242 / 256, 240 / 256, 230 / 256, 1)
        sm = ScreenManager()
        sm.add_widget(EntryPanel(name='entrypanel'))
        sm.add_widget(MainPanel(name='mainpanel'))
        return sm


if __name__ == '__main__':
    MyApp().run()