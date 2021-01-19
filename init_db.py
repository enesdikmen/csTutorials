from psycopg2 import connect





def init_table():
    
    with connect("dbname=postgres user=postgres password=12345 host=localhost") as conn:
        with conn.curosr() as cur:

            

            querry ="""CREATE TABLE Educator(
            EducatorID SERIAL,
            EducatorName VARCHAR(50) NOT NULL,
            InfoURL VARCHAR(255),
            AvgRating FLOAT8,
            PRIMARY KEY(EducatorID)
            );"""
            cur.execute(querry)

            

            querry ="""CREATE TABLE Tutorial(
            TutorialID SERIAL,
            title VARCHAR(255) NOT NULL,
            EducatorID INT NOT NULL,
            Platform VARCHAR (50),
            url VARCHAR (255) NOT NULL UNIQUE,
            Skill VARCHAR (50),
            Length INT[2],
            Info TEXT,
            RatingNum INT DEFAULT 0,
            TutorialRating  FLOAT8,
            PRIMARY KEY (TutorialID),
            FOREIGN KEY (EducatorID) 
            REFERENCES Educator(EducatorID)
            );
            """
            cur.execute(querry)

            querry ="""CREATE TABLE UserAcc(
            UserID SERIAL,
            UserEmail VARCHAR(255) NOT NULL UNIQUE,
            Password VARCHAR(255) NOT NULL,
            isAdmin BOOL NOT NULL DEFAULT false,
            CreatedAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (UserID)
            );
            """
            cur.execute(querry)

            querry ="""CREATE TABLE Enrollment(
            EnrollmentID SERIAL,
            UserID INT NOT NULL,
            TutorialID INT NOT NULL,
            EnrollmentTime TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            EndTime TIMESTAMP,
            Status VARCHAR(50),
            PRIMARY KEY(EnrollmentID),
            FOREIGN KEY (UserID)
            REFERENCES UserAcc(UserID)
            ON DELETE CASCADE,
            FOREIGN KEY (TutorialID)
            REFERENCES Tutorial(TutorialID)
            ON DELETE CASCADE
            );
            """
            cur.execute(querry)

            querry ="""CREATE TABLE RatingComment(
            RatingID SERIAL,
            UserID INT NOT NULL,
            TutorialID INT NOT NULL,
            Rating INT NOT NULL,
            Comment TEXT,
            RatingTime TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(RatingID),
            FOREIGN KEY (UserID)
            REFERENCES UserAcc(UserID)
            ON DELETE CASCADE,
            FOREIGN KEY (TutorialID)
            REFERENCES Tutorial(TutorialID)
            ON DELETE CASCADE
            );
            """
            cur.execute(querry)
            
            querry = """CREATE TABLE Topic(
            TopicID SERIAL,
            TopicName VARCHAR(50) NOT NULL UNIQUE,
            PRIMARY KEY(TopicID)
            );
            """
            cur.execute(querry)

            querry ="""CREATE TABLE TutorialTopic(
            TutTopicID SERIAL,
            TutorialID INT NOT NULL,
            TopicID INT NOT NULL,
            PRIMARY KEY(TutTopicID),
            FOREIGN KEY(TutorialID)
            REFERENCES Tutorial(TutorialID)
            ON DELETE CASCADE,
            FOREIGN KEY(TopicID)
            REFERENCES Topic(TopicID)
            ON DELETE CASCADE
            );
            """
            cur.execute(querry)

    
def drop_all():
    conn = connect("dbname=postgres user=postgres password=12345 host=localhost")
    cur = conn.cursor()
    cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
    conn.commit()
    cur.close()
    conn.close()