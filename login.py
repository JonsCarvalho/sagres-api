import requests
from bs4 import BeautifulSoup

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