# Academic Information System with CIA Triad Security Principle

A secure Academic Information System built using **Python** and integrated with a **MySQL** database. This system handles student data, courses, and grade management while strictly adhering to core information security guidelines.

## 🚀 Features & Security Implementation

### 1. Security Core (CIA Triad Principles)
* **Confidentiality:** Multi-user access control differentiating Admins and Students. Sensitive credentials are secured using **Password Hashing** in the database.
* **Integrity:** Role-based access control grants data manipulation rights (CRUD) exclusively to Admins. To ensure auditability, the system records an **Activity Log / Audit Trail**.
* **Availability:** Powered by a stable platform architecture combining Python and real-time database transactions via MySQL.

### 2. User Roles & Functionalities
* **Admin Menu:** Kelola Mahasiswa (CRUD), Kelola Dosen, Kelola Mata Kuliah, Kelola KRS (Grades), and Backup Database.
* **Student Menu:** View Personal Profile, View Grades per Semester, View Course List, and View Faculty Data.

## 🛠️ Tech Stack & Tools Used
* **Language:** Python
* **Database:** MySQL (XAMPP / phpMyAdmin)
* **IDE:** PyCharm / VS Code
