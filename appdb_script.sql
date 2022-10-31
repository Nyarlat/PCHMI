create table contactrequests (
    id integer PRIMARY KEY autoincrement, 
    firstname varchar(255) NOT NULL, 
    lastname varchar(255), 
    email varchar(255),  
    reqtext varchar(255), 
    createdAt datetime, 
    updatedAt datetime, 
    ownerId integer, 
    CONSTRAINT fk_owner_id 
    FOREIGN KEY (ownerId) 
    REFERENCES logins(id) 
    ON DELETE CASCADE
    
create table logins (
    id integer PRIMARY KEY autoincrement, 
    username varchar(255) NOT NULL UNIQUE, 
    email varchar(255) NOT NULL UNIQUE, 
    password varchar(255) NOT NULL UNIQUE
);
