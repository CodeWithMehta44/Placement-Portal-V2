# 🎓 Placement Portal V2

A full-stack Placement Portal Application built using **Flask**, **Vue.js**, and **SQLite**. The portal provides role-based access for **Admin**, **Student**, and **Company** users with secure JWT authentication.

---

# 🚀 Tech Stack

## Backend
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- SQLite

## Frontend
- Vue 3
- Vue Router
- Axios
- Vite

---

# 📂 Project Structure

```
Placement-Portal-V2
│
├── backend
│   ├── models
│   ├── routes
│   ├── app.py
│   ├── database.py
│   └── seed.py
│
├── frontend
│   ├── src
│   │   ├── views
│   │   ├── router
│   │   ├── services
│   │   └── components
│   └── public
│
└── README.md
```

---

# ✨ Features

## 👨‍💼 Admin
- Secure Login
- JWT Authentication
- Protected Dashboard
- View Logged-in Profile
- Logout

---

## 👨‍🎓 Student
- Student Registration
- Student Login
- JWT Authentication
- Protected Dashboard
- Logout

---

## 🏢 Company
- Company Login
- Protected Dashboard
- Logout

---

# 🔐 Authentication

- JWT-based Authentication
- Password Hashing
- Role-Based Access Control
- Protected API Routes
- Axios Interceptors
- Route Guards
- Automatic User Authentication
- Secure Logout

---

# 🗄️ Database Models

- User
- Student
- Company
- Job Position
- Application
- Placement

---

# 📌 Milestone Progress

## ✅ Milestone 1 - Database Models & Schema

- User Model
- Student Model
- Company Model
- Job Position Model
- Application Model
- Placement Model
- Database Relationships
- Admin Seed Script

**Status:** ✅ Completed

---

## ✅ Milestone 2 - Authentication & Role-Based Access

- Student Registration
- Login System
- JWT Authentication
- Role-Based Routing
- Protected Routes
- Axios Interceptors
- Current User API (`/me`)
- Logout
- Dashboard Authentication

- Milestone 3 - CompanyDashboard 

**Status:** ✅ Completed

---

## ⏳ Upcoming Milestones

- Placement Drive Management
- Company Approval
- Student Applications
- Resume Upload
- Placement Management
- Admin Analytics

---

# ⚙️ Installation

## Backend Setup

```bash
cd backend

pip install -r requirements.txt

python seed.py

python app.py
```

Backend runs on:

```
http://127.0.0.1:5000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

# 🔑 Default Admin Credentials

```
Email:
admin@portal.com

Password:
admin123
```

---

# 👨‍💻 Author

**Ashish Mehta**

IIT Madras BS Degree Student

Learning Full Stack Development through Project-Based Development.

---
