import os
import readline
import glob
import requests
from anime_api.apis import NekosAPI
from PIL import Image

nekos = NekosAPI()


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

    speed = ask_for_song_speed(effect)
    image_url = nekos.get_random_image().url
    image_path = 'cover.jpg'
    response = requests.get(image_url)
    with open(image_path, 'wb') as f:
        f.write(response.content)

    resize_image(image_path, 'cover.jpg', (640, 640))

    if effect == 1:
        os.system(
            f'ffmpeg -i "{song_path}" -filter:a "atempo=1.0,asetrate=44100*{speed}" output.mp3')
    elif effect == 2:
        os.system(
            f'ffmpeg -i "{song_path}" -i "{image_path}" -map 0:0 -map 1:0 -filter:a "atempo={speed},asetrate=44100*{speed}" output.mp3')
    else:
        print("\nInvalid choice. Please enter 1 or 2.")
        return

    print("Song has been processed!")


def ask_for_song_speed(effect):
    speed = 0.0

    # slowed
    if effect == 1:
        speed = input(
            "\nEnter custom speed (up to 0.5) or leave blank for default value (0.9):\n> ")

        if speed == '':
            speed = 0.9
        else:
            speed = float(speed)

        if speed < 0.5:
            speed = 0.5

        if speed == 1.0:
            print("\nInvalid value for speed.")

    # nightcore
    else:
        speed = input(
            "\nEnter custom speed (up to 2.0) or leave blank for default value (1.2):\n> ")

        if speed == '':
            speed = 1.2
        else:
            speed = float(speed)

        if speed > 2.0:
            speed = 2.0

        if speed < 1.0:
            speed = 1.08

    return speed


def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    print(f"The original image size is {width} wide x {height} tall")

    resized_image = original_image.resize(size)
    width, height = resized_image.size
    print(f"The resized image size is {width} wide x {height} tall")
    resized_image.save(output_image_path)


if __name__ == "__main__":
    process_song()
