BEGIN TRANSACTION;
CREATE TABLE `staff` (
	`id`	INTEGER,
	`name`	TEXT NOT NULL,
	`type`	TEXT DEFAULT 'STAFF',
	`office_space`	TEXT,
	PRIMARY KEY(`id`)
);
CREATE TABLE "offices_occupants" (
	`id`	INTEGER UNIQUE,
	`occupant_1`	TEXT,
	`occupant_2`	TEXT,
	`occupant_3`	TEXT,
	`occupant_4`	TEXT,
	`occupant_5`	TEXT,
	`occupant_6`	INTEGER,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`id`) REFERENCES offices
) WITHOUT ROWID;
CREATE TABLE `offices` (
	`id`	INTEGER,
	`name`	TEXT,
	`type`	TEXT DEFAULT 'OFFICE',
	`MAX_CAPACITY`	INTEGER DEFAULT 6,
	PRIMARY KEY(`id`)
) WITHOUT ROWID;
CREATE TABLE "livingspaces_occupants" (
	`id`	INTEGER UNIQUE,
	`occupant_1`	TEXT,
	`occupant_2`	TEXT,
	`occupant_3`	TEXT,
	`occupant_4`	TEXT,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`id`) REFERENCES `livingspaces`(`id`)
) WITHOUT ROWID;
CREATE TABLE "livingspaces" (
	`id`	INTEGER UNIQUE,
	`name`	TEXT,
	`type`	TEXT DEFAULT 'LIVING',
	`MAX_CAPACITY`	INTEGER DEFAULT 4,
	PRIMARY KEY(`id`)
);
CREATE TABLE `fellows` (
	`id`	INTEGER,
	`name`	TEXT,
	`type`	TEXT DEFAULT 'FELLOW',
	`office_space`	TEXT,
	`living_space`	TEXT,
	`accommodation`	TEXT DEFAULT 'N',
	PRIMARY KEY(`id`)
) WITHOUT ROWID;
COMMIT;
