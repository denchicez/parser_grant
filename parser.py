from bs4 import BeautifulSoup
import vk
import requests
import csv
import sys
import validators
import urllib.request
import json
import time
URL = 'https://xn--80afcdbalict6afooklqi5o.xn--p1ai/public/application/cards?SearchString=&Statuses%5B0%5D.Selected=true&Statuses%5B0%5D.Name=%D0%BF%D0%BE%D0%B1%D0%B5%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8C+%D0%BA%D0%BE%D0%BD%D0%BA%D1%83%D1%80%D1%81%D0%B0'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://xn--80afcdbalict6afooklqi5o.xn--p1ai/'
FILE = 'ans.csv'

def get_html(url,params=None): # делаем запрос на html страничку
    try:
        r = requests.get(url, headers=HEADERS, params=params)
        return r
    except:
        print('ЭКСТРЕННОЕ СОХРАНЕНИЕ')
        file_saving()
        sys.exit()
def getVariantsOfWords(word): # получаем слово в нормальной кодировке]
    trans = '[]{}0123456789.,!@\"#№;$%^:&?*()\'\\/|' # 'плохие' символы
    for c in trans:
        word = word.replace(c, '') # убираем их
    small = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    big = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    enSmall = 'abcdefghijklmnopqrstuvwxyz'
    enBig = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphaToSmall = {}
    alphaToBig = {}
    for i in range(len(big)):
        alphaToSmall[big[i]] = small[i]
        alphaToBig[small[i]] = big[i]
    for i in range(len(enBig)):
        alphaToSmall[enBig[i]] = enSmall[i]
        alphaToBig[enSmall[i]] = enBig[i]    
    res = ''
    words = []
    for c in word:
        if (alphaToSmall.get(c) != None):
            res = res + alphaToSmall.get(c)
        else:
            res = res + c
    words.append(res)
    if (len(res) > 0 and alphaToBig.get(res[0]) != None):
        res = alphaToBig.get(res[0]) + res[1:]
    words.append(res)
    res = ''
    for c in word:
        if (alphaToBig.get(c) != None):
            res = res + alphaToBig.get(c)
        else:
            res = res + c
    words.append(res)
    return words # возвращаем маленькими, с большой, большие
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('li', class_='pagination__item')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
def NameCheck(string,code1,code2): #Можно ли расшифровать stirng с помощью code1 и code2
    letters = ['“','…','”','<','>','«','»',chr(9),chr(13),chr(10),'(',')','|',':',' ',chr(34),'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','а','a','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я','-','+',',','.','/','[',']','1','2','3','4','5','6','7','8','9','0','#','№','-','—','_','=','}','{','+','!','?','#']
    try:
        string=string.encode(code1).decode(code2) #декодируем если можно
    except:
        return False # выходим
    try:
        string=string.lower() # пытаемся сделать нижний регистр
    except:
        string=string
    for delite_symbole in letters: #удаляем символы
        string=string.replace(delite_symbole,'')
    if(len(string)>2): #Если длина остатков больше 2 выходим
        return False
    else:
        return True #все верно
def get_true_followers(s):
    s=str(s)
    s = s.replace(',', '.')
    s = s.replace(chr(160), ' ')
    if (s.find('млн подписчиков') != -1):
        s = s.replace(' млн подписчиков', '')
        return int(float(s) * 1000000)
    if (s.find(' тыс. подписчиков') != -1):
        s = s.replace(' тыс. подписчиков', '')
        return int(float(s) * 1000)
    s = s.replace(' подписчиков', '')
    s = s.replace(' подписчика', '')
    s = s.replace(' подписчик', '')   
    try:
        return int(float(s))
    except:
        return 0
def get_links_from_page(url):
    links = set()
    try:
        resp = urllib.request.urlopen(url)
        soup = BeautifulSoup(resp, 'html.parser')
    except:
        return links
    try:
        for link in soup.find_all('a', href=True):
            links.add(link['href'])
    except:
        return links
    return links
def VKFollowers(url_name):
    if(url_name.find('public')!=-1):
        try:
            id_of_group=(url_name[21:])
            podpisota = vk_api.groups.getMembers(group_id=id_of_group, v=5.92)['count']
        except:
            podpisota=0
    elif(url_name.find('club')!=-1):
        try:
            id_of_group=(url_name[19:])
            podpisota = vk_api.groups.getMembers(group_id=id_of_group, v=5.92)['count']
        except:
            podpisota=0
    else:
        try:
            id_of_group=url_name[15:]
            podpisota = vk_api.groups.getMembers(group_id=id_of_group, v=5.92)['count']
        except:
            podpisota=0
    return podpisota
def InstFollowers(url_name):
    try:
        url_name=url_name+'?__a=1'
        HTML2=get_html(url_name).text
        data = json.loads(HTML2)
        return(data['graphql']['user']['edge_followed_by']['count'])
    except:
        return 0
def find_number_youtube(index,string): # ищем следующее число после строки
    KolKov=0
    stroka=''
    for i in range(index,len(string)):
        if(string[i]==chr(34)):
            KolKov+=1
        if(KolKov==5):
            break
        if(KolKov==4 and string[i]!=chr(34)):
            stroka=stroka+string[i]
    return stroka
def YoutubeFollowers(url):
    try:
        HTML_youtube=get_html(url).text
        soup_youtube=str(BeautifulSoup(HTML_youtube,'html.parser'))
        ind = soup_youtube.find('subscriberCountText')
        if(ind==-1):
            return 0
        else:
            return (find_number_youtube(ind,soup_youtube))
    except:
        return 0
def get_social_links(links):
    prefixes = [['https://www.youtube.com/channel/','http://www.youtube.com/', 'https://www.youtube.com/user/','https://www.youtube.com/c/'], ['https://vk.com/'], ['https://www.instagram.com/']]
    youtube = []
    youtube_links=set()
    vk = []
    vk_links=set()
    inst = []
    inst_links=set()
    youtube_count=0
    vk_count=0
    inst_count=0
    for link in links:
        for i in range(len(prefixes)):
            val = ''
            for media in prefixes[i]:
                if (link.find(media) != -1):
                    val = link
            if(len(val)!=0):
                if(i==0):
                    youtube_links.add(link)
                    youtube.append(val)
                if(i==1):
                    vk_links.add(link)
                    vk.append(val)
                if(i==2):
                    inst_links.add(link)
                    inst.append(val)
    if (len(youtube) != 0):
        val = -1
        for link in youtube:
            follow = get_true_followers(YoutubeFollowers(link))
            if (follow > val):
                val = follow
        youtube_count = val
    if (len(vk) != 0):
        val = -1
        for link in vk:
            follow = VKFollowers(link)
            if (follow > val):
                val = follow
        vk_count=val
    if (len(inst) != 0):
        val = -1
        for link in inst:
            follow = InstFollowers(link) 
            if (follow > val):
                val = follow
        inst_count = val
    return youtube_count,vk_count,inst_count,youtube_links,vk_links,inst_links  
def file_saving():
    with open(FILE, 'w', newline="",errors='ignore') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['размер гранта','перечислено фондом','конкурс','регион получателя гранта','направление','название проекта','рейтинг проекта','номер заявки','дата подачи','срок реализации','организация','инн орагнизации','огрн организации','софинансирование','краткое описание','цель','задачи','социальная значимость','география проекта','целевая группа проекта','адрес организации','веб-сайт организации','Работает ли сайт?','title сайта организации','description сайта организации','keywords сайта организации','Cайт принадлежит организации?','Количество подписчиков Instagramm','Ссылки на соц. сети в Instagramm','Количество подписчиков VK','Ссылки на соц. сети в VK','Количество подписчиков youtube','Ссылки на соц. сети в youtube'])
        for grant in all_grants:
            writer.writerow([grant['размер гранта'],grant['перечислено фондом'],grant['конкурс'],grant['регион получателя гранта'],grant['направление'],grant['название проекта'],grant['рейтинг проекта'],grant['номер заявки'],grant['дата подачи'],grant['срок реализации'],grant['организация'],grant['инн орагнизации'],grant['огрн организации'],grant['софинансирование'],grant['краткое описание'],grant['цель'],grant['задачи'],grant['социальная значимость'],grant['география проекта'],grant['целевая группа проекта'],grant['адрес организации'],grant['веб-сайт организации'],grant['Работает ли сайт?'],grant['title сайта организации'],grant['description сайта организации'],grant['keywords сайта организации'],grant['Cайт принадлежит организации?'],grant['Количество подписчиков Instagramm'],grant['Ссылки на соц. сети в Instagramm'],grant['Количество подписчиков VK'],grant['Ссылки на соц. сети в VK'],grant['Количество подписчиков youtube'],grant['Ссылки на соц. сети в youtube']])
def urlChecker(url): #работает ли сайт?
    try:
        if not validators.url(url):
            return False
    except:
        return False
    try:
        r = requests.head(url)
        return r.status_code == 200
    except:
        return False
def decode(string):
    all_code = ['UTF-8','cp1251','latin1'] #возможные виды кодировок
    chk=0
    for code_in_all1 in all_code:
        for code_in_all2 in all_code:
            if(NameCheck(string,code_in_all1,code_in_all2)==True):
                code1=code_in_all1
                code2=code_in_all2
                chk=1
                break
        if(chk==1): #если нашлась кодировка 
            string=string.encode(code1).decode(code2) #декодируем
            return string,code1,code2
    return 'У сайта неизвестная кодировка','UTF-8', 'UTF-8'
def is_site_correct(html_str, all_names,code1,code2):
    allwords=getVariantsOfWords(all_names)
    for name in allwords:
        trans = '[]{}0123456789.,!@\"#№;$%^:&?*()\'\\/|' # 'плохие' символы
        for c in trans:
            name = name.replace(c, '') # убираем их
        try:
            name=name.encode(code2).decode(code1) #кодируем в кодировку сайта
        except:
            return False
        words = name.split() # делим на слова
        buff = []
        for word in words:
            if (len(word) > 2):
                buff.append(word) # удаляем короткие, добовляем хорошие
        words = buff
        try:
            for word in words:
                if html_str.find(word) != -1: # ищем
                    return True
        except:
            return False
    return False
def get_content_from_main(html):
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find('div',class_='table table--p-present table--projects')
    items=cards.find_all('a')
    URL = 'https://xn--80afcdbalict6afooklqi5o.xn--p1ai'
    for item in items:
        if(item!=None):
            project_price=item.find('div',class_='projects__price').text                             #размер гранта
            fond_invest=item.find('span',class_='projects__str-no-wrap').text                        #перечислено фондом
            contest=item.find('div',class_='contest').text                                           #конкурс
            region=(item.find('div',class_='projects__descr')).find('div').text                      #регион получателя гранта
            direction=item.find('div',class_='direction').text                                       #направление
            title=item.find('div',class_='projects__title').text                                     #название проекта
            ####################################################################
            url_item = URL+item.get('href')
            url_item = url_item.strip()
            html_item = (get_html(url_item)).text
            soup_item = BeautifulSoup(html_item, 'html.parser')
            all_data = soup_item.find_all('li',class_='winner-info__list-item')
            ####################################################################
            rating = all_data[2].find('span',class_='winner-info__list-item-text').text              # рейтинг проекта
            number_request = all_data[3].find('span',class_='winner-info__list-item-text').text      # номер заявки
            date_request = all_data[4].find('span',class_='winner-info__list-item-text').text        # дата подачи
            date_realization = all_data[5].find('span',class_='winner-info__list-item-text').text    # срок реализации
            oranization = all_data[6].find('span',class_='winner-info__list-item-text').text         # организация
            inn = all_data[7].find('span',class_='winner-info__list-item-text').text                 # инн орагнизации
            orgn = all_data[8].find('span',class_='winner-info__list-item-text').text                # огрн орнанизации
            sofinance = soup_item.find_all('span',class_='circle-bar__info-item-number')[1].text     # софинансирование
            #дополнительная инфа
            all_dop_data=soup_item.find_all('div',class_='winner__details-box js-ancor-box')
            winner_summary=all_dop_data[0].text                                                      # краткое описание
            winner_aim=all_dop_data[1].text                                                          # цель
            winner_tasks=all_dop_data[2].text                                                        # задачи
            winner_social=all_dop_data[3].text                                                       # социальная значимость 
            winner_geo=all_dop_data[4].text                                                          # география проекта
            winner_target=all_dop_data[5].text                                                       # целевая группа проекта
            winner_contacts=all_dop_data[6]                                                          # контакты организации
            winner_adress=winner_contacts.find('span',class_='winner__details-contacts-item').text   # адрес организации  
            try:
                winner_site=winner_contacts.find('a',class_='winner__details-contacts-item winner__details-contacts-item--link').get('href') #ccылка на веб-сайт
            except:
                winner_site='Нет'#ccылка на веб-сайт
            #################################
            try:
                if(winner_site==None or winner_site=='Нет'):
                    site_is_work=False
                else:
                    if(urlChecker(winner_site)==False):    
                        if(winner_site[:4]!='http'):
                            winner_site='http://'+winner_site
                        site_is_work=urlChecker(winner_site)
                        if(site_is_work==False):
                            if(winner_site[:5]=='http:'):
                                winner_site= 'https'+winner_site[4-(len(winner_site)):]
                                site_is_work=urlChecker(winner_site)
                    else:
                        site_is_work=True
            except:
                site_is_work=False
                
            podpis_inst='Нет аккаунта'
            podpis_vk='Нет аккаунта'
            podpis_youtube='Нет аккаунта'
            links_youtube='Нет аккаунта'
            links_vk='Нет аккаунта'
            links_inst='Нет аккаунта'
            #парсинг title, keywords, description           
            if(site_is_work==True):
                HTML2=get_html(winner_site).text
                soup2=BeautifulSoup(HTML2,'html.parser') 
                all_code = ['UTF-8','cp1251','latin1'] #возможные виды кодировок
                try:
                    title_org_site=(soup2.find('title')).text #title с кодировкой сайта 
                    title_org_site,code1,code2 = decode(title_org_site)
                    site_correct=is_site_correct(winner_site,oranization,code1,code2)
                except:
                    code1='UTF-8'
                    code2='UTF-8'
                    title_org_site='Не найдено' 
                    site_correct='False'
                if(title_org_site!='У сайта неизвестная кодировка' and title_org_site!='Не найдено'):
                    #парсинг description сайта c декодировкой
                    podpis_youtube,podpis_vk,podpis_inst, youtubes,vks,insts=social_links=get_social_links(get_links_from_page(winner_site))
                    if(podpis_youtube==0):
                        podpis_youtube='Нет аккаунта'
                    else:
                        links_youtube=youtubes 
                    if(podpis_vk==0):
                        podpis_vk='Нет аккаунта'
                    else:
                        links_vk=vks 
                    if(podpis_inst==0):
                        podpis_inst='Нет аккаунта'
                    else:
                        links_inst=insts
                    try:
                        description_org_site=soup2.find(attrs={"name":"description"})
                        description_org_site=str(description_org_site)
                        description_org_site=BeautifulSoup(description_org_site, 'html.parser')
                        description_org_site=description_org_site.meta['content']
                        description_org_site=description_org_site.encode(code1).decode(code2)
                    except:
                        description_org_site='Не найдено'
                    if(description_org_site==''):
                        description_org_site='Отсутсвует'
                    #парсинг keywords сайта c декодировкой
                    try:
                       keywords_org_site=soup2.find(attrs={"name":"keywords"})
                       keywords_org_site=str(keywords_org_site)
                       keywords_org_site = BeautifulSoup(keywords_org_site, 'html.parser')
                       keywords_org_site=keywords_org_site.meta['content']
                       keywords_org_site=keywords_org_site.encode(code1).decode(code2)
                    except:
                        keywords_org_site='Не найдено'
                    if(keywords_org_site==''):
                        keywords_org_site='Отсутсвует'
                    site_correct=is_site_correct(HTML2,oranization,code1,code2)
                        
                #неизвестная кодировка сайта
                else:
                    site_correct='False'
                    title_org_site='Cайт не работает или не существует'
                    description_org_site='У сайта неизвестная кодировка'
                    keywords_org_site='У сайта неизвестная кодировка'
            else:
                site_correct='False'
                title_org_site='Cайт не работает или не существует'
                description_org_site='Cайт не работает или не существует'
                keywords_org_site='Cайт не работает или не существует'
            #################################
            all_grants.append({
                'размер гранта' : project_price,
                'перечислено фондом': fond_invest,
                'конкурс':contest,
                'регион получателя гранта':region,
                'направление':direction,
                'название проекта':title,
                'рейтинг проекта':rating,
                'номер заявки':number_request,
                'дата подачи':date_request,
                'срок реализации':date_realization,
                'организация':oranization,
                'инн орагнизации':inn,
                'огрн организации':orgn,
                'софинансирование':sofinance,
                'краткое описание':winner_summary,
                'цель':winner_aim,
                'задачи':winner_tasks,
                'социальная значимость':winner_social,
                'география проекта':winner_geo,
                'целевая группа проекта':winner_target,
                'адрес организации':winner_adress,
                'веб-сайт организации':winner_site,
                'Работает ли сайт?':site_is_work,
                'title сайта организации': title_org_site,           
                'description сайта организации': description_org_site,
                'keywords сайта организации': keywords_org_site,
                'Cайт принадлежит организации?': site_correct,
                'Количество подписчиков Instagramm': podpis_inst,
                'Ссылки на соц. сети в Instagramm': links_inst, #
                'Количество подписчиков VK': podpis_vk,
                'Ссылки на соц. сети в VK': links_vk, #
                'Количество подписчиков youtube': podpis_youtube,
                'Ссылки на соц. сети в youtube': links_youtube, #           
            })
def parse(URL):
    URL = URL.strip()
    try:
        URL_COUNT='https://xn--80afcdbalict6afooklqi5o.xn--p1ai/public/application/cards?SearchString=&Statuses%5B0%5D.Selected=true&Statuses%5B0%5D.Name=%D0%BF%D0%BE%D0%B1%D0%B5%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8C+%D0%BA%D0%BE%D0%BD%D0%BA%D1%83%D1%80%D1%81%D0%B0&&page=501'
        URL_COUNT = URL_COUNT.strip()
        html = get_html(URL_COUNT)
        pages_count = get_pages_count(html.text)
    except:
        URL_COUNT='https://xn--80afcdbalict6afooklqi5o.xn--p1ai/public/application/cards?SearchString=&Statuses%5B0%5D.Selected=true&Statuses%5B0%5D.Name=%D0%BF%D0%BE%D0%B1%D0%B5%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8C+%D0%BA%D0%BE%D0%BD%D0%BA%D1%83%D1%80%D1%81%D0%B0'
        URL_COUNT = URL_COUNT.strip()
        html = get_html(URL_COUNT)
        pages_count = get_pages_count(html.text)        
    for page in range(1,pages_count+1): #pages_count
        print(f'Парсинг страницы {page} из {pages_count}...')
        html=get_html(URL, params={'page': page})
        get_content_from_main(html.text)
start_time = time.time()
token = "3fb7074e3fb7074e3fb7074e373fc20ea433fb73fb7074e6000a2640396190c4d381005"  # Сервисный ключ доступа
session = vk.Session(access_token=token)
vk_api = vk.API(session)
all_grants=[]
parse(URL)
file_saving()
print("--- %s seconds ---" % (time.time() - start_time)) 
