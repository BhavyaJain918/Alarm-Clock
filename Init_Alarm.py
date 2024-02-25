import mysql.connector
def create_database(username , password):
    try:
        mydb = mysql.connector.connect(host = "localhost" , user = username, passwd = password)
        mycursor = mydb.cursor()
        try:
            mycursor.execute("CREATE DATABASE Clock")
            mycursor.execute("USE Clock")
            mycursor.execute("CREATE TABLE Alarm (Time varchar(10) NOT NULL , Date varchar(15) NOT NULL , Message varchar(40) , UNIQUE(Time , Date))")
            mydb.commit()
            mycursor.close()
            mydb.close()
            return 0
        except mysql.connector.errors.DatabaseError as d:
            mycursor.close()
            mydb.close()
            return d.errno
    except mysql.connector.errors.ProgrammingError as e:
        return (f"Error occurred: {e}")
if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    print(create_database(username , password))