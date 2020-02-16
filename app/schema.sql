DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS beat;
DROP TABLE IF EXISTS producer;
DROP TABLE IF EXISTS client;


CREATE TABLE client(
	c_id BINARY(16) NOT NULL UNIQUE,
	email VARCHAR(36) NOT NULL UNIQUE,
	phone_number INT(20) NOT NULL UNIQUE,
	name VARCHAR(36) NOT NULL,
	pwd VARCHAR(36) NOT NULL,

	PRIMARY KEY(c_id)
);

CREATE TABLE producer(
	producer_id BINARY(16) NOT NULL UNIQUE,
	email VARCHAR(36) NOT NULL UNIQUE,
	name VARCHAR(36) NOT NULL,
	phone_number VARCHAR(36) NOT NULL UNIQUE,
	pwd VARCHAR(36) NOT NULL,

	PRIMARY KEY(producer_id)
);

CREATE TABLE beat(
	beat_id BINARY(16) UNIQUE NOT NULL,
	producer_id BINARY(16) NOT NULL,
	name VARCHAR(36) NOT NULL,
	genre VARCHAR(36) NOT NULL,
	address VARCHAR(36) NOT NULL,
	preview_address VARCHAR(36) NOT NULL,
	lease_price INT(11) NOT NULL,
	selling_price INT(11),

	PRIMARY KEY(beat_id),
	FOREIGN KEY(producer_id) REFERENCES producer(producer_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE payment(
	payment_id BINARY(16) UNIQUE NOT NULL,
	beat_id BINARY(16) NOT NULL,
	amount INT(11) NOT NULL,
	client_id BINARY(16) NOT NULL,

	PRIMARY KEY(payment_id),
	FOREIGN KEY(beat_id) REFERENCES beat(beat_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);