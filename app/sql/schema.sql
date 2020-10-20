DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS beat;
DROP TABLE IF EXISTS producer;
DROP TABLE IF EXISTS client;


CREATE TABLE client(
	c_id BINARY(16) NOT NULL UNIQUE,
	profile_image VARCHAR(100) NOT NULL UNIQUE,
	email VARCHAR(36) NOT NULL UNIQUE,
	phone_number INT(20) NOT NULL UNIQUE,
	name VARCHAR(36) NOT NULL,
	pwd VARCHAR(1024) NOT NULL,

	PRIMARY KEY(c_id)
);

CREATE TABLE client_profile(
	profile_id BINARY(16) NOT NULL UNIQUE,
	client_id BINARY(16) NOT NULL,

	bio VARCHAR(255),
	profession VARCHAR(100),
	address VARCHAR(100),
	city VARCHAR(100),

	PRIMARY KEY(profile_id),
	FOREIGN KEY(client_id) REFERENCES client(c_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE producer(
	producer_id BINARY(16) NOT NULL UNIQUE,
	profile_image VARCHAR(100) NOT NULL UNIQUE,
	email VARCHAR(36) NOT NULL UNIQUE,
	name VARCHAR(36) NOT NULL,
	phone_number VARCHAR(36) NOT NULL UNIQUE,
	pwd VARCHAR(1024) NOT NULL,

	PRIMARY KEY(producer_id)
);

CREATE TABLE producer_profile(
	profile_id BINARY(16) NOT NULL UNIQUE,
	producer_id BINARY(16) NOT NULL,
	bio VARCHAR(255),
	profession VARCHAR(100),
	address VARCHAR(100),
	city VARCHAR(100),

	PRIMARY KEY(profile_id),
	FOREIGN KEY(producer_id) REFERENCES producer(producer_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE beat(
	beat_id BINARY(16) UNIQUE NOT NULL,
	producer_id BINARY(16) NOT NULL,
	beat_image VARCHAR(100) NOT NULL,
	name VARCHAR(36) NOT NULL,
	address VARCHAR(100) NOT NULL,
	prev_address VARCHAR(100) NOT NULL,
	lease_price INT(11) NOT NULL,
	selling_price INT(11) NOT NULL,
	upload_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	beat_hash VARCHAR(100) NOT NULL,

	PRIMARY KEY(beat_id),
	FOREIGN KEY(producer_id) REFERENCES producer(producer_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE beat_interaction(
	interaction_id BINARY(16) UNIQUE NOT NULL,
	interaction_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	beat_id BINARY(16) NOT NULL,

	PRIMARY KEY(interaction_id),
	FOREIGN KEY(beat_id) REFERENCES beat(beat_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE category(
	category_id BINARY(16) UNIQUE NOT NULL,
	category_name VARCHAR(36) NOT NULL,
	PRIMARY KEY(entry_id),
);

CREATE TABLE payment(
	payment_id BINARY(16) UNIQUE NOT NULL,
	beat_id BINARY(16) NOT NULL,
	amount INT(11) NOT NULL,
	client_id BINARY(16) NOT NULL,

	PRIMARY KEY(payment_id),
	FOREIGN KEY (beat_id) REFERENCES beat(beat_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE category(
	category_id BINARY(16) UNIQUE NOT NULL,
	category_name VARCHAR(16) NOT NULL,

	PRIMARY KEY(category_id)
);
