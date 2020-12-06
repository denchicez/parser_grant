# Парсер сайта [президентскиегранты.рф](https://xn--80afcdbalict6afooklqi5o.xn--p1ai/). 
### Информация о грантах победителях с информацией об размере гранта, кол-во денег перечисленных фондом, вид конкруса, регион получателя гранта, направление, название проекта, рейтинг проекта, дата подачи, срок реализации проекта, наименование организации, инн организации, огрн организации, софинансирование, краткое описание проекта, цель, задачи, социальная значимость, география проекта, целевая группа проекта, адрес организации, веб-сайт, работает ли сайт?, title сайта, description сайта, keywords сайта, сайт принадлежит организации?, ссылки на соц. сети в Instagramm, количество подписчиков VK, ссылки на соц. сети VK, количество подписчиков youtube, ссылки на соц. сети в youtube.
Пример уже обработанных [данных](https://drive.google.com/file/d/1LyJkJqroRLs9q9Lei63puHpweQMNZN9e/view) первых 200 страниц
## Download packages 
```
- sudo apt update
- sudo apt install python3-pip
- pip3 install beautifulsoup4
- pip3 install requests
- pip3 install vk
- pip3 install validators
- pip3 install joblib
```
## Run script
### Script template
##### Script template input
```
python3 <путь до parser.py>
```
##### Script template output
```
Файл - ans.csv
```

### Script simple
##### Script simple input
```
python3 /home/user/test/parser.py
```
##### Script simple output
```
Файл - /home/user/ans.csv
```
