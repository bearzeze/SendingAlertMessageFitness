# **Sending Alert Messages**

## Python script that sends GSM messages to Fitness members whose membership fees have expired.


When python script is executed it will do next:

* Getting all data from Google Sheets using API
* Choosing only members which membership is going to expire on the date set into script (for example tomorrow)
* Constructing appropriate message 
* Using Selenium going into GSM operator web app, logining and sending message
* Tracking message history

## **How To Use Script**
Just run the script

## **Technical Specifications**
This script posses three major parts:
1. Getting data using API
2. Constructing appropriate message
3. Sending alert message

### **Generarting Members Data Using API**
AFitness workers add and update all user's membership using Google Sheets. They insert name and surname, telephone number and date of membership expiration. When script is executed it turns data from Google Sheets into JSON using Sheety API application. Then, only members with sooner expired membership is going to be extracted (most offen is tomorrow that expiration, but it can be handled with this date in the script). 

### **Constructing Appropriate Message**
Different prices are for the male and female members. Also message is constructed in Bosnian where there are differences between male and female verb construction. So program will determine the members sex based on its name. There is application for this - GENDER API, but problem is that only 500 calling is possible for free monthly, so database of names and genders are created (a lot of members names are repeated). First that name is queried in the databse, and if there is no such name it is determined using API and after that stored into the database. But sometimes API cannot determine the gender for the given name so it will finally ask the one who execute script what is the gender for that name and after that stored into the database.

Also message would discard all non-alphabetic letters that is heavily used in our language. This is because when sending message with these letters using GSM web page, it gives less maximum numbers of letters which can be send.

### **Sending Alert Message**
Message will be sent using the possibility of sending message from the mobile operator web app. This is done using Selenium.

## **Needs To Be Done**
- Automatic script execution (problem is how the gender would be determined if Gender API cannot find correct gender)
- Sending messages through Whatsapp/Viber in order to avoid GSM expenses

## **Contact**
Any information, bugs or questions can be sent on the e-mail adress: i.zejd@hotmail.com

