-- Drop the database if it exists
DROP DATABASE IF EXISTS hbnb_dev_db;

-- Create the database if it doesnt exist
CREATE DATABASE hbnb_dev_db;

-- Create a new user if the user doesnt exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privilaged to the user on hbnb_dev_db
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilage to hbnb_dev on performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Use FLUSH to apply changes
FLUSH PRIVILEGES;

