import os
from ..folder import create_content_folders, get_folder_content, delete_content_download_files, move_content_file

def test_create_content_folders(tmpdir):
    content_folder = tmpdir.mkdir("Movies")
    content_download_folder = tmpdir.mkdir("Downloads")
    content_title = "The Creator (2023).mp4"

    create_content_folders(content_folder, content_download_folder, content_title)

    assert os.path.isdir(os.path.join(content_folder, content_title))
    assert os.path.isdir(content_download_folder)

def test_get_folder_content(request, tmpdir, monkeypatch):
    content_folder = tmpdir.mkdir("Movies")
    content_files = ["The Creator (2023).mp4", "Iron Man (2019).avi", "Freelancer (2023).mp4", "Titanic (1999).dead", "The Room (2003).txt"]

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

    content_download_folder_status = delete_content_download_files(content_download_folder)
    
    assert content_download_folder_status == None

