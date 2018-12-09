insert into patients(username, id_num, password, name, age, birthday, sex, height, weight, img) values ("patient1", 2938490, "password", "Max Z", 21, "July 6", "X", "60 in", 123, "https://66.media.tumblr.com/fc6c724a178c19c028fc33d2c19d8177/tumblr_pgo5oultCp1r9z0kqo1_640.png");

insert into patients(username, id_num, password, name, age, birthday, sex, height, weight, img) values ("patient2", 9438, "password", "Edwin Z", 18, "June 17", "M", "68 in", 999, "https://66.media.tumblr.com/a488faeb262a0ae714cca91deeca65f4/tumblr_phkl0cystq1s0s8m8_540.jpg");

insert into patients(username, id_num, password, name, age, birthday, sex, height, weight, img) values ("patient3", 43825, "password", "Wendy C", 22, "August 43", "F", "63 in", 676, "https://66.media.tumblr.com/ca38901911eea94f5596fb202e92f2bf/tumblr_pgp98xrmzX1rd615wo1_500.gif");

insert into patients(username, id_num, password, name, age, birthday, sex, height, weight, img) values ("patient4", 43984, "password", "Matt C", 21, "March 19", "M", "69 in", 989, "https://66.media.tumblr.com/a77da79293850e89ddc89fe647843a7e/tumblr_pey3v5AnH41wjwprio2_540.jpg");

insert into doctors (username, password, name, id_number)
values ("doc1", "docTest1", "Dr. Juniper", 11);

insert into doctors (username, password, name, id_number)
values ("doc2", "docTest2", "Dr. Oak", 12);

insert into doctors (username, password, name, id_number)
values ("doc1", "docTest1", "Dr. Elm", 13);

insert into relationships(dr_id, patient_id, relationship_id) values (11, 9438, 9384909482304);

insert into relationships(dr_id, patient_id, relationship_id) values (12, 9438, 9384909482305);

insert into relationships(dr_id, patient_id, relationship_id) values (13, 9438, 9384909482306);


insert into patients(username, id_num, password, name, age, birthday, sex, height, weight, img) values ("admin@gmail.com", 43989, "admin", "Test Patient", 21, "April 1", "F", "69 in", 110, "https://citizenmed.files.wordpress.com/2011/08/user-icon1.jpg");

insert into doctor_notes(dr_id, patient_id, note_id, subject, date, content) values (13, 9438, 1234567890, "Allergy Test now", date('NOW'), "Please call to see results");

insert into doctor_notes(dr_id, patient_id, note_id, subject, date, content)
values (11, 9438, 123456780, "Rash Appointment", date('NOW'), "now Please call if rash get worse");