-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--- Create table players, default wins and losses = 0 and id is serial key. 
--- Player can't register without a name
create table players (name text not null, id serial primary key, wins int default 0, losses int default 0);

--- Create table with id as primary key and winner and looser id requires referencing with players table
create table matches (id serial primary key, winner int references players(id), looser int references players(id));

--- Create a view standings which sorts players based on wins and then losses
create view standings as select * from players order by wins desc, losses;

