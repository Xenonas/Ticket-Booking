import mysql.connector as mysql
from municipality import *

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
        print("Error creating db...")

def signup(c):
    
    mail = input("Insert E-mail...")
    phone = input("Insert Phone number...")
    fname = input("Insert First name...")
    lname = input("Insert Last name...")
    print("We are almost there, now let's figure out your sign in credentials")
    
    while(True):
        username = input("Insert what you wish to be your account username...")
        if (uidexists(username,c)==0):
            break;
        print("This username already exists, please try again...")
        
    password = input("Insert your password (we recommend at least 8 characters,one number and one letter)")

    query = "INSERT INTO customer (Username, Password, Email, Phone, CustomerName, CustomerSurname)VALUES (%s,%s,%s,%s,%s,%s);"
    
    try:  
        cursor = c.cursor() 
        cursor.execute(query, (username,password,mail,phone,fname,lname) )
        c.commit()
        print("You signed up succesfully! Now log in to your new account:")
    except:
        print("Error siging up...")
        return False

def uidexists(uname,c):

    query = "SELECT Password FROM customer WHERE Username=%s;"
    try:  
        cursor = c.cursor() 
        cursor.execute(query,(uname,))
        userpass = cursor.fetchall()
        
        if(userpass==[]):
            return 0;
        return userpass[0][0];
    except:
        print("mistake in trying to check if uid exists")
        return False

def munidexists(muname,c):

    query = "SELECT MunPassword FROM municipality WHERE MunUsername=%s;"
    try:  
        cursor = c.cursor() 
        cursor.execute(query,(muname,))
        munpass = cursor.fetchall()
        
        if(munpass==[]):
            return 0;
        return munpass[0][0];
    except:
        return False

def login(c):
    
    while (True):
        username = input("Insert your username:")
        password = input("Insert your password:")

        if(uidexists(username,c)==password):
            break;

        print("Not correct cridentials, please try again.")
        
    query = "SELECT Cust_ID FROM customer WHERE Username=%s;"
    try:  
        cursor = c.cursor() 
        cursor.execute(query,(username,))
        userid = cursor.fetchall()[0][0]
        return userid;
    except:
        return False


def munclogin(c):
    
    while (True):
        username = input("Insert municipality username:")
        password = input("Insert municipality password:")

        if(munidexists(username,c)==password):
            break;

        print("Not correct cridentials, please try again.")

    
def select_all_events(c):
    try:
        cursor = c.cursor()
        cursor.execute("SELECT * FROM event;")
        records = cursor.fetchall()
        
        for event in records:
            print("Event Code:",event[0],"|",end=" ")
            print("Event Title: ",event[1],"|",end=" ")
            print("Event Type: ",event[2])

    except:
        return False
    
def showlocation(locationid,c):
    try:
        cursor = c.cursor()
        query = "SELECT * FROM location WHERE Location_ID=%s;"
        cursor.execute(query,(locationid,))
        records = cursor.fetchall()
        
        for location in records:
            print("Event Code:",location[0])
            print("Location Name: ",location[1])
            print("Location Type: ",location[2])
            print("Town: ",location[3],"|",end=" ")
            print("Street: ",location[4],"|",end=" ")
            print("Street Number: ",location[5],"|",end=" ")
            print("Postal Code: ",location[6])
            print("\n")
            
    except:
        return False

def getlocation(locationid,c):
    try:
        cursor = c.cursor()
        query = "SELECT * FROM location WHERE Location_ID=%s;"
        cursor.execute(query,(locationid,))
        records = cursor.fetchall()
        
        for location in records:
            return location[1]
            
    except:
        return False
def showevent(eventid,c):
    try:
        cursor = c.cursor()
        query = "SELECT * FROM event WHERE Event_ID=%s;"
        cursor.execute(query,(eventid,))
        records = cursor.fetchall()
        
        if (len(records)==0):
            print("This event code does not exist!")
            return False
        
        for event in records:
            print("Event Code:",event[0])
            print("Event Title: ",event[1])
            print("Event Type: ",event[2])
            print("Event Description: ",event[3])
            if (event[4]=='0'):
                print("Event Price: free entrance")
            else:
                print("Event Price: ",event[4],"€")
            print("Event Location:", getlocation(str(event[6]),c))
            print("\n")

            show_projections(event[0],c)

        return [event[1],float(event[4]),event[6]]

    except:
        print("Not a valid event code!")
        return False

def show_projections(eventcode, c):
    try:
        cursor = c.cursor()
        cursor.execute("SELECT * FROM projection WHERE Event_ID=%s;",(eventcode,))
        records = cursor.fetchall()
        
        for projection in records:
            print("Projection Code:", projection[0], "|", end=" ")
            print("Projection Date: ", projection[1], "|", end=" ")
            print("Projection Time: ", projection[2], "|", end=" ")
            print("Duration: ", projection[3])


    except:
        return False
    
def get_projection(projectioncode, c):
    try:
        cursor = c.cursor()
        cursor.execute("SELECT * FROM projection WHERE Projection_ID=%s;",(projectioncode,))
        records = cursor.fetchall()
        
        for projection in records:
            return [str(projection[1]),str(projection[2])]

    except:
        return False
        
    
def show_discounts(eventid, c):
    try:
        cursor = c.cursor()
        cursor.execute("SELECT * FROM discount WHERE Event_ID=%s;",(eventid,))
        records = cursor.fetchall()
        
        for discount in records:
            print("Discount Code:", discount[0], "|", end=" ")
            print("Discount Type: ", discount[2], "|", end=" ")
            print("Discount Percentage: ", int(discount[3]*100),"%")
            print("\n")

    except:
        return False
    
def check_discount_code(eventcode, discountcode, c):
    try:
        cursor = c.cursor()
        cursor.execute("SELECT * FROM discount WHERE Discount_ID=%s AND Event_ID=%s;",((discountcode),(eventcode,)))
        records = cursor.fetchall()
        
        if(len(records)==0):
            return False

        return True

    except:
        return False
    
def show_available_seats(projectionid, c):
    try:
        cursor = c.cursor()
        cursor.execute("SELECT * FROM available JOIN seat ON available.Seat_ID = seat.Seat_ID WHERE Projection_ID=%s;",(projectionid,))
        records = cursor.fetchall()
        
        if(len(records)==0):
            print("No available seats for that projection or not a valid projection code")
            return False;

        if( records[0][7] ):
            for seat in records:
                print("Seat Code:", seat[0], end="|")
                print("Row: ", seat[7], end="|")
                print("Column: ", seat[8])
                
            return True
        
        else:
            return False

    except:
        return False

def check_if_discount_exists(eventid, c):
    try:
        cursor = c.cursor()
        cursor.execute("SELECT * FROM discount WHERE Event_ID=%s;",(eventid,))
        records = cursor.fetchall()

        if(len(records)==0):
            return False
        
        return True
        
    except:
        print("Error")
        return False
    
def check_seat(seatid, c):
    try:
        cursor = c.cursor()
        cursor.execute("SELECT * FROM available WHERE Seat_ID=%s;",(seatid,))
        records = cursor.fetchall()
        
        if(len(records)==0):
            print("No available seats for that projection or not a valid projection code")
            return False
        if(records[0][1]==0):
            print("This seat is already booked!")
            return False
        return seatid
    except:
        print("Error in checking seat")
        return False
    
def get_random_seat(projectionid, c):
    try:
        cursor = c.cursor()
        cursor.execute("SELECT MIN(Seat_ID) FROM available WHERE Projection_ID=%s AND SeatAvailability=1;",(projectionid,))
        records = cursor.fetchall()
        return(records[0][0])
    except:
        print("Problem during trying to generate seat");
        return False
        
def book_seat(seatid, projectionid, c):

    try:
        cursor = c.cursor()
        query ="UPDATE available SET SeatAvailability=0 WHERE Seat_ID=%s AND Projection_ID=%s;"
        cursor.execute(query,(seatid,projectionid))
        c.commit()
    except:
        print("Problem during trying to book seat")
        return False
    
def ticket_file(eventn, projid, projdate, projtime, seatid, cost, discount):
    text = "Event name:"+ str(eventn)+"\nDate:"+str(projdate)+" Time:"+str(projtime)+"\nSeat number:"+str(seatid)
    text = text + " Cost:"+str( cost*(1-discount) )
    text.encode('ascii', 'ignore')

    file_name = str(projid)+str(seatid)+".txt"
    
    f = open(file_name, "a", encoding='utf8')
    f.write(text)
    f.close()
   
def create_ticket(customerid, projectionid, seatid, discountid,c):
    if(discountid):
        varq = "INSERT INTO ticket (Cust_ID, Projection_ID, Seat_ID, Discount_ID) VALUES ("

        query = varq+str(customerid) + "," + str(projectionid) + "," + str(seatid) + "," + str(discountid) +");"
    else:
        varq = "INSERT INTO ticket (Cust_ID, Projection_ID, Seat_ID) VALUES ("

        query = varq + str(customerid) + "," + str(projectionid) + "," + str(seatid) + ");"
   
    try:  
        cursor = c.cursor() 
        cursor.execute(query)
        c.commit()
        print("You booked your ticket succesfully!")
        
    except Error:
        print("Error in booking ticket")
        return False

def isint(st):
    try: 
        int(st)
        return True
    
    except:
        return False
    
def ticket_booking(customer, c):
    select_all_events(c)
    while(1):
        print("Insert EVX, where X is an event code, to see more information about it")
        command = input()
        if(command[:2] == "EV" and isint(command[2:])):
            [eventn, cost, locationcode] = showevent(command[2:],c)
            print("If you want to book this event write BOOK PRX, where X is the wanted projection code",
                  "or write LOCATION for more information about the location of the event")
            book = input()
            if ( book=="LOCATION" ):
                showlocation(locationcode,c)
            projectioncode = book[7:]
            if(book[:7] == "BOOK PR" and isint(projectioncode)):
                [prj_date,prj_time] = get_projection(projectioncode, c)
                check_specific_seat = show_available_seats(projectioncode,c)
                if( check_specific_seat ):
                    print("Type a seat code or RANDOM if you do not care for specific seating")
                    seatcode = input()
                else:
                    seatcode = "RANDOM"
                if(seatcode=="RANDOM"):
                    seatcode = get_random_seat(projectioncode, c)
                if (isint(seatcode) and check_seat(seatcode, c) ):
                    if(check_if_discount_exists(command[2:], c)):
                        show_discounts(command[2:], c)
                        print("Type a discount code if you are eligible for one or type NO")
                        discode = input()
                        if(discode=="NO"):
                            discode = False
                        elif( not(check_discount_code(command[2:], discode, c)) ):
                            print("Not correct discount code")
                    else:
                        discode = False
                        
                    if(check_seat(seatcode, c)):
                        book_seat(seatcode, projectioncode, c)
                        create_ticket(customer, projectioncode, seatcode, discode, c)
                        if(discode == False):
                            discode = 0
                        ticket_file(eventn, projectioncode, prj_date, prj_time, seatcode, cost, discode)

def user_node(c):
    print("Hello, welcome to our ticket booking system for cultural events")
    print("If you already have an account you can sign (i)n or you can sign (u)p")
    answer = input()
    
    if(answer=="u"):
        signup(c)
        print("Now you can sign in!")
        customer = login(c)
    if(answer=="i"):
        customer = login(c)
    print("customerid",customer)

    print("To view events type SHOW EVENTS, or LOG OUT to log out of your account")
    action = input()
    if(action=="SHOW EVENTS"):
        ticket_booking(customer, c)

    elif(action=="LOG OUT"):
        pass

    else:
        print("No recognised command")

def welcome_node():
    database = "gamw"
    db = create_connection(database)
    print("Welcome to our booking system, type '1' to enter as a user or '2' to enter as a municipality")
    while(1):
        use = input()
        if (use=='1'):
            user_node(db)
        elif (use=='2'):
            municipality_dialogue(db)
        else:
            print( "Choose either 1(user) or 2 (municipality)" )

def main():
    welcome_node()   
    
if __name__ == '__main__':
    main()
