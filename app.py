#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import login
import timetable
import subjects
import validation

app = Flask(__name__)

@app.route('/subjects/', methods=['POST'])
def route_subjects():
    
    if request.content_length == None or request.content_length == 0:
        return "É necessário uma requisição com usuário e senha, consulte a documentação da API."
    else:
        page = login.sagres_login(request.json['username'], request.json['password'])

        return jsonify(subjects.sagres_subjects(page))

@app.route('/timetable/', methods=['POST'])
def route_timetable():

    if request.content_length == None or request.content_length == 0:
        return "É necessário uma requisição com usuário e senha, consulte a documentação da API."
    else:
        page = login.sagres_login(request.json['username'], request.json['password'])
        
        return jsonify(timetable.sagres_timetable(page))

@app.route('/all/', methods=['POST'])
def route_all():
    
    if request.content_length == None or request.content_length == 0:
        return "É necessário uma requisição com usuário e senha, consulte a documentação da API."
    else:
        page = login.sagres_login(request.json['username'], request.json['password'])
        
        all_json = []
        instance = {}

        instance['timetable'] = timetable.sagres_timetable(page)
        instance['subjects'] = subjects.sagres_subjects(page)

        all_json.append(instance)
        
        return jsonify(all_json)

@app.route('/validation/', methods=['POST'])
def route_validation():
    
    if request.content_length == None or request.content_length == 0:
        return "É necessário uma requisição com usuário e senha, consulte a documentação da API."
    else:
        page = login.sagres_login(request.json['username'], request.json['password'])

        return jsonify(validation.sagres_validation(page))

@app.route('/')
def index():
    return "<h1>Bem vindo! Esta é a API do portal acadêmico da UESC</h1>"

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
