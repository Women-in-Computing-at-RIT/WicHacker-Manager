ALTER TABLE Permissions ADD COLUMN type ENUM('READ', 'WRITE') NOT NULL;

INSERT INTO Permissions (permission, type) values ('Hackers', 'READ'); # View hacker information
INSERT INTO Permissions (permission, type) values ('Hackers', 'WRITE'); # Edit hackers: i.e. Change Hacker Application Status
INSERT INTO Permissions (permission, type) values ('Permissions', 'READ'); # view permissions
INSERT INTO Permissions (permission, type) values ('Permissions', 'WRITE'); # edit user's permissions

# CheckIn used for volunteers to lookup hackers and set that they're checked in. Only returns some data
INSERT INTO Permissions (permission, type) values ('CheckIn', 'READ');
INSERT INTO Permissions (permission, type) values ('CheckIn', 'WRITE');

INSERT INTO Permissions (permission, type) values ('Statistics', 'READ'); # for organizers to view statistics
INSERT INTO Permissions (permission, type) values ('Console', 'READ');
INSERT INTO Permissions (permission, type) values ('Console', 'WRITE');
