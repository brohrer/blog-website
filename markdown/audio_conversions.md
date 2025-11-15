# Working with audio files in Python

Converting audio files from formats you can listen to, store, transmit,
and analyze can be migraine-inducing (at least for me) so here are
some shortcuts that work for getting all that done (at least for me).

[Here is a runnable script](https://github.com/brohrer/blog/blob/main/code/audio.py)
demonstrating all the snippets below.

### Libraries

There is a vibrant and confusing landscape of libraries and tools for
working with audio in Python.

One pair that has worked well for me is `soundfile` and `simpleaudio`.
They cover the tasks I need to do, and have licenses that allow me to use
them in code at work.

[soundfile](https://python-soundfile.readthedocs.io/) is an open source
tool for manipulating audio files, released under the
[BSD 3-clause license](https://en.wikipedia.org/wiki/BSD_licenses).
The [source code](https://github.com/bastibe/python-soundfile) is browsable.

[simpleaudio](https://simpleaudio.readthedocs.io/en/latest/index.html) is an
[MIT Licensed](https://en.wikipedia.org/wiki/MIT_License) cross-platform
library for playing turning audio files into phyiscal vibrations of the air.

```import simpleaudio as sa
import soundfile as sf```

### Read an .mp3 to a Numpy array

```audio_data, samplerate = sf.read(mp3_filename)```

### Write a Numpy array to an .mp3 file.

```sf.write(mp3_filename, audio_data, samplerate)```

### Convert a Numpy array to a string of .mp3-formatted bytes.

```mp3_buf = io.BytesIO()
mp3_buf.name = 'file.mp3'
sf.write(mp3_buf, audio_data, samplerate)
mp3_buf.seek(0)  # Necessary for read() to return all bytes
mp3_bytes = mp3_buf.read()```

An `mp3_buf` name that ends in `.mp3` is important because soundfile
infers file type from the filename extension.

### Convert a string of .mp3-formatted bytes to a Numpy array.

```new_mp3_buf = io.BytesIO(mp3_bytes)
new_mp3_buf.name = 'new_file.mp3'
new_audio_array, new_samplerate = sf.read(new_mp3_buf)```

### Convert a string of bytes to a base64-encoded ASCII string.

```base64_mp3_bytes = base64.b64encode(mp3_bytes)
base64_mp3_string = base64_mp3_bytes.decode("ascii")```

### Convert a base64-encoded ASCII string to a string of bytes.

```new_base64_mp3_bytes = base64_mp3_string.encode("ascii")
new_mp3_bytes = base64.b64decode(new_base64_mp3_bytes)```

### Other file types

soundfile can work with other filetypes in the same way including
.wav, .flac, and .ogg.

### Normalize Numpy data for simpleaudio playback

This ensures that the playback takes advantage of the full range of
the audio playback volume. It doesn't try to push too hard and overdrive,
but it also doesn't leave range unused.
[From the docs](https://simpleaudio.readthedocs.io/en/latest/tutorial.html#using-numpy):

```audio_array = data * 32767 / max(abs(data))
audio_array = audio_array.astype(np.int16)```

### Play audio from a Numpy array

[From the docs](https://simpleaudio.readthedocs.io/en/latest/simpleaudio.html#simpleaudio.play_buffer):

```# simpleaudio.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
play_obj = sa.play_buffer(audio_array, num_channels, 2, samplerate)
play_obj.wait_done()```

