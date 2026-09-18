create database if not exists club_encuentro;
use club_encuentro;
-- Creación de las 4 tablas: deportes, canchas, socios y reservas.
create table if not exists deportes (
id INT auto_increment primary key,
nombre VARCHAR(190) not null unique
);

create table if not exists canchas (
id INT auto_increment primary key,
nombre VARCHAR(190) not null,
id_deporte INT not null,
precio_hora INT not null check (precio_hora > 0), -- valida que la tarifa sea entera y positiva
techada BOOLEAN not null default false, 
activa BOOLEAN not null default true,
foreign key (id_deporte) references deportes(id) -- relaciona la columna id_deporte con la pk de la tabla deportes
);

create table if not exists socios (
id INT auto_increment primary key,
nombre VARCHAR(190) not null,
email VARCHAR(190) not null unique, -- unique impide que un socio se registre con el mismo email. *NOTA*: Debe ser en minúscula y sin espacio en sus extremos
activo BOOLEAN not null default true
);

create table if not exists reservas (
id INT auto_increment primary key,
id_socio INT not null,
id_cancha INT not null,
fecha_hora_inicio DATETIME not null, -- la zona horaria fija es GMT-3
fecha_hora_fin DATETIME not null,
precio_hora INT not null check (precio_hora > 0),
precio_total INT not null check (precio_total > 0),
estado VARCHAR(20) not null default 'confirmada' check (estado in('confirmada', 'cancelada', 'finalizada')),
foreign key (id_socio) references  socios(id),
foreign key (id_cancha) references canchas(id)
);
-- precarga inicial de deportes
insert ignore into deportes (id, nombre)
values (1, 'Fútbol'), (2, 'Pádel'), (3, 'Tenis');