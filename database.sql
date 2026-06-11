CREATE DATABASE IF NOT EXISTS akademik_ica;
USE akademik_ica;

==========================================
CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
==========================================
CREATE TABLE IF NOT EXISTS mahasiswa (
    nim VARCHAR(20) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    jurusan VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);
==========================================
CREATE TABLE IF NOT EXISTS mata_kuliah (
    kode VARCHAR(10) PRIMARY KEY,
    nama_matkul VARCHAR(100) NOT NULL,
    sks INT NOT NULL
);
==========================================
CREATE TABLE IF NOT EXISTS nilai (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nim VARCHAR(20),
    kode_matkul VARCHAR(10),
    nilai FLOAT,
    FOREIGN KEY (nim) REFERENCES mahasiswa(nim) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (kode_matkul) REFERENCES mata_kuliah(kode) ON DELETE CASCADE ON UPDATE CASCADE
);
==========================================
CREATE TABLE IF NOT EXISTS log_aktivitas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pengguna VARCHAR(100),
    aktivitas TEXT,
    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
=========================================
INSERT INTO admin (username, password) VALUES
('admin', '$2b$12$yHn9JjZ6vID7C1P7Q9Yy7uP8bM.1mG9zWJZbHk4mL0clzLQZkOpni'); 
=========================================
INSERT INTO mata_kuliah (kode, nama_matkul, sks) VALUES
('IF101', 'Dasar Pemrograman', 3),
('IF102', 'Struktur Data', 3),
('IF103', 'Basis Data', 3),
('IF104', 'Jaringan Komputer', 3),
('IF105', 'Keamanan Siber', 3),
('IF106', 'Sistem Operasi', 3),
('IF107', 'Kecerdasan Buatan', 3);
