import mp3_player
import time
import random
import global_events as events
import threading


class MusicSelectModule (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("Start music select module!")
        module_start()
        print("Music select module stopped!")


# Define the playlist.
playlist = ['C:\AMI\Avicii - Wake Me Up.mp3',
            'C:\AMI\Miley Cyrus - Wrecking Ball.mp3',
            'C:\AMI\Daft Punk - Get Lucky(feat. Pharrell Williams).mp3',
            'C:\AMI\John Newman - Love Me Again.mp3',
            'C:\AMI\Mika - Celebrate(feat. Pharrell Williams).mp3']


def start_music_module():
    events.set_value("Music_player_state", "PLAYING")
    events.set_value("Music_location", random.choice(playlist))

    music_thread = mp3_player.MusicModule("Music_Thread")
    music_thread.start()


def module_start():
    events._init()
    start_music_module()
    events.to_string()
    time.sleep(0.01)
    while True:
        if events.get_value("Music_player_state") == "STOP":
            print("Music ending")
            start_music_module()
            events.to_string()


if __name__ == "__main__":

    music_select_thread = MusicSelectModule("Music_Select_Thread")
    music_select_thread.start()

    number = input("input:")

    running = True

    while running:
        if number == "1":
            events.set_value("Music_player_state", "STOP")
            break

        elif number == "2":
            events.set_value("Music_player_state", "PAUSE")
            events.to_string()
            number = input("input:")

        elif number == "3":
            events.set_value("Music_player_state", "PLAYING")
            number = input("input:")
