-- Practice database used by the SQL console and SQL practical quizzes.
CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT, location TEXT);
INSERT INTO departments VALUES
 (1,'QA','Pune'),(2,'Development','Bengaluru'),(3,'HR','Mumbai'),(4,'Sales','Delhi'),(5,'Support','Pune');

CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, department_id INTEGER, salary INTEGER, manager_id INTEGER, join_date TEXT, city TEXT);
INSERT INTO employees VALUES
 (1,'Asha',2,95000,NULL,'2019-04-01','Bengaluru'),
 (2,'Ravi',1,52000,1,'2021-06-15','Pune'),
 (3,'Neha',1,61000,1,'2020-01-10','Pune'),
 (4,'Karan',2,78000,1,'2022-03-01','Bengaluru'),
 (5,'Priya',3,45000,NULL,'2018-09-20','Mumbai'),
 (6,'Vikram',2,78000,1,'2023-07-05','Hyderabad'),
 (7,'Sneha',4,39000,5,'2024-01-08','Delhi'),
 (8,'Arjun',1,47000,3,'2024-02-12','Pune'),
 (9,'Meera',4,56000,5,'2021-11-30','Delhi'),
 (10,'Rahul',NULL,30000,NULL,'2025-05-19','Mumbai');

CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT, signup_date TEXT);
INSERT INTO users VALUES
 (1,'Anil','anil@mail.com','Pune','2025-01-03'),
 (2,'Bina','bina@mail.com','Mumbai','2025-01-15'),
 (3,'Chetan','chetan@mail.com','Pune','2025-02-01'),
 (4,'Divya','divya@mail.com','Delhi','2025-02-20'),
 (5,'Anil K','anil@mail.com','Nagpur','2025-03-11'),
 (6,'Esha','esha@mail.com','Mumbai','2025-03-25'),
 (7,'Farhan','farhan@mail.com',NULL,'2025-04-02'),
 (8,'Bina S','bina@mail.com','Mumbai','2025-04-18');

CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, product TEXT, amount INTEGER, status TEXT, order_date TEXT);
INSERT INTO orders VALUES
 (101,1,'Laptop',55000,'delivered','2025-02-01'),
 (102,1,'Mouse',700,'delivered','2025-02-03'),
 (103,2,'Phone',22000,'cancelled','2025-02-10'),
 (104,3,'Headphones',3000,'delivered','2025-03-05'),
 (105,3,'Keyboard',1500,'pending','2025-03-07'),
 (106,4,'Monitor',12000,'delivered','2025-03-15'),
 (107,6,'Phone',25000,'delivered','2025-04-01'),
 (108,6,'Charger',900,'pending','2025-04-03'),
 (109,1,'Bag',1800,'delivered','2025-04-10');

CREATE TABLE bugs (id INTEGER PRIMARY KEY, title TEXT, module TEXT, severity TEXT, priority TEXT, status TEXT, reported_by INTEGER, created_on TEXT);
INSERT INTO bugs VALUES
 (1,'Login fails with valid password','Login','Critical','High','Open',2,'2025-05-01'),
 (2,'Typo on signup page','Signup','Low','Low','Closed',3,'2025-05-02'),
 (3,'Cart total wrong after discount','Cart','Major','High','Open',2,'2025-05-03'),
 (4,'Logo blurry on mobile','Home','Minor','Low','Open',8,'2025-05-04'),
 (5,'Payment page crashes','Payment','Critical','High','Fixed',3,'2025-05-05'),
 (6,'Forgot password email not sent','Login','Major','Medium','Reopened',2,'2025-05-06'),
 (7,'Search returns duplicates','Search','Minor','Medium','Open',8,'2025-05-07'),
 (8,'Profile photo upload slow','Profile','Minor','Low','Closed',3,'2025-05-08');
