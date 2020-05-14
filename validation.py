from bs4 import BeautifulSoup

def sagres_validation(page):
    
    content_sagres = BeautifulSoup(page.content, 'html.parser')


    validation=[]
    instance = {}
    if("A sua tentativa de acesso não foi bem-sucedida." in content_sagres.text or page.url == "https://www.prograd.uesc.br/PortalSagres/Acesso.aspx"):
        instance['status'] = 'erro'
    if(page.url == "https://www.prograd.uesc.br/PortalSagres/Modules/Portal/Default.aspx"):
        instance['status'] = 'sucess'
        
    validation.append(instance)
    
    return validation