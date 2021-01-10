import mysql.connector as mysql
from municipality import *
import pandas as pd


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
    
    mail = input("Insert E-mail: ")
    phone = input("Insert Phone number: ")
    while(not phone.isnumeric()):
        phone = input("Phone consists of numbers only!\nPlease insert Phone number: ")
    fname = input("Insert First name: ")
    lname = input("Insert Last name: ")
    print("We are almost there, now let's figure out your sign in credentials")
    
    while(True):
        username = input("Insert what you wish to be your account username: ")
        if (uidexists(username,c)==0):
            break;
        print("This username already exists, please try again: ")
        
    password = input("Insert your password (we recommend at least 8 characters,one number and one letter): ")

    query = "INSERT INTO customer (Username, Password, Email, Phone, CustomerName, CustomerSurname)VALUES (%s,%s,%s,%s,%s,%s);"
    
    try:  
        cursor = c.cursor() 
        cursor.execute(query, (username,password,mail,phone,fname,lname) )
        c.commit()
        print("You signed up succesfully! Now log in to your new account:")
    except:
        print("Error occured while signing up...")
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
        
def show_cities(c):
    cursor = c.cursor()
    query = "SELECT DISTINCT Town FROM event JOIN location ON event.Location_ID = location.Location_ID ;"
    cursor.execute(query)
    records = cursor.fetchall()
    cities ={}
    for i in range(0,len(records)):
        print("City Code: "+str(i)+"| City: "+records[i][0])
        cities[i] = records[i][0]
    return cities

def choose_city(city, c):
    try:
        cursor = c.cursor()
        query = "SELECT fix.Event_ID, fix.EventTitle, fix.EventType FROM (SELECT e.Event_ID, e.EventTitle, e.EventType, e.Location_ID FROM projection as p JOIN event as e on p.Event_ID=e.Event_ID GROUP BY e.Event_ID ORDER BY p.ProjectionDate) as fix JOIN location ON fix.Location_ID = location.Location_ID WHERE location.Town=%s;"
        cursor.execute(query,(city,))
        records = cursor.fetchall()

        column_names=["Event Code","Event Title","Event Type"]
        list_of_records = [list(item) for item in records]
        df = pd.DataFrame(list_of_records, index=None, columns=column_names)
        print(df.to_string(index=False))

    except:
        return False

def select_city(c):
    cities = show_cities(c)
    print("Please type a city code: ")
    citycode = input()
    city = cities[int(citycode)]
    choose_city(city, c)
    
    
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
            print("Address: ",location[4],",",location[5],",",location[6],",",location[3])
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
            print("Event Code: ",event[0])
            print("Event Title: ",event[1])
            print("Event Type: ",event[2])
            print("Event Description: ",event[3])
            if (event[4]=='0'):
                print("Event Price: free entrance")
            else:
                print("Event Price: ",event[4],"Euro")
            print("Event Location:", getlocation(str(event[6]),c))
            print("\n")

            show_projections(event[0],c)

        return [event[1],float(event[4]),event[6]]

    except:
        print("Not a valid event code!")
        return False

def show_projections(eventcode, c):

    cursor = c.cursor()
    cursor.execute("SELECT Projection_ID, ProjectionDate, ProjectionTime, Duration FROM projection WHERE Event_ID=%s;",(eventcode,))
    records = cursor.fetchall()

    column_names=["Projection Code","Projection Date","Projection Time","Duration"]
    list_of_records = [list(item) for item in records]
    df = pd.DataFrame(list_of_records, index=None, columns=column_names)
    print(df.to_string(index=False))


    
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
        cursor.execute("SELECT DiscountPercentage FROM discount WHERE Discount_ID=%s AND Event_ID=%s;",(discountcode,eventcode))
        records = cursor.fetchall()
        
        if(len(records)==0):
            return False
        
        return records[0][0]

    except:
        return False
    
def show_available_seats(projectionid, c):
    try:
        cursor = c.cursor()
        cursor.execute("SELECT seat.Seat_ID, seat.SeatRow, seat.SeatColumn FROM available JOIN seat ON available.Seat_ID = seat.Seat_ID WHERE available.SeatAvailability=1 AND available.Projection_ID=%s;",(projectionid,))
        records = cursor.fetchall()
        
        if(len(records)==0):
            print("No available seats for that projection or not a valid projection code")
            return False;

        if( records[0][2] ):
            column_names=["Seat Code","Row","Column"]
            list_of_records = [list(item) for item in records]
            df = pd.DataFrame(list_of_records, index=None, columns=column_names)
            print(df.to_string(index=False))
            

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

    file_name = "booking" + str(projid)+str(seatid)+".txt"
    
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
        
    except:
        print("Error in booking ticket")
        return False

def isint(st):
    try: 
        int(st)
        return True
    
    except:
        return
    
def isflt(st):
    try: 
        float(st)
        return True
    
    except:
        return False
    
def ticket_booking(customer, c):
    select_city(c)
    while(1):
        print("Insert EVX, where X is an event code, to see more information about it, or BACK to go back")
        command = input()
        if(command=="BACK"):
            break
        if(command[:2] == "EV" and isint(command[2:])):
            [eventn, cost, locationcode] = showevent(command[2:],c)
            print("If you want to book this event type BOOK PRX, where X is the wanted projection code",
                  "or type LOCATION for more information about the location of the event")
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
                            disnum = check_discount_code(command[2:], discode, c)
                    else:
                        discode = False
                        
                    if(check_seat(seatcode, c)):
                        book_seat(seatcode, projectioncode, c)
                        create_ticket(customer, projectioncode, seatcode, discode, c)
                        if(discode == False):
                            disnum = 0
                        ticket_file(eventn, projectioncode, prj_date, prj_time, seatcode, cost, disnum)
    return True


def search_cost(c):

    print("Please type a maximum event cost")
    cost = input()
    while (not(isflt(cost))):
        print("Please type a maximum event cost")
        cost = input()        
    cost = float(cost)    
    try:
        cursor = c.cursor()
        query = "SELECT Event_ID, EventTitle, EventType, EventCost FROM event WHERE EventCost<%s ;"
        cursor.execute(query,(cost,))
        records = cursor.fetchall()

        column_names=["Event Code","Event Title","Event Type","Event Cost"]
        list_of_records = [list(item) for item in records]
        df = pd.DataFrame(list_of_records, index=None, columns=column_names)
        print(df.to_string(index=False))


    except:
        return False
    
def Give_Date():
    print("\nEnter Projection Date:\nFORMAT: XXXX-XX-XX (YEAR-MONTH-DAY)")
    Year=input("Enter Year:")
    Month=input("Enter Month:")
    Day=input("Enter Day:")
    ProjectionDate=str(Year + "-" + Month + "-" + Day)
    print(ProjectionDate)
    if(not check_DATE(Year,Month,Day)):
        print("\nWrong Data Type inserted\n")
        return
    return ProjectionDate;

def search_date(c):
    cursor = c.cursor()
    print("Search Starting Date:")
    start_date=Give_Date()
    print(start_date)
    if(start_date==1):
        return 0;
    print("Search Ending Date:")
    end_date=Give_Date()
    print(end_date)
    if(end_date==1):
        return 0;
    query="SELECT e.Event_ID,e.EventTitle,p.Projection_ID,p.projectiondate FROM event AS e JOIN projection AS p ON e.Event_ID=p.Event_ID WHERE p.ProjectionDate BETWEEN '" + start_date + "' AND '" + end_date + "' ORDER BY e.Event_ID,p.Projection_ID"
    cursor.execute(query,)
    items=cursor.fetchall()
    print("\n-- Search Results -- \n")
    list_of_items = [list(item) for item in items]
    df = pd.DataFrame(list_of_items, index=None, columns=["Event_Code","Event_Title","Projection_ID","Projection_Date"])
    print(df.to_string(index=False))
    return 0;

def search_seats(c):

    print("Please type how many seats available you want per event")
    numseats = input()
    while (not(isint(numseats))):
        print("Please type how many seats available you want per event")
        numseats = input()
    numseats = int(numseats)    
    
    cursor = c.cursor()
    query = "SELECT event.Event_ID ID, event.EventTitle Title,SUM(sts.SeatAvailability) Aval, COUNT(sts.SeatAvailability) Tot FROM (SELECT projection.Event_ID, available.SeatAvailability FROM projection JOIN available ON projection.Projection_ID = available.Projection_ID ) as sts JOIN event ON sts.Event_ID= event.Event_ID GROUP BY event.Event_ID HAVING (SUM(sts.SeatAvailability)>%s) ;"
    cursor.execute(query,(numseats,))
    records = cursor.fetchall()
        
    column_names=["Event Code","Event Title","Available Seats","Total Seats"]
    list_of_records = [list(item) for item in records]
    for i in range(0,len(list_of_records)):
        list_of_records[i][2] = int(list_of_records[i][2])
    df = pd.DataFrame(list_of_records, index=None, columns=column_names)
    print(df.to_string(index=False))
    
def info(c):
    print("Type COST to search for events up to a certain cost, DATE to search for events via date, or SEATS to see the number of available seats per event")
    search_query = input()
    while (not(search_query in ["COST","DATE","SEATS"])):
            print("Type COST to search for events up to a certain cost, DATE to search for events via date, or SEATS to see the number of available seats per event")
            search_query = input()
    if (search_query=="COST"):
           search_cost(c)
    elif (search_query=="DATE"):
           search_date(c)
    else:
        search_seats(c)
    
def user_node(c):
    print("Hello, welcome to our ticket booking system for cultural events")
    print("If you already have an account you can sign (i)n or you can sign (u)p, or type 0 to exit")
    answer = input()
    while(answer not in ["i","u","0"]):
        answer = input("Be careful! Press (i) to sign in, (u) to sign up or 0 to exit: ")
    if(answer=="u"):
        signup(c)
        print("Now you can sign in!")
        customer = login(c)
    if(answer=="i"):
        customer = login(c)

    while(1):
        action = input("To view events or book type SHOW EVENTS, or INFO to view specific events based on different searches, or LOG OUT to log out of your account\n")
        while(action not in ["SHOW EVENTS","LOG OUT","INFO"]):
            print("No recognised command")
            action = input("To view events type SHOW EVENTS, or INFO to view specific events based on different searches , or LOG OUT to log out of your account")
        if(action=="SHOW EVENTS"):
            ticket_booking(customer, c)

        elif(action=="LOG OUT"):
            break

        elif(action=="INFO"):
            info(c)
    

def welcome_node():
    database = "booking"
    db = create_connection(database)
    cursor=db.cursor()
    
    print("Welcome to our booking system, type '1' to enter as a user or '2' to enter as a municipality")
    while(1):
        use = input()
        if (use=='1'):
            user_node(db)
        elif (use=='2'):
            municipality_dialogue(db,cursor)
        else:
            print( "Choose either 1(user) or 2 (municipality)" )
        print("Welcome to our booking system, type '1' to enter as a user or '2' to enter as a municipality")

def main():
    welcome_node()   
    
if __name__ == '__main__':
    main()
