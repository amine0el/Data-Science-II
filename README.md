# Data-Science-II

first you should have an envirement. if you work with pycharm is already initialt. with VScode run this code

```
python -m venv .env
```
In VS Code, open the Command Palette (View > Command Palette or (⇧⌘P)). Then select the Python: Select Interpreter command

---
to install the Packeges required run this code im Terminal or CMD

```
pip install -r requirement.txt
```
---
to init the django app

change the directory to Web Application in the Terminal

```
cd Web\ Application/
```
and run this commands
```
python manage.py runserver
```

###### if webserver shows an Error: "no such column: mgcapp_document.name"
1. Delete db.sqlite3 in "Web Application" Folder and 001_init.py in "migrations" Folder
2. Go To Folder "Web Application"
3. run "python manage.py makemigrations"
4. run "python manage.py migrate"


data/genres_original/jazz/jazz.00054.wav hat ein fehler