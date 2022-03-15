CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'clientpw';

GRANT ALL PRIVILEGES ON totydb.* TO 'appadmin'@'localhost';
GRANT SELECT ON totydb.* TO 'appclient'@'localhost';

FLUSH PRIVILEGES;
