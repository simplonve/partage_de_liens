#Flask
est un framework (équivalent à sinatra pour ruby) pour un serveur web qui fonctionne avec Python.
#Dépendances
pour l'installer vous aurez besoin des librairies de Python.
**Sous Linux** installer les dépendances avec ces commandes :
`$ sudo apt-get install python python-pip` et 
`$ sudo pip install flask`
#Premiers pas
Vous créer un dossier pour votre projet, puis y rajouter un fichier main.py (ou foo.py), l'éditer comme suit :
```python
#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello !"


if __name__ == '__main__':
    app.run(debug=True)

```
Si vous vous rendez sur le chemin du dossier et que vous exécutez avec la commande `python main.py` pour lancer le serveur,
rendez-vous à l'adresse <a href="http://localhost:5000/">http://localhost:5000/</a> et vous aurez un "Hello!".
Ligne 4, on importe la classe Flask depuis le module flask, et on s’en sert ligne 5 pour instancier l’objet app. 
Cet objet est fondamental. Lors de l’instanciation de app, vous noterez qu’on lui passe en paramètre __name__ (qui vaut '__main__' dans ce cas). 
Ce paramètre est utile lorsque l’on a plusieurs applications WSGI.
Voyons maintenant la fin du code : ligne 12, on lance notre application en mode debug, qui nous aidera à détecter les erreurs dans notre code.
ne autre manière d'activer le mode debug aurait été d'écrire
```python
app.debug = True
```
Cela revient au même : l'objet app est configurable. On peut par exemple lui configurer sa clé secrète (qui sera indispensable 
pour sécuriser les sessions des visiteurs, mais nous n'en sommes pas encore là). Il suffit de faire :

`app.secret_key = '2d9-E2.)f&é,A$p@fpa+zSU03êû9_`

Faites cela de votre côté et gardez votre clé bien secrète.
à la ligne 12 de notre code. Lorsque l'on appelle la méthode run() de app, 
le serveur HTTP + WSGI de Flask est automatiquement lancé. 
Le coeur du code, c’est la fonction index, c’est elle qui se charge de renvoyer “Hello !”.
’on a décoré cette fonction avec le décorateur @app.route qui prend en paramètre une route. 
Cette route est celle par laquelle notre fonction sera accessible.
Dans le jargon, pour désigner une fonction qui renvoie une page web, on utilise le mot vue.
Par conséquent, chaque fonction décorée par @app.route est une vue.`
(Ici ce fichier correspond au fichier app.rb dans sinatra). 


