create table customer (
	email			varchar(50) not null,
	password		varchar(50),
	name 			varchar(50),
	building_num	numeric(5),
	street			varchar(50),
	city			varchar(50),
	state			varchar(2),
	phone_num		numeric(20),
	pass_num		numeric(9),
	pass_expiration	date,
	pass_country	varchar(50),
	date_of_birth	date,
	
	primary key (email)
);

create table airline_staff (
	username		varchar(50) not null,
	password		varchar(50),
	f_name			varchar(50),
	l_name			varchar(50),
	date_of_birth	date,
	phone_num		numeric(20),
	email			varchar(50) not null,
	airline_name	varchar(50) not null,

	
	primary key (username),
	foreign key (airline_name) references airline
		on delete cascade on update cascade
);

create table airline (
	airline_name	varchar(50) not null,
	
	primary key (airline_name)
);

create table airplane (
	airplane_ID		numeric(5) not null,
	airline_name	varchar(50) not null,
	num_of_seats	numeric(5),
	company			varchar(50),
	age				numeric(5),
	
	primary key (airplane_ID),
	foreign key (airline_name) references airline
		on delete cascade on update cascade
);

create table flight (
	airline_name	varchar(50) not null,
	airplane_ID		numeric(5) not null,
	flight_num		numeric(10) not null,
	base_price		numeric(7, 2) not null,
	status			varchar(9) not null
		check (status in ('delayed', 'on time', 'cancelled')),
	depart_airport	varchar(50),
	arrive_airport	varchar(50),
	depart_time		timestamp not null,
	arrive_time		timestamp,
	
	primary key (flight_num),
	foreign key (airline_name) references airline
		on delete cascade on update cascade,
	foreign key (depart_airport, arrive_airport) references airport
		on delete cascade on update cascade,
	foreign key (airplane_ID) references airplane
		on delete cascade on update cascade
);

create table airport (
	name	varchar(50) not null,
	city	varchar(50),
	country	varchar(50),
	type	varchar(13)
		check (type in ('domestic', 'international', 'both')),
	
	primary key (name)
);

create table purchase (
	email			varchar(50) not null,
	ticket_ID		numeric(10) not null,
	purchase_dt		timestamp,
	card_type		varchar(50),
	card_num		numeric(16),
	card_holder		varchar(50),
	card_expiration	date,
	
	foreign key (email) references customer
		on delete cascade on update cascade,
	foreign key (ticket_ID) references ticket
		on delete cascade on update cascade
);

create table ticket (
	ticket_ID		numeric(10) not null,
	airline_name	varchar(50) not null,
	flight_num		numeric(10) not null,
	sold_price		numeric(7, 2) not null,
	
	primary key (ticket_ID),
	foreign key (airline_name) references airline
		on delete cascade on update cascade,
	foreign key (flight_num) references flight
		on delete cascade on update cascade
);

create table rate (
	email		varchar(50) not null,
	flight_num	numeric(10) not null,
	comment		varchar(50) not null,
	stars		int not null,
	
	foreign key (email) references customer
		on delete cascade on update cascade,
	foreign key (flight_num) references flight
		on delete cascade on update cascade
);
