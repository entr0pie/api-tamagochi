BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "parent" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"surname"	TEXT,
	"password"	TEXT NOT NULL,
	"gender"	TEXT NOT NULL DEFAULT 'n' CHECK("gender" IN ('f', 'm', 'n')),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "children" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"surname"	TEXT,
	"acess_token"	TEXT NOT NULL,
	"balance"	INTEGER NOT NULL DEFAULT 0,
	"gender"	TEXT NOT NULL DEFAULT 'n' CHECK("gender" IN ('f', 'm', 'n')),
	"id_parent_fk"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_parent_fk") REFERENCES "parent"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "task" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"period"	INTEGER,
	"frequency"	TEXT NOT NULL,
	"is_visible"	INTEGER NOT NULL DEFAULT 0 CHECK("is_visible" IN (0, 1)),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "inventory" (
	"id"	INTEGER NOT NULL UNIQUE,
	"id_children"	INTEGER NOT NULL,
	"id_item"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_children") REFERENCES "children"("id") ON DELETE CASCADE,
	FOREIGN KEY("id_item") REFERENCES "item"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tamagochi" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"head"	INTEGER,
	"chest"	INTEGER,
	"feet"	INTEGER,
	"glasses"	INTEGER,
	"scenario"	INTEGER,
	"size"	INTEGER NOT NULL,
	"id_children_fk"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("head") REFERENCES "inventario"("id") ON UPDATE CASCADE,
	FOREIGN KEY("chest") REFERENCES "inventario"("id") ON UPDATE CASCADE,
	FOREIGN KEY("feet") REFERENCES "inventario"("id") ON UPDATE CASCADE,
	FOREIGN KEY("glasses") REFERENCES "inventario"("id") ON UPDATE CASCADE,
	FOREIGN KEY("scenario") REFERENCES "inventario"("id") ON UPDATE CASCADE,
	FOREIGN KEY("id_children_fk") REFERENCES "children"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "mood" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"category"	TEXT NOT NULL CHECK("category" IN ('positive', 'negative')),
	"image"	BLOB NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "reward" (
	"id"	INTEGER NOT NULL UNIQUE,
	"type"	INTEGER NOT NULL,
	"value"	INTEGER NOT NULL DEFAULT 0,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "item" (
	"id"	INTEGER NOT NULL UNIQUE,
	"type"	TEXT NOT NULL CHECK("type" IN ('head', 'chest', 'feet', 'glasses', 'scenario')),
	"description"	TEXT NOT NULL,
	"image"	BLOB NOT NULL,
	"value"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "log_reward" (
	"id"				INTEGER NOT NULL UNIQUE,
	"id_reward_fk"		INTEGER NOT NULL,
	"id_children_fk"	INTEGER NOT NULL,
	"timestamp"			DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_reward_fk") REFERENCES "reward"("id"),
	FOREIGN KEY("id_children_fk") REFERENCES "children"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "children_task" (
	"id"				INTEGER NOT NULL UNIQUE,
	"id_children_fk"	INTEGER NOT NULL,
	"id_task_fk"		INTEGER NOT NULL,
	"is_done"			INTEGER NOT NULL DEFAULT 0 CHECK("is_done" IN (0, 1)),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_task_fk") REFERENCES "tarefa"("id_task_pk") ON DELETE CASCADE,
	FOREIGN KEY("id_children_fk") REFERENCES "children"("id_children_pk") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "log_mood" (
	"id"	INTEGER NOT NULL UNIQUE,
	"id_mood_fk"	INTEGER NOT NULL,
	"id_children_fk"	INTEGER NOT NULL,
	"id_children_task_fk"	INTEGER,
	"timestamp"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_mood_fk") REFERENCES "mood"("id") ON DELETE CASCADE,
	FOREIGN KEY("id_children_fk") REFERENCES "children"("id_children_pk") ON DELETE CASCADE,
	FOREIGN KEY("id_children_task_fk") REFERENCES "children_task"("id")
);
COMMIT;
