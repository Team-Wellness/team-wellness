insert into patients(username, id_num, password, name, age, birthday, sex, height, weight, img) values ("patient1", 2938490, "password", "Max Z", 21, "July 6", "X", "60 in", 123, "https://66.media.tumblr.com/fc6c724a178c19c028fc33d2c19d8177/tumblr_pgo5oultCp1r9z0kqo1_640.png");

insert into patients(username, id_num, password, name, age, birthday, sex, height, weight, img) values ("patient2", 9438, "password", "Edwin Z", 18, "June 17", "M", "68 in", 999, "https://66.media.tumblr.com/a488faeb262a0ae714cca91deeca65f4/tumblr_phkl0cystq1s0s8m8_540.jpg");

insert into patients(username, id_num, password, name, age, birthday, sex, height, weight, img) values ("patient3", 43825, "password", "Wendy C", 22, "August 43", "F", "63 in", 676, "https://66.media.tumblr.com/ca38901911eea94f5596fb202e92f2bf/tumblr_pgp98xrmzX1rd615wo1_500.gif");

insert into patients(username, id_num, password, name, age, birthday, sex, height, weight, img) values ("patient4", 43984, "password", "Matt C", 21, "March 19", "M", "69 in", 989, "https://66.media.tumblr.com/a77da79293850e89ddc89fe647843a7e/tumblr_pey3v5AnH41wjwprio2_540.jpg");

insert into relationships(dr_id, patient_id, relationship_id) values (1, 2938490, 9384909482304);

insert into message(patient, dr, msg_id, day, subject, body) values (43948, 1, 5, "October 5th, 2018", "Message Title", "This is the message body.");

insert into message(patient, dr, msg_id, day, subject, body) values (43948, 1, 6, "December 5th, 2018", "Another Subject", "Hi! This is a message.");

insert into message(patient, dr, msg_id, day, subject, body) values (9438, 1, 7, "July 2nd, 2018", "Annnnnd another subject", "How exciting!");

insert into message(patient, dr, msg_id, day, subject, body) values (32848, 1, 8, "June 1st, 2018", "Subject Subject", "I am a message.");

insert into message(patient, dr, msg_id, day, subject, body) values (43825, 1, 9, "February 10th, 2018", "I'm a patient", "Oh yes I am.");

insert into message(patient, dr, msg_id, day, subject, body) values (43984, 1, 10, "December 1st, 2018", "Message Title", "Message body");

insert into doctors(username, password, name, id_number) values ('doctor1', 'password', 'Dr. Amelia Badelia', 456);