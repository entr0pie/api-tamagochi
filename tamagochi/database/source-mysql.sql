CREATE DATABASE Tamagochi IF NOT EXISTS; 
USE Tamagochi;

CREATE TABLE Parent IF NOT EXISTS (
  id int not null auto_increment,
  name varchar(255) not null,
  surname varchar(255) not null,
  email varchar(64) not null,
  password varchar(32) not null,
  gender enum('m', 'f', 'n') not null,
  PRIMARY KEY(id)
);

CREATE TABLE Child IF NOT EXISTS (
  id int not null auto_increment,
  name varchar(255) not null,
  surname varchar(255) not null,
  access_token varchar(64) not null,
  balance int unsigned not null,
  gender enum('m', 'f', 'n') not null,
  parent int not null,
  PRIMARY KEY(id),
  FOREIGN KEY(parent) REFERENCES Parent(id)
);

CREATE TABLE Task IF NOT EXISTS (
  id int not null auto_increment,
  name VARCHAR(64) not null,
  description VARCHAR(255) not null,
  period enum('morning', 'afternoon', 'night') not null,
  frequency VARCHAR(16) not null,
  is_visible BOOLEAN not null,
  parent int not null,
  PRIMARY KEY(id),
  FOREIGN KEY(parent) REFERENCES Parent(id)
);

CREATE TABLE Item IF NOT EXISTS (
	id int not null auto_increment,
  type enum('head', 'chest', 'feet', 'glasses', 'scenario') NOT NULL,
  description varchar(255) not null,
  image BLOB not null,
  value smallint unsigned not null,
  PRIMARY KEY(id)
);

CREATE TABLE Inventory IF NOT EXISTS (
  id int not null auto_increment,
  child int not null,
  item int not null,
  FOREIGN KEY(child) REFERENCES Child(id),
  FOREIGN KEY(item) REFERENCES Item(id)
);

CREATE TABLE Tamagochi IF NOT EXISTS (
	id int not null auto_increment,
  name varchar(64) not null,
  head int not null,
  chest int not null,
  feet int not null,
  glasses int not null,
  scenario int not null,
  size int not null,
  child int not null,
  PRIMARY KEY (id),
  FOREIGN KEY (head) REFERENCES Item (id),
  FOREIGN KEY (chest) REFERENCES Item (id),
  FOREIGN KEY (feet) REFERENCES Item (id),
  FOREIGN KEY (glasses) REFERENCES Item (id),
  FOREIGN KEY (scenario) REFERENCES Item (id),
  FOREIGN KEY (child) REFERENCES Child (id)
);

CREATE TABLE Mood IF NOT EXISTS (
  id int not null auto_increment,
  name varchar(32) not null,
  category enum('positive', 'negative') not null,
  image BLOB not null,
  PRIMARY KEY(id)
);

CREATE TABLE Reward IF NOT EXISTS (
  id int not null auto_increment,
  type int not null,
  value smallint unsigned not null,
  description varchar(255) not null,
  PRIMARY KEY(id)
);

CREATE TABLE Log_Reward IF NOT EXISTS (
  id int not null auto_increment,
  reward int not null,
  child int not null, 
  timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(reward) REFERENCES Reward(id),
  FOREIGN KEY(child) REFERENCES Child(id),
  PRIMARY KEY(id)
);

CREATE TABLE Child_Task IF NOT EXISTS (
  id int not null auto_increment,
  child int not null,
  task int not null,
  done BOOLEAN not null,
  PRIMARY KEY(id),
  FOREIGN KEY(child) REFERENCES Child(id),
  FOREIGN KEY(task) REFERENCES Task(id)
);

CREATE TABLE Log_Mood IF NOT EXISTS (
  id int not null auto_increment,
  mood int not null,
  child int not null,
  child_task int not null,
  PRIMARY KEY(id),
  FOREIGN KEY(mood) REFERENCES Mood(id),
  FOREIGN KEY(child) REFERENCES Child(id),
  FOREIGN KEY(child_task) REFERENCES Child_Task(id)
);


