
from psycopg2 import connect
from tables import Topic, Tutorial, Educator
from passlib.hash import pbkdf2_sha256 as hasher


class Database:
    def __init__(self, dbinfo):
        self.dbinfo = dbinfo
        # self.conn = connect("dbname=postgres user=postgres password=12345 host=localhost")
        # self.cur = self.conn.cursor()
    
    #topic table methods
    def add_topic(self, topic):
        if self.get_topic(topic.name): #if topic already exists
            return False
        else:
            with connect(self.dbinfo) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"INSERT INTO topic(TopicName) VALUES ('{topic.name}');")
                    conn.commit()
                    rowcount = cur.rowcount
            return rowcount

    def update_topic(self, topicName, topicID):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"UPDATE Topic SET TopicName='{topicName}' WHERE TopicID='{topicID}'; ")
                conn.commit()
                rowcount = cur.rowcount    
        return rowcount
    def delete_topic(self, topicName):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM Topic WHERE TopicName='{topicName}';")
                conn.commit()
                rowcount =  cur.rowcount
        return rowcount

    def get_topic(self, topicName):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT*FROM Topic WHERE topicName = '{topicName}';")
                topic = cur.fetchone()
        return topic
        
    def get_topics(self):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT*FROM Topic;")        
                rows = cur.fetchall()
        return rows

    def get_topic_names(self):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT(TopicName) FROM Topic;")
                rows = cur.fetchall()
        return rows

    #educator table methods
    def add_educator(self, educator):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"INSERT INTO educator(EducatorName, InfoURL) VALUES ('{educator.name}', '{educator.infoURL}');")
                conn.commit()
                rowcount = cur.rowcount
        return rowcount
    def get_educator_names(self):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EducatorID, EducatorName FROM Educator;")
                rows = cur.fetchall()
        return rows

    def get_educator(self, educatorName):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT*FROM Educator WHERE educatorName='{educatorName}';")
                row = cur.fetchone()
        return Educator(id=row[0], name=row[1], infoURL=row[2]) if row else None
    
    def update_educator(self, educatorID, educatorName, educatorURL):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"UPDATE Educator SET EducatorName='{educatorName}', InfoURL='{educatorURL}' WHERE educatorID='{educatorID}'; ")
                conn.commit()
                rowcount = cur.rowcount
        return rowcount

    def delete_educator(self, educatorID):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM Educator WHERE EducatorID={educatorID};")
                conn.commit()
                rowcount = cur.rowcount
        return rowcount
    #userAcc table methods
    def validate_signup(self, Email, password):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT*FROM UserAcc WHERE UserEmail='{Email}';")
                row = cur.fetchall()
        if row:
            return False
        else:
            return True


    def validate_login(self, email, password):
    
        #fetchs the hashed password from database and verifies if it is correct
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT(Password) FROM UserAcc WHERE UserEmail= %s;", (email,))
                row = cur.fetchone()

        if row:#true if an account with email exists
            if hasher.verify(password, row[0]):#true if password is correct
                return True
            else:
                return False
        else:
            return False        

    def add_user(self, email, password):
        if self.validate_signup(email, password):
            with connect(self.dbinfo) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"INSERT INTO UserAcc(UserEmail, Password) VALUES ('{email}', '{password}') RETURNING userid;")
                    row = cur.fetchone()

                    conn.commit()
            return row
        else:
            return False
    
    def get_user(self, userID):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT useremail, password FROM UserAcc WHERE userid= %s;", (userID,))
                row = cur.fetchone()
        return row

    def get_userID(self, userEmail):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT userid FROM UserAcc WHERE UserEmail= %s;", (userEmail,))
                row = cur.fetchone()
        return row[0]

    def get_is_admin(self, userID):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT isadmin FROM useracc WHERE userid=%s", (userID,))
                row = cur.fetchone()
        return row

    #tutorial table methods
    def add_tutorial(self, tutorial):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO tutorial(title, educatorid, platform, url, skill, length, info, ratingnum, tutorialrating)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING tutorialid;""", (tutorial.title, tutorial.educatorID, tutorial.platform,
                   tutorial.url, tutorial.skill, tutorial.length, tutorial.info, tutorial.ratingNum, tutorial.tutorialRating))
                conn.commit()
                rowcount = cur.fetchone()
        return rowcount
                
                

    def get_tutorial(self, tutorialID):
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT*FROM tutorial WHERE tutorialid = %s;", (tutorialID, ))
                row = cur.fetchone()
        return Tutorial(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

    def get_tutorials(self):
        tutorials = []
        with connect(self.dbinfo) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT*FROM tutorial;")
                rows = cur.fetchall()

        for row in rows:
            tutorials.append((row[0], Tutorial(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])))
        return tutorials

    def update_tutorial(self, tutorialID, tutorial):
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("""UPDATE Tutorial SET title=%s, educatorid=%s, platform=%s, url=%s, skill=%s, length=%s, info=%s WHERE tutorialid=%s; """,
                (tutorial.title, tutorial.educatorID, tutorial.platform, tutorial.url, tutorial.skill, tutorial.length, tutorial.info, tutorialID))
                conn.commit()
                rowcount = cur.rowcount
        return rowcount

    def remove_tutorial(self, tutorialID):
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Tutorial WHERE tutorialid=%s;", (tutorialID, ))
                conn.commit()
                rowcount = cur.rowcount
        return rowcount

    def get_tutorialPoints(self, tutorialid):
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("SELECT rating FROM ratingcomment WHERE tutorialid=%s;", (tutorialid, ))
                rows = cur.fetchall()
                
        return rows

    def refresh_tutorialRating(self, tutorialid):
        ratings = self.get_tutorialPoints(tutorialid)
        ratingnum = len(ratings)
        if ratingnum == 0:
            return None
        else:
            total = 0
            for rating in ratings:
                total += rating[0]
            
            avgRating = round(total/ratingnum, 2)
            with connect(self.dbinfo) as conn:  
                with conn.cursor() as cur:
                    cur.execute("UPDATE tutorial SET ratingnum=%s, tutorialrating=%s WHERE tutorialid=%s;", (ratingnum, avgRating, tutorialid))
                    rowcount = conn.commit()
            return rowcount

    # tutorialtopic table methods

    def assign_topic(self, tutorialid, topicid): #add operation
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("INSERT INTO tutorialtopic(tutorialid, topicid) VALUES (%s, %s);", (tutorialid, topicid))
                conn.commit()
                rowcount = cur.rowcount
        return rowcount
    
    def remove_tuttopic(self, tutorialid, topicid):
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tutorialtopic WHERE tutorialid = %s AND topicid = %s;", (tutorialid, topicid))
                conn.commit()
                rowcount = cur.rowcount
        return rowcount


    def get_topics_of(self, tutorialid):#returns the topics of passed tutorial
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("SELECT (topicid) FROM tutorialtopic WHERE tutorialid = %s;", (tutorialid, ))
                rows = cur.fetchall()
        return rows
    
    def get_topics_with(self, tutorialid): #returns all the topics but the one the tutorial has with the tutorial id
        with connect(self.dbinfo) as conn:  
                    with conn.cursor() as cur:
                        cur.execute("""SELECT topic.topicid, topic.topicname, tutorialtopic.tutorialid FROM topic  LEFT JOIN tutorialtopic 
                        ON topic.topicid=tutorialtopic.topicid AND tutorialtopic.tutorialid = %s ;""", (tutorialid, ))
                        rows = cur.fetchall()
        return rows

    def set_topics(self, tutorialid, topics): #Updates the topics of passed tutorial to passed topic list
        old_topics = self.get_topics_of(tutorialid)
        old_topics = [row[0] for row in old_topics]
        topics = [int(i) for i in topics]
        print("oldsod", old_topics)
        print("topcs: ",topics)
        #difference between list of old topics and new ones
        diff = list(list(set(old_topics)-set(topics)) + list(set(topics)-set(old_topics))) 
        print("diff: ", diff)
        for topicid in diff:
            if topicid in old_topics:
                self.remove_tuttopic(tutorialid, topicid)
            if topicid in topics:
                self.assign_topic(tutorialid, topicid)

    #enrollment table methods
    def add_enrollment(self, userid, tutorialid, status="In progress"):
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("INSERT INTO enrollment(userid, tutorialid, status) VALUES (%s, %s, %s);", (userid, tutorialid, status))
                conn.commit()
                rowcount = cur.rowcount
        return rowcount

    def get_enrollment(self, userid, tutorialid):#make this with join
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("SELECT enrollmentid, status FROM enrollment WHERE userid=%s AND tutorialid=%s;", (userid, tutorialid))
                row = cur.fetchone()
        return row

    def get_enrollments_of(self, userid):
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                #triple join
                cur.execute("""SELECT enrollmentid, title, platform, educatorname, enrollmenttime, status, e.tutorialid FROM enrollment AS e INNER JOIN
                 tutorial AS et ON e.userid = %s AND e.tutorialid = et.tutorialid INNER JOIN educator AS ed ON et.educatorid = ed.educatorid;""", (userid, ))

                row = cur.fetchall()
        return row


    def remove_enrollment(self, enrollmentid):
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("DELETE FROM enrollment WHERE enrollmentid = %s;", (enrollmentid, ))
                conn.commit()
                rowcount = cur.rowcount
        return rowcount

#rating comment table methods

    def add_rating(self, userid, tutorialid, rating, comment = None):
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("INSERT INTO ratingcomment(userid, tutorialid, rating, comment) VALUES (%s, %s, %s, %s);", (userid, tutorialid, rating, comment))
                conn.commit()
                rowcount = cur.rowcount
        return rowcount
    
    def get_tutorial_ratings(self, tutorialid):
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("""SELECT ratingid, r.userid, useremail, rating, comment, ratingtime FROM ratingcomment AS r INNER JOIN
                 useracc AS ru ON r.userid = ru.userid AND r.tutorialid = %s;""", (tutorialid, ))
                rows = cur.fetchall()
        return rows

    def update_rating(self, ratingid, rating, comment = None):
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("UPDATE ratingcomment SET rating = %s, comment = %s WHERE ratingid = %s;", (rating, comment, ratingid))
                conn.commit()
                rowcount = cur.rowcount
        return rowcount

    def has_rating(self, tutorialid, userid): #to check if a user has rated a tutorial
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("SELECT rating FROM ratingcomment WHERE tutorialid = %s AND userid = %s;", (tutorialid, userid))
                row = cur.fetchone()
        return row

    def delete_comment(self, ratingid):
        with connect(self.dbinfo) as conn:  
            with conn.cursor() as cur:
                cur.execute("DELETE FROM ratingcomment WHERE ratingid = %s;", (ratingid, ))
                conn.commit()
                rowcount = cur.rowcount
        return rowcount


db = Database("dbname=postgres user=postgres password=12345 host=localhost")
