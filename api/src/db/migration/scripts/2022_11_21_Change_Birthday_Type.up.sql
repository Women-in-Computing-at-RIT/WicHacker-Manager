ALTER TABLE Applications DROP COLUMN birthday;
ALTER TABLE Applications ADD COLUMN birthday VARCHAR(10) NOT NULL;