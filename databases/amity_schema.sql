CREATE TABLE [IF NOT EXIST] [amity_schema.sql] staff (
id integer PRIMARY KEY,
name  NOT NULL,
type  DEFAULT 'STAFF'
office_space ,
)[WITHOUT ROWID];

CREATE TABLE [IF NOT EXIST] [amity_schema.sql].fellows(
id integer PRIMARY KEY,
name  NOT NULL,
type  DEFAULT 'FELLOW',
office_space ,
living_space ,
accommodation CHAR DEFAULT 'N'
)[WITHOUT ROWID];

CREATE TABLE [IF NOT EXIST] [amity_schema.sql].offices(
id integer PRIMARY KEY,
name  not NULL,
type  DEFAULT 'OFFICE',
MAX_CAPACITY integer DEFAULT 6
)[WITHOUT ROWID];

CREATE TABLE [IF NOT EXIST] [amity_schema.sql].offices_occupants(
id integer PRIMARY KEY,
FOREIGN KEY (id) REFERENCES offices (id)
ON DELETE CASCADE ON UPDATE NO ACTION
occupant_1 ,
occupant_2 ,
occupant_3 ,
occupant_4 ,
occupant_5 ,
occupant_6 
);

CREATE TABLE [IF NOT EXIST] [amity_schema.sql].livingspaces(
id integer PRIMARY KEY,
name  not NULL,
type  DEFAULT 'LIVING',
MAX_CAPACITY integer DEFAULT 4
)[WITHOUT ROWID];

CREATE TABLE [IF NOT EXIST] [amity_schema.sql].livingspaces_occupants(
id integer PRIMARY KEY,
FOREIGN KEY (id) REFERENCES livingspaces (id)
ON DELETE CASCADE ON UPDATE NO ACTION
occupant_1 ,
occupant_2 ,
occupant_3 ,
occupant_4 
);