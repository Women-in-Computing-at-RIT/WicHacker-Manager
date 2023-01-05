ALTER TABLE Applications DROP COLUMN gender;
ALTER TABLE Applications DROP COLUMN level_of_study;
ALTER TABLE Applications DROP COLUMN has_attended_wichacks;
ALTER TABLE Applications DROP COLUMN has_attended_hackathons;
ALTER TABLE Applications DROP COLUMN bus_rider;
ALTER TABLE Applications DROP COLUMN bus_stop;
ALTER TABLE Applications DROP COLUMN dietary_restrictions;
ALTER TABLE Applications DROP COLUMN special_accommodations;
ALTER TABLE Applications DROP COLUMN affirmed_agreements;

ALTER TABLE Applications ADD COLUMN year VARCHAR(255) NOT NULL;
ALTER TABLE Applications ADD COLUMN has_attended BOOLEAN NOT NULL;
ALTER TABLE Applications ADD COLUMN resume VARCHAR(255);

ALTER TABLE Applications DROP COLUMN status;
ALTER TABLE Users ADD COLUMN status ENUM('APPLIED', 'ACCEPTED', 'REJECTED', 'CONFIRMED') DEFAULT NULL;;