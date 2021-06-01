#insert into books and delivery people table

INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('And then there were none','Agatha Christie',210);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Harry Potter and the Philosopher\'s Stone','J. K. Rowling',300);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Harry Potter and the Chamber of Secrets','J. K. Rowling',310);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Harry Potter and the Prisoner of Azkaban','J. K. Rowling',310);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Harry Potter and the Goblet of Fire','J. K. Rowling',320);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Harry Potter and the Order of the Phoenix','J. K. Rowling',300);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Harry Potter and the Half-Blood Prince','J. K. Rowling',310);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Harry Potter and the Deathly Hallows','J. K. Rowling',290);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Da Vinci Code','Dan Brown',750);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Angels & Demons','Dan Brown',500);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Inferno','Dan Brown',450);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Cat O Nine Tales','Jeffery Archer',250);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Only Time Will Tell','Jeffery Archer',300);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('To Cut a Long Story Short','Jeffery Archer',200);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('The Sky is Falling','Sidney Sheldon',450);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('The Doomsday Conspiracy','Sidney Sheldon',300);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('The Firm','John Grisham',300);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('Time to Kill','John Grisham',200);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('The Runaway Jury','John Grisham',550);
INSERT INTO BOOK(BNAME,AUTHOR,PRICE) VALUES ('The President is Missing','James Patterson',400);

UPDATE BOOK SET BSTATUS='A';

INSERT INTO DELPPL(FNAME,LNAME,PHONENO) VALUES ('Ben','Wyatt',5642967527);
INSERT INTO DELPPL(FNAME,LNAME,PHONENO) VALUES ('Ann','Perkins',8563734523);
INSERT INTO DELPPL(FNAME,LNAME,PHONENO) VALUES ('Jake','Peralta',2642967527);
INSERT INTO DELPPL(FNAME,LNAME,PHONENO) VALUES ('Phoebe','Buffay',4752967527);

UPDATE DELPPL SET ORDERCOUNT=0;
