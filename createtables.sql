CREATE TABLE `Customer` (`Cust_ID` int(10) NOT NULL  AUTO_INCREMENT PRIMARY KEY,`Username` varchar(20) NOT NULL,`Password` varchar(20) NOT NULL,`Email` varchar(30) NOT NULL,`Phone` int(13) NOT NULL,`CustomerName` varchar(20) NOT NULL,`CustomerSurname` varchar(20) NOT NULL);
CREATE TABLE `Municipality` (`Municipality_ID` int(10) NOT NULL  AUTO_INCREMENT PRIMARY KEY,`Username` varchar(20) NOT NULL,`MunPassword` varchar(20) NOT NULL,`Email` varchar(30) NOT NULL);
CREATE TABLE `Location` (`Location_ID` int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,`VenueName` varchar(50) NOT NULL,`VenueType` varchar(20) NOT NULL,`Town` varchar(20) NOT NULL,`Street` varchar(50) NOT NULL,`StreetNumber` varchar(4) NOT NULL,`PostalCode` int(5) NOT NULL,Municipality_ID int(10) NOT NULL,
     FOREIGN KEY (Municipality_ID) REFERENCES Municipality(Municipality_ID));
CREATE TABLE `Seat` (`Seat_ID` int(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,`Seat_Number` int(20) NOT NULL,`Location_ID` int(10) NOT NULL,`SeatRegion` varchar(20),`SeatRow` int(10),`SeatColumn` int(10),FOREIGN KEY (Location_ID) REFERENCES Location(Location_ID) ON DELETE CASCADE);
CREATE TABLE `Event` (`Event_ID` int(10) NOT NULL  AUTO_INCREMENT PRIMARY KEY,`EventTitle` varchar(40) NOT NULL,`EventType` varchar(10) NOT NULL,`EventDescription` TEXT NOT NULL,`EventCost` varchar(6) NOT NULL,`Municipality_ID` int(10) NOT NULL,`Location_ID` int(10) NOT NULL,FOREIGN KEY (Municipality_ID) REFERENCES Municipality(Municipality_ID),FOREIGN KEY (Location_ID) REFERENCES Location(Location_ID) ON UPDATE CASCADE ON DELETE CASCADE);
CREATE TABLE `Projection` (`Projection_ID` int(10) NOT NULL  AUTO_INCREMENT PRIMARY KEY,`ProjectionDate` DATE NOT NULL,`ProjectionTime` TIME NOT NULL,`Duration` varchar(15) NOT NULL,`Event_ID` int(10) NOT NULL,FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID) ON UPDATE CASCADE ON DELETE CASCADE);
CREATE TABLE `Available` (`Seat_ID` int(20) NOT NULL,`SeatAvailability` BINARY(1) NOT NULL,`Projection_ID` int(10) NOT NULL,FOREIGN KEY (Projection_ID) REFERENCES Projection(Projection_ID) ON UPDATE CASCADE ON DELETE CASCADE,PRIMARY KEY(Seat_ID,Projection_ID));
CREATE TABLE `Discount` (`Discount_ID` int(12) NOT NULL AUTO_INCREMENT PRIMARY KEY,`Event_ID` int(10) NOT NULL,`DiscountType` varchar(10) NOT NULL,`DiscountPercentage` FLOAT(2),FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID) ON UPDATE CASCADE ON DELETE CASCADE);
CREATE TABLE `Ticket` (`Ticket_ID` int(15) NOT NULL AUTO_INCREMENT PRIMARY KEY,`Cust_ID` int(10) NOT NULL,`Projection_ID` int(10) NOT NULL,`Seat_ID` int(20) NOT NULL,`Discount_ID` int(12),FOREIGN KEY (Cust_ID) REFERENCES Customer(Cust_ID),FOREIGN KEY (Projection_ID) REFERENCES Projection(Projection_ID) ON UPDATE CASCADE,FOREIGN KEY (Seat_ID) REFERENCES Seat(Seat_ID),FOREIGN KEY (Discount_ID) REFERENCES Discount(Discount_ID) ON UPDATE CASCADE);
INSERT INTO municipality (Username, MunPassword, Email) VALUES ("MuncHeraklion","1234","heraklion@municipality.gr");
INSERT INTO municipality (Username, MunPassword, Email) VALUES ("MuncPatras","1111","patras@municipality.gr");
INSERT INTO location (VenueName, VenueType, Town, Street, StreetNumber, PostalCode, Municipality_ID) VALUES ("Κηποθέατρο Μάνος Χατζηδάκης", "Θέατρο", "Ηράκλειο", "Λεωφόρος Νικολάου Πλαστήρα", 12, 71201,1);
INSERT INTO location (VenueName, VenueType, Town, Street, StreetNumber, PostalCode, Municipality_ID) VALUES ("Πύλη Βηθλεέμ", "Ανοιχτό Θέατρο", "Ηράκλειο", "Λεωφόρος Νικολάου Πλαστήρα", 67, 71201,1);
INSERT INTO location (VenueName, VenueType, Town, Street, StreetNumber, PostalCode, Municipality_ID) VALUES ("Κηποθέατρο Ν. Καζαντζάκης", "Ανοιχτό Θέατρο", "Ηράκλειο", "Γεωρ. Γεωργιάδου", 1, 71305,1);
INSERT INTO location (VenueName, VenueType, Town, Street, StreetNumber, PostalCode, Municipality_ID) VALUES ("Τεχνόπολις", "Σινεμά", "Ηράκλειο", "Αμουδάρα", 127, 71606,1);
INSERT INTO location (VenueName, VenueType, Town, Street, StreetNumber, PostalCode, Municipality_ID) VALUES ("Δημοτικό Θέατρο Απόλλων", "Κλειστό θέατρο", "Πάτρα", "Πλ. Γεωρ. Α 31", 31, 26221,2);
INSERT INTO event (EventTitle, EventType, EventDescription, EventCost , Municipality_ID, Location_ID) VALUES ("Ερωτόκριτος", "Παράσταση", "Το Θεατροδρόμιο παρουσιάζει την παράσταση για παιδιά και μεγάλους «Ερωτόκριτος»", 0, 1, 1);
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-08', '21:30:00', "80 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-09', '22:30:00', "80 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO event (EventTitle, EventType, EventDescription, EventCost , Municipality_ID, Location_ID) VALUES ("Μαθητική Μπαντίνα", "Κονσέρτο", "Παρουσίαση μαθητικής μπαντίνας των Μουσικών Σχολών «ΧΑΡΗΣ ΣΑΡΡΗΣ»", 0, 1, 1);
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-03', '21:30:00', "2 ώρες", (SELECT MAX(Event_ID) FROM event));
INSERT INTO event (EventTitle, EventType, EventDescription, EventCost , Municipality_ID, Location_ID) VALUES ("ΛΩΞΑΝΤΡΑ", "Παράσταση", "«ΛΩΞΑΝΤΡΑ» της Μαρίας Ιορδανίδου σε σκηνοθεσία Σωτήρη Χατζάκη", 20, 1, 4);
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-10', '21:30:00', "120 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-11', '21:30:00', "120 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO  discount (Event_ID, DiscountType, DiscountPercentage) VALUES ((SELECT MAX(Event_ID) FROM event), "Φοιτική", 0.25);
INSERT INTO  discount (Event_ID, DiscountType, DiscountPercentage) VALUES ((SELECT MAX(Event_ID) FROM event),"Άνεργοι", 0.25);
INSERT INTO  discount (Event_ID, DiscountType, DiscountPercentage) VALUES ((SELECT MAX(Event_ID) FROM event), "ΑΜΕΑ", 0.25);
INSERT INTO event (EventTitle, EventType, EventDescription, EventCost , Municipality_ID, Location_ID) VALUES ("Ταξίδι στην Μελωδία", "Συναυλία", "ΡΕΣΙΤΑΛ ΚΙΘΑΡΑΣ Σπουδαίων Ελλήνων Κιθαριστών", 7, 1, 3);
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-10', '21:30:00', "120 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO  discount (Event_ID, DiscountType, DiscountPercentage) VALUES ((SELECT MAX(Event_ID) FROM event), "Άνεργοι", 0.3);
INSERT INTO event (EventTitle, EventType, EventDescription, EventCost , Municipality_ID, Location_ID) VALUES ("Η Μάσα και ο αρκούδος", "Παράσταση", "Το ΘΕΑΤΡΟ ΤΕΧΝΗ & ΟΡΑΜΑ Παιδική σκηνή Δελφινάκι παρουσιάζει το παραδοσιακό ρωσικό παραμύθι «Η Μάσα και ο αρκούδος» σε τέσσερις παραστάσεις.", 8, 1, 2);
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-11', '19:30:00', "100 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-11', '21:30:00', "100 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-12', '19:30:00', "100 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-12', '21:30:00', "100 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO event (EventTitle, EventType, EventDescription, EventCost , Municipality_ID, Location_ID) VALUES ("ΤΟ ΝΗΣΙ ΤΩΝ ΣΥΝΑΙΣΘΗΜΑΤΩΝ", "Παράσταση", "Η παράσταση απευθύνεται σε παιδιά από 4-12 ετών, ανοικτό θέατρο “Πύλη Βηθλεέμ”: ΘΕΑΤΡΟ ΓΙΑ ΠΑΙΔΙΑ και όχι μόνο. Η διεθνής ομάδα Hippo παρουσιάζει τη διαδραστική παράσταση «ΤΟ ΝΗΣΙ ΤΩΝ ΣΥΝΑΙΣΘΗΜΑΤΩΝ» βασισμένη σε μια ιστορία του Χορχέ Μπουκάι.", 10, 1, 3);
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-12', '21:30:00', "90 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO  discount (Event_ID, DiscountType, DiscountPercentage) VALUES ((SELECT MAX(Event_ID) FROM event), "Άνεργοι", 0.5);
INSERT INTO  discount (Event_ID, DiscountType, DiscountPercentage) VALUES ((SELECT MAX(Event_ID) FROM event), "Πολύτεκνοι", 0.5);
INSERT INTO event (EventTitle, EventType, EventDescription, EventCost , Municipality_ID, Location_ID) VALUES ("Αφιέρωμα στον Bach", "Κονσέρτο", "Η Ορχήστρα «Young Masters» του Johann Sebastian Bach Music School του Μουσικού Πανεπιστημίου της Βιέννης, θα συμπράξει με την Συμφωνική Ορχήστρα Νέων Κρήτης Δήμου Ηρακλείου και θα πραγματοποιήσει μία συναυλία στα πλαίσια των εκδηλώσεων για το «Ελληνοαυστριακό Μουσικό Καλοκαίρι» σε συνεργασία με την J.S.Bach Musikschule και του Πανεπιστημίου Μουσικής Βιέννης.", 0, 1, 4);
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-14', '21:30:00', "80 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO event (EventTitle, EventType, EventDescription, EventCost , Municipality_ID, Location_ID) VALUES ("Οι Καλόπιστοι Θεατρίνοι", "Παράσταση", "Το ΔΗ.ΠΕ.ΘΕ. Πάτρας παρουσιάζει την παράσταση «οι Καλόπιστοι Θεατρίνοι» του Μαριβώ, η οποία πραγματοποιείται στο πλαίσιο του έργου NeTT- Δίκτυο Θεάτρων για την αξιοποίηση της Πολιτιστικής και Φυσικής Κληρονομιάς και την ανάπτυξη του Αειφόρου Τουρισμού (Network of Theatres for the valorization of Cultural and Natural Heritage to develop a Sustainable Tourism) του προγράμματος Ευρωπαϊκής Εδαφικής Συνεργασίας INTERREG Ελλάδα Ιταλία 2014-2020.", 0, 2, 5);
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-13', '21:00:00', "90 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-07-14', '22:00:00', "90 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO event (EventTitle, EventType, EventDescription, EventCost , Municipality_ID, Location_ID) VALUES ("Δεν είμαστε κουραμπιέδες!", "Stand up", "Τρεις ηθοποιοί επί σκηνής αφηγούνται ιστορίες πασχίζοντας να ψυχαγωγήσουν τους θεατές και να δικαιολογήσουν την ύπαρξή τους σε μια εποχή που η Τέχνη απαξιώνεται και θεωρείται περιττή πολυτέλεια. Οι ηθοποιοί, μαζί με το κοινό, ανακαλύπτουν τη χαρά της δημιουργίας, το παράλογο και την ποίηση που παρεισφρέουν στην καθημερινότητα, τις μικρές, θριαμβευτικές νίκες της ζωής έναντι του θανάτου.", 8, 2, 5);
INSERT INTO projection (ProjectionDate, ProjectionTime, Duration, Event_ID) VALUES ('2021-09-11', '21:30:00', "100 λεπτά", (SELECT MAX(Event_ID) FROM event));
INSERT INTO  discount (Event_ID, DiscountType, DiscountPercentage) VALUES ((SELECT MAX(Event_ID) FROM event),"‘Άνεργοι", 0.25);

