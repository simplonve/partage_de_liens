#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
from datetime import date
from time import localtime, strftime
from flask import Flask, request, redirect, flash, render_template, g, jsonify, abort

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == "GET":
		return render_template('index.html')

	else:
			if request.form["submit"] == "ajouter":
				return render_template('form.html', titre='Ajout de lien', bouton='insert')

			elif request.form["submit"] == "modifier":
				return render_template('form.html', titre='Modifier un lien', bouton='update')

			elif request.form["submit"] == "update":
				return render_template('index.html')

			elif request.form["submit"] == "insert":
				return render_template('index.html')

			elif request.form["submit"] == "supprimer":
				return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
