-- DDL Statement --
-- Start creating Database --
drop database ration1;
create database ration1;
USE ration1;
-- Start creating tables --
DROP TABLE IF EXISTS ration1.admin_info;
Create table ration1.admin_info
(admin_id varchar(10) primary key,
admin_password varchar(20)
);

DROP table IF exists ration1.userinfo;
Create table ration1.userinfo
(ration_number bigint primary key,
 passwd varchar(9),
  name varchar(30),
AadharCard varchar(12),
totalincome integer,
familymember integer,
card_type varchar(5));

DROP table if exists ration1.Stockinfo;
Create table ration1.Stockinfo
(commodity_code varchar(3) primary key,
 commodity_name varchar(12),
 bpl_cost integer,
 bpl_max_weight integer,
 apl_cost integer,
 apl_max_weight integer);
  
DROP table IF exists ration1.user_ration_info;
Create table ration1.user_ration_info
(ration_number integer primary key,
card_type varchar(3),
wheat_bal integer,
rice_bal integer,
lentils_bal integer,
trans_date Date);
-- End DDL --
-- DML Statement --
-- Inserting static data --
Insert into ration1.admin_info (admin_id, admin_password) values ('admin', 'admin'); 
Insert into ration1.Stockinfo (commodity_code, commodity_name, bpl_cost, bpl_max_weight, apl_cost, apl_max_weight)
values ('RCE', 'Rice', 3, 25, 10, 20);

Insert into ration1.Stockinfo (commodity_code, commodity_name, bpl_cost, bpl_max_weight, apl_cost, apl_max_weight)
values ('WHT', 'Wheat', 2, 15, 10, 10);

Insert into ration1.Stockinfo (commodity_code, commodity_name, bpl_cost, bpl_max_weight, apl_cost, apl_max_weight)
values ('LNT', 'Lentil', 5, 20, 15, 10);

-- BPL is below poverty line
-- APL is above poverty line

Insert into ration1.userinfo
(ration_number,passwd,name,AadharCard,totalincome,familymember,card_type)
VALUES (1111111111,'password','Johnathan Joestar', 123456789123, 1000000, 4,'APL');

Insert into ration1.userinfo
(ration_number,passwd,name,AadharCard,totalincome,familymember,card_type)
VALUES (1111111112,'password','Reiner Braun', 234567891234, 700000, 5,'APL');

Insert into ration1.userinfo
(ration_number,passwd,name,AadharCard,totalincome,familymember,card_type)
VALUES (1111111113,'password','Eren Yaeger', 345678912345, 100000, 6,'BPL');

Insert into ration1.userinfo
(ration_number,passwd,name,AadharCard,totalincome,familymember,card_type)
VALUES (1111111114,'password','Lelouch Vi Britannia', 56789123456, 50000, 3,'BPL');

Insert into ration1.userinfo
(ration_number,passwd,name,AadharCard,totalincome,familymember,card_type)
VALUES (1111111115,'password','Johann Leibert', 67891234567, 30000, 7,'BPL');

Insert into ration1.user_ration_info(ration_number,card_type,wheat_bal,rice_bal,lentils_bal,trans_date)
VALUES(1111111111,'APL',2,5,3, '2022-05-02');
Insert into ration1.user_ration_info(ration_number,card_type,wheat_bal,rice_bal,lentils_bal,trans_date)
VALUES(1111111112,'APL',3,4,2, '2022-05-03');

insert into ration1.user_ration_info(ration_number,card_type,wheat_bal,rice_bal,lentils_bal,trans_date)
VALUES(1111111113,'BPL',3,4,2, '2022-05-03');

insert into ration1.user_ration_info(ration_number,card_type,wheat_bal,rice_bal,lentils_bal,trans_date)
VALUES(1111111114,'BPL',1,1,1, '2022-05-03');

insert into ration1.user_ration_info(ration_number,card_type,wheat_bal,rice_bal,lentils_bal,trans_date)
VALUES(1111111115,'BPL',1,1,1, '2022-05-03');



 