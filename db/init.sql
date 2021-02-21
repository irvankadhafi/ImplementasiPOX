CREATE DATABASE implementasipox;
use implementasipox;

CREATE TABLE `dockerhost` (
  `iddocker` int(11) NOT NULL,
  `iduser` int(11) UNSIGNED NOT NULL,
  `dockername` varchar(128) NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `dockerstatus` int(11) NOT NULL,
  `jenisdocker` varchar(128) NOT NULL,
  `ip_address` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `linkofswitch` (
  `source` int(11) UNSIGNED NOT NULL,
  `destination` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `user` (
  `id_user` int(11) UNSIGNED NOT NULL,
  `username` varchar(64) NOT NULL,
  `pwd` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `dockerhost`
  ADD KEY `iduser` (`iduser`);

ALTER TABLE `linkofswitch`
  ADD KEY `source` (`source`);

ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`,`username`);
  
ALTER TABLE `user`
  MODIFY `id_user` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;

ALTER TABLE `dockerhost`
  ADD CONSTRAINT `dockerhost_ibfk_1` FOREIGN KEY (`iduser`) REFERENCES `user` (`id_user`);

ALTER TABLE `linkofswitch`
  ADD CONSTRAINT `linkofswitch_ibfk_1` FOREIGN KEY (`source`) REFERENCES `user` (`id_user`);
COMMIT;
