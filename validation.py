from bs4 import BeautifulSoup

def sagres_validation(page):
    
    content_sagres = BeautifulSoup(page.content, 'html.parser')


    validation=[]
    instance = {}
    if "A sua tentativa de acesso não foi bem-sucedida." in content_sagres.text:
        instance['status'] = 'erro'
    else:
        instance['status'] = 'sucess'
        
    validation.append(instance)
    
    return validation