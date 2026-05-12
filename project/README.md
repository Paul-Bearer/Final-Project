# Final Project
## Description

My final project is a basic funeral management database built for funeral homes with multiple locations with multiple employees.The purpose of this application is to help staff keep track of deceased information, funeral services, finances, and case progress in one organized system.


I chose this subject because I am a funeral director and I have firsthand experience with the gap between funeral service and modern technology. Many funeral homes still rely on outdated software that's clunky and difficult to use. Even newer systems often miss the mark by adding features without improving simplicity. In funeral service, simplicity matters. Of all the things funeral directors deal with, confusing and slow software make the job even harder. My goal with this project was to create something practical, straightforward, and easy to understand, while still being powerful enough to manage the important parts of  keeping track of a funeral.


This project differs from previous CS50 projects because it's a specialized management tool designed for a specific profession. Its purpose is case management, service scheduling, obituary editing, and financial tracking in a funeral home setting. These are tied directly to the funeral industry, making the project unique and relevant to my profession. 


The project is also complex because it uses Django on the backend with JavaScript on the frontend to create a better experience for the user. It includes multiple models (5), relationship data, dynamic page updates, editable sections, case tracking, and financial calculations. Rather than navigating multiple pages, JavaScript allows the user to stay in the same case they started. This way the program can feel more efficient than confusing. 


The program starts with a basic login to keep track of users. From there you are directed to the main/index page. This page displays all deceased individuals connected to the funeral home, including cases across multiple locations. It also shows basic case details and service information so users can quickly review what is happening.


At the top of the page the user has the ability to create a ‘New Case’. In order to create the case, the user must enter required information such as the deceased’s name, location, date of birth, and date of death. While the information is basic, it creates the foundation for the rest of the case and allows the user to move forward with managing services and records.


After the case is created, you will be directed to that deceased person's edit page. Here the user can edit deceased info, obituary, events, finances, and completed status. Everything on this page will run with JavaScript to keep the workflow smooth. 


Deceased Info keeps track of basic vital statistic information that would be needed for a death certificate. This information can be edited and saved. Obituary can be edited and saved as well. 


The events section allows the user to add an event/funeral service and scheduling information. It stores details such as the type of event, location, date, time, and duration. These events help staff stay organized, schedule properly, and answer questions from callers. Event information can be added, edited, and deleted, and it is displayed both on the individual case page and on the main index page.


The finances section allows the user to select funeral home products and services from pre-stored options.  When the user selects an item, it is added to a list of products/services. The total price is always adjusted when a new item is added or deleted. The items can also be edited. The user can edit the price, quantity, and edit a note. For example, if the user chooses casket, they would add in the description of the casket under notes. 


Status is simply making the case as completed, as default the case is listed as “in progress”, until changed. 


This project allowed me to combine my professional experience in funeral service with the programming skills I’ve learned in CS50W. This is a real problem in the industry and I felt like it would be a good idea to create something I have some knowledge of. It has more potential than to be called just a database, it's a practical tool that reflects real-world workflow that's used every day in the funeral industry. 

## How to start
Open your terminal and run `pip install -r requirements.txt`

## How to run
Open your terminal and run `python manage.py runserver`

