###akademik_ica.py
from moduls.auth import login_admin, registrasi_admin, login_mahasiswa
from moduls.mahasiswa import tambah_mahasiswa, lihat_mahasiswa, lihat_info_pribadi
from moduls.nilai import tambah_nilai, lihat_nilai_mahasiswa
from moduls.matakuliah import lihat_matakuliah
from moduls.backup import backup_data

def menu_admin():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Tambah Mahasiswa")
        print("2. Lihat Mahasiswa")
        print("3. Tambah Nilai")
        print("4. Lihat Nilai")
        print("5. Backup Data")
        print("6. Lihat Mata Kuliah")
        print("7. Hapus Mahasiswa")
        print("8. Kembali")
        pilih = input("Pilih: ")

        if pilih == "1":
            tambah_mahasiswa()
        elif pilih == "2":
            lihat_mahasiswa()
        elif pilih == "3":
            tambah_nilai()
        elif pilih == "4":
            nim = input("Masukkan NIM Mahasiswa: ")
            lihat_nilai_mahasiswa(nim)
        elif pilih == "5":
            backup_data()
        elif pilih == "6":
            lihat_matakuliah()
        elif pilih == "7":
            from moduls.mahasiswa import hapus_mahasiswa
            hapus_mahasiswa()
        elif pilih == "8":
            break
        else:
            print("Pilihan tidak valid!")

def menu_mahasiswa(nim):
    while True:
        print("\n=== Menu Mahasiswa ===")
        print("1. Lihat Info Pribadi")
        print("2. Lihat Nilai")
        print("3. Lihat Mata Kuliah")
        print("4. Keluar")
        pilih = input("Pilih: ")

        if pilih == "1":
            lihat_info_pribadi(nim)
        elif pilih == "2":
            lihat_nilai_mahasiswa(nim)
        elif pilih == "3":
            lihat_matakuliah()
        elif pilih == "4":
            break
        else:
            print("Pilihan tidak valid!")

def main():
    while True:
        print("\n=== Sistem Akademik ICA ===")
        print("1. Login Admin")
        print("2. Registrasi Admin")
        print("3. Login Mahasiswa")
        print("4. Keluar")
        pilih = input("Pilih: ")

        if pilih == "1":
            if login_admin():
                menu_admin()
        elif pilih == "2":
            registrasi_admin()
        elif pilih == "3":
            nim = login_mahasiswa()
        if nim:
            menu_mahasiswa(nim)
        elif pilih == "4":
            print("Terima kasih telah menggunakan Sistem Akademik ICA!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()

###__init__.py

###db.py
import mysql.connector

def connect():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",            # sesuaikan username MySQL kamu
            password="",            # isi password jika ada
            database="akademik_ica" # pastikan database ini sudah dibuat
        )
        return db
    except mysql.connector.Error as err:
        print(f" Gagal koneksi ke database: {err}")
        return None

###auth.py
from moduls.db import connect
import bcrypt

# =============================
# Registrasi Admin
# =============================
def registrasi_admin():
    db = connect()
    if not db:
        return
    username = input("Masukkan username baru: ")
    password = input("Masukkan password: ")

    # hash password sebelum disimpan
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, hashed_pw))
        db.commit()
        print(" Registrasi admin berhasil!")
    except Exception as e:
        print(f" Gagal registrasi admin: {e}")
    finally:
        cursor.close()
        db.close()


# =============================
# Login Admin
# =============================
def login_admin():
    db = connect()
    if not db:
        return False

    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    cursor = db.cursor()
    cursor.execute("SELECT password FROM admin WHERE username=%s", (username,))
    result = cursor.fetchone()

    if result:
        stored_hash = result[0].encode('utf-8') if isinstance(result[0], str) else result[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            print(f"Login berhasil! Selamat datang, {username}")
            return True
        else:
            print("Password salah.")
    else:
        print("Username tidak ditemukan.")

    cursor.close()
    db.close()
    return False


# =============================
# Login Mahasiswa
# =============================
def login_mahasiswa():
    db = connect()
    if not db:
        return False

    nim = input("Masukkan NIM Mahasiswa: ")
    password = input("Masukkan Password: ")

    cursor = db.cursor()
    cursor.execute("SELECT password, nama FROM mahasiswa WHERE nim=%s", (nim,))
    result = cursor.fetchone()

    if result:
        stored_hash = result[0].encode('utf-8') if isinstance(result[0], str) else result[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            print(f"Login mahasiswa berhasil! Selamat datang, {result[1]}")
            return nim
        else:
            print("Password salah.")
    else:
        print("NIM tidak ditemukan.")

    cursor.close()
    db.close()
    return False

###mahasiswa.py
import mysql.connector
from moduls.db import connect
from bcrypt import hashpw, gensalt

# ========================================
# TAMBAH MAHASISWA
# ========================================
def tambah_mahasiswa():
    db = connect()
    if not db:
        print(" Gagal koneksi ke database.")
        return

    cursor = db.cursor()
    nim = input("Masukkan NIM: ")
    nama = input("Masukkan Nama: ")
    jurusan = input("Masukkan Jurusan: ")
    password = input("Masukkan Password Mahasiswa: ")

    hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    try:
        cursor.execute(
            "INSERT INTO mahasiswa (nim, nama, jurusan, password) VALUES (%s, %s, %s, %s)",
            (nim, nama, jurusan, hashed_password)
        )
        db.commit()
        print("Mahasiswa berhasil ditambahkan!")
    except Exception as e:
        print("Gagal menambah mahasiswa:", e)
    finally:
        cursor.close()
        db.close()


# ========================================
# LIHAT MAHASISWA
# ========================================
def lihat_mahasiswa():
    db = connect()
    if not db:
        print("Gagal koneksi ke database.")
        return

    cursor = db.cursor()
    cursor.execute("SELECT nim, nama, jurusan FROM mahasiswa")
    result = cursor.fetchall()

    print("\n=== Daftar Mahasiswa ===")
    for mhs in result:
        print(f"NIM: {mhs[0]}, Nama: {mhs[1]}, Jurusan: {mhs[2]}")

    cursor.close()
    db.close()


# ========================================
# LIHAT INFO PRIBADI MAHASISWA
# ========================================
def lihat_info_pribadi(nim):
    db = connect()
    if not db:
        print("Gagal koneksi ke database.")
        return

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT nim, nama, jurusan FROM mahasiswa WHERE nim = %s", (nim,))
    data = cursor.fetchone()

    if data:
        print("\n=== Info Pribadi Mahasiswa ===")
        print(f"NIM     : {data['nim']}")
        print(f"Nama    : {data['nama']}")
        print(f"Jurusan : {data['jurusan']}")
    else:
        print("Data mahasiswa tidak ditemukan.")

# ========================================
# HAPUS MAHASISWA
# ========================================
def hapus_mahasiswa():
    db = connect()
    if not db:
        print("Gagal koneksi ke database.")
        return

    cursor = db.cursor()
    nim = input("Masukkan NIM Mahasiswa yang ingin dihapus: ").strip()

    try:
        # Cek apakah mahasiswa ada
        cursor.execute("SELECT * FROM mahasiswa WHERE nim = %s", (nim,))
        data = cursor.fetchone()

        if not data:
            print("❌ Mahasiswa tidak ditemukan.")
            return

        konfirmasi = input(f"Apakah Anda yakin ingin menghapus mahasiswa '{data[1]}' (NIM: {nim})? (y/n): ").lower()
        if konfirmasi == "y":
            # Hapus nilai terkait di tabel nilai terlebih dahulu (jika ada)
            cursor.execute("DELETE FROM nilai WHERE nim = %s", (nim,))
            # Hapus mahasiswa
            cursor.execute("DELETE FROM mahasiswa WHERE nim = %s", (nim,))
            db.commit()
            print("✅ Mahasiswa dan data nilainya berhasil dihapus!")
        else:
            print("❌ Penghapusan dibatalkan.")

    except Exception as e:
        print(f"Terjadi kesalahan saat menghapus mahasiswa: {e}")
    finally:
        cursor.close()
        db.close()

###nilai.py
from moduls.db import connect

def tambah_nilai():
    db = connect()
    cursor = db.cursor()
    nim = input("Masukkan NIM: ")
    kode_matkul = input("Masukkan Kode Mata Kuliah: ")
    nilai = input("Masukkan Nilai: ")

    try:
        cursor.execute(
            "INSERT INTO nilai (nim, kode_matkul, nilai) VALUES (%s, %s, %s)",
            (nim, kode_matkul, nilai)
        )
        db.commit()
        print("Nilai berhasil ditambahkan.")
    except mysql.connector.Error as err:
        print(f"Gagal menambah nilai: {err}")
    finally:
        cursor.close()
        db.close()

def lihat_nilai_mahasiswa(nim):
    db = connect()
    if not db: return
    cursor = db.cursor()
    cursor.execute("""
        SELECT m.nama_matkul, n.nilai 
        FROM nilai n 
        JOIN mata_kuliah m ON n.kode_matkul = m.kode 
        WHERE n.nim=%s
    """, (nim,))
    data = cursor.fetchall()
    print("\n=== Nilai Mahasiswa ===")
    if data:
        for d in data:
            print(f"{d[0]}: {d[1]}")
    else:
        print("Belum ada nilai.")

###matakuliah.py
from moduls.db import connect

def lihat_matakuliah():
    db = connect()
    if not db: return
    cursor = db.cursor()
    cursor.execute("SELECT kode, nama_matkul, sks FROM mata_kuliah")
    data = cursor.fetchall()
    print("\n=== Daftar Mata Kuliah ===")
    for d in data:
        print(f"{d[0]} - {d[1]} ({d[2]} SKS)")
    print("==========================")

###backup.py
import os
import subprocess

def backup_data():
    try:
        backup_dir = "SistemAkademikICA/database"
        backup_file = os.path.join(backup_dir, "akademik_ica.sql")

        # Buat folder jika belum ada
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Jalankan perintah mysqldump
        command = "mysqldump -u root --password= your_password akademik_ica > " + backup_file
        os.system(command)

        print(f" Backup database berhasil disimpan ke: {backup_file}")
    except Exception as e:
        print(f" Gagal backup: {e}")

###log_activity
def log(aksi, nama):
    with open("SistemAkademikICA/backup/log.txt", "a") as f:
        f.write(f"{aksi} oleh {nama}\n")

###.env
DB_HOST=localhost
DB_USER=root
DB_PASS=
DB_NAME=akademik_ica

###requirements.txt
mysql-connector-python
bcrypt
python-dotenv
