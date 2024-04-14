# Name: Hamzah Hamad
# ID: 101230812
# Group: 170 (Alone)

import psycopg2
from datetime import datetime, timedelta

#Connecting Database to Application
def Data_Base_Connection():
    return psycopg2.connect (
        host="INSERT HERE",
        dbname="INSERT HERE",
        user="INSERT HERE",
        password="INSERT HERE"
    )

# == AUTHENICATE USER DPEPENDING ON ROLE == 
def authenticate_user():
    user_type = input("Enter user type (member/trainer/staff): ").lower()
    if user_type == 'member':   #authenticate members
        email = input("Enter your email: ")
        query = "SELECT Member_id, 'member' FROM MemberProfiles WHERE Member_email = %s"         #Query to check member email againse MemberProfiles's data
    elif user_type == 'trainer': #authenicate personal trainers
        name = input("Enter your full name: ")
        query = "SELECT Trainer_id, 'trainer' FROM CertifiedTrainers WHERE Trainer_name = %s"    #Query to check trainer name against CertifiedTrainers's data
    elif user_type == 'staff':  #authenicate adminstrative staff
        name = input("Enter your full name: ")
        query = "SELECT Staff_id, 'staff' FROM Staff WHERE Staff_name = %s"                      #Query to check staff name against Staff's Data 
    else:
        print("Invalid user type.")
        return None, None

    connection = Data_Base_Connection()             #establish a connection
    cursor = connection.cursor()                    #Create a cursor object to interact with database
    
    # For trainers and staff, we're using the name to authenticate instead of email
    identifier = email if user_type == 'member' else name
    cursor.execute(query, (identifier,))
    
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if result:
        return result  # Return a tuple (user ID, role)
    else:
        print(f"{user_type.capitalize()} not found.")
        return None, None

# == EVERYTHING MEMBER RELATED STARTS HERE == 

# 1. Register Members 
def register_member():
    name = input("Please Enter Your Full Name: ")
    email = input("Please Enter Your Email Address: ")
    DOB = input("Please Enter Your Date of Birth (YYYY-MM-DD):  ")

    connection = Data_Base_Connection()             #establish a connection
    cursor = connection.cursor()                    #Create a cursor object to interact with database
    cursor.execute("INSERT INTO MemberProfiles (Member_name, Member_email, Member_DOB) VALUES (%s, %s, %s)", (name, email, DOB))        #Query to add member details to MemberProfiles table 

    connection.commit()
    cursor.close()
    connection.close()
    print("You are now registered. \n Welcome to Our Health and Fitness Club {name}!")

# 2. Profile Management (Updating personal information, fitness goals, health metrics)
def update_member_details(member_id):
    new_name = input("Enter the New Name: ")
    new_email = input("Enter the New Email Address: ")
    new_DOB = input("Enter the Correct Date of Birth (YYYY-MM-DD): ")

    connection = Data_Base_Connection()             #establish a connection
    cursor = connection.cursor()
    cursor.execute("UPDATE MemberProfiles SET Member_name = %s, Member_email = %s, Member_DOB = %s WHERE Member_id = %s", (new_name, new_email, new_DOB, member_id))     #Query to update member details in the MemberProfiles table.

    connection.commit()
    cursor.close()
    connection.close()
    print("Profile updated successfully!")

# 3. Dashboard Display (Displaying exercise routines, fitness achievements, health statistics)
def personalized_dashboard(member_id):
    connection = Data_Base_Connection()                 #establish a connection
    cursor = connection.cursor()                        #Create a cursor object to interact with database
    cursor.execute("SELECT Metric_id, Member_id, Current_weight, Current_fat_percent, Current_muscle_mass FROM HealthMetrics WHERE Member_id = %s", (member_id,))  #Query to retrieve all the metric data for the member
    Healthmetrics = cursor.fetchone()

    if Healthmetrics:  # Check if the query returned any data
        print(f"Current Metrics: ID: {Healthmetrics[0]}, Member ID: {Healthmetrics[1]}, Weight: {float(Healthmetrics[2])} kg, Fat %: {float(Healthmetrics[3])}, Muscle Mass: {float(Healthmetrics[4])} kg")  #Prints metric data 
    else:
        print("No metrics found for this member.")

    cursor.close()
    connection.close()

# Helper function for Step 4. (Instead of letting the user type the Trainer's ID, we let them use their name and we do our part on figuring out if the trainer exists)
def get_trainer_id_by_name(trainer_name):
    connection = Data_Base_Connection()                 #establish a connection
    cursor = connection.cursor()                        #Create a cursor object to interact with database
    cursor.execute("SELECT Trainer_id FROM CertifiedTrainers WHERE Trainer_name = %s", (trainer_name,))  #Query to get the id of the trainer based on the provided name
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else None


# 4. Schedule Management (Scheduling personal training sessions or group fitness classes. The system must ensure that the trainer is available)
def schedule_session_or_class(member_id):
    print("Available Trainers:\n> Donald Jump (Personal Trainer) - $99 /session \n > Michael Dancon (Fitness Instructor) - $35 / session")
    trainer_name = input("Enter Trainer Name: ")
    start_date = input("Enter session date and time (YYYY-MM-DD HH:MM): ")

    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M")

    session_length = timedelta(hours = 1)
    end_date = start_date + session_length

    trainer_id = get_trainer_id_by_name(trainer_name)
    if not trainer_id:
        print("Trainer not found.")
        return

    connection = Data_Base_Connection()                         #establish a connection
    cursor = connection.cursor()                                #Create a cursor object to interact with database

    try:
        if trainer_name == 'Donald Jump':
            cursor.execute("INSERT INTO PersonalTrainingSessions (Member_id, Trainer_id, Start_date, End_Date, Session_price) VALUES (%s, %s, %s, %s, 99)", (member_id, trainer_id, start_date, end_date))  #Query to add session details to PersonalTrainingSessions's table
        
        elif trainer_name == 'Michael Dancon':
            cursor.execute("INSERT INTO FitnessClasses (Member_id, Trainer_id, Start_date, End_Date, class_price) VALUES (%s, %s, %s, %s, 35)", (member_id, trainer_id, start_date, end_date)) #Query to add session details to FitnessClasses table
        
        cursor.execute("INSERT INTO PersonalSchedule (Trainer_id, Member_id, From_time, Availability) VALUES (%s, %s, %s, %s)", (trainer_id, member_id, start_date, end_date)) #Query to add session details PersonalSchedule. 
    
        connection.commit()
        print("Booking Confirmed!")

    finally:
        cursor.close()
        connection.close()

# 5. Extra function that allows member to see the sessions/classes they've booked.
def view_confirmed_bookings(member_id): 
    connection = Data_Base_Connection()         # Establish a connection
    cursor = connection.cursor()                #Create a cursor object to interact with database

    # Retrieve all fitness classes booked by the member
    cursor.execute("SELECT Class_id, Trainer_id, Start_date, End_date, Class_price FROM FitnessClasses WHERE Member_id = %s", (member_id,))  
    fitness_classes = cursor.fetchall()
    
    # Retrieve all personal training sessions booked by the member
    cursor.execute("SELECT Session_id, Trainer_id, Start_date, End_date, Session_price FROM PersonalTrainingSessions WHERE Member_id = %s ", (member_id,))
    training_sessions = cursor.fetchall()

    cursor.close() 
    connection.close() 

    # Check if the user has booked any classes or sessions
    if fitness_classes or training_sessions:
        print("Your booked fitness classes:")
        for fitclass in fitness_classes:
            print(f"Class ID: {fitclass[0]}, Trainer ID: {fitclass[1]}, Start: {fitclass[2]}, End: {fitclass[3]}, Price: {fitclass[4]}")

        print("\nYour booked personal training sessions:")
        for trainsessions in training_sessions:
            print(f"Session ID: {trainsessions[0]}, Trainer ID: {trainsessions[1]}, Start: {trainsessions[2]}, End: {trainsessions[3]}, Price: {trainsessions[4]}")
    else:
        print("You have no booked classes or sessions.")

# == EVERYTHING MEMBER RELATED ENDS HERE == 

# == EVERYTHING TRAINER RELATED STARTS HERE == 

# 1. Schedule Management (Trainer can set the time for which they are available.)
def setting_trainers_availability(trainer_id):
    available__start_time = input("Enter available time (YYYY-MM-DD HH:MM): ")
    available_start_time = datetime.strptime(available__start_time, "%Y-%m-%d %H:%M")

    available__end_time = input("Enter availablity end time (YYYY-MM-DD HH:MM): ")
    available_end_time = datetime.strptime(available__end_time, "%Y-%m-%d %H:%M")

    connection = Data_Base_Connection()                     #establish a connection
    cursor = connection.cursor()                            #Create a cursor object to interact with database

    try:
        cursor.execute("INSERT INTO PersonalSchedule (Trainer_id, From_time, Availability) VALUES (%s, %s, %s)", (trainer_id, available_start_time, available_end_time))

        connection.commit()
        print("Availability set Successfully!")

    finally: 
        cursor.close()
        connection.close()

# 2. Member Profile Viewing (Search by Member’s name)
def view_member_profile(): 
    member_name = input("Enter member's name to search: ")

    connection = Data_Base_Connection()                 #establish a connection
    cursor = connection.cursor()                        #Create a cursor object to interact with database
    cursor.execute("SELECT * FROM MemberProfiles WHERE Member_name LIKE %s", (f"%{member_name}%",))          #Query to retrieve member profile based on the provided name
    profiles = cursor.fetchall()


    for profile in profiles: 
        print(f"\nID: {profile[0]}, Name: {profile[1]}, Email: {profile[2]}, Date of Birth: {profile[3]}")
    
    cursor.close()
    connection.close()

# == EVERYTHING TRAINER RELATED ENDS HERE == 

# == EVERYTHING STAFF RELATED STARTS HERE == 

# 1. Room Booking Management
def room_booking_managment():
    session_id = int(input("Enter session ID for booking: "))
    date_time = input("Enter booking date and time (YYYY-MM-DD HH:MM): ")

    connection = Data_Base_Connection()                 #establish a connection
    cursor = connection.cursor()                        #Create a cursor object to interact with database
    cursor.execute("INSERT INTO RoomBooking (Session_id, Availability) VALUES (%s, %s)", (session_id, date_time))       #Query to add room booking details to RoomBooking

    connection.commit()
    cursor.close()
    connection.close()
    print("Room Booked Successfully!")


# 2. Equipment Maintenance Monitoring
def equipment_maintenance_monitoring():
    equipment_name = input("Enter equipment name: ")
    start_date = input("Enter start date of maintenance (YYYY-MM-DD): ")
    return_date = input("Enter anticipated return date (YYYY-MM-DD): ")

    connection = Data_Base_Connection()                 #establish a connection
    cursor = connection.cursor()                        #Create a cursor object to interact with database
    cursor.execute("INSERT INTO EquipmentMaintenance (Equipment_name, Start_date, Return_date) VALUES (%s, %s, %s)", (equipment_name, start_date, return_date)) #Query to add maintenance details to Equipment Maintenance table

    connection.commit()
    cursor.close()
    connection.close()
    print("Maintenance Logged Successfully!")


# 3. Class Schedule Updating
def FitnessClass_schedule_updating(): 
    class_id = int(input("Enter class ID to update: "))
    new_time = input("Enter new time for the class (YYYY-MM-DD HH:MM): ")

    connection = Data_Base_Connection()                 #establish a connection
    cursor = connection.cursor()                        #Create a cursor object to interact with database
    cursor.execute("UPDATE FitnessClasses SET Start_date = %s WHERE Class_id = %s", (new_time, class_id)) #Query to update FitnessClasses's data 

    connection.commit()
    cursor.close()
    connection.close()
    print("Fitness Class Schedule Updated Successfully!")


# 4. Billing and Payment Processing (Your system should assume integration with a payment service
def billing_and_payment():
    billing_id = int(input("Enter billing ID: "))
    payment_date = input("Enter payment date (YYYY-MM-DD): ")

    connection = Data_Base_Connection()                 #establish a connection
    cursor = connection.cursor()                        #Create a cursor object to interact with database
    cursor.execute("INSERT INTO PaymentProcessing (Billing_id, Shipment_date VALUES (%s,%s)", (billing_id, payment_date)) #Query to add billing details to Billing's table

    connection.commit()
    cursor.close()
    connection.close()
    print("Payment Processed Successfully!")

# == EVERYTHING STAFF RELATED ENDS HERE == 

# == MAIN FUNCTION FOR USER-INTERACTION == 
def main(): 
    user_id, role = authenticate_user() 

    if  user_id and role: 
        if role == 'member':
            while True: 
                print("\nMember's Menu:")
                print("1. Register")
                print("2. Update My Profile")
                print("3. Display Personalized Dashboard")
                print("4. Schedule a Session")
                print("5. View Scheduled Bookings")
                print("6. Exit")

                choice = input("What would you like to do today?")
                if choice == '1':
                    register_member()
                elif choice == '2':
                    update_member_details(user_id)
                elif choice == '3':
                    personalized_dashboard(user_id)
                elif choice == '4':
                    schedule_session_or_class(user_id)
                elif choice == '5':
                    view_confirmed_bookings(user_id)
                elif choice == '6':
                    break
                else:
                    print("Invalid option!")
                    main()
        
        elif role == 'trainer':
            while True: 
                print("\nTrainer's Menu:")
                print("1. Set Avaiability")
                print("2. View Member Profile")
                print("3. Exit")
                choice = input("What would you like to do today?")
                if choice == '1': 
                    setting_trainers_availability(user_id)
                elif choice == '2':
                    view_member_profile()
                elif choice == '3':
                    break
                else:
                    print("Invalid option")
                    main()

        elif role == 'staff':
            while True:
                print("\nStaff Menu:")
                print("1. Manage Room Booking")
                print("2. Log Equipment Maintenance")
                print("3. Update Class Schedule")
                print("4. Process Payments")
                print("5. Exit")
                choice = input("What would you like to do today?")
                if choice == '1':
                    room_booking_managment()
                elif choice == '2':
                    equipment_maintenance_monitoring()
                elif choice == '3':
                    FitnessClass_schedule_updating()
                elif choice == '4':
                    billing_and_payment()
                elif choice == '5':
                    break
                else:
                    print("Invalid option")
                    main()
                    
    else:
        print("Invalid login.")
        main()
    
if __name__ == "__main__":
    main()
