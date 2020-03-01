Cashr is an application which helps to track spending by monitoring transactions. Built using Flask in Python, transactions are entered into a MYSQL database through a Vuetify front end. 

The categories that transactions can be are:
- Food and Juice
- Alcohol
- Health and Hygiene
- Travel
- Sports & Leisure
- Presents & Gifts
- Flat
- Utilities
- Other

Notes on error handling:
- if an error such as "Can't connect to MySQL server on 'localhost:3306' because the target machine actively refused it" appears, open task manager, find the service "MySQL80" and make sure its running.

Things to add:
- Pigar for automating requirements file.