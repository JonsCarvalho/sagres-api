import requests
from bs4 import BeautifulSoup


def sagres_login(username, password):
    data = {}
    with requests.session() as s:

        url = "https://www.prograd.uesc.br/PortalSagres/Acesso.aspx"
        url_default = "https://www.prograd.uesc.br/PortalSagres/Modules/Portal/Default.aspx"
        page = s.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        viewState = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        viewStateGenerator = soup.find(
            'input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        eventValidation = soup.find(
            'input', attrs={'name': '__EVENTVALIDATION'})['value']

        data['__EVENTTARGET'] = ""
        data['__EVENTARGUMENT'] = ""
        data['__VIEWSTATE'] = viewState
        data['__VIEWSTATEGENERATOR'] = viewStateGenerator
        data['__EVENTVALIDATION'] = eventValidation
        data["ctl00$PageContent$LoginPanel$UserName"] = username
        data["ctl00$PageContent$LoginPanel$Password"] = password
        data["ctl00$PageContent$LoginPanel$LoginButton"] = "Entrar"
        page = s.post(url, data=data)

        data_aux = {}
        if(page.url != url_default and page.url != url):
            soup2 = BeautifulSoup(page.content, 'html.parser')

            aspForm = soup2.find(
                'input', attrs={'name': '__aspnetForm_ClientStateInput'})['value']
            vState = soup2.find('input', attrs={'name': '__VSTATE'})['value']
            eventValidation2 = soup2.find(
                'input', attrs={'name': '__EVENTVALIDATION'})['value']

            data_aux['__EVENTTARGET'] = ""
            data_aux['__EVENTARGUMENT'] = ""
            data_aux['__VIEWSTATE'] = vState
            data_aux['__VIEWSTATE'] = ""
            data_aux['__EVENTVALIDATION'] = eventValidation2
            data_aux['ctl00$btnLogin'] = "Acessar o SAGRES Portal"

            page = s.post(page.url, data=data_aux)
            
        return page
