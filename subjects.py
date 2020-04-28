from bs4 import BeautifulSoup

def sagres_subjects(page):
    
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
            else:
                if "T0" in subjects_list[index].text:
                    instance['class-practice'] = ""
                    instance['class-practice-location'] = ""
                else:
                    instance['class-theoretical'] = ""
                    instance['class-theoretical-location'] = ""
                    
            subjects.append(instance) 

    return subjects