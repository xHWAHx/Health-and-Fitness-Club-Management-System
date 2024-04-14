-- Create Member Profiles
INSERT INTO MemberProfiles (Member_name, Member_email, Member_DOB) VALUES
('Hamzah H.', 'Hamzahhamad3@cmail.carleton.ca', '2003-02-17'),
('Alex J.', 'AlexJay@example.carleton.ca', '1984-04-21'),
('Josh K.', 'JoshKen@example.carleton.ca', '1999-09-03');

-- Assign Members Fitness Goals
INSERT INTO FitnessGoals (Member_id, Weight_goal, Fat_percentage_goal, Muscle_mass_goal) VALUES
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'Hamzahhamad3@cmail.carleton.ca'), 75, 15, 45),
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'AlexJay@example.carleton.ca'), 55, 20, 30),
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'JoshKen@example.carleton.ca'), 95, 30, 50),

-- Assign Members Sample Metric Data 
INSERT INTO HealthMetrics (Member_id, Current_weight, Current_fat_percent, Current_muscle_mass) VALUES
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'Hamzahhamad3@cmail.carleton.ca'), 85, 28, 40),
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'AlexJay@example.carleton.ca'), 65, 20, 35),
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'JoshKen@example.carleton.ca'), 75, 15, 45),

-- Create Sample Personal Trainers
INSERT INTO CertifiedTrainers (Trainer_name, Trainer_role) VALUES
('Donald Jump', 'Personal Trainer'),
('Michael Dancon', 'Fitness Instructor');

-- Insert Sample data into Trainers' Personal Schedule
INSERT INTO PersonalSchedule (Trainer_id, Member_id, From_time, Availability) VALUES
((SELECT Trainer_id FROM CertifiedTrainers WHERE Trainer_name = 'Donald Jump'), (SELECT Member_id FROM MemberProfiles WHERE Member_email = 'Hamzahhamad3@cmail.carleton.ca'), '2024-04-15 09:00', '2024-04-15 10:00'),
((SELECT Trainer_id FROM CertifiedTrainers WHERE Trainer_name = 'Donald Jump'), (SELECT Member_id FROM MemberProfiles WHERE Member_email = 'AlexJay@example.carleton.ca'), '2024-04-16 07:00', '2024-04-16 08:59'),
((SELECT Trainer_id FROM CertifiedTrainers WHERE Trainer_name = 'Michael Dancon'), (SELECT Member_id FROM MemberProfiles WHERE Member_email = 'JoshKen@example.carleton.ca'), '2024-04-15 09:00', '2024-04-15 10:00');

-- Insert sample data into PersonalTrainingSessions
INSERT INTO PersonalTrainingSessions (Member_id, Trainer_id, Start_date, End_date, Session_price) VALUES
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'Hamzahhamad3@cmail.carleton.ca'), (SELECT Trainer_id FROM CertifiedTrainers WHERE Trainer_name = 'Donald Jump'), '2024-04-15 09:00', '2024-04-15 10:00', 99),
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'AlexJay@example.carleton.ca'), (SELECT Trainer_id FROM CertifiedTrainers WHERE Trainer_name = 'Donald Jump'), '2024-04-16 07:00', '2024-04-15 08:59', 198),
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'JoshKen@example.carleton.ca'), (SELECT Trainer_id FROM CertifiedTrainers WHERE Trainer_name = 'Donald Jump'), '2024-04-17 09:00', '2024-04-17 10:00', 99);

-- Insert sample data into FitnessClasses
INSERT INTO FitnessClasses (Member_id, Trainer_id, Start_date, End_date, Class_price) VALUES
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'Hamzahhamad3@cmail.carleton.ca'), (SELECT Trainer_id FROM CertifiedTrainers WHERE Trainer_name = 'Michael Dancon'), '2024-04-20 08:00', '2024-04-20 09:00', 65),
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'AlexJay@example.carleton.ca'), (SELECT Trainer_id FROM CertifiedTrainers WHERE Trainer_name = 'Michael Dancon'), '2024-04-21 17:00', '2024-04-21 18:00', 97);

-- Insert sample data into RoomBooking
-- Note: Assuming a room booking relates to a session or class. Example uses session.
INSERT INTO RoomBooking (Session_id, Availability) VALUES
((SELECT Session_id FROM PersonalTrainingSessions WHERE Member_id = (SELECT Member_id FROM MemberProfiles WHERE Member_email = 'Hamzahhamad3@cmail.carleton.ca')), '2024-04-15 09:00'),
((SELECT Session_id FROM PersonalTrainingSessions WHERE Member_id = (SELECT Member_id FROM MemberProfiles WHERE Member_email = 'AlexJay@example.carleton.ca')), '2024-04-16 07:00'),
((SELECT Session_id FROM PersonalTrainingSessions WHERE Member_id = (SELECT Member_id FROM MemberProfiles WHERE Member_email = 'JoshKen@example.carleton.ca')), '2024-04-17 09:00'),

-- Insert sample data into EquipmentMaintenance
INSERT INTO EquipmentMaintenance (Equipment_name, Start_date, Return_date) VALUES
('Treadmill', '2024-04-10', '2024-04-12'),
('Leg Press', '2024-03-09', '2024-04-09'),
('Chest Press', '2023-09-09', '2024-04-05'),
('Exercise Bike', '2024-03-17', NULL);  -- NULL indicates the equipment hasn't been returned yet.

-- Insert sample data into Billing
INSERT INTO Billing (Member_ID, Class_price, Session_cost, Registration_cost, Due_date) VALUES
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'Hamzahhamad3@cmail.carleton.ca'), 65, 99, 100, '2024-05-01'),
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'AlexJay@example.carleton.ca'), 97, 198, 100, '2024-05-15'),
((SELECT Member_id FROM MemberProfiles WHERE Member_email = 'JoshKen@example.carleton.ca'), 0, 99, 100, '2024-05-15'),

-- Insert sample data into PaymentProcessing
-- Note: Assuming a payment is related to a billing record.
INSERT INTO PaymentProcessing (Billing_id, Shipment_date) VALUES
((SELECT Billing_id FROM Billing WHERE Member_ID = (SELECT Member_id FROM MemberProfiles WHERE Member_email = 'Hamzahhamad3@cmail.carleton.ca')), '2024-03-20'),
((SELECT Billing_id FROM Billing WHERE Member_ID = (SELECT Member_id FROM MemberProfiles WHERE Member_email = 'AlexJay@example.carleton.ca')), '2024-02-02'),
((SELECT Billing_id FROM Billing WHERE Member_ID = (SELECT Member_id FROM MemberProfiles WHERE Member_email = 'JoshKen@example.carleton.ca')), '2024-03-22'),

-- Insert sample data into Staff
INSERT INTO Staff (Staff_name, Staff_position) VALUES
('Emma L.', 'Manager'),
('Nick J.', 'Receptionist'),
('Hailey D.', 'Assistant Manager');

