# Employee Manager (MySQL + Tkinter)

A simple Employee Management System built with Python, Tkinter, MySQL, and Pandas.
It provides a GUI for adding, updating, deleting, searching, and exporting employee data stored in a MySQL database.

✨ Features

Login window to connect with MySQL credentials

Auto-creation of database (employee_db) and table (employees) if not present

Add / Update / Delete employees

Search employees by name

Export employee records to CSV

Virtual environment support (via setup script)

📦 Requirements

Python 3.8+

MySQL Server & Client

Python dependencies (installed automatically via requirements.txt):

mysql-connector-python

pandas

⚡ Quick Start
🔹 1. Clone the Repository
git clone https://github.com/<your-username>/employee-manager.git
cd employee-manager

🔹 2. Run the Setup Script

On Windows:

setup.bat


On Linux/Mac:

chmod +x setup.sh
./setup.sh


👉 This will:

Check for Python (install if missing)

Check for MySQL (install if missing)

Create a virtual environment (venv/)

Install all dependencies from requirements.txt

Launch the application

⚙️ Manual Setup (Optional)

If you don’t want to use the setup.bat / setup.sh scripts:

# Create virtual environment
python -m venv venv
# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python database.py

📂 Project Structure
employee-manager/
│
├── database.py        # Main application (Tkinter + MySQL GUI)
├── requirements.txt   # Python dependencies
├── setup.bat          # Windows installer
├── setup.sh           # Linux installer
└── README.md          # Project documentation

🗄️ Database Info

Database: employee_db (auto-created)

Table: employees

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    salary DECIMAL(10,2)
);

📤 Exporting Data

Click "Export to CSV" inside the app to save all employee records into a .csv file.

🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.
