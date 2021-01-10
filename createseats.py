import mysql.connector as mysql

def create_connection(name):
    
    try:
        db = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = name
        )
        return db
    
    except:
        print("error in creating connection")

def create_seats_withoutspecific(locid, numofseats, c):

    for i in range(1,numofseats+1):
        varq = "INSERT INTO seat (Seat_Number, Location_ID) VALUES ("
        query = varq+str(i)+", "+str(locid)+");"

        try:  
            cursor = c.cursor() 
            cursor.execute(query)
            c.commit()
        except:
            print("error in creating nonspecific seats")
            return False

def create_seats_specific(locid, numseatrow, numseatcolumn,c):
    numseat = 0
    for i in range(1, numseatcolumn+1):
        for j in range(1, numseatrow+1):
            numseat+=1
            varq = "INSERT INTO seat (Seat_Number, Location_ID, SeatRow, SeatColumn) VALUES ("
            query = varq+str(numseat)+", "+str(locid)+", "+str(j)+", "+str(i)+");"
            try:  
                cursor = c.cursor() 
                cursor.execute(query)
                c.commit()
            except:
                print("error in creating seats")
                return False

def initialize_availability(projectionid,c):
    try:
        cursor = c.cursor()
        #prwta vriskoyme to eventid apo projectionid
        query = "SELECT Event_ID FROM projection WHERE Projection_ID='"+str(projectionid)+"';"
        cursor.execute(query)
        records = cursor.fetchall()
        eventid = records[0][0]        
        
        #vriskoyme to locid apo eventid
        query = "SELECT Location_ID FROM event WHERE Event_ID='"+str(eventid)+"';"
        cursor.execute(query)
        records = cursor.fetchall()
        locationid = records[0][0]

        #epeita apo ton pinaka seats pairnoyme oles tis diathesimes theseis
        query = "SELECT Seat_ID FROM seat WHERE Location_ID='"+str(locationid)+"';"
        cursor.execute(query)
        list_of_seats = cursor.fetchall()

        #meta gia kathe thesi sto antistoixo location to shmeiwnoyme ws available alability=1
        for seat in list_of_seats:
            query = "INSERT INTO available (Seat_ID, SeatAvailability, Projection_ID) VALUES ("+str(seat[0])+",1,"+ str(projectionid) +");"
            cursor.execute(query)
            c.commit()
        
    except:
        print("error in initialization")
        return False


    
database = "booking"
db = create_connection(database)

create_seats_withoutspecific(1,100,db)
create_seats_withoutspecific(2,200,db)
create_seats_withoutspecific(3,120,db)
create_seats_specific(4,4,8,db)
create_seats_withoutspecific(5,100,db)
for i in range(1,16):
    initialize_availability(i,db)

