#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
from datetime import date
import rethinkdb as rdb
import jeudelavie as jdv
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from time import localtime, strftime
from flask import Flask, request, redirect, flash, render_template, g, jsonify, abort

RDB_HOST =  os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
TODO_DB = 'partage'

def dbSetup():
    connection = rdb.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        rdb.db_create(TODO_DB).run(connection)
        rdb.db(TODO_DB).table_create('lien').run(connection)
        print 'Database setup completed. Now run the app without --setup.'
    except RqlRuntimeError:
        print 'App database already exists. Run the app without --setup.'
    finally:
        connection.close()

def requet(titre, url, description, categorie):
    rdb.db('partage').table('lien').insert([{ 'titre' : titre, 'url' : url, 'description' : description, 'categorie' : categorie}]).run(g.rdb_conn)
    flash('Task Added')

def delete(id):
    rdb.db('partage').table("lien").get(id).delete().run(g.rdb_conn)
    flash('Lien supprimer')

def modif(titre, url, description, id, categorie):
    rdb.db('partage').table("lien").get(id).update({ 'titre' : titre, 'url' : url, 'description' : description, 'categorie' : categorie}).run(g.rdb_conn)

app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    try:
        g.rdb_conn = rdb.connect(host=RDB_HOST, port=RDB_PORT, db=TODO_DB)
    except RqlDriverError:
        abort(503, "No database connection could be established.")

@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "GET":
        list_lien = list(rdb.table('lien').order_by('titre').run(g.rdb_conn))
        return render_template('index.html', list_lien=list_lien)

    else:
            if request.form["submit"] == "ajouter":
                return render_template('form.html', titre='Ajout de lien', bouton='insert',)

            elif request.form["submit"] == "modifier":
                id = request.form['id']
                titre = request.form['titre']
                lien = request.form['url']
                categorie = request.form['categorie']
                description = request.form['description']
                return render_template('form.html', titre='Modifier un lien', bouton='update', title=titre, url=lien, descr=description, id=id, cat=categorie)

            elif request.form["submit"] == "update":
                id = request.form['id']
                titre = request.form['titre']
                lien = request.form['lien']
                descr = request.form['description']
                categorie = request.form['categorie']
                modif(titre, lien, descr, id, categorie)
                list_lien = list(rdb.table('lien').order_by('titre').run(g.rdb_conn))
                return render_template('index.html', list_lien=list_lien)

            elif request.form["submit"] == "insert":
                titre = request.form['titre']
                lien = request.form['lien']
                descr = request.form['description']
                categorie = request.form['categorie']
                requet(titre, lien, descr, categorie)
                list_lien = list(rdb.table('lien').order_by('titre').run(g.rdb_conn))
                return render_template('index.html', list_lien=list_lien)

            elif request.form["submit"] == "supprimer":
                id = request.form['id']
                delete(id)
                list_lien = list(rdb.table('lien').order_by('titre').run(g.rdb_conn))
                return render_template('index.html', list_lien=list_lien)

            elif request.form["submit"] == "tri":
                categorie = request.form['categorie']
                list_lien = list(rdb.table('lien').filter({'categorie' : categorie}).run(g.rdb_conn))
                return render_template('index.html', list_lien=list_lien, cat=categorie)

@app.route('/Jeudelavie')
def gameoflife():
    return render_template('jeudelavie.html', titre='Game Of Life', jeudelavie=jdv)

if __name__ == '__main__':
    app.secret_key = '\xf8\xff\xbc\xfe\xde\x03\x8b\x81\xc9\x9c\xc4\xbe\x95\xa2\xf2'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
