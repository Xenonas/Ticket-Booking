import mysql.connector as mysql
from sqlite3 import Error
import datetime

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
    except Error as e:
        print(e)
        return False

def choose_action():
    MatricesList=["SHOW","ADD","DELETE","UPDATE"]
    action_num=5
    while action_num not in [1,2,3,4]:
        action_num=int(input("Press 1 to SHOW a matrix\nPress 2 to ADD a query\nPress 3 to DELETE a query\nPress 4 to UPDATE a query\n"))
    choice=MatricesList[action_num-1]
    print("\nYou have chosen the function --- " + choice + " ---\n")
    return action_num

def choose_number_of_actions(action_num):
    MatricesList=["SHOW","ADD","DELETE","UPDATE"]
    action=MatricesList[action_num-1]
    times='-1'
    while not times.isnumeric(): 
        times=input("\nType the number of queries (integer value) you want to " + action)
    print("\nYou have chosen to " + action + " a query " + times + " times\n")
    return int(times)
 
def select_matrix():
    MatricesList=["event","projection","discount","location"]
    x=5
    while x not in [1,2,3,4]:
        x=int(input("Press 1 for Event, 2 for Projection, 3 for Discount, 4 for Location:\n"))
    choice=MatricesList[x-1]
    print("\nYou have chosen the --- " + choice + " Table ---")
    return choice

def showall(matrix_name,Mun_ID,db):
    try:
        cursor = db.cursor()
        print("\nBelow lays the --- " + matrix_name + " Table ---\n")
        if(matrix_name=="location"):
            query="SELECT * FROM " + matrix_name + " WHERE Municipality_ID=%s"
            cursor.execute(query,(Mun_ID,))
        elif(matrix_name=="event"):
            query="SELECT * FROM " + matrix_name 
            cursor.execute(query)
        elif(matrix_name=="projection"):
            query="SELECT mat.Projection_ID,mat.ProjectionDate,mat.ProjectionTime,mat.duration FROM " + matrix_name + " AS mat JOIN event AS e ON mat.event_ID=e.event_ID WHERE e.Municipality_ID=%s"

            cursor.execute(query,(Mun_ID,))
        else:
            query="SELECT mat.Discount_ID,mat.DiscountType,mat.DiscountPercentage FROM " + matrix_name + " AS mat JOIN event AS e ON mat.event_ID=e.event_ID WHERE e.Municipality_ID=%s"
            cursor.execute(query,(Mun_ID,))
        items=cursor.fetchall()
        for item in items:
            for i in range(len(item)):
                if(matrix_name=="projection"):
                    print (item[i], end='\t\t')
                else:
                    print(item[i], end='\t')
            print("\n")

    except Error as e:
        print(e)
        return False

def show_Event_ID(db,Mun_ID):
    try:
        cursor = db.cursor()
        query="SELECT Event_ID,EventTitle FROM event WHERE Municipality_ID=%s ORDER BY EventTitle" 
        cursor.execute(query,(Mun_ID,))
        items=cursor.fetchall()
        print("\nBelow lays the --- Event_ID Table ---\n[Event_ID,EventTitle]")
        for item in items:
            print(item)

    except Error as e:
        print(e)
        return False

def show_Location_ID(db,Mun_ID):
    try:
        cursor = db.cursor()
        query="SELECT Location_ID,VenueName,VenueType,Town FROM location WHERE Municipality_ID=%s" 
        cursor.execute(query,(Mun_ID,))
        items=cursor.fetchall()
        print("\nBelow lays the --- Location_ID Table ---\n[Location_ID,VenueName,VenueType,Town]")
        for item in items:
            print(item)
    
    except Error as e:
        print(e)
        return False
    
def add_event(cursor,db,Mun_ID):
    try:
        EventTitle=str(input("\nEnter new event title:"))
        print("Enter new event type:\nΕνδεικτικά: ['Παράσταση','Ταινία','Κονσέρτο','Συναυλία','Ομιλία']")
        EventType=str(input())
        EventDescription=str(input("Enter new event description:"))
        EventCost=int(input("Enter new event cost in euros:"))
        Municipality_ID=int(Mun_ID)
        string="Municipality"
        print("Enter Location ID:\n(Choose one of the already existing)\n")
        show_Location_ID(db,Mun_ID)
        Location_ID=int(input())
        string="Location"
        check=ID_exists(Location_ID,string,db)
        if(check==0):
            print("\nLocation_ID does not exist!!\nQuery was not added!!\n ")
            return 0;
        values=[EventTitle,EventType,EventDescription,EventCost,Municipality_ID,Location_ID]
        cursor.execute("INSERT INTO event (EventTitle,EventType,EventDescription,EventCost,Municipality_ID,Location_ID) VALUES (%s,%s,%s,%s,%s,%s)",(values))
        db.commit()
        print("\nData inserted succesfully!!\n")
    except:
        print("\nWARNING:\nWrong Data Type inserted\nTry again please...")

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

def add_projection(cursor,db,Mun_ID):
    try:
        print("\nEnter Projection Date:\nFORMAT: XXXX-XX-XX (YEAR-MONTH-DAY)")
        Year=input("Enter Year:")
        Month=input("Enter Month:")
        Day=input("Enter Day:")
        ProjectionDate=str(Year + "-" + Month + "-" + Day)
        print(ProjectionDate)
        if(not check_DATE(Year,Month,Day)):
            print("\nWARNING:\nWrong Data Type inserted\nTry again please...")
            return 0;
        print("Enter Projection Time:\nFORMAT: XX:XX:XX (HOUR:MINUTE:SECOND)\n")
        Hour=input("Enter Hour:")
        Minutes=input("Enter Minutes:")
        Seconds=input("Enter Seconds:")

        ProjectionTime=Hour + ":" + Minutes + ":" + Seconds
        if(not check_TIME(Hour,Minutes,Seconds)):
            print("\nWARNING:\nWrong Data Type inserted\nTry again please...")
            return 0;

        Duration=input("Enter Duration:")
        print("Enter Event_ID:\n(Choose one of the already existing)\n")
        show_Event_ID(db,Mun_ID)
        Event_ID=int(input())
        string="Event"
        check=ID_exists(Event_ID,string,db)
        if(check==0):
            print("\nEvent_ID does not exist!!\nQuery was not added!!\n ")
            return 0;
        values=[ProjectionDate,ProjectionTime,Duration,Event_ID]
        
        cursor.execute("INSERT INTO projection (ProjectionDate,ProjectionTime,Duration,Event_ID) VALUES (%s,%s,%s,%s)",(values))
        db.commit()
        print("\nData inserted succesfully!!\n")
    except:
        print("\nWARNING:\nWrong Data Type inserted\nTry again please...")
        return False

def add_discount(cursor,db,Mun_ID):
    try:
        print("Enter Event_ID:\n (Choose one of the already existing)\n")
        show_Event_ID(db,Mun_ID)
        Event_ID=int(input())
        
        string="Event"
        check=ID_exists(Event_ID,string,db)
        if(check==0):
            print("\nEvent_ID does not exist!!\nQuery was not added!!\n ")
            return 0;
        DiscountType=str(input("Enter Discount Type:\nΕνδεικτικά: ['Φοιτητική','Άνεργοι','ΑΜΕΑ','Πολύτεκνοι']"))
        DiscountPercentage=str(input("Enter Discount Percentage (0-100, 3 digits max):"))
        values=[Event_ID,DiscountType,DiscountPercentage]
        cursor.execute("INSERT INTO discount (Event_ID,DiscountType,DiscountPercentage) VALUES (%s,%s,%s)",(values))
        db.commit()
        print("\nData inserted succesfully!!\n")
    except:
        print("\nWARNING:\nWrong Data Type inserted\nTry again please...")

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
    
def delete_query(cursor,matrix_name,db):
    try:
        x=int(input("ID of element to delete "))
        query="DELETE FROM " + matrix_name + " where " + matrix_name + "_ID=%s"
        print(query + "\n")
        cursor.execute(query,(x,))
        db.commit()
        print("\n{} ROWS DELETED\n".format(cursor.rowcount))
    except Error as e:
        print(e)
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
            new_entry=input("\nPlease enter new string:\n")
        elif(attribute=="EventCost"):
            new_entry=input("\nPlease enter new Price (integer):")
        elif(attribute=="DiscountPercentage"):
            new_entry=input("\nPlease enter new discount (0-100, 3 digits max):")
        elif(attribute=="Event_ID"):
            print("Enter Event_ID:\n(Choose one of the already existing)\n")
            show_Event_ID(db,Municipality_ID)
            new_entry=int(input())
            string="Event"
            check=ID_exists(new_entry,string,db)
            if(check==0):
                print("\nEvent_ID does not exist!!\nQUERY FIELD NOT UPDATED!!\n")
                return 0;
        elif(attribute=="Location_ID"):
            print("Enter Location ID:\n(Choose one of the already existing)\n")
            show_Location_ID(db,Municipality_ID)
            new_entry=int(input())
            string="Location"
            check=ID_exists(new_entry,string,db)
            if(check==0):
                print("\nLocation_ID does not exist!!\nQUERY FIELD NOT UPDATED!!\n")
                return 0;
        elif(attribute=="ProjectionDate"):
            print("\nEnter Projection Date:\nFORMAT: XXXX-XX-XX (YEAR-MONTH-DAY)")
            Year=input("Enter Year:")
            Month=input("Enter Month:")
            Day=input("Enter Day:")
            new_entry=str(Year + "-" + Month + "-" + Day)
            if(not check_DATE(Year,Month,Day)):
                print("\nWARNING:\nWrong Data Type inserted\nQUERY FIELD NOT UPDATED!!\n")
                return 0;
        else:
            print("Enter Projection Time:\nFORMAT: XX:XX:XX (HOUR:MINUTE:SECOND)\n")
            Hour=input("Enter Hour:")
            Minutes=input("Enter Minutes:")
            Seconds=input("Enter Seconds:")
            new_entry=Hour + ":" + Minutes + ":" + Seconds
            if(not check_TIME(Hour,Minutes,Seconds)):
                print("\nWARNING:\nWrong Data Type inserted\nQUERY FIELD NOT UPDATED!!\n")
                return 0;
        return new_entry;
    except:
        print("\nWARNING:\nWrong Data Type inserted\nQUERY FIELD NOT UPDATED!!\n ")
        return 0;
                
def query_ID_check(matrix_name,cursor):
    query_ID="AAA"
    while(not query_ID.isnumeric()):
        query_ID=input("\nChoose query ID which will be updated: ")
    q="SELECT COUNT(*) FROM " + matrix_name +" WHERE " + matrix_name + "_ID=%s"
    cursor.execute(q,(query_ID,))
    row_count=int(cursor.fetchone()[0])
    if(row_count==0):
        print("\nNo query has such ID\nNO QUERY SELECTED")
        return 0;
    return int(query_ID);
        
def update_one(matrix_name,cursor,db,attribute,new_entry,query_ID):
    try:
        query="UPDATE " + matrix_name +" SET " + attribute + "=%s" " WHERE " +matrix_name + "_ID=%s"
        print(query)
        cursor.execute(query,(new_entry,query_ID,))
        db.commit()
        print("\n{} ROWS UPDATED\n".format(cursor.rowcount))
    except:
        print("\nWARNING:\nWrong Data Type inserted\nTry again please...")
        return False

def municipality_dialogue(db):
    municipality_ID=munclogin(db)
    indicator=input("\nPress 0 to sign out or anything else to manage the database:\n")
    while(indicator!="0"):
        action=choose_action()
        choice=select_matrix()
        if(action==1):
            showall(choice,municipality_ID,db)
        elif(action==2 and choice!="location"):
            times=choose_number_of_actions(action)
            for i in range(times):
                print("\nQuery ADDITION number " + str(i+1))
                addall(choice,db,municipality_ID) 
        elif(action==3 and choice!="location"):
            times=choose_number_of_actions(action)
            for i in range(times):
                print("\nQuery DELETION number " + str(i+1))
                delete_query(cursor,choice,db)  
        elif(action==4 and choice!="location"):
            times=choose_number_of_actions(action)
            for i in range(times):
                print("\nQuery UPDATE number " + str(i+1))
                query_ID=query_ID_check(choice,cursor)
                if(query_ID!=0):
                    atr_list=attribute_generator(choice)
                    for attribute in atr_list:
                        decision=decision_generator(attribute,choice)
                        if(decision!='0'):
                            new_entry=input_restrictions(attribute,municipality_ID,db) 
                            if(new_entry!=0):    
                                update_one(choice, cursor,db,attribute,new_entry,query_ID)
        else: 
            print("\nWARNING:\nNO PERMISSION GRANTED TO ADD TO LOCATION TABLE\nCONTACT DATABASE MANAGER\n")
        indicator=input("\nPress 0 to sign out or anything else to manage the database:\n")
    return 0;
