import pytest

from hobbytrader import github

def test_init_defaults():
    github_object = github.Github()
    assert github_object.owner == 'MapleFrogStudio'
    assert github_object.branch == 'main'

def test__repr():
    github_object = github.Github()
    result = github_object.__repr__()
    assert result == 'MapleFrogStudio -> DATASETS -> main'


def test_github_setup():
    repo = 'DATA-2023-06-02'
    github_object = github.Github(repository=repo)
    assert github_object.repo == repo

def test_url():
    url = 'https://api.github.com/repos/MapleFrogStudio/DATASETS/contents/'
    github_object = github.Github()
    #print(github_object.url)
    assert github_object.url == url

def test_url_path():
    github_object = github.Github()
    url_path = github_object.url_path('DAILY')
    print(url_path)
    assert url_path == 'https://api.github.com/repos/MapleFrogStudio/DATASETS/contents/DAILY'

def test_file_links():
    github_object = github.Github(repository='DATA-2023-06')
    files = github_object.file_links(starts_with='NASDAQ-BM0')
    # print(type(files))
    assert len(files) > 1

def test_files_links_bad_subfolder():
    github_object = github.Github(repository='DATA-2023-06')
    files = github_object.file_links(folder='bad_folder')
    assert len(files) == 0

def test_file_links_without_starts_with():
    github_object = github.Github(repository='DATA-2023-06')
    files = github_object.file_links(starts_with=None)
    assert len(files) >= 0


          