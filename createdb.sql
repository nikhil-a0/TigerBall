DROP TABLE IF EXISTS events;

CREATE TABLE events
(event_id SERIAL NOT NULL, sport TEXT, location TEXT, event_date DATE, start_time TIME,
end_time TIME, visibility BOOLEAN, organizer_id TEXT);

-----

CREATE TABLE eventsparticipants
(event_id INTEGER, participant_id TEXT);

-- ---------------------------------------------------------------------
