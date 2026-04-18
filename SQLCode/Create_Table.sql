---Create Table for the database

---Student
CREATE TABLE Student (
    NYU_Email VARCHAR(255),
    First_Name VARCHAR(255) NOT NULL,
    Last_Name VARCHAR(255),
    Hashed_Password VARCHAR(255) NOT NULL,
    Account_Role VARCHAR(15) NOT NULL,
    PRIMARY KEY (NYU_Email)
);

--Student_Available_Time
CREATE TABLE Student_Available_Time (
    Time_ID INT PRIMARY KEY,
    Week_Day INT NOT NULL,
    NYU_Email VARCHAR(255),
    Start_Time TIME,
    End_Time TIME,
    FOREIGN KEY (NYU_Email) REFERENCES Student(NYU_Email)
);

--Course
CREATE TABLE Course (
    Course_ID INT PRIMARY KEY,
    Course_Name VARCHAR(255)
);

--Student_Course
CREATE TABLE Student_Course (
    NYU_Email VARCHAR(255),
    Course_ID INT,
    PRIMARY KEY (NYU_Email, Course_ID),
    FOREIGN KEY (NYU_Email) REFERENCES Student(NYU_Email),
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID)
);

--Location
CREATE TABLE Location (
    Location_ID INT PRIMARY KEY,
    Building VARCHAR(255) NOT NULL,
    Room VARCHAR(255) NOT NULL,
    Capacity INT
);

---Meeting
CREATE TABLE Meeting (
    Meeting_ID INT PRIMARY KEY,
    Start_Time TIMESTAMP NOT NULL,
    End_Time TIMESTAMP,
    Meeting_Note TEXT,
    Num_Of_Students INT,
    Course_ID INT,
    Location_ID INT,
    FOREIGN KEY (Course_ID) REFERENCES Course(Course_ID),
    FOREIGN KEY (Location_ID) REFERENCES Location(Location_ID)
);

--Invitation
CREATE TABLE Invitation (
    Invitation_ID INT PRIMARY KEY,
    Sent_Date DATE,
    Meeting_ID INT,
    NYU_Email VARCHAR(255),
    FOREIGN KEY (NYU_Email) REFERENCES Student(NYU_Email),
    FOREIGN KEY (Meeting_ID) REFERENCES Meeting(Meeting_ID)
);

--Feedback
CREATE TABLE Feedback (
    NYU_Email VARCHAR(255),
    Meeting_ID INT,
    Rating INT,
    Comment TEXT,
    PRIMARY KEY (NYU_Email, Meeting_ID),
    FOREIGN KEY (NYU_Email) REFERENCES Student(NYU_Email),
    FOREIGN KEY (Meeting_ID) REFERENCES Meeting(Meeting_ID)
);

--Meeting_Request
CREATE TABLE Meeting_Request (
    Meeting_ID INT,
    NYU_Email VARCHAR(255),
    PRIMARY KEY (Meeting_ID, NYU_Email),
    FOREIGN KEY (NYU_Email) REFERENCES Student(NYU_Email),
    FOREIGN KEY (Meeting_ID) REFERENCES Meeting(Meeting_ID)
);

--Study_Material
CREATE TABLE Study_Material (
    Study_Material_ID SERIAL PRIMARY KEY,
    File_Name VARCHAR(255) NOT NULL,
    File_Path TEXT,
    Meeting_ID INT,
    FOREIGN KEY (Meeting_ID) REFERENCES Meeting(Meeting_ID)
);
