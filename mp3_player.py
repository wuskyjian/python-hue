import time
import pygame
import threading
import global_events as events
import random

command_event = threading.Event()
music_start_event = threading.Event()

playlist = ['C:\AMI\Avicii - Wake Me Up.mp3',
            'C:\AMI\Miley Cyrus - Wrecking Ball.mp3',
            'C:\AMI\Daft Punk - Get Lucky(feat. Pharrell Williams).mp3',
            'C:\AMI\John Newman - Love Me Again.mp3',
            'C:\AMI\Mika - Celebrate(feat. Pharrell Williams).mp3',
            'C:\AMI\Daniel Powter - Crazy All My Life.mp3']


class MusicPlaying(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("Music detection started.")
        # Wait the music start.
        music_start_event.wait()

        # Start detecting weather the music is playing.
        while events.get_value("Music player running"):
            # Wait the music start.
            music_start_event.wait()
            # Detected the music ended and change to another one.
            if not pygame.mixer.music.get_busy():
                # Start playing a new music.
                music_start_event.clear()
                music_play()
            time.sleep(0.01)
        print("Music detection stopped.")


class MusicModule(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("Start music module!")

        music_play()
        events.set_value("Music player running", True)

        while events.get_value("Music player running"):
            # Wait for command.
            command_event.wait()

            # Get command and perform operation.
            current_state = events.get_value("Music_player_state")
            if current_state == "PAUSE":
                music_pause()

            if current_state == "PLAYING":
                music_unpause()

            if current_state == "CHANGE":
                music_stop()

            if current_state == "QUIT":
                # Stop the player.
                events.set_value("Music player running", False)
                music_stop()

            command_event.clear()
        print("Music module stopped!")


# Play the music.
def music_play():
    pygame.mixer.init()

    # TODO: get implementation of select new song.
    events.set_value("Music_location", str(random.choice(playlist)))

    # events.to_string()

    music_location = events.get_value("Music_location")
    pygame.mixer.music.load(music_location)
    pygame.mixer.music.play()
    music_start_event.set()

    # print("Playing music @%s" % music_location)


# Music paused.
def music_pause():
    # print("Music paused.")
    pygame.mixer.music.pause()


# Music unpaused.
def music_unpause():
    # print("Music unpaused.")
    pygame.mixer.music.unpause()


# Stop or Change the playing music.
def music_stop():
    pygame.mixer.music.fadeout(1000)


if __name__ == "__main__":

    events._init()

    music = MusicModule("Music model")
    detection = MusicPlaying("Music playing")

    music.start()
    detection.start()

    running = True
    while running:
        time.sleep(0.2)
        number = input("input:")
        if number == "1":
            events.set_value("Music_player_state", "CHANGE")
            command_event.set()
            print("Changing song......")

        elif number == "2":
            events.set_value("Music_player_state", "PAUSE")
            command_event.set()
            print("Music paused......")

        elif number == "3":
            events.set_value("Music_player_state", "PLAYING")
            command_event.set()
            print("Music continued......")

        elif number == "4":
            events.set_value("Music_player_state", "QUIT")
            command_event.set()
            print("Music STOPPED.")
            break

    music.join()
    detection.join()
