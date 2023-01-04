# add new values needed for applications
ALTER TABLE Applications ADD COLUMN gender VARCHAR(127) NOT NULL;
ALTER TABLE Applications ADD COLUMN level_of_study VARCHAR(127) NOT NULL;
ALTER TABLE Applications ADD COLUMN has_attended_wichacks BOOLEAN NOT NULL;
ALTER TABLE Applications ADD COLUMN has_attended_hackathons BOOLEAN NOT NULL;
ALTER TABLE Applications ADD COLUMN bus_rider BOOLEAN;
ALTER TABLE Applications ADD COLUMN bus_stop VARCHAR(255);
ALTER TABLE Applications ADD COLUMN dietary_restrictions VARCHAR(255);
ALTER TABLE Applications ADD COLUMN special_accommodations VARCHAR(255);
ALTER TABLE Applications ADD COLUMN affirmed_agreements BOOLEAN NOT NULL;

# remove no longer needed values
ALTER TABLE Applications DROP COLUMN year;
ALTER TABLE Applications DROP COLUMN has_attended;
ALTER TABLE Applications DROP COLUMN resume;

# move application status to application table
ALTER TABLE Applications ADD COLUMN status ENUM('APPLIED', 'ACCEPTED', 'REJECTED', 'CONFIRMED') DEFAULT NULL;
ALTER TABLE Users DROP COLUMN status;