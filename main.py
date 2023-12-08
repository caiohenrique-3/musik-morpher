import os
import readline
import glob


def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


def process_song():
    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    song_path = input("Enter song path: ")
    print("Choose effect:")
    print("1. Slow & Reverb")
    print("2. Nightcore")
    effect = int(input("Enter your choice (1 or 2): "))
    if effect == 1:
        # Slow & Reverb effect
        os.system(
            f'ffmpeg -i "{song_path}" -filter:a "atempo=0.8,asetrate=44100*0.8" output.mp3')
    elif effect == 2:
        # Nightcore effect
        os.system(
            f'ffmpeg -i "{song_path}" -filter:a "atempo=1.25,asetrate=44100*1.25" output.mp3')
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return
    print("Song has been processed!")


if __name__ == "__main__":
    process_song()
