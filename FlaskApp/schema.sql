 create table if not exists doctors(
username VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
name VARCHAR(255) NOT NULL,
id_number INT PRIMARY KEY
);

create table if not exists patients(
username VARCHAR(255) NOT NULL,
id_num INT PRIMARY KEY,
password VARCHAR(255) NOT NULL,
name VARCHAR(255) NOT NULL,
age INT, 
birthday VARCHAR(255) NOT NULL,
sex VARCHAR(255) NOT NULL,
height VARCHAR(255) NOT NULL,
weight INT,
img VARCHAR(255) NOT NULL
);

create table if not exists relationships(
dr_id INT,
patient_id INT,
relationship_id INT PRIMARY KEY
);

create table if not exists doctor_notes(
dr_id INT,
patient_id INT,
note_id INT PRIMARY KEY,
subject VARCHAR(255) NOT NULL,
date DATE NOT NULL,
content VARCHAR(255) NOT NULL
);

create table if not exists medication(
record_id INT PRIMARY KEY,
medicine VARCHAR(255) NOT NULL,
notes VARCHAR(255) NOT NULL,
grace_period INT
);

create table if not exists message(
patient VARCHAR(255) NOT NULL,
dr INT,
msg_id INT PRIMARY KEY,
day varchar(255) NOT NULL,
subject VARCHAR(255) NOT NULL,
body VARCHAR(300) NOT NULL
);


create table if not exists entries(
date DATE NOT NULL,
patient_id INT,
entry_id INT PRIMARY KEY,
mood INT, 
sleep INT,
exercise INT,
medication TIME NOT NULL,
diet VARCHAR(255) NOT NULL,
img LONGBLOB NOT NULL
);

