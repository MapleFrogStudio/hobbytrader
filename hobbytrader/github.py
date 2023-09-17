import requests
import re

class Github:
    """Utility class to retrieve github info and links"""

    def __init__(self, owner='MapleFrogStudio', repository='DATASETS', branch='main'):
        self.owner = owner
        self.repo  = repository
        self.branch = branch

    def __repr__(self):
        return(f'{self.owner} -> {self.repo} -> {self.branch}')

    @property
    def url(self):
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/'
        return url
    
    def url_path(self, folder='/'):
        if folder == '/' or folder == '' or folder is None:
            return self.url
        
        return self.url+folder


    def file_links(self, folder='/', starts_with=''):
        ''' Return a list of files from  github repo that start_with a specifc string '''
        url = self.url_path(folder=folder)

        content = requests.get(url)
        data = content.json()
        
        if isinstance(data, list):
            if starts_with == '' or starts_with is None:
                raw_urls = [record['download_url'] for record in data if record['type'] == 'file']
            else:
                pattern = pattern = r"^" + starts_with + r".*\.csv$"
                raw_urls = [record['download_url'] for record in data if record['type'] == 'file' and re.match(pattern, record['name'])]

            return raw_urls
        else:
            return []

