# **🏨 Hotel Management System (Python)**  
*A console-based hotel management system for managing bookings, rooms, and customer records.*  

![Python](https://img.shields.io/badge/Python-3.x-blue)  
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)  
![Console-Based](https://img.shields.io/badge/Interface-Console%20Only-green)  

---

## **📌 Overview**  
This **Hotel Management System** is a **Python-based console application** designed to streamline hotel operations, including:  
- **Room booking & availability checks**  
- **Customer registration & records**  
- **Billing & invoice generation**  
- **Admin management**  

Built with **Python 3** and **SQLite**, it provides a simple yet efficient solution for small to medium-sized hotels.  

---

## **✨ Features**  
### **1. User Roles**  
- **Admin**: Manage rooms, view bookings, generate reports.  
- **Receptionist**: Handle check-ins/check-outs, process payments.  
- **Guest**: View room availability (if implemented).  

### **2. Room Management**  
- Add/update/delete rooms (Standard, Deluxe, Suite).  
- Check room availability by date.  

### **3. Booking System**  
- Book/Cancel reservations.  
- Automated billing calculation.  

### **4. Database**  
- **SQLite** for storing:  
  - Customer details  
  - Room data  
  - Booking records  

---

## **⚙️ Installation & Setup**  

### **Prerequisites**  
- **Python 3.6+** ([Download Python](https://www.python.org/downloads/))  
- **SQLite3** (Usually bundled with Python)  

### **Steps to Run**  
1. **Clone the repository:**  
   ```bash
   git clone https://github.com/mahrukhkashan/Hotel-Management-System-in-Python.git
   cd Hotel-Management-System-in-Python
   ```

2. **Install dependencies (if any):**  
   ```bash
   pip install -r requirements.txt  # If a requirements file exists
   ```

3. **Run the application:**  
   ```bash
   python main.py  # or the respective entry file
   ```

---

## **📂 Project Structure**  
```
Hotel-Management-System/
├── database/            # SQLite database files
├── modules/             # Core functionality
│   ├── booking.py       # Booking logic
│   ├── room.py          # Room management
│   └── customer.py      # Customer handling
├── main.py              # Entry point
└── README.md            # Project documentation
```

---

## **🖥️ Usage**  
1. **Launch the application:**  
   ```bash
   python main.py
   ```
2. **Login as Admin/Receptionist:**  
   - Default credentials (if hardcoded):  
     - **Username:** `admin`  
     - **Password:** `admin123`  
3. **Follow the console menu to:**  
   - Book a room  
   - Check out a guest  
   - Generate invoices  

