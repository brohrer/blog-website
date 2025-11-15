# /// script
# requires-python = ">=3.10.0,<3.11"
# dependencies = [
#     "numpy",
#     "simpleaudio",
#     "soundfile",
# ]
# ///
import base64
import io
import numpy as np
import simpleaudio as sa
import soundfile as sf

mp3file = "speech.mp3"
temp_mp3file = "delete_me.mp3"


def main():
    ## Reading an MP3 from a file to a NumpyArray
    audio_data, samplerate = sf.read(mp3file)
    if len(audio_data.shape) == 1:
        num_samples = audio_data.shape[0]
        num_channels = 1
    else:
        num_samples, num_channels = audio_data.shape

    display_info(audio_data, samplerate)
    play_array_as_audio(audio_data, samplerate)

    ## Writing a Numpy arrayto an MP3 file.
    sf.write(temp_mp3file, audio_data, samplerate)

    ## Convert a Numpy array to a string of .mp3-formatted bytes.
    mp3_buf = io.BytesIO()
    # Infers file type from name extension.
    mp3_buf.name = 'file.mp3'
    sf.write(mp3_buf, audio_data, samplerate)
    mp3_buf.seek(0)  # Necessary for `.read()` to return all bytes
    mp3_bytes = mp3_buf.read()

    ## Convert a string of .mp3-formatted bytes to a Numpy array.
    new_mp3_buf = io.BytesIO(mp3_bytes)
    # Infers file type from name extension.
    new_mp3_buf.name = 'new_file.mp3'
    new_audio_array, new_samplerate = sf.read(new_mp3_buf)

    # display_info(new_audio_array, new_samplerate)
    # play_array_as_audio(new_audio_array, new_samplerate)

    ## Converting a string of bytes to a base64 encoded ascii string.
    base64_mp3_bytes = base64.b64encode(mp3_bytes)
    base64_mp3_string = base64_mp3_bytes.decode("ascii")
    # print(base64_mp3_string)

    ## Converting a base64 encoded ascii string to a string of bytes.
    new_base64_mp3_bytes = base64_mp3_string.encode("ascii")
    new_mp3_bytes = base64.b64decode(new_base64_mp3_bytes)

    ## Other file types
    # Can work with .wav, .flac,. ogg, and others.
    # Infers file type from filename extension.


def display_info(data, samplerate):
    if len(data.shape) == 1:
        num_samples = data.shape[0]
        num_channels = 1
    else:
        num_samples, num_channels = data.shape

    print(
        f"data type: {type(data)}, " +
        f"length: {num_samples}, " +
        f"channels: {num_channels}, " +
        f"sample rate: {samplerate}, " +
        f"seconds: {float(num_samples) / float(samplerate)}"
    )


def play_array_as_audio(data, samplerate):
    if len(data.shape) == 1:
        num_channels = 1
    else:
        _, num_channels = data.shape

    ## Normalize Numpy data for simpleaudio playback
    # https://simpleaudio.readthedocs.io/en/latest/tutorial.html#using-numpy
    audio_array = data * 32767 / max(abs(data))
    audio_array = audio_array.astype(np.int16)

    ## Play audio from a Numpy array
    # simpleaudio.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    # https://simpleaudio.readthedocs.io/en/latest/simpleaudio.html#simpleaudio.play_buffer
    play_obj = sa.play_buffer(audio_array, num_channels, 2, samplerate)
    play_obj.wait_done()


if __name__ == "__main__":
    main()
