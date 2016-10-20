USE mlb_project1;

create table player(
CONSTRAINT uc_playerID UNIQUE (player_page_link,player_fn,player_ln)
,id INT AUTO_INCREMENT PRIMARY KEY
,player_page_link varchar(90)
,player_alias varchar(20)
,player_fn varchar(20)
,player_ln varchar(20)
 );

