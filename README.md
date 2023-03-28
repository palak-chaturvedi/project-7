# STOCKIFY

## About

## Requirements
1. Python Version 3.10\
1. Django==4.1.6\
    You can run 
```pip install django``` to install .
2. Bootstrap
3. Django Crisy Forms
4. Yahoo Finance API<br>
```pip install yahoo-fin==0.8.9.1```\
```pip install yahoofinance==0.0.2 ```\
```pip install yfinance==0.2.12```

## Flow of files
The code is created using Django framework. 
The paper_trading is the name of the django project which contains multiples app.
The paper_trading subfolder contains the settings.py which contains the settings related to the project.
Such as the django secret key, the authentication apps, allowed apps and host, location of the frontend and the static files.

All the functionalities are divided into respective apps which can be shown using the multiple subfolder such as
> authenticate 
>>(for authentication of users)

>homepage 
>>(for the home page of the main web app)

> simulator 
> >(for simulation of paper trading using virtual money)

> prediction 
> >(for prediction and stock investment calculator whose functionalities can be accessed from the dashboard page)

> stock 
>>(for the calculation of top gainers and top loosers in the market using data scraping and sentimental analysis)

> static 
>>(contains the static files such as the js and css related to the main page)

> blog 
> >(contains the functionality of adding articles by a looged in user, view all the articles and read a particular article)

Each directory does a single functionality which is authenticated in the settings.py.
Each directory consists of variours common subfolder that are
> 1. templates
>> Contains the html files and template tags related to that functionality
> 2. init.py 
>> It is the initialization file required by the django module.
> 3. apps.py
>> It is required to register a django app which can be accessed and merged with other files.
> 4. views.py
> > It contains function definition for all the functionalities in a particular app.
> >> For example, authenticate/views.py contains login, register and other functions.
And the simulator/views.py contains trade, view_history, dashboard, stocktracker funtions.
> 5. urls.py
> > It creates the url related to a particular function. That is when a particular url is accessed it will call a particular function.
> >>For example , when ```\simulator\dashboard``` is accessed it open the dashboard of a particular user.
> 6. models.py
> > It contains the format of the tables that will be stored in the sqllite database.
> 

### Steps to run 
1. Clone the directory
```git clone https://github.com/palak-chaturvedi/project-7```
2. Go to paper_trading directory
```cd project-7/paper_trading```
3. Run the server
```python manage.py runserver```
4. Click on the localhost link
```http://127.0.0.1:8000/```
5. To create a super user and view the accounts.
```python manage.py createsuperuser```
6. And then login in to
```http://127.0.0.1:8000/admin/```

# Note
>To get the real time stock prices of the companies the site calls the yahoo API everytime to register the changes in the portfolio and the profit.
Also the live stock trackers makes call to the direct API.

