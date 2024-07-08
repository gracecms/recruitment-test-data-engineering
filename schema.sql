drop table if exists people;
drop table if exists places;

create table places (
    id int auto_increment primary key,
    city varchar(255) unique,
    county varchar(255),
    country varchar(255)
);


create table people (
    id int auto_increment primary key,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    date_of_birth DATE,
    city_of_birth VARCHAR(255),
    FOREIGN KEY (city_of_birth) REFERENCES places(city)
);
