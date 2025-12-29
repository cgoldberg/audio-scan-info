import logging
import shutil
from pathlib import Path

import mutagen

import audio_info

SAMPLES_PATH = Path("tests", "sample_files").resolve()
VALID_FILE_STEM = "Artist - Title"
LOG_LEVEL = logging.INFO


def copy_file(filename, path):
    samples_filepath = Path("tests", "sample_files", filename).resolve()
    Path(path / Path(filename).parent).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SAMPLES_PATH / filename, path / filename)
    try:
        audio = mutagen.File(samples_filepath, easy=True)
        assert "Test Artist" in audio["artist"]
        assert "Test Title" in audio["title"]
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
    assert info["length"] == "00:01"
    assert info["bitrate"] == "8 kbps"
    assert info["bitrate mode"] == "CBR"
    assert info["sample rate"] == "8.0 kHz"
    assert info["channels"] == "1"


def test_get_metadata_flac(tmp_path):
    filename = f"{VALID_FILE_STEM}.flac"
    copy_file(filename, tmp_path)
    filepath = tmp_path / filename
    tags, info = audio_info.get_metadata(filepath)
    assert len(tags) == 2
    assert tags["artist"] == "Test Artist"
    assert tags["title"] == "Test Title"
    assert len(info) == 5
    assert info["length"] == "00:01"
    assert info["bitrate"] == "45 kbps"
    assert info["bits per sample"] == "16"
    assert info["sample rate"] == "8.0 kHz"
    assert info["channels"] == "1"


def test_analyze_mp3(tmp_path, caplog):
    filename = f"{VALID_FILE_STEM}.mp3"
    copy_file(filename, tmp_path)
    filepath = tmp_path / filename
    caplog.set_level(LOG_LEVEL)
    audio_info.analyze_file(filepath)
    for record in caplog.records:
        assert record.levelname == "INFO"
    assert f"\u27a4  File: {filepath}\n" in caplog.text
    assert "   \u2794 Info:\n" in caplog.text
    assert "       length: 00:01\n" in caplog.text
    assert "       bitrate: 8 kbps\n" in caplog.text
    assert "       sample rate: 8.0 kHz\n" in caplog.text
    assert "       bitrate mode: CBR\n" in caplog.text
    assert "       channels: 1\n" in caplog.text
    assert "   \u2794 Tags:\n" in caplog.text
    assert "       artist: Test Artist\n" in caplog.text
    assert "       title: Test Title\n" in caplog.text


def test_analyze_flac(tmp_path, caplog):
    filename = f"{VALID_FILE_STEM}.flac"
    copy_file(filename, tmp_path)
    filepath = tmp_path / filename
    caplog.set_level(LOG_LEVEL)
    audio_info.analyze_file(filepath)
    for record in caplog.records:
        assert record.levelname == "INFO"
    assert f"\u27a4  File: {filepath}\n" in caplog.text
    assert "   \u2794 Info:\n" in caplog.text
    assert "       length: 00:01\n" in caplog.text
    assert "       bitrate: 45 kbps\n" in caplog.text
    assert "       bits per sample: 16\n" in caplog.text
    assert "       sample rate: 8.0 kHz\n" in caplog.text
    assert "       channels: 1\n" in caplog.text
    assert "   \u2794 Tags:\n" in caplog.text
    assert "       artist: Test Artist\n" in caplog.text
    assert "       title: Test Title\n" in caplog.text


def test_analyze_unknown_file(caplog):
    filename = Path("Unknown - File.mp3")
    caplog.set_level(LOG_LEVEL)
    audio_info.analyze_file(filename)
    for record in caplog.records:
        assert record.levelname == "ERROR"
    assert f"\u27a4  File: {filename}\n"
    assert "   \u2717 Error:\n     can't find file\n" in caplog.text


def test_run_filenames(tmp_path, caplog):
    filenames = [f"{VALID_FILE_STEM}.{extension}" for extension in ("mp3", "flac")]
    for filename in filenames:
        copy_file(filename, tmp_path)
    caplog.set_level(LOG_LEVEL)
    audio_info.run(tmp_path, filenames)
    for record in caplog.records:
        assert record.levelname == "INFO"
    for filepath in (tmp_path / filename for filename in filenames):
        assert f"\u27a4  File: {filepath}\n"
    assert "   \u2794 Info:\n" in caplog.text
    assert "       length: 00:01\n" in caplog.text
    assert "       bitrate: 45 kbps\n" in caplog.text
    assert "       bits per sample: 16\n" in caplog.text
    assert "       sample rate: 8.0 kHz\n" in caplog.text
    assert "       channels: 1\n" in caplog.text
    assert "   \u2794 Info:\n" in caplog.text
    assert "       length: 00:01\n" in caplog.text
    assert "       bitrate: 8 kbps\n" in caplog.text
    assert "       sample rate: 8.0 kHz\n" in caplog.text
    assert "       bitrate mode: CBR\n" in caplog.text
    assert "       channels: 1\n" in caplog.text
    assert "   \u2794 Tags:\n" in caplog.text
    assert "       artist: Test Artist\n" in caplog.text
    assert "       title: Test Title\n" in caplog.text


def test_run_dir(tmp_path, caplog):
    filenames = [path.relative_to(SAMPLES_PATH) for path in SAMPLES_PATH.rglob("**/*") if path.is_file()]
    num_files = len(filenames)
    for filename in filenames:
        copy_file(filename, tmp_path)
    caplog.set_level(LOG_LEVEL)
    audio_info.run(tmp_path, [])
    for record in caplog.records:
        assert record.levelname in ("ERROR", "INFO")
    temp_files = [tmp_path / filename for filename in filenames]
    assert num_files == len(temp_files)
    for filepath in temp_files:
        assert f"\u27a4  File: {filepath}\n" in caplog.text
