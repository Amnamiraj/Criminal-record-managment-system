--Create database criminal record managament
CREATE DATABASE crms;

--Use criminal record managament
USE crms;

--Criminal Table
CREATE TABLE Criminal (
    Criminal_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    Address VARCHAR(200),
    Criminal_History TEXT,
    Arrest_Status VARCHAR(50)
);

--Insert value in criminal table
INSERT INTO Criminal
VALUES
(1, 'Ali Khan', 35, 'Male', 'Lahore, Punjab', 'Theft; Robbery', 'Arrested'),
(2, 'Usman Butt', 28, 'Male', 'Karachi, Sindh', 'Fraud', 'Not Arrested'),
(3, 'Zainab Sheikh', 30, 'Female', 'Multan, Punjab', 'Kidnapping; Assault', 'Arrested'),
(4, 'Rashid Qamar', 36, 'Male', 'Rawalpindi', 'Assault; Drug dealing', 'Arrested');

--Show criminal table 
SELECT * FROM Criminal;

-- Crime Table
CREATE TABLE Crime (
    Crime_ID INT PRIMARY KEY,
    Crime_Type VARCHAR(100),
    Crime_Date DATE,
    Crime_Location VARCHAR(200),
    Crime_Description TEXT,
    Evidence_Collected TEXT,
    Victim_ID INT,
    Criminal_ID INT,
    FOREIGN KEY (Criminal_ID) REFERENCES Criminal(Criminal_ID)
);

--Insert value in Crime table
INSERT INTO Crime VALUES
(1, 'Robbery', '2024-02-11', 'Lahore', 'Bank robbery at Model Town.', 'CCTV Footage; Fingerprints', 1, 1),
(2, 'Fraud', '2023-11-05', 'Karachi', 'Scam involving fake housing society.', 'Documents; Bank Records', 2, 2),
(3, 'Kidnapping', '2023-12-22', 'Multan', 'Kidnapping of school child.', 'Witness Reports', 3, 3),
(4, 'Murder', '2023-08-15', 'Peshawar', 'Targeted shooting in market.', 'Bullet casing', 4, NULL);

--Show crime table 
SELECT * FROM Crime;

-- Victim Table
CREATE TABLE Victim (
    Victim_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    Contact_Number VARCHAR(20),
    Address VARCHAR(200),
    Injury_Status VARCHAR(100),
    Crime_ID INT,
    Statement TEXT,
    FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID)
);

--Insert value in Victim table
INSERT INTO Victim VALUES
(1, 'Rehan Tariq', 42, 'Male', '03001234567', 'Lahore', 'Minor Injury', 1, 'Victim saw the suspect fleeing.'),
(2, 'Sadia Rehman', 38, 'Female', '03111234567', 'Karachi', 'None', 2, 'Victim defrauded in housing scam.'),
(3, 'Hamza Yousaf', 12, 'Male', '03211234567', 'Multan', 'Traumatized', 3, 'Kidnapped outside school gate.'),
(4, 'Tariq Iqbal', 55, 'Male', '03256767882','Peshawar', 'Fatal', 4, 'Deceased due to targeted shooting.');

--Show Victim table 
SELECT * FROM Victim;

-- Police Officer Table
CREATE TABLE Police_Officer (
    Officer_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Rank VARCHAR(50),
    Badge_Number VARCHAR(20),
    Contact_Number VARCHAR(20),
    PoliceStation VARCHAR(100),
    Assigned_Cases TEXT,
    Crime_ID INT,
    FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID)
);

--Insert value into Police Officer table
INSERT INTO Police_Officer VALUES
(1, 'Inspector Asim', 'Inspector', 'PK-001', '03001112222', 'Model Town Police Station', '1,2', 1),
(2, 'DSP Khalid', 'DSP', 'PK-002', '03002223333', 'Clifton Police Station', '2,3', 2),
(3, 'Constable Waseem', 'Constable', 'PK-003', '03003334444', 'Multan Central', '3', 3),
(4, 'SI Nadeem', 'Sub-Inspector', 'PK-004', '03004445555', 'Peshawar HQ', '4', 4);

--Show Police Officer
SELECT * FROM Police_Officer;

-- Investigation Report Table
CREATE TABLE Investigation_Report (
    Report_ID INT PRIMARY KEY,
    Crime_ID INT,
    Officer_ID INT,
    Investigation_Details TEXT,
    Findings TEXT,
    Report_Date DATE,
    Case_Status VARCHAR(100),
    FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID),
    FOREIGN KEY (Officer_ID) REFERENCES Police_Officer(Officer_ID)
);

--Insert value into Investigation Report table
INSERT INTO Investigation_Report VALUES
(1, 1, 1, 'Interviewed bank staff and reviewed footage.', 'Confirmed identity of robber.', '2024-02-15', 'Closed'),
(2, 2, 2, 'Analyzed fake documents and money trail.', 'Identified fraud network.', '2023-11-10', 'Ongoing'),
(3, 3, 3, 'Visited school and questioned witnesses.', 'Found vehicle used for kidnapping.', '2023-12-26', 'Sent to Forensic'),
(4, 2, 2, 'Interviewed suspects, reviewed documents.', 'Found scam details.', '2025-06-24', 'Sent to Forensic');

--Show Investigation Report table
SELECT * FROM Investigation_Report;

-- Court Case Table
CREATE TABLE Court_Case (
    Case_ID INT PRIMARY KEY,
    Crime_ID INT,
    Court_Name VARCHAR(100),
    Judge_Name VARCHAR(100),
    Hearing_Date DATE,
    Case_Status VARCHAR(50),
    Verdict TEXT,
    FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID)
);

--Insert value into Court Case table
INSERT INTO Court_Case VALUES
(1, 1, 'Lahore High Court', 'Justice Malik', '2024-03-01', 'Closed', 'Guilty'),
(2, 2, 'Karachi Sessions Court', 'Justice Tariq', '2023-12-01', 'Ongoing', 'Pending'),
(3, 3, 'Multan Family Court', 'Justice Raza', '2024-01-10', 'Ongoing', 'Pending'),
(4, 4, 'Peshawar High Court', 'Justice Noman', '2023-09-01', 'Closed', 'Guilty');

--Show Court Case table
SELECT * FROM Court_Case;

-- Witness Table
CREATE TABLE Witness (
    Witness_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    Contact_Number VARCHAR(20),
    Address VARCHAR(200),
    Statement TEXT,
    Crime_ID INT,
    FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID)
);

--Insert value into Witness table
INSERT INTO Witness VALUES
(1, 'Asad Mehmood', 40, 'Male', '03011234567', 'Lahore', 'Saw suspect enter bank.', 1),
(2, 'Nida Rizvi', 35, 'Female', '03021234567', 'Karachi', 'Saw fraud meetings.', 2),
(3, 'Rashid Jameel', 50, 'Male', '03031234567', 'Multan', 'Identified suspect car.', 3),
(4, 'Shahbaz Ali', 38, 'Male', '03041234567', 'Peshawar', 'Heard gunshot.', 4);

--Show Witness table
SELECT * FROM Witness;

-- Evidence Table
CREATE TABLE Evidence (
    Evidence_ID INT PRIMARY KEY,
    Crime_ID INT,
    Evidence_Type VARCHAR(100),
    Description TEXT,
    Collected_By VARCHAR(100),
    Collection_Date DATE,
    Storage_Location VARCHAR(100),
    FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID)
);

--Insert value into Evidence table
INSERT INTO Evidence VALUES
(1, 1, 'CCTV', 'Bank CCTV footage', 'Inspector Asim', '2024-02-11', 'Evidence Room 1'),
(2, 2, 'Document', 'Forged papers', 'DSP Khalid', '2023-11-06', 'Evidence Room 2'),
(3, 3, 'Witness Report', 'School teacher statement', 'Constable Waseem', '2023-12-23', 'Locker A'),
(4, 2, 'DNA Sample', 'Blood sample from crime scene', 'Forensic Dr. Sara', '2025-06-24', 'Lab Shelf 5');

--Show Evidence table
SELECT * FROM Evidence;

-- Complaint/FIR Table
CREATE TABLE Complaint_FIR (
    Complaint_ID INT PRIMARY KEY,
    Complainant VARCHAR(100),
    Crime_ID INT,
    Complaint_Date DATE,
    Description TEXT,
    Filed_By INT,
    Status VARCHAR(50),
    FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID),
    FOREIGN KEY (Filed_By) REFERENCES Police_Officer(Officer_ID)
);

--Insert value into Complaint/FIR Table 
INSERT INTO Complaint_FIR VALUES
(1, 'Bank Manager', 1, '2024-02-11', 'Reported robbery with weapons.', 1, 'Filed'),
(2, 'Ali Raza', 2, '2023-11-05', 'Reported fraud in housing project.', 2, 'Filed'),
(3, 'Principal', 3, '2023-12-22', 'Reported missing student.', 3, 'Filed'),
(4, 'Public Citizen', 4, '2023-08-15', 'Reported dead body found.', 4, 'Filed'),
(5, 'Ahmed Saleem', 2, '2025-06-24', 'Car theft at night', 1, 'In Progress');

--Show Complaint/FIR Table
SELECT * FROM Complaint_FIR;

-- Suspect Table
CREATE TABLE Suspect (
    Suspect_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    Address VARCHAR(200),
    Contact_Number VARCHAR(20),
    Crime_ID INT,
    Status VARCHAR(50),
    FOREIGN KEY (Crime_ID) REFERENCES Crime(Crime_ID)
);

--Insert value into Suspect Table
INSERT INTO Suspect VALUES
(1, 'Zafar Iqbal', 37, 'Male', 'Lahore', '03211234567', 1, 'Arrested'),
(2, 'Mehmood Jan', 44, 'Male', 'Karachi', '03221234567', 2, 'Under Investigation'),
(3, 'Sadia Abbas', 29, 'Female', 'Multan', '03231234567', 3, 'Arrested'),
(4, 'Aslam Shah', 41, 'Male', 'Peshawar', '03241234567', 4, 'Arrested');

--Show Suspect Table
SELECT * FROM Suspect;

--View All FIRs
SELECT * FROM Complaint_FIR 
WHERE Filed_By = 1;

--Add New FIR:
INSERT INTO Complaint_FIR
VALUES
(6, 'Ali Raza', 2, '2025-06-24', 'House theft at night', 1, 'Filed');

--Update FIR:
UPDATE Complaint_FIR
SET Status = 'In Progress'
WHERE Complaint_ID = 5;

--View Assigned Crimes:
SELECT * FROM Crime
WHERE Crime_ID = 1;

--Add Criminal Record:
INSERT INTO Criminal (Criminal_ID, Name, Age, Gender, Address, Criminal_History, Arrest_Status)
VALUES 
(5, 'Zahid Qamar', 36, 'Male', 'Rawalpindi', 'Assault; child traffic', 'Arrested');

--Search Criminal Record by Name
SELECT * FROM Criminal
WHERE Name LIKE '%Ali%';

--Display Witnesses for a Case
SELECT Name, Statement FROM Witness
WHERE Crime_ID = 1;

--View All Evidence for a Crime:
SELECT * FROM Evidence
WHERE Crime_ID = 1;

--List Suspects for a Crime:
SELECT * FROM Suspect
WHERE Crime_ID = 1;

--Count of FIRs by Status:
SELECT Status, COUNT(*) AS Total_FIRs
FROM Complaint_FIR
GROUP BY Status;

--Display fir_records:
SELECT * FROM Complaint_FIR;

--View FIRS assigned to Police officer:
SELECT * FROM Complaint_FIR
WHERE Filed_By = 1;


--View All FIRs Received:
SELECT * FROM Complaint_FIR WHERE Status = 'Filed';

--Count number of FIRs by Status with HAVING filter for > 1 FIR
SELECT Status, COUNT(*) AS Total_FIRs
FROM Complaint_FIR
GROUP BY Status
HAVING COUNT(*) > 1;

--Find latest forensic report updates 
SELECT Report_ID, Crime_ID, Findings, Report_Date
FROM Investigation_Report
WHERE Case_Status = 'Sent to Forensic'
ORDER BY Report_Date DESC;

--Show investigation reports with officer names and only those marked 'Sent to Forensic'
SELECT ir.Report_ID, p.Name AS Officer_Name, ir.Case_Status, ir.Findings
FROM Investigation_Report ir
INNER JOIN Police_Officer p ON 
ir.Officer_ID = p.Officer_ID
WHERE ir.Case_Status = 'Sent to Forensic'
ORDER BY ir.Report_Date DESC;

--Show evidence collected per crime with total evidence count
SELECT c.Crime_ID, c.Crime_Type, COUNT(e.Evidence_ID) AS Total_Evidence
FROM Crime c
INNER JOIN Evidence e ON
c.Crime_ID = e.Crime_ID
GROUP BY c.Crime_ID, c.Crime_Type
HAVING COUNT(e.Evidence_ID) >= 1;

--View suspects with crime details 
SELECT s.Name AS Suspect_Name, s.Status, c.Crime_Type, c.Crime_Location
FROM Suspect s
INNER JOIN Crime c ON
s.Crime_ID = c.Crime_ID;

--Find all witnesses with their statement and crime date
SELECT w.Name AS Witness_Name, w.Statement, c.Crime_Date
FROM Witness w
INNER JOIN Crime c ON 
w.Crime_ID = c.Crime_ID
ORDER BY c.Crime_Date DESC;

--List all FIRs with complainant, officer, and case status 
SELECT f.Complaint_ID, f.Complainant, p.Name AS Officer_Name, f.Status
FROM Complaint_FIR f
INNER JOIN Police_Officer p ON 
f.Filed_By = p.Officer_ID
ORDER BY f.Status;

--List all court cases with crime details and judges
SELECT cc.Case_ID, cc.Court_Name, cc.Judge_Name, cc.Hearing_Date, cc.Case_Status, c.Crime_Type
FROM Court_Case cc
INNER JOIN Crime c ON 
cc.Crime_ID = c.Crime_ID;

--List criminal records with total number of crimes 
SELECT cr.Criminal_ID, cr.Name, COUNT(c.Crime_ID) AS Total_Crimes
FROM Criminal cr
LEFT JOIN Crime c ON cr.Criminal_ID = c.Criminal_ID
GROUP BY cr.Criminal_ID, cr.Name
ORDER BY Total_Crimes DESC;

--Count how many complaints each police officer has filed
SELECT p.Name AS Officer_Name, COUNT(f.Complaint_ID) AS Total_Complaints
FROM Police_Officer p
INNER JOIN Complaint_FIR f ON p.Officer_ID = f.Filed_By
GROUP BY p.Name
HAVING COUNT(f.Complaint_ID) >= 1;

--Find crimes with equal to 1 suspect
SELECT c.Crime_ID, c.Crime_Type, COUNT(s.Suspect_ID) AS Suspect_Count
FROM Crime c
INNER JOIN Suspect s ON c.Crime_ID = s.Crime_ID
GROUP BY c.Crime_ID, c.Crime_Type
HAVING COUNT(s.Suspect_ID) = 1;










