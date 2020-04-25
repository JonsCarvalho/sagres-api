#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/login/', methods=['GET'])
def sagres_login():
    
    if request.content_length == None or request.content_length == 0:
        return "É necessário uma requisição com usuário e senha, consulte a documentação da API."
    else:
        username = request.json['username']
        password = request.json['password']

        data = {}

        with requests.session() as s:
            url = "https://www.prograd.uesc.br/PortalSagres/Acesso.aspx"
            r = s.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            
            
            viewState = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
            viewStateGenerator = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
            eventValidation = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
            

            data['__EVENTTARGET'] = ""
            data['__EVENTARGUMENT'] = ""
            data['__VIEWSTATE'] = viewState
            data['__VIEWSTATEGENERATOR'] = viewStateGenerator
            data['__EVENTVALIDATION'] = eventValidation
            data["ctl00$PageContent$LoginPanel$UserName"] = username
            data["ctl00$PageContent$LoginPanel$Password"] = password
            data["ctl00$PageContent$LoginPanel$LoginButton"] = "Entrar"
            r = s.post(url, data=data)
            
            return r.content

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Bem vindo! Esta é a API do portal acadêmico da UESC</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.config['JSON_AS_ASCII'] = False
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
