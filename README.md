## Flights Deal Tracker

### About
This project is a flights deal tracker program. It looks through a list of cities provided in the Google Sheets and looks for the lowest flight price. If it finds a better flight price, it will update the spreadsheet with details of the flight and it will send an email to the email address provided in notification_manager.py.

### Technologies used
1. Sheety API 
2. Tequila API
3. SMTP 

### How to setup the project
1. This requires a Google Sheets account linked to Sheety. 
2. Open a Google spreadsheet and add the link to a new project created in Sheety. 
3. Obtain an authorization token from Sheety https://dashboard.sheety.co/ and add it to data_manager.py
4. Obtain an API key from Tequila and add it to flight_search.py
5. Run main.py
6. Check google spreadsheet 
7. Check email for low price deals alert



