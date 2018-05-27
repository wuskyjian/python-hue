import global_events as events
import mp3_player
import time

events._init()

music = mp3_player.MusicModule("Music model")
detection = mp3_player.MusicPlaying("Music playing")

music.start()
detection.start()

running = True

command_event = mp3_player.command_event

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
