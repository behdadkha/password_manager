CREATE TABLE user(
	username varchar(50) NOT NULL,
	password varchar(100) NOT NULL,
	PRIMARY KEY(username)
);

CREATE TABLE website(
	username varchar(50) NOT NULL,
	URL varchar(100),
	web_username varchar(50),
	web_password varchar(50),

	FOREIGN KEY(username) refrences user(username) on DELETE CASCADE
);