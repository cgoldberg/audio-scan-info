import logging
import re
import shutil
from pathlib import Path

import mutagen
import pytest

import audio_info




FILE_EXTENSIONS = ["mp3", "flac"]
SAMPLES_PATH = Path("tests", "sample_files").resolve()
VALID_FILE_STEM = "Artist - Title"
LOG_LEVEL = logging.INFO


def copy_file(filename, path):
    samples_filepath = Path("tests", "sample_files", filename).resolve()
    Path(path / Path(filename).parent).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SAMPLES_PATH / filename, path / filename)
    try:
        audio = mutagen.File(samples_filepath, easy=True)
        assert ORIGINAL_ARTIST_TAG in audio["artist"]
        assert ORIGINAL_TITLE_TAG in audio["title"]
    except mutagen.MutagenError:
        pass


def test_get_metadata_mp3(tmp_path):
    filename = f"{VALID_FILE_STEM}.mp3"
    copy_file(filename, tmp_path)
    filepath = tmp_path / filename
    tags, info = audio_info.get_metadata(filepath)
    assert len(tags) == 2
    assert tags["artist"] == "Test Artist"
    assert tags["title"] == "Test Title"
    assert len(info) == 5
    assert "length" in info
    assert "bitrate" in info
    assert "bitrate mode" in info
    assert "sample rate" in info
    assert "channels" in info


def test_get_metadata_mp3(tmp_path):
    filename = f"{VALID_FILE_STEM}.flac"
    copy_file(filename, tmp_path)
    filepath = tmp_path / filename
    tags, info = audio_info.get_metadata(filepath)
    assert len(tags) == 2
    assert tags["artist"] == "Test Artist"
    assert tags["title"] == "Test Title"
    assert len(info) == 5
    assert "length" in info
    assert "bitrate" in info
    assert "bits per sample" in info
    assert "sample rate" in info
    assert "channels" in info


@pytest.mark.parametrize("file_extension", FILE_EXTENSIONS)
def test_analyze(file_extension, tmp_path, caplog):
    artist = "Artist"
    title = "Title"
    filename = f"{VALID_FILE_STEM}.{file_extension}"
    copy_file(filename, tmp_path)
    filepath = tmp_path / filename
    caplog.set_level(LOG_LEVEL)
    audio_info.analyze_file(filepath)
    #for record in caplog.records:
    #    assert record.levelname == "INFO"
    #assert f"\u27a4  File: {filepath}\n   \u2794 Tags:\n" in caplog.text
    #assert f"     artist: {artist}\n" in caplog.text
    #assert f"     title: {title}\n" in caplog.text


def test_analyze_unknown_file(caplog):
    filename = Path("Unknown - File.mp3")
    caplog.set_level(LOG_LEVEL)
    audio_info.process_file(filename)
    for record in caplog.records:
        assert record.levelname == "ERROR"
    #assert f"\u27a4  File: {filename}\n   \u2717 Error:\n     can't find file\n" in caplog.text


def test_run_filenames(tmp_path, caplog):
    artist = "Artist"
    title = "Title"
    filenames = [f"{VALID_FILE_STEM}.{file_extension}" for file_extension in FILE_EXTENSIONS]
    for filename in filenames:
        copy_file(filename, tmp_path)
    caplog.set_level(LOG_LEVEL)
    audio_info.run(tmp_path, filenames)
    for record in caplog.records:
        assert record.levelname == "INFO"
    #for filepath in (tmp_path / filename for filename in filenames):
    #    assert f"\u27a4  File: {filepath}\n   \u2794 Tags:\n     artist: {artist}\n     title: {title}\n" in caplog.text
    #    audio = mutagen.File(filepath, easy=True)
    #    assert verify_tags_set(audio, artist, title)


def test_run_dir(tmp_path, caplog):
    artist = "Artist"
    title = "Title"
    filenames = [path.relative_to(SAMPLES_PATH) for path in SAMPLES_PATH.rglob("*") if path.is_file()]
    for filename in filenames:
        copy_file(filename, tmp_path)
    caplog.set_level(LOG_LEVEL)
    audio_info.run(tmp_path, [])
    for record in caplog.records:
        assert record.levelname in ("ERROR", "INFO")
    #for filepath in (tmp_path / filename for filename in filenames):
    #    matches = (
    #        f"\u27a4  File: {filepath}\n   \u2794 Tags:\n     artist: {artist}\n     title: {title}\n",
    #        f"\u27a4  File: {filepath}\n   \u2717 Error:",
    #    )
    #    assert any([match in caplog.text for match in matches])
