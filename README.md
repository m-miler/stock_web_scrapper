# Content of Project
* [General info](#general-info)
* [Technologies](#technologies)
* [Environment](#environment)
* [Setup](#setup)

## General Info
Stock Web Scrapper is an application for gathering and storage data concerning stock prices and companies 
basic information. The application also serves an API, to communicate with the future main Home Finance application.

## Technologies
<ul>
<li>Python 3.10</li>
<li>Django 4.14</li>
<li>DjangoRestFramework</li>
<li>Docker</li>
<li>PostgreSQL</li>
<li>Celery</li>
<li>Requests</li>
<li>Selenium</li>
</ul>

## Setup
1. Clone GitHub repository 
``` 
git clone https://github.com/m-miler/stock_web_scrapper.git
```
2. Install docker and docker-compose then run in project file.
```
  docker compose -f .\devOps\docker-compose-dev.yml up -d --build
```

> [!NOTE]
> To add company names and/or indexes to the database, update_company and populate_indexes command 
> from manage.py needs to be triggerd manually inside container using **exec**.  
`docker exec -it <container_id> python manage.py update_company/populate_indexes`