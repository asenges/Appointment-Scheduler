#/usr/bin/python

from flask import Flask, request, jsonify, make_response
import uuid
import myapp_utils as utils

app = Flask(__name__)


class Appointment_list():

    appointments = []

    def find_user(self, user_id):
        min = 0
        max = len(self.appointments) - 1
    
        while max >= min:
            guess = (min + max) // 2

            if getattr(self.appointments[guess], 'user_id') == user_id:
                return guess

            elif getattr(self.appointments[guess], 'user_id') < user_id:
                min = guess + 1
                
            else:
                max = guess - 1
                

        return -1


    def __repr__(self):
        return f'{self.appointments}'
    

    def add_obj_to_list(self, obj):
        self.appointments.append(obj)



class Appointment():    

    def __init__(self, user_id):
        self.date_time = []
        self.user_id = user_id

    def __repr__(self):
        return f'{self.date_time}'

    def add_appointment(self, date_time):
        self.date_time.append(date_time)

    def set_user(self, user_id):
        self.user_id.append(user_id)





appointment_list = Appointment_list()


def create_appointment_object(date_time, user_id=None):
    '''
    In this version the List is Organized by an incremental user_id.
    If the ID received exists, it takes a new appointment for an existing user. But if it doesn't exist 
    the App assigns a new ID and store the new appointment for the new user and return its ID.
    '''
    date_time = utils.unix_time(date_time)
    obj_prefix = "appointment_"
    obj_uuid = uuid.uuid4()
    
    if user_id is not None:
        globals()[f"{obj_prefix}{obj_uuid}"] = Appointment(user_id)
    else:
        elements = len(appointment_list.appointments)
        globals()[f"{obj_prefix}{obj_uuid}"] = Appointment(elements+1)   

    globals()[f"{obj_prefix}{obj_uuid}"].add_appointment(date_time)
    appointment_list.add_obj_to_list(globals()[f"{obj_prefix}{obj_uuid}"])
    
    return elements + 1




@app.route('/appointments', methods = ['POST'])
def create_appointment():
    data = request.get_json()
    if isinstance(data["user_id"], int) and data["user_id"] >= 0:
        if len(appointment_list.appointments):
            user_list_pos = appointment_list.find_user(data["user_id"])
            if user_list_pos >= 0:

                # Comparing Dates to look for Appointments in the same day
                dates_list = getattr(appointment_list.appointments[user_list_pos], 'date_time')
                date_time = utils.unix_time(data["date_time"])
                for date in dates_list:
                    difference = date - date_time
                    if difference >= 0.0 and difference <= 1800:
                        time_list = utils.human_time(getattr(appointment_list.appointments[user_list_pos], 'date_time'))
                        return make_response(jsonify({"Date_time_already_busy": time_list }) , 406)

                
                id_user = data["user_id"]
                date_time = utils.unix_time(data["date_time"])
                appointment_list.appointments[user_list_pos].add_appointment(date_time)                
                return make_response(jsonify({f"User_Updated_{id_user}": getattr(appointment_list.appointments[user_list_pos], 'date_time')}) , 201) 

            else:
                # Creates the Sequence of Elements in the List
                id_user = create_appointment_object(data['date_time'])
                return make_response(jsonify({"User_Id_Created": id_user}),201)
            

        else:
            # Creates the First Element in the List
            id_user = create_appointment_object(data['date_time'])
            return make_response(jsonify({"User_Id_Created": id_user}),201)

                
    return make_response(jsonify({"Bad_Request": data["user_id"]}),400)





@app.route('/appointments/<id>', methods = ['GET'])
def get_appointments_by_id(id):

    user_list_pos = appointment_list.find_user(int(id))
    
    if user_list_pos >= 0:

        time_list = utils.human_time(getattr(appointment_list.appointments[user_list_pos], 'date_time'))
        return make_response(jsonify({"Appointments": time_list }) , 201)

    else:
            
        return make_response(jsonify({"User_Not_Found": id}),404)




if __name__ == "__main__":
    app.run(debug=True)

