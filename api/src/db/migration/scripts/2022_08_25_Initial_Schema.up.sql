CREATE TABLE IF NOT EXISTS Users(
    user_id INT AUTO_INCREMENT,
    auth_id BIGINT UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    pronouns VARCHAR(63) NOT NULL,
    address_id INT,
    application_id INT,
    is_virtual BOOLEAN NOT NULL,
    sponsor_id INT,
    status_id ENUM('APPLIED', 'ACCEPTED', 'REJECTED', 'CONFIRMED') DEFAULT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS Permissions(
    permission_id INT AUTO_INCREMENT,
    permission VARCHAR(255) NOT NULL,
    PRIMARY KEY (permission_id)
);

CREATE TABLE IF NOT EXISTS UserPermissions(
    permission_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (permission_id, user_id)
);

CREATE TABLE IF NOT EXISTS Sponsors(
    sponsor_id INT AUTO_INCREMENT,
    company_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (sponsor_id)
);

CREATE TABLE IF NOT EXISTS Perks(
    perk_id INT AUTO_INCREMENT,
    description VARCHAR(255),
    PRIMARY KEY (perk_id)
);

CREATE TABLE IF NOT EXISTS SponsorPerks(
    perk_id INT NOT NULL,
    sponsor_id INT NOT NULL,
    PRIMARY KEY (perk_id, sponsor_id)
);

CREATE TABLE IF NOT EXISTS Addresses(
    address_id INT AUTO_INCREMENT,
    address1 VARCHAR(255) NOT NULL ,
    address2 VARCHAR(255),
    city VARCHAR(255) NOT NULL,
    subdivision VARCHAR(255) NOT NULL ,
    country VARCHAR(255) NOT NULL ,
    PRIMARY KEY (address_id)
);

CREATE TABLE IF NOT EXISTS Applications(
    application_id INT AUTO_INCREMENT,
    major VARCHAR(255) NOT NULL,
    year VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL ,
    resume VARCHAR(255),
    shirt_id ENUM('X-Small', 'Small', 'Medium', 'Large', 'X-Large', 'XX-Large', 'XXX-Large') DEFAULT NULL,
    has_attended BOOLEAN NOT NULL ,
    PRIMARY KEY (application_id)
);