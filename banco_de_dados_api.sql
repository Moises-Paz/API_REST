create database api;
use api;
create table usuarios
(
	id integer primary key,
    nome varchar(50),
    login varchar(30),
    senha varchar(30)
);
insert into usuarios(id, nome, login, senha) values(01,'MOISES PAZ MELO DOS SANTOS','2020002946','123456');
select * from usuarios;


















