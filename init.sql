CREATE DATABASE IF NOT EXISTS einvoice;
CREATE USER IF NOT EXISTS 'crazythursday'@'%' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON einvoice.* TO 'crazythursday'@'%';
FLUSH PRIVILEGES;
