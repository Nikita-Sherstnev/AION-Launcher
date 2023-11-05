import time
import sys, traceback
from threading import Thread, Lock
from functools import partial
import subprocess

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

from modules.client import Client


Window.size = (600, 400)

lock = Lock()
client = Client()
client_downloaded = False


class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.size = (600, 400)
        self.add_widget(Label(text='AION Launcher', color=(1,1,1,1), pos=(200, 150)))

        self.download_client_btn = Button(text='Загрузить клиент', size_hint=(.2, .2), pos=(500, 200))
        self.play_btn = Button(text='Играть', size_hint=(.2, .2), pos=(500, 80))

        self.download_client_btn.bind(on_press=self.download_game)
        self.play_btn.bind(on_press=start_game)

        self.add_widget(self.download_client_btn)
        self.add_widget(self.play_btn)

        self.download_indicator = Label(text='', color=(1,1,1,1), pos=(0, -200))
        self.add_widget(self.download_indicator)


    def download_game(self, instance):
        print('start download')
        client.change_torrent_status(1, None)

        event = Clock.schedule_interval(partial(update_torrent_info, client, self), 0.5)


def start_game(instance):
    # if client_downloaded:
    subprocess.run("start bin32\\aion.bin -ip:46.72.238.101 -port:2107 -cc:1 -lang:enu -noweb -nowebshop -nokicks -ncg -noauthgg -ls -charnamemenu -ingameshop -win10-mouse-fix",
                    shell=True, check=True)
    # else:
    #     popup = Popup(title='Test popup',
    #                 content=Label(text='Необходимо скачать клиент!', color=(1,1,1,1)),
    #                 background_color=(1,1,1,1), size=(300, 300), size_hint=(300, 300))
    #     popup.open()


def update_torrent_info(client, ui, *largs):
    with lock:
        torrent_info = client.get_torrents_info()[0]

    percents = round(torrent_info['downloaded'] / torrent_info['length'] * 100, 2)

    ui.download_indicator.text = f"{torrent_info['downloaded']} / {torrent_info['length']} Mb"
    ui.ids.my_progress_bar.value = percents


class AIONLauncher(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    try:
        AIONLauncher().run()
        client.exit()
    except Exception as exc:
        print(exc)
        traceback.print_exc(file=sys.stdout)
        time.sleep(100)