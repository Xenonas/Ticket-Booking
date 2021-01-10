import mysql.connector as mysql
import datetime
import pandas as pd
import pathlib

def munidexists(muname,c):

    query = "SELECT MunPassword FROM municipality WHERE Username='"+muname+"';"
    try:  
        cursor = c.cursor() 
        cursor.execute(query)
        munpass = cursor.fetchall()
        
        if(munpass==[]):
            return 0;
        return munpass[0][0];
    except:
        print("Error during checking whether municipality id exists")
        return False

def munclogin(db):
    
    while (True):
        username = input("Insert municipality username:")
        password = input("Insert municipality password:")

        if(munidexists(username,db)==password):
            cursor = db.cursor()
            cursor.execute("SELECT Municipality_ID FROM municipality WHERE Username='"+ username +"';")
            Municipality_ID=str(cursor.fetchone()[0]) 
            return Municipality_ID;
        print("Not correct cridentials, please try again.")
         

def ID_exists(ID,string,db):

    query = "SELECT " +string+ "_ID FROM " + string + " WHERE " + string +"_ID=%s"
    try:  
        cursor = db.cursor() 
        cursor.execute(query,(ID,))
        check_query = cursor.fetchall()
        
        if(check_query==[]):
            return 0;
        print(string+ "_ID is valid!")
        return 1;
    except:
        print("error during checking whether code exists")
        return False

def choose_action():
    MatricesList=["SHOW","ADD","DELETE","UPDATE","BOOKING"]
    action_num=6
    while action_num not in [1,2,3,4,5]:
        action_num=int(input("Press 1 to show a matrix\nPress 2 to add a query\nPress 3 to delete a query\nPress 4 to update a query\nPress 5 to see the BOOKINGS\n"))
    choice=MatricesList[action_num-1]
    return action_num

def choose_number_of_actions(action_num):
    MatricesList=["SHOW","ADD","DELETE","UPDATE"]
    action=MatricesList[action_num-1]
    times='-1'
    while not times.isnumeric(): 
        times=input("\nType the number of queries (integer value) you want to " + action + " or type 0 to exit: ")
    print("\nYou have chosen to " + action + " a query " + times + " time(s)\n")
    return int(times)
 
def select_matrix():
    MatricesList=["event","projection","discount","location"]
    x=5
    while x not in [1,2,3,4]:
        x=int(input("Press 1 for Event, 2 for Projection, 3 for Discount, 4 for Location:\n"))
    choice=MatricesList[x-1]
    return choice

def showall(matrix_name,Mun_ID,db):
    try:
        cursor = db.cursor()
        print("\n--- " + matrix_name + " ---\n")
        if(matrix_name=="location"):
            query="SELECT Location_ID,VenueName,VenueType,Town,Street,StreetNumber,PostalCode FROM " + matrix_name + " WHERE Municipality_ID=%s"
            column_names=["Location_Code","Venue_Name","Venue_Type","Town","Street","Street_Number","Postal_Code"]
        elif(matrix_name=="event"):
            query="SELECT Event_ID,EventTitle,EventType,EventDescription,EventCost FROM " + matrix_name + " WHERE Municipality_ID=%s"
            cursor.execute(query,(Mun_ID,))
            items=cursor.fetchall()
            for item in items:
                print("Event Code:",item[0])
                print("Event Title: ",item[1])
                print("Event Type: ",item[2])
                print("Event Description: ",item[3])
                print("Event Price: ",item[4],"€")
                print("\n")
            return 0;
        elif(matrix_name=="projection"):
            query="SELECT mat.Projection_ID,mat.ProjectionDate,mat.ProjectionTime,mat.duration FROM " + matrix_name + " AS mat JOIN event AS e ON mat.event_ID=e.event_ID WHERE e.Municipality_ID=%s"
            column_names=["Projection_Code","Projection_Date","Projection_Time","Duration"]
        else:
            query="SELECT mat.Discount_ID,mat.DiscountType,mat.DiscountPercentage FROM " + matrix_name + " AS mat JOIN event AS e ON mat.event_ID=e.event_ID WHERE e.Municipality_ID=%s"
            column_names=["Discount_Code","Discount_Type","Discount_Percentage"]
        cursor.execute(query,(Mun_ID,))
        items=cursor.fetchall()
        list_of_items = [list(item) for item in items]
        df = pd.DataFrame(list_of_items, index=None, columns=column_names)
        print(df.to_string(index=False))
       
    except:
        print("\nerror showing matrix")
        return False

def show_Event_ID(db,Mun_ID):
    try:
        cursor = db.cursor()
        query="SELECT Event_ID,EventTitle FROM event WHERE Municipality_ID=%s ORDER BY EventTitle" 
        cursor.execute(query,(Mun_ID,))
        items=cursor.fetchall()
        list_of_items = [list(item) for item in items]
        column_names=["Event_Code","Event_Title"]
        df = pd.DataFrame(list_of_items, index=None, columns=column_names)
        print(df.to_string(index=False))
        Event_ID=int(input("\nEnter Event_ID: "))
        for i in range(len(list_of_items)):
            if(list_of_items[i][0]==Event_ID):
                return Event_ID
        return 0;
    
    except:
        print("\nError on event ID validation\n")
        return False

def show_Location_ID(db,Mun_ID):
    try:
        cursor = db.cursor()
        query="SELECT Location_ID,VenueName,VenueType,Town FROM location WHERE Municipality_ID=%s" 
        cursor.execute(query,(Mun_ID,))
        items=cursor.fetchall()
        list_of_items = [list(item) for item in items]
        column_names=["Location_Code","Venue_Name","Venue_Type","Town"]
        df = pd.DataFrame(list_of_items, index=None, columns=column_names)
        print(df.to_string(index=False))
        Location_ID=int(input("\nEnter Location_ID: "))
        for i in range(len(list_of_items)):
            if(list_of_items[i][0]==Location_ID):
                return Location_ID
        return 0;
    
    except:
        print("\nerror showing location ID")
        return False
    
def add_event(cursor,db,Mun_ID):
    try:
        EventTitle=str(input("\nEnter new event title: "))
        print("Enter new event type:\nΕνδεικτικά: (Παράσταση,Ταινία,Κονσέρτο,Συναυλία,Ομιλία)")
        EventType=str(input())
        EventDescription=str(input("Enter new event description: "))
        EventCost=int(input("Enter new event cost: "))
        Municipality_ID=int(Mun_ID)
        string="Municipality"
        print("Enter Location ID:\n(Choose one of the already existing)\n")
        Location_ID=show_Location_ID(db,Mun_ID)
        if(Location_ID==0):
            print("Location NOT in your Municipality\n")
            return 0;
        string="Location"
        check=ID_exists(Location_ID,string,db)
        if(check==0):
            print("\nLocation_ID does not exist\nQuery was not added...\n ")
            return 0;
        values=[EventTitle,EventType,EventDescription,EventCost,Municipality_ID,Location_ID]
        cursor.execute("INSERT INTO event (EventTitle,EventType,EventDescription,EventCost,Municipality_ID,Location_ID) VALUES (%s,%s,%s,%s,%s,%s)",(values))
        db.commit()
        print("\nData inserted succesfully!!\n")
    except:
        print("\nWrong Data Type inserted")
        return False

def check_DATE(Year,Month,Day):
    if(str(Year+Month+Day).isnumeric()):
        if(len(Year)==4 and len(Month)==2 and len(Day)==2):
            if(Month[0]=='0'):
                Month=Month[1]
            if(Day[0]=='0'):
                Day=Day[1]
            try:
                if(datetime.date(year=int(Year),month=int(Month),day=int(Day))>datetime.date.today()):
                    return 1;
            except:
                    return 0;
        else:    
            return 0;
    return 0;

def check_TIME(Hour,Minutes,Seconds):
    if(str(Hour+Minutes+Seconds).isnumeric and len(Hour)==2 and len(Minutes)==2 and len(Seconds)==2):
        if(int(Hour)//25==0 and int(Minutes)//60==0 and int(Seconds)//60==0):
            return 1;
        return 0;
    return 0;

def initialize_availability(projectionid,c):
    try:
        cursor = c.cursor()

        query = "SELECT Event_ID FROM projection WHERE Projection_ID='"+str(projectionid)+"';"
        cursor.execute(query)
        records = cursor.fetchall()
        eventid = records[0][0]

        query = "SELECT Location_ID FROM event WHERE Event_ID='"+str(eventid)+"';"
        cursor.execute(query)
        records = cursor.fetchall()
        locationid = records[0][0]

        query = "SELECT Seat_ID FROM seat WHERE Location_ID='"+str(locationid)+"';"
        cursor.execute(query)
        list_of_seats = cursor.fetchall()

        for seat in list_of_seats:
            query = "INSERT INTO available (Seat_ID, SeatAvailability, Projection_ID) VALUES ("+str(seat[0])+",1,"+ str(projectionid) +");"
            cursor.execute(query)
            c.commit()

    except:
        print("\nerror in initialization")
        return False
    
def add_projection(cursor,db,Mun_ID):
    try:
        print("\nEnter Projection Date:\nFORMAT: XXXX-XX-XX (YEAR-MONTH-DAY)")
        Year=input("Enter Year: ")
        Month=input("Enter Month: ")
        Day=input("Enter Day: ")
        ProjectionDate=str(Year + "-" + Month + "-" + Day)
        print(ProjectionDate)
        if(not check_DATE(Year,Month,Day)):
            print("\nWrong Data Type inserted")
            return 0;
        print("Enter Projection Time:\nFORMAT: XX:XX:XX (HOUR:MINUTE:SECOND)\n")
        Hour=input("Enter Hour: ")
        Minutes=input("Enter Minutes: ")
        Seconds=input("Enter Seconds: ")
        ProjectionTime=Hour + ":" + Minutes + ":" + Seconds
        if(not check_TIME(Hour,Minutes,Seconds)):
            print("\nWrong Data Type inserted\n")
            return 0;
        Duration=input("Enter Duration: ")
        print("Enter Event_ID:\n(Choose one of the already existing)\n")
        Event_ID=show_Event_ID(db,Mun_ID)
        if(Event_ID==0):
            print("Event NOT organised by your Municipality\nInvalid Insertion\n")
            return 0;
        string="Event"
        check=ID_exists(Event_ID,string,db)
        if(check==0):
            print("\nEvent_ID does not exist\n ")
            return 0;
        values=[ProjectionDate,ProjectionTime,Duration,Event_ID]
        cursor.execute("INSERT INTO projection (ProjectionDate,ProjectionTime,Duration,Event_ID) VALUES (%s,%s,%s,%s)",(values))
        db.commit()
        print("\nData inserted succesfully!!\n")
        query="SELECT MAX(Projection_ID) FROM Projection"
        cursor.execute(query)
        Projection_ID=list(cursor.fetchone())
        Projection_ID=Projection_ID[0]
        initialize_availability(Projection_ID,db)
    except:
        print("\nWrong Data Type inserted\n")
        return False

def add_discount(cursor,db,Mun_ID):
    try:
        print("Enter Event_ID:\n(Choose one of the already existing)\n")
        Event_ID=show_Event_ID(db,Mun_ID)
        if(Event_ID==0):
            print("Event NOT organised by your Municipality\n")
            return;
        
        string="Event"
        check=ID_exists(Event_ID,string,db)
        if(check==0):
            print("\nEvent_ID does not exist!!\n ")
            return 0;
        DiscountType=str(input("Enter Discount Type:\nΕνδεικτικά: (Φοιτητική,Άνεργοι,ΑΜΕΑ,Πολύτεκνοι)"))
        DiscountPercentage=float(input("Enter Discount Percentage (0-1, float number): "))
        if(DiscountPercentage>1.0 or DiscountPercentage<0.0):
            print("\nWARNING:\nWrong Data Type inserted")
            return 0;
        values=[Event_ID,DiscountType,DiscountPercentage]
        cursor.execute("INSERT INTO discount (Event_ID,DiscountType,DiscountPercentage) VALUES (%s,%s,%s)",(values))
        db.commit()
        print("\nData inserted succesfully!!\n")
    except:
        print("\nWARNING:\nWrong Data Type inserted\n")
        return False
    
def addall(matrix_name,db,municipality_ID):
    try:
        cursor = db.cursor()
        if(matrix_name=="event"):
            add_event(cursor,db,municipality_ID)
        elif(matrix_name=="projection"):
            add_projection(cursor,db,municipality_ID)
        else:
            add_discount(cursor,db,municipality_ID)
    except:
        return False

def check_deletion_ID(db,municipality_ID,matrix_name,ID):
    try:
        cursor = db.cursor()
        query="SELECT Event_ID FROM " + matrix_name + " WHERE " + matrix_name + "_ID=%s" 
        cursor.execute(query,(ID,))
        query_to_delete=list(cursor.fetchall()[0])
        query="SELECT Event_ID FROM Event WHERE Municipality_ID=%s"
        cursor.execute(query,(municipality_ID,))
        items=cursor.fetchall()
        list_of_event_ID= [list(item) for item in items]
        for i in range(len(list_of_event_ID)):
            if(list_of_event_ID[i]==query_to_delete):
                return 1
        return 0;
    
    except:
        print("\nError during deletion...")
        return False
    
def delete_query(cursor,matrix_name,db,municipality_ID):
    try:
        ID=input("ID of element to delete: ")
        if(not ID.isnumeric() or int(ID)<=0):
            print("\nID must be a positive integer\nNo query deleted\n")
            return 0;
        check=check_deletion_ID(db,municipality_ID,matrix_name,ID)
        if(check==0):
            print("\nInformation of a different Municipality\nDELETION NOT ALLOWED\n")
            return 0;
        query="DELETE FROM " + matrix_name + " where " + matrix_name + "_ID=" + ID
        cursor.execute(query,)
        db.commit()
        print("\n{} ROW DELETED\n".format(cursor.rowcount))
    except:
        print("\nError during query deletion")
        return False

def attribute_generator(choice):
    if(choice=="event"):
        attribute_list=["EventTitle","EventType","EventDescription","EventCost","Location_ID"]
    elif(choice=="projection"):
        attribute_list=["ProjectionDate","ProjectionTime","Duration","Event_ID"]
    else:
        attribute_list=["Event_ID","DiscountType","DiscountPercentage"]
    return attribute_list;

def decision_generator(attribute,matrix_name):
    print("\nWould you like to update " + attribute + " of the " + matrix_name + " Table?")
    print("Press any key for YES\nPress 0 for NO")
    decision=input("")
    return decision

def input_restrictions(attribute,Municipality_ID,db):
    try:
        if(attribute in ["EventTitle","EventType","EventDescription","Duration","DiscountType"]):
            new_entry=input("\nPlease enter new text: ")
        elif(attribute=="EventCost"):
            new_entry=input("\nPlease enter new cost(integer): ")
        elif(attribute=="DiscountPercentage"):
            new_entry=float(input("\nPlease enter new discount (0-1, float number): "))
            if(new_entry>1.0 or new_entry<0.0):
                print("\nWrong Data Type inserted\n")
                return 0;
        elif(attribute=="Event_ID"):
            print("Enter Event_Code:\n(Choose one of the already existing)\n")
            new_entry=show_Event_ID(db,Municipality_ID)
            if(new_entry==0):
               print("Event NOT organised by your Municipality\n")
               return 0;
            string="Event"
            check=ID_exists(new_entry,string,db)
            if(check==0):
                print("Event_Code does not exist!!\n")
                return 0;
        elif(attribute=="Location_ID"):
            print("Enter Location_Code:\n(Choose one of the already existing)\n")
            new_entry=show_Location_ID(db,Municipality_ID)
            if(new_entry==0):
                print("Location NOT in your Municipality\n")
                return 0;
            string="Location"
            check=ID_exists(new_entry,string,db)
            if(check==0):
                print("\nLocation_ID does not exist\nQuery field was not updated\n")
                return 0;
        elif(attribute=="ProjectionDate"):
            print("\nEnter new Date:\nFORMAT: XXXX-XX-XX (YEAR-MONTH-DAY)")
            Year=input("Enter Year: ")
            Month=input("Enter Month: ")
            Day=input("Enter Day: ")
            new_entry=str(Year + "-" + Month + "-" + Day)
            if(not check_DATE(Year,Month,Day)):
                print("\nWrong Data Type inserted\n")
                return 0;
        else:
            print("Enter Projection Time:\nFORMAT: XX:XX:XX (HOUR:MINUTE:SECOND)\n")
            Hour=input("Enter Hour: ")
            Minutes=input("Enter Minutes: ")
            Seconds=input("Enter Seconds: ")
            new_entry=Hour + ":" + Minutes + ":" + Seconds
            if(not check_TIME(Hour,Minutes,Seconds)):
                print("\nWrong Data Type inserted\n")
                return 0;
        return new_entry;
    except:
        print("\nAn error occured\nQuery field not updated\n ")
        return 0;

def update_validation(cursor,Municipality_ID,matrix_name,query_ID):
    try:
        query="SELECT Event_ID FROM event WHERE Municipality_ID=%s ORDER BY EventTitle" 
        cursor.execute(query,(Municipality_ID,))
        items=cursor.fetchall()
        list_of_items = [list(item) for item in items]
        query="SELECT Event_ID FROM " + matrix_name + " WHERE " + matrix_name + "_ID=%s" 
        cursor.execute(query,(query_ID,))
        element=list(cursor.fetchall()[0])
        for i in range(len(list_of_items)):
            if(list_of_items[i]==element):
                return 1;
        print("\nInformation of a different Municipality\nUPDATE NOT ALLOWED\n")
        return 0; 
    except:
        print("\nError showing event")
        return False
    
def query_ID_check(matrix_name,cursor,Municipality_ID):
    query_ID="AAA"
    while(not query_ID.isnumeric()):
        query_ID=input("\nChoose the query ID which you want updated: ")
    q="SELECT COUNT(*) FROM " + matrix_name +" WHERE " + matrix_name + "_ID=%s"
    cursor.execute(q,(query_ID,))
    row_count=int(cursor.fetchone()[0])
    if(row_count==0):
        print("\nNo query has such ID\nNo query selected")
        return 0;
    back=update_validation(cursor,Municipality_ID,matrix_name,query_ID)
    if(back==1):
        return int(query_ID);
    return 0;
        
def update_one(matrix_name,cursor,db,attribute,new_entry,query_ID):
    try:
        query="UPDATE " + matrix_name +" SET " + attribute + "=%s" " WHERE " +matrix_name + "_ID=%s"
        print(query)
        cursor.execute(query,(new_entry,query_ID,))
        db.commit()
        print("\n{} ROW UPDATED\n".format(cursor.rowcount))
    except:
        print("\nWrong Data Type inserted\n")
        return False

def booking(db,cursor,Μunicipality_ID): 
    print("\nWould you like to see the bookings that have been made in an EXCEL SHEET?\nPress (y) for YES or (n) for NO: ")
    decision=input()
    while (decision!="y" and decision!="n"):
        decision=input("Wrong Input\nPress (y) for YES or (n) for NO: ")
    if(decision=="y"):
        try:
            path=str(pathlib.Path(__file__).parent.absolute())
            query="SELECT p.Projection_ID,t.Seat_ID,t.Ticket_ID FROM Projection AS p JOIN Ticket AS t ON p.Projection_ID=t.Projection_ID JOIN Event AS e ON p.Event_ID=e.Event_ID WHERE e.Municipality_ID=%s ORDER BY p.Projection_ID"
            cursor.execute(query,(Μunicipality_ID,))
            items=cursor.fetchall()
            print("\nBooking Tables have been successfully exported!\n")

            list_of_items = [list(item) for item in items]
            df = pd.DataFrame(list_of_items, index=None, columns=["Projection_ID","Seat_ID","Ticket_ID"])
            fullpath=path+'\Booked_Tickets.csv'
            df.to_csv (fullpath, index = False, encoding="utf-8")
            query="SELECT p.Projection_ID,count(Ticket_ID) AS Ticket_Num FROM Projection AS p JOIN Ticket AS t ON p.Projection_ID=t.Projection_ID JOIN Event AS e ON p.Event_ID=e.Event_ID WHERE e.Municipality_ID=%s GROUP BY p.Projection_ID ORDER BY p.Projection_ID "
            cursor.execute(query,(Μunicipality_ID,))
            items=cursor.fetchall()
            list_of_items = [list(item) for item in items]
            df = pd.DataFrame(list_of_items, index=None, columns=["Projection_ID","Number_of_Tickets"])
            
            fullpath=path+'\Spectars_Per_Projection.csv'
            df.to_csv (fullpath, index = False, encoding="utf-8")
            
        except:
            print("\nError during printing bookings\n")
            return False    
    else:
        print("\nMaybe another time...\n")
    return 0;
    
def municipality_dialogue(db,cursor):
    municipality_ID=munclogin(db)
    indicator=input("\nPress 0 to sign out or anything else to manage the database: ")
    while(indicator!="0"):
        action=choose_action()
        if(action!=5):
            choice=select_matrix()
        if(action==1):
            showall(choice,municipality_ID,db)
        elif(action==2 and choice!="location"):
            times=choose_number_of_actions(action)
            for i in range(times):
                print("\nQuery addition number " + str(i+1))
                addall(choice,db,municipality_ID) 
        elif(action==3 and choice!="location"):
            times=choose_number_of_actions(action)
            for i in range(times):
                print("\nQuery deletion number " + str(i+1))
                delete_query(cursor,choice,db,municipality_ID)  
        elif(action==4 and choice!="location"):
            times=choose_number_of_actions(action)
            for i in range(times):
                print("\nQuery update number " + str(i+1))
                query_ID=query_ID_check(choice,cursor,municipality_ID)
                if(query_ID!=0):
                    atr_list=attribute_generator(choice)
                    for attribute in atr_list:
                        decision=decision_generator(attribute,choice)
                        if(decision!='0'):
                            new_entry=input_restrictions(attribute,municipality_ID,db) 
                            if(new_entry!=0):    
                                update_one(choice, cursor,db,attribute,new_entry,query_ID)
        elif(action==5):    
            booking(db,cursor,municipality_ID)
        else: 
            print("\nNo permission to add to location table\nPlease contact database manager\n")
        indicator=input("\nPress any key to manage the database or 0 to sign out: ")
    return 0;
