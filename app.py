#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import lxml.html as parser

app = Flask(__name__)

def sagres_login(username, password):
    data = {}
    with requests.session() as s:
        url = "https://www.prograd.uesc.br/PortalSagres/Acesso.aspx"
        page = s.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
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
        page = s.post(url, data=data)

        return page

@app.route('/subjects/', methods=['GET'])
def sagres_subjects():
    
    if request.content_length == None or request.content_length == 0:
        return "É necessário uma requisição com usuário e senha, consulte a documentação da API."
    else:
        page = sagres_login(request.json['username'], request.json['password'])
        
        content_sagres = BeautifulSoup(page.content, 'html.parser')
  
        table = content_sagres.find(class_='meus-horarios-legenda') 

        subjects_list =table.findAll('tr')
        
        subjects=[]

        for index in range (len(subjects_list)): 
            if "".join(subjects_list[index].text.split()) != "" and (":" in subjects_list[index].text) == False:
                instance = {} 
                
                instance['id'] = subjects_list[index].text.replace('\n', '').split(' - ')[0]
                instance['subject'] = subjects_list[index].text.replace('\n', '').split(' - ')[1]
                index += 1
                if ":" in subjects_list[index].text:
                    if "T0" in subjects_list[index].text:
                        instance['class-theoretical'] = "".join(subjects_list[index].text.replace('\n', '').split(' :: ')[0].split())
                        instance['class-theoretical-location'] = subjects_list[index].text.replace('\n', '').split(' :: ')[1]
                    else:
                        instance['class-practice'] = "".join(subjects_list[index].text.replace('\n', '').split(' :: ')[0].split())
                        instance['class-practice-location'] = subjects_list[index].text.replace('\n', '').split(' :: ')[1]
                if ":" in subjects_list[index+1].text:
                    index += 1
                    if "T0" in subjects_list[index].text:
                        instance['class-theoretical'] = "".join(subjects_list[index].text.replace('\n', '').split(' :: ')[0].split())
                        instance['class-theoretical-location'] = subjects_list[index].text.replace('\n', '').split(' :: ')[1]
                    else:
                        instance['class-practice'] = "".join(subjects_list[index].text.replace('\n', '').split(' :: ')[0].split())
                        instance['class-practice-location'] = subjects_list[index].text.replace('\n', '').split(' :: ')[1]
                subjects.append(instance) 

        return jsonify(subjects)

@app.route('/')
def index():
    return "<h1>Bem vindo! Esta é a API do portal acadêmico da UESC</h1>"

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
