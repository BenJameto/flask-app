-- Creación de la tabla Hospital
CREATE TABLE IF NOT EXISTS hospital (
    ID_hospital SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

-- Creación de la tabla Paciente
CREATE TABLE IF NOT EXISTS paciente (
    ID_paciente SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido_p VARCHAR(50) NOT NULL,
    apellido_m VARCHAR(50),
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    email VARCHAR(100)
);

-- Creación de la tabla Medico
CREATE TABLE IF NOT EXISTS medico (
    ID_doctor SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido_p VARCHAR(50) NOT NULL,
    apellido_m VARCHAR(50),
    departamento VARCHAR(100),
    ID_hospital INTEGER,
    telefono VARCHAR(20),
    email VARCHAR(100),
    FOREIGN KEY (ID_hospital) REFERENCES hospital(ID_hospital) ON DELETE SET NULL
);

-- Creación de la tabla Cita
CREATE TABLE IF NOT EXISTS cita (
    ID_cita SERIAL PRIMARY KEY,
    fecha_creacion DATE NOT NULL,
    hora TIME NOT NULL,
    estado VARCHAR(20),
    motivo VARCHAR(255),
    ID_paciente INTEGER,
    ID_doctor INTEGER,
    FOREIGN KEY (ID_paciente) REFERENCES paciente(ID_paciente) ON DELETE CASCADE,
    FOREIGN KEY (ID_doctor) REFERENCES medico(ID_doctor) ON DELETE SET NULL
);

-- Creación de la tabla Receta
CREATE TABLE IF NOT EXISTS receta (
    ID_receta SERIAL PRIMARY KEY,
    fecha_emision DATE NOT NULL,
    medicamento VARCHAR(255) NOT NULL,
    ID_paciente INTEGER,
    ID_doctor INTEGER,
    FOREIGN KEY (ID_paciente) REFERENCES paciente(ID_paciente) ON DELETE CASCADE,
    FOREIGN KEY (ID_doctor) REFERENCES medico(ID_doctor) ON DELETE SET NULL
);

-- Creación de la tabla Tratamiento
CREATE TABLE IF NOT EXISTS tratamiento (
    ID_tratamiento SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    ID_paciente INTEGER,
    ID_doctor INTEGER,
    ID_receta INTEGER,
    FOREIGN KEY (ID_paciente) REFERENCES paciente(ID_paciente) ON DELETE CASCADE,
    FOREIGN KEY (ID_doctor) REFERENCES medico(ID_doctor) ON DELETE SET NULL,
    FOREIGN KEY (ID_receta) REFERENCES receta(ID_receta) ON DELETE SET NULL
);

-- Creación de la tabla Habitación
CREATE TABLE IF NOT EXISTS habitacion (
    ID_habitacion SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    ID_hospital INTEGER,
    FOREIGN KEY (ID_hospital) REFERENCES hospital(ID_hospital) ON DELETE SET NULL
);
