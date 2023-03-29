import json
from time import sleep
import requests
from bs4 import BeautifulSoup


def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0"
		}

    req = requests.get(url, headers)
    
    with open('project.html', 'w') as file:
        file.write(req.text) 

    with open('project.html') as file:
        src = file.read()
    project_data_list = []
    soup = BeautifulSoup(src, 'lxml')
    articles = soup.find(class_='view-content').find_all(class_='views-row')    
    a = 1
    name = f'project{a}'
    projects_urls = []
    for article in articles:
        project_url = 'https://www.towave.ru' + article.find('span', class_='field-content').find('a').get('href')
       
        projects_urls.append(project_url)
       
   
    for project_url in projects_urls:

        req = requests.get(project_url)
        try:
            project_name = project_url.split('/')[-1].split('.')[-2] 
        except Exception:
            project_name = ""
        a += 1    
        with open(f"data/{project_name}.html", 'w') as file:
            file.write(req.text) 

        with open(f"data/{project_name}.html") as file:
            src = file.read()
        project_about_info = ''
        soup = BeautifulSoup(src, 'lxml')
        project_data = soup.find('div', class_='node-startups') 

        try:
            project_logo = project_data.find('div', class_='odd').find('img').get('src') 
        except Exception:
            project_logo = 'No project logo'
        try:   
            project_title = project_data.find('div', class_='odd').find('img').get('alt')
        except Exception:
            project_title = "No name project"
        try:
            project_link = project_data.find('div', class_='field-field-startup-link').find('a').get('href')
        except Exception:
            project_link = 'No link project'
        try:    
            project_about = project_data.find('div', class_='content').find_all('p')
            for item in project_about:
                project_about_info += item.text
        except Exception:
            project_about_info = "NO PROJECT INFO"
        
        project_data_list.append(
            {
            "Имя проекта:": project_title,
            "Логотип:": project_logo,
            "Ссылка на сайт:": project_link,
            "Описание проекта:": project_about_info
            }
        )
    with open("data/project_data.json", "a", encoding="utf-8") as file:
        json.dump(project_data_list, file, indent=4, ensure_ascii=False)
    

for i in range(1, 71):
   
    get_data(f'https://www.towave.ru/start?page={i}') 
    print(f"Делаю {i} страницу...")       
    sleep(1)