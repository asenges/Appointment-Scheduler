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


def create_appointment_object(user_id, date_time):
    

    # TO-DO: Order this List for Binary Search Function or Change Structure to use a Dictionary
    date_time = utils.unix_time(date_time)
    obj_prefix = "appointment_"
    obj_uuid = uuid.uuid4()
    globals()[f"{obj_prefix}{obj_uuid}"] = Appointment(user_id)
    globals()[f"{obj_prefix}{obj_uuid}"].add_appointment(date_time)
    appointment_list.add_obj_to_list(globals()[f"{obj_prefix}{obj_uuid}"])
    




@app.route('/appointments', methods = ['POST'])
def create_appointment():
    data = request.get_json()
    if isinstance(data["user_id"], int) and data["user_id"] > 0:
        if len(appointment_list.appointments):
            user_list_pos = appointment_list.find_user(data["user_id"])
            if user_list_pos >= 0:
                # TO-DO: Restrict dates for the same day
                date_time = utils.unix_time(data["date_time"])
                appointment_list.appointments[user_list_pos].add_appointment(date_time)                
                return make_response(jsonify({"User_Updated": 
                        getattr(appointment_list.appointments[user_list_pos], 'date_time') }) , 201) 

            else:
                create_appointment_object(data['user_id'], data['date_time'])
                return make_response(jsonify({"User_Added": data}),201)
            

        else:
            create_appointment_object(data['user_id'], data['date_time'])
            return make_response(jsonify({"User_Added": data}),201)

                
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

