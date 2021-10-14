Appointment-Scheduler

App V1.1 is the newest version of this app

It's an App that has two Endpoints (POST and GET)


Appointments

POST
http://127.0.0.1:5000/appointments


Bodyraw (json)

json
{
  "date_time": "2021-10-16 02:38:00",
  "user_id": 2
}


GET
http://127.0.0.1:5000/appointments/3



POST Receives a date_time and a user_id, if the user_id is in memory it compares the dates and time and assign a new appointment. 
If the user ID doesn't exists it add it with the new date and return an AUTO_INCREMENT User_ID (Which you can use to update new Appointments)
To create a New User and Appointment you can use 0 for the user_Id and the app will return the AUTO_INCREMENT User_ID. 


GET Receives a User_ID and returns the appointments for this user.


Run App

python app_v1_1.py



Enjoy!
