ALTER TABLE Users DROP COLUMN is_virtual;
ALTER TABLE Applications ADD COLUMN is_virtual BOOLEAN;

ALTER TABLE Users DROP COLUMN pronouns;