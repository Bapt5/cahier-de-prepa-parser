import requests
import bs4
import re
import datetime

class File:

    unit_to_bytes = {
        'ko': 1000,
        'Mo': 1000**3,
        'Go': 1000**6,
        'To': 1000**9,
        'Po': 1000**12,
    }

    def __init__(self, name: str, url: str, infos: str, path, client) -> None:
        # remove forbidden characters
        name = name.replace('/', '_')
        name = name.replace('\\', '_')
        name = name.replace(':', '_')
        name = name.replace('*', '_')
        name = name.replace('?', '_')
        name = name.replace('"', '_')
        name = name.replace('<', '_')
        name = name.replace('>', '_')
        name = name.replace('|', '_')

        self.name: str = name
        self.url: str = url
        self.extension: str = None
        self.date: datetime._Date = None
        self.size: int = None
        self.path = path

        self._client = client

        """
        (pdf, 02/07/2023, 729 ko)
        (pdf, 03/07/2023, 8 Mo)
        """
        # parse infos
        regex = r"\((?P<extension>[^,]+), (?P<date>[0-9]{2}\/[0-9]{2}\/[0-9]{4}), (?P<size>[0-9]+)(.?)(?P<unit>[a-zA-Z]+)\)"
    
        match = re.search(regex, infos)
        if match is None:
            return

        self.extension = match.group('extension') if match.group('extension') != "sans ext" else None

        # add extension to name
        if self.extension and not self.name.endswith(f".{self.extension}"):
            self.name += f".{self.extension}"

        self.date = datetime.datetime.strptime(match.group('date'), "%d/%m/%Y").date() if match.group('date') else None
        
        unit = match.group('unit')
        self.size = int(match.group('size')) * self.unit_to_bytes[unit] if match.group('size') else None

    def download(self, path: str = None) -> str:
        req = self._client._session.get(self.url, stream=True)

        if path is None:
            path = self.name
        else:
            path += f"/{self.name}"

        with open(path, 'wb') as file:
            for chunk in req.iter_content(chunk_size=1024):
                file.write(chunk)
        
        return path

    def __repr__(self) -> str:
        return f"File(name={self.name}, extension={self.extension}, date={self.date}, size={self.size})"

class Folder:

    def __init__(self, name: str, url: str, content: str, path, client) -> None:
        # remove forbidden characters
        name = name.replace('/', '_')
        name = name.replace('\\', '_')
        name = name.replace(':', '_')
        name = name.replace('*', '_')
        name = name.replace('?', '_')
        name = name.replace('"', '_')
        name = name.replace('<', '_')
        name = name.replace('>', '_')
        name = name.replace('|', '_')

        self.name: str = name
        self.url: str = url
        self.nb_files: int = None
        self.nb_folders: int = None
        self.path = path

        self._client = client

        if content is None:
            return
        elif content == "(vide)":
            self.nb_files = 0
            self.nb_folders = 0
        else:
            """
            (6 répertoires, 1 document)
            (1 répertoire)
            (8 documents)
            """
            # parse content
            regex = r"\(((?P<folders>[0-9]+) répertoires?)?(, )?((?P<files>[0-9]+) documents?)?\)"

            match = re.search(regex, content)
            if match is None:
                return

            self.nb_files = int(match.group('files')) if match.group('files') else 0
            self.nb_folders = int(match.group('folders')) if match.group('folders') else 0

    def get_content(self) -> tuple[list['Folder'], list['File']]:
        """Renvoie une liste de dossiers et une liste de fichiers"""
        req = self._client._session.get(self.url)
        soup = bs4.BeautifulSoup(req.text, 'html.parser')

        warning = soup.find('div', {'class': 'warning'})

        if warning is not None:
            raise Exception(warning.text)

        folders_tags = soup.find_all('p', {'class': 'rep'})

        folders = []

        for folder_tag in folders_tags:
            """
            <p class="rep">
                <span class="repcontenu">(2 répertoires)</span>
                <a href="?info">
                    <span class="icon-rep"></span>
                    <span class="nom">Informatique</span>
                </a>
            </p>
            """

            # Si il fait partie des documents récents (<h3>Documents récents</h3> avant)
            if folder_tag.find_previous('h3', text='Documents récents') is not None:
                continue

            folder_name = folder_tag.find('span', {'class': 'nom'}).text
            folder_url = folder_tag.find('a').get('href')
            folder_content = folder_tag.find('span', {'class': 'repcontenu'})

            if folder_content is None:
                folder_content = None
            else:
                folder_content = folder_content.text

            folders.append(
                Folder(
                    folder_name, 
                    f"{self._client.url}/docs{folder_url}", 
                    content=folder_content, 
                    path=self.path + [self],
                    client=self._client))
            
        files_tags = soup.find_all('p', {'class': 'doc'})

        files = []

        for file_tag in files_tags:
            """
            <p class="doc">
                <span class="docdonnees">(pdf, 02/07/2023, 729&nbsp;ko)</span>
                <a href="download?id=1">
                    <span class="icon-doc-pdf"></span>
                    <span class="nom">exos_vac</span>
                </a>
            </p>
            """

            # Si il fait partie des documents récents (<h3>Documents récents</h3> avant)
            if file_tag.find_previous('h3', text='Documents récents') is not None:
                continue

            file_name = file_tag.find('span', {'class': 'nom'}).text
            file_url = file_tag.find('a').get('href')
            file_infos = file_tag.find('span', {'class': 'docdonnees'}).text

            files.append(
                File(
                    file_name, 
                    f"{self._client.url}/{file_url}", 
                    infos=file_infos, 
                    path=self.path + [self],
                    client=self._client))
        
        return folders, files

    def __repr__(self) -> str:
        return f"Folder(name={self.name}, nb_files={self.nb_files}, nb_folders={self.nb_folders})"


class Client:

    def __init__(self, url: str) -> None:
        if url.endswith('/'):
            url = url[:-1]

        self.url: str = url

        self.main_folder: Folder = Folder('Répertoire racine', url + "/docs", content=None, path=[], client=self)

        self._session = requests.Session()

    def authentificate(self, username: str, password: str) -> None:
        self.username: str = username
        self.password: str = password

        req = self._session.post(self.url + '/ajax.php', 
                                 data={"login": username, 
                                       "motdepasse": password,
                                       "permconn": 1, 
                                       "connexion": 1})
        try:
            json = req.json()
        except ValueError:
            return
        else:
            if json['etat'] == 'nok':
                raise Exception(json['message'])