import os
import readline
import glob


def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


def process_song():
    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    song_path = input("Enter song path:\n> ")

    print("\nChoose effect:")
    print("1. Slow & Reverb")
    print("2. Nightcore\n")
    effect = int(input("Enter your choice (1 or 2):\n> "))

    if effect == 1:
        os.system(
            f'ffmpeg -i "{song_path}" -filter:a "atempo=0.8,asetrate=44100*0.8" output.mp3')
    elif effect == 2:
        speed = ask_for_song_speed()

        os.system(
            f'ffmpeg -i "{song_path}" -filter:a "atempo={speed},asetrate=44100*{speed}" output.mp3')
    else:
        print("\nInvalid choice. Please enter 1 or 2.")
        return
    print("Song has been processed!")


def ask_for_song_speed():
    speed = input(
        "\nEnter custom speed (up to 2.0) or leave blank for default value (1.2):\n> ")
    if speed == '':
        speed = '1.2'

    speed = float(speed)

    if speed > 2.0:
        speed = 2.0

    if speed < 1.0:
        speed = 1.08

    return speed


if __name__ == "__main__":
    process_song()
