-- Create a database ifit doesnt exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create a new user if the user doesnt exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges to th user
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT  privileges to on performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Use FLUSH to apply changes
FLUSH PRIVILEGES
