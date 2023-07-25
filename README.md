# FlyAwayRobot

This is a scrapper that search for flight info in Gol[https://www.voegol.com.br/] and save the results in json files.

## Setting up the environment:

 - Make sure you have python 3.9 or higher installed

 - Make sure you have the chromedriver installed and matching your chrome version

Create the environment
```
python3 -m venv venv
```
Activate the environment:
```
source venv/bin/activate
```
Install de dependencies:
```
pip install -r requirements.txt
```
## Defining the attributtes to run the scrapper
Create a .env file based on env.example, and set the search variables :
    - ROBOCORP_CLOUD      ("True" if your are deploying the robot in Robocorp Cloud, "False" if local)
    - ORIGIN_CITY         (Ex: Aracaju)
    - DESTINATION_CITY    (Ex:"sao paulo - todos os aeroportos")
    - DEPARTURE_DATE      (Ex:"22/12/2023" - The date must be in this format)
    - RETURN_DATE         (Ex : "09/01/2024")
    - NUMBER_OF_ADULTS    (Ex: 3)
    - NUMBER_OF_CHILDREN  (Ex: 1)

## Start the scrapper
Run tasks.py