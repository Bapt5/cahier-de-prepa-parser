<p align="center">
  <a href="https://github.com/Bapt5/cahier-de-prepa-parser">
    <img src="https://cahier-de-prepa.fr/favicon.ico" alt="Logo" height="80">
  </a>

  <h3 align="center">cahier-de-prepa-parser</h3>

  <p align="center">
    Python parser pour Cahier de Prépa
    <br />
  </p>
</p>

[![pypi version](https://img.shields.io/pypi/v/cahier-de-prepa-parser.svg)](https://pypi.org/project/cahier-de-prepa-parser/)
[![python version](https://img.shields.io/pypi/pyversions/cahier-de-prepa-parser.svg)](https://pypi.org/project/cahier-de-prepa-parser/)
[![license](https://img.shields.io/pypi/l/cahier-de-prepa-parser.svg)](https://pypi.org/project/cahier-de-prepa-parser/)

## Introduction

C'est un parser python pour Parcoursup qui permet de récupérer les fichiers et dossiers stocké sur Cahier de Prépa. 

## A propos

### Dependances

 - beautifulsoup4
 - requests

### Installation
**Stable**

Intallez directement depuis pypi avec la commande `pip install cahier-de-prepa-parser` (Si vous êtes sous Windows et avez des difficultés avec cette commande, utilisez celle-ci en supposant que vous avez python 3.x.x installé sur votre ordinateur: `py -3 -m pip install cahier-de-prepa-parser`)

**Latest**

Vous pouvez installez la dernière version de la bibliothèque directement depuis Github

`pip install git+https://github.com/Bapt5/cahier-de-prepa-parser`

### Usage

Un programme simple permettant de récupérer tous les voeux et d'en afficher le nom et l'établissement
```python
from cdp_parser import *

client = cdp.Client("https://cahier-de-prepa.fr/votre-classe")

client.authentificate("username", "password")

folders, files = client.main_folder.get_content()
print(folders)
print(files)

```

## Contribution

N'hésitez pas à apporter votre contribution. Toute aide est appréciée. Pour contribuer, veuillez créer un Pull Request avec vos changements.

La configuration de l'environnement de développement consiste simplement à cloner le dépôt et à s'assurer que vous avez toutes les dépendances en
en exécutant `pip install -r requirements.txt`.

## Ajout de fonctionnalités

Parcoursupy couvre les fonctionnalités essentielles, mais si vous avez besoin de quelque chose qui n'est pas encore implémenté, vous pouvez [créer un issue](https://github.com/Bapt5/cahier-de-prepa-parser/issues/new) avec votre demande. (ou vous pouvez contribuer en l'ajoutant vous-même)

## License

Mozilla Public License, version 2.0