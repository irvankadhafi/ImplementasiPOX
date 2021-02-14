CREATE DATABASE implementasipox;
use implementasipox;

CREATE TABLE `linkofswitch` (
  `source` int(11) UNSIGNED NOT NULL,
  `destination` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `user` (
  `id_user` int(11) UNSIGNED NOT NULL,
  `username` varchar(64) NOT NULL,
  `pwd` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `linkofswitch`
  ADD KEY `source` (`source`);
 
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`,`username`);
  
ALTER TABLE `user`
  MODIFY `id_user` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;

ALTER TABLE `linkofswitch`
  ADD CONSTRAINT `linkofswitch_ibfk_1` FOREIGN KEY (`source`) REFERENCES `user` (`id_user`);
COMMIT;
