# audio-info

### Show metadata, tags, and stream information for audio files (MP3, FLAC)

---

[![Supported Python Versions](https://img.shields.io/pypi/pyversions/audio-info)](https://pypi.org/project/audio-info)

- Copyright (c) 2025 [Corey Goldberg][github-home]
- Development: [GitHub][github-repo]
- Download/Install: [PyPI][pypi-audio-info]
- License: [MIT][mit-license]

----

## About:

`audio_info` is a Python CLI program that shows metadata, tags, and stream
information from MP3 and FLAC audio files. It can be used on individual files
or a library of files.

MP3 information:
- ID3 tags
- APEv2 tags
- length
- bitrate
- sample rate
- bitrate mode
- channels
- track gain
- track peak
- album gain

FLAC information:
- FLAC tags (Vorbis comment block)
- length
- bitrate
- bits per sample
- sample rate
- channels
- check for existense of embedded pictures, cuesheets, and seek table

## Requirements:

- Python 3.12+

## Installation:

Install from [PyPI][pypi-audio-info]:

```
pip install audio-info
```

## CLI Options:

- If filenames are given as command-line options, it will only process those files
- If no filename is specified, it will process all files (recursively) in the current directory
- A different directory can be specified using the `--dir` option

```
usage: audio_info [-h] [-d DIR] [filename ...]

positional arguments:
  filename       [optional] file to process (multiple allowed)

options:
  -h, --help     show this help message and exit
  -d, --dir DIR  start directory
```

## Usage Examples:

#### Install from PyPI with pipx:

```
pipx install audio-info
```

#### Show information from a single file:

```
audio_info "Some Artist - Some Title.mp3"
```

#### Show information from all files in current directory (recurse subdirectories):

```
audio_info
```

#### Show information from all files in a directory (recurse subdirectories):

```
audio_info --clean --dir=/path/to/files
```

[github-home]: https://github.com/cgoldberg
[github-repo]: https://github.com/cgoldberg/audio-info
[pypi-audio-info]: https://pypi.org/project/audio-info
[mit-license]: https://raw.githubusercontent.com/cgoldberg/audio-info/refs/heads/main/LICENSE
