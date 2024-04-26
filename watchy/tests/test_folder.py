import os
import subprocess
from ..folder import (
    create_content_folders,
    get_folder_content,
    delete_content_download_files,
    move_content_file,
)


def test_create_content_folders(tmpdir):
    content_folder = tmpdir.mkdir("Movies")
    content_download_folder = tmpdir.mkdir("Downloads")
    content_title = "The Creator (2023).mp4"

    create_content_folders(content_folder, content_download_folder, content_title)

    assert os.path.isdir(os.path.join(content_folder, content_title))
    assert os.path.isdir(content_download_folder)


def test_get_folder_content(request, tmpdir, monkeypatch):
    content_folder = tmpdir.mkdir("Movies")
    content_files = [
        "The Creator (2023).mp4",
        "Iron Man (2019).avi",
        "Freelancer (2023).mp4",
        "Titanic (1999).dead",
        "The Room (2003).txt",
    ]

    for content_file in content_files:
        content_folder.join(content_file).write("")

    # Fake the change of folder to the content folder
    monkeypatch.chdir(request.fspath.dirname)

    content_files = get_folder_content(content_folder, None)

    assert "The Creator (2023)" in content_files
    assert "Iron Man (2019)" in content_files
    assert "Freelancer (2023)" in content_files
    assert "Titanic (1999)" in content_files
    assert "The Room (2003)" not in content_files


def test_delete_content_download_files(tmpdir):
    content_download_folder = tmpdir.mkdir("Downloads")

    content_download_folder_status = delete_content_download_files(
        content_download_folder
    )

    assert content_download_folder_status == None


def test_move_content_file_movie(tmpdir, monkeypatch):
    download_file = {"title": "The Creator (2023)"}
    content_folder = tmpdir.mkdir("Movies")
    content_download_folder = tmpdir.mkdir("Downloads")
    content_file = "The Creator (2023).mp4"
    content_title = None

    content_download_folder.join(content_file).write("")

    def mock_chmod_check_output(command, **kwargs):
        return b"mock chmod permission change"

    # Fake the change of folder to the content folder
    monkeypatch.setattr(subprocess, "check_output", mock_chmod_check_output)

    return_code = 0
    destination_path = move_content_file(
        download_file,
        str(content_download_folder),
        content_folder,
        content_title,
        return_code,
    )

    assert destination_path == os.path.join(content_folder, content_file)


def test_move_content_file_tv_show(tmpdir, monkeypatch):
    download_file = {"title": "Last Week Tonight With John Oliver S01E01"}
    content_folder = tmpdir.mkdir("TV Shows")
    content_download_folder = tmpdir.mkdir("Downloads")
    content_file = "Last Week Tonight With John Oliver S01E01.mp4"
    content_title = "Last Week Tonight With John Oliver"

    content_download_folder.join(content_file).write("")

    def mock_chmod_check_output(command, **kwargs):
        return b"mock chmod permission change"

    # Fake the change of folder to the content folder
    monkeypatch.setattr(subprocess, "check_output", mock_chmod_check_output)

    return_code = 0
    destination_path = move_content_file(
        download_file,
        str(content_download_folder),
        content_folder,
        content_title,
        return_code,
    )

    assert destination_path == os.path.join(content_folder, content_title, content_file)


def test_move_content_file_download_timeout(tmpdir, monkeypatch):
    download_file = {"title": "The Creator (2023)"}
    content_folder = tmpdir.mkdir("Movies")
    content_download_folder = tmpdir.mkdir("Downloads")
    content_file = "The Creator (2023).timeout"
    content_title = None

    content_download_folder.join(content_file).write("")

    def mock_chmod_check_output(command, **kwargs):
        return b"mock chmod permission change"

    # Fake the change of folder to the content folder
    monkeypatch.setattr(subprocess, "check_output", mock_chmod_check_output)

    return_code = 2
    destination_path = move_content_file(
        download_file,
        str(content_download_folder),
        content_folder,
        content_title,
        return_code,
    )

    assert destination_path == os.path.join(content_folder, content_file)
