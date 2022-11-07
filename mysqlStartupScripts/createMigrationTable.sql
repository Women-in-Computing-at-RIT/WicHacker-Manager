CREATE TABLE IF NOT EXISTS Migrations(
    migration_id INT AUTO_INCREMENT,
    version VARCHAR(255) NOT NULL,
    dirtyVersion BOOL NOT NULL,
    PRIMARY KEY (migration_id)
);

INSERT INTO Migrations (version, dirtyVersion) VALUES (0, FALSE);

