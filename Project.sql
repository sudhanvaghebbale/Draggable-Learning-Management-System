CREATE TABLE Quiz (
	Name varchar(500),
	Instructor varchar(100) NOT NULL,
	Quiz_Level varchar(50) NOT NULL,
	Description varchar(100),
	Status varchar(1),
	PRIMARY KEY (Name)
);

CREATE TABLE Questions (
	ID varchar(20) NOT NULL,
	Question varchar(1000),
	Level varchar(100) NOT NULL,
	Quiz_Name varchar(500),
	FOREIGN KEY (Quiz_Name) REFERENCES Quiz(Name)
);

CREATE TABLE Answer (
	ID varchar(20) NOT NULL,
	Choice varchar(20) NOT NULL,
	Quiz_Name varchar(500),
	Question_ID varchar(5),
	FOREIGN KEY (Quiz_Name) REFERENCES Quiz(Name)
);

CREATE TABLE Grades (
	Quiz_Name varchar(500),
	Email varchar(50) NOT NULL,
	Score varchar(3) NOT NULL,
	Instructor varchar(50) NOT NULL,
	Last_Taken DATETIME NOT NULL,
	FOREIGN KEY (Quiz_Name) REFERENCES Quiz(Name),
	FOREIGN KEY (Email) REFERENCES Users(Email)
);