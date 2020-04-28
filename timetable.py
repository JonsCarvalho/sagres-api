from bs4 import BeautifulSoup

def sagres_timetable(page):
    
    content_sagres = BeautifulSoup(page.content, 'html.parser')

    table = content_sagres.find(class_='meus-horarios') 

    timetable_list =table.findAll('td')
    
    timetable=[]

    days=['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB', 'DOM']

    for index in range (len(timetable_list)): 
        instance = {}
        if ":" in timetable_list[index].text:
            indexDays = 0
            chunks, chunk_size = len(timetable_list[index].text.replace('\n', '')), len(timetable_list[index].text.replace('\n', ''))//2
            instance['start-time'] = [ timetable_list[index].text.replace('\n', '')[i:i+chunk_size] for i in range(0, chunks, chunk_size) ][0]
            instance['end-time'] = [ timetable_list[index].text.replace('\n', '')[i:i+chunk_size] for i in range(0, chunks, chunk_size) ][1]
            
            index +=1

            for i in range(7):
                if len(timetable_list[index].text.replace('\n', '')) < 5:
                    instance[days[indexDays]] = ''
                    indexDays += 1
                    index += 1
                else:
                    instance[days[indexDays]] = [ timetable_list[index].text.replace('\n', '')[i:i+6] for i in range(0, 9, 6) ][0] +'-'+ [ timetable_list[index].text.replace('\n', '')[i:i+6] for i in range(0, 9, 6) ][1]
                    indexDays += 1
                    index += 1

            timetable.append(instance)

    return timetable