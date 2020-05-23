# FSci Qualification Framework (QF) Project
[![Python Version](https://img.shields.io/badge/python-3.6.8-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.0.4-brightgreen.svg)](https://djangoproject.com)

This project is parts of CSS321 and CSS322 Software Engineering subjects, which cooperate with Faculty of Science of King Mongkut's University of Technology Thonburi (KMUTT).
## Installation
1. Clone this repository to location that you want.
```bash
git clone https://github.com/WayneSkywalker/QFSci.git
```
2. Install python environment called 'pipenv'
```bash
pip install pipenv
```
3. Create python environment at your root project location.
```bash
pipenv shell
```
4. Install all libraries required
```bash
pipenv install
```
## Usage
### first time usage 
1. Open your python environment that was created at your root project location.
```bash
pipenv shell
```
2. move to QFSci folder
```bash
cd qfsci
```
3. then, check if manage.py exists.
```bash
dir
```
you will see...
```bash
05/22/2020  04:48 PM    <DIR>          .
05/22/2020  04:48 PM    <DIR>          ..
03/08/2020  10:00 AM               646 manage.py
03/08/2020  10:00 AM    <DIR>          QFSci
05/04/2020  07:57 PM    <DIR>          qfsci_manager
               1 File(s)            646 bytes
               4 Dir(s)  911,458,639,872 bytes free
```
4. setup database using these commands
```bash
python manage.py makemigrations
python manage.py migrate
```
5. To run server, run this command...
```bash
python manage.py runserver
```

### Non-first time usage
1. Open your python environment that was created at your root project location.
```bash
pipenv shell
```
2. Run this command...
```bash
cd qfsci
```
3. To run server, run this command...
```bash
python manage.py runserver
```
4. To query in python shell, run this command...
```bash
python manage.py shell
```
## License
The source code is released under the _________ License.