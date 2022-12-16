ALTER TABLE Applications DROP COLUMN birthday;
ALTER TABLE Applications ADD COLUMN birthday DATE NOT NULL;