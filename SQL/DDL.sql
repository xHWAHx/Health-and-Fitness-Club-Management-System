-- DDL for MemberProfiles
CREATE TABLE MemberProfiles (
    Member_id SERIAL PRIMARY KEY,
    Member_name VARCHAR(50) NOT NULL,
    Member_email VARCHAR(50) NOT NULL UNIQUE,
    Member_DOB DATE NOT NULL
);

-- DDL for FitnessGoals
CREATE TABLE FitnessGoals (
    Goal_id SERIAL PRIMARY KEY,
    Member_id INTEGER NOT NULL REFERENCES MemberProfiles(Member_id),
    Weight_goal DECIMAL NOT NULL,
    Fat_percentage_goal DECIMAL NOT NULL,
    Muscle_mass_goal DECIMAL NOT NULL
);

-- DDL for HealthMetrics
CREATE TABLE HealthMetrics (
    Metric_id SERIAL PRIMARY KEY,
    Member_id INTEGER NOT NULL REFERENCES MemberProfiles(Member_id),
    Current_weight DECIMAL NOT NULL,
    Current_fat_percent DECIMAL NOT NULL,
    Current_muscle_mass DECIMAL NOT NULL
);

-- DDL for CertifiedTrainers
CREATE TABLE CertifiedTrainers (
    Trainer_id SERIAL PRIMARY KEY,
    Trainer_name VARCHAR(50) NOT NULL,
    Trainer_role VARCHAR(50)
);

-- DDL for PersonalSchedule
CREATE TABLE PersonalSchedule (
    Schedule_id SERIAL PRIMARY KEY,
    Trainer_id INTEGER NOT NULL REFERENCES CertifiedTrainers(Trainer_id),
    Member_id INTEGER REFERENCES MemberProfiles(Member_id),
    From_time TIMESTAMP NOT NULL,
    Availability TIMESTAMP NOT NULL
);

-- DDL for PersonalTrainingSessions
CREATE TABLE PersonalTrainingSessions (
    Session_id SERIAL PRIMARY KEY,
    Member_id INTEGER NOT NULL REFERENCES MemberProfiles(Member_id),
    Trainer_id INTEGER NOT NULL REFERENCES CertifiedTrainers(Trainer_id),
    Start_date TIMESTAMP NOT NULL,
    End_date TIMESTAMP NOT NULL,
    Session_price DECIMAL NOT NULL
);

-- DDL for FitnessClasses
CREATE TABLE FitnessClasses (
    Class_id SERIAL PRIMARY KEY,
    Member_id INTEGER REFERENCES MemberProfiles(Member_id),
    Trainer_id INTEGER REFERENCES CertifiedTrainers(Trainer_id),
    Start_date TIMESTAMP NOT NULL,
    End_date TIMESTAMP NOT NULL,
    Class_price DECIMAL NOT NULL
);

-- DDL for RoomBooking
CREATE TABLE RoomBooking (
    Room_id SERIAL PRIMARY KEY,
    Session_id INTEGER REFERENCES PersonalTrainingSessions(Session_id),
    Class_id INTEGER REFERENCES FitnessClasses(Class_id),
    Availability TIMESTAMP NOT NULL
);

-- DDL for EquipmentMaintenance
CREATE TABLE EquipmentMaintenance (
    Equipment_id SERIAL PRIMARY KEY,
    Equipment_name VARCHAR(50) NOT NULL,
    Start_date DATE NOT NULL,
    Return_date DATE
);

-- DDL for Billing
CREATE TABLE Billing (
    Billing_id SERIAL PRIMARY KEY,
    Member_ID INTEGER NOT NULL REFERENCES MemberProfiles(Member_id),
    Class_price DECIMAL,
    Session_cost DECIMAL NOT NULL,
    Registration_cost DECIMAL NOT NULL,
    Due_date DATE NOT NULL
);

-- DDL for PaymentProcessing
CREATE TABLE PaymentProcessing (
    Payment_id SERIAL PRIMARY KEY,
    Billing_id INTEGER NOT NULL REFERENCES Billing(Billing_id),
    Shipment_date DATE NOT NULL
);

-- DDL for Staff
CREATE TABLE Staff (
    Staff_id SERIAL PRIMARY KEY,
    Staff_name VARCHAR(50) NOT NULL,
    Staff_position VARCHAR(50) NOT NULL
);

