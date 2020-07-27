import argparse
import random
from pydub import AudioSegment
from pydub.playback import play


def my_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stringy",
        default="The quick brown fox jumps over the lazy dog.",
        help="input string"
    )
    parser.add_argument(
        "--pitch",
        default="med",
        choices=["high", "med", "low", "lowest"],
        help='choose between "high", "med", "low", or "lowest"'
    )
    parser.add_argument(
        "--rnd_factor",
        type=float,
        help="random factor"
    )
    parser.add_argument(
        "--uniform_sample_rate",
        type=float,
        default=44100,
        help="uniform sample rate"
    )

    return parser.parse_args()


def main():
    # Get arguments.
    argument = my_parser()

    stringy = argument.stringy.lower()
    sounds = {}
    keys = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        "u", "v", "w", "x", "y", "z", "th", "sh", " ", "."
    ]
    for index, ltr in enumerate(keys):
        num = index + 1
        if num < 10:
            num = "0" + str(num)
        sounds[ltr] = (
            "./sounds/" +
            argument.pitch +
            "/sound" +
            str(num) +
            ".wav"
        )

    if argument.rnd_factor is None:
        if argument.pitch == "med":
            rnd_factor = .35
        else:
            rnd_factor = .25
    else:
        rnd_factor = argument.rnd_factor

    infiles = []

    for i, char in enumerate(stringy):
        if char == "s" and stringy[i+1] == "h":  # test for "sh" sound
            infiles.append(sounds["sh"])
        elif char == "t" and stringy[i+1] == "h":  # test for "th" sound
            infiles.append(sounds["th"])
        # test if previous letter was "s" or "s" and current letter is "h"
        elif char == "h" and (stringy[i-1] == "s" or stringy[i-1] == "t"):
            pass
        elif char == "," or char == "?":
            infiles.append(sounds["."])
        elif char == stringy[i-1]:  # skip repeat letters
            pass
        # skip characters that are not letters or periods.
        elif char.isalpha() or char == ".":
            infiles.append(sounds[char])
        # skip characters that are not letters or periods.
        else:
            pass

    combined_sounds = None

    print("Length of text is", len(infiles))
    for index, sound in enumerate(infiles):
        tempsound = AudioSegment.from_wav(sound)
        if stringy[len(stringy)-1] == "?":
            if index >= len(infiles)*.8:
                # shift the pitch up by half an octave
                # speed will increase proportionally
                octaves = random.random() * rnd_factor + (index-index*.8) * .1 + 2.1
            else:
                octaves = random.random() * rnd_factor + 2.0
        else:
            # shift the pitch up by half an octave
            # speed will increase proportionally
            octaves = random.random() * rnd_factor + 2.3
        new_sample_rate = int(tempsound.frame_rate * (2.0 ** octaves))
        new_sound = tempsound._spawn(
            tempsound.raw_data,
            overrides={"frame_rate": new_sample_rate}
        )
        # set uniform sample rate
        new_sound = new_sound.set_frame_rate(argument.uniform_sample_rate)
        if combined_sounds:
            combined_sounds = combined_sounds + new_sound
        else:
            combined_sounds = new_sound

    combined_sounds.export("./sound.wav", format="wav")


if __name__ == "__main__":
    main()
