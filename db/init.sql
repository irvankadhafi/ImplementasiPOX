CREATE DATABASE implementasipox;
use implementasipox;
CREATE TABLE `linkofswitch` ( 
   `source` INT(11),
   `destination` INT(11),
   `user_iduser` INT(11) NOT NULL,
   `user_username` VARCHAR(64),
    PRIMARY KEY `Primary key`(

    )
);
CREATE TABLE `user` ( 
   `iduser` INT(11) NOT NULL,
   `username` VARCHAR(64),
   `pwd` VARCHAR(64),
    PRIMARY KEY `Primary key`(
   `iduser`,
   `username`
    )
);
ALTER TABLE `linkofswitch` 
  ADD CONSTRAINT `user-linkofswitch`
  FOREIGN KEY ( 
   `user_iduser`, 
   `user_username`
)   REFERENCES `user`( 
   `iduser`, 
   `username`
) ;

