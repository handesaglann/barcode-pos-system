🧾 Barcode-Based Inventory and POS System

This project is a Python-based desktop inventory and point-of-sale (POS) application designed for small retail businesses such as grocery stores, markets, and kiosks.
It enables fast barcode-based sales, automatic stock tracking, and basic sales reporting, all while working fully offline.

🔍 Overview

The system allows users to manage products, track inventory levels, and process sales through a simple and intuitive graphical user interface built with Tkinter.

All data is stored locally using SQLite, making the application lightweight, portable, and suitable for environments without internet access.

✨ Features
🛒 Point of Sale (POS)

Barcode-based product scanning

Manual product selection from product list

Add products to cart automatically

Supports scanning the same product multiple times (grouped as x2, x3, etc.)

Real-time total price calculation

Remove selected items from cart

Complete sales and save transactions to database

Automatic stock reduction after each sale

📦 Inventory Management

Add, update, and delete products via Admin Panel

Store barcode, product name, price, and stock quantity

Real-time stock tracking

Visual indicators for:

Out-of-stock items

Negative stock values

Automatic stock updates during sales

📋 Product List

View all products in a scrollable table

Live search by product name

Add selected product to cart with a single click

Scrollbar support for large product lists

📊 Sales & Reporting

Daily sales summary:

Total number of sales

Daily revenue (turnover)

Revenue report by selected date

Product-based sales details for a selected day

Weekly revenue visualization using bar charts

Charts generated with Matplotlib

🔐 Admin Panel

Add new products

Update product prices

Delete products

Increase stock quantities

All changes are saved instantly to the database

🧠 Technical Highlights

Fully offline-first

SQLite-based local database

Scrollable and responsive Tkinter interface

Mouse wheel scrolling support

No external server or API required

🗂️ Database Structure
products
Field	Description
barcode	Product barcode (PRIMARY KEY)
name	Product name
price	Product price
stock	Stock quantity
sales
Field	Description
id	Sale ID
date	Sale date
total	Total sale amount
sale_items
Field	Description
id	Record ID
sale_date	Sale date
barcode	Product barcode
product_name	Product name
price	Product price
🛠️ Technologies Used
Technology	Description
Python	Core programming language
Tkinter	Desktop graphical user interface
SQLite3	Local database management
Matplotlib	Data visualization and charts
Datetime	Date-based transaction tracking
📁 Project Structure
barcode_inventory_system/
│
├── app.py              # Main application file
├── market.db           # SQLite database
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── assets/             # Optional assets (icons, images)

▶️ Installation
Clone the Repository
git clone https://github.com/your-username/barcode_inventory_system.git
cd barcode_inventory_system

Install Dependencies
pip install matplotlib

Run the Application
python app.py

⚙️ How It Works

A barcode scanner acts as a keyboard input device

When a barcode is scanned:

The product is searched in the database

If found, it is added to the cart

Stock quantity is reduced automatically

Total price is updated instantly

Completed sales are stored with date and product details

Sales data can be reviewed via reports and charts

🏪 Use Cases

Small grocery stores

Local markets

Cafeterias

Offline retail environments

Educational and portfolio projects

Developers learning Python GUI applications

💼 Licensing & Commercial Use

This project is suitable for:

Local license-based deployment

One-time purchase software models

Offline-first business environments

It can be extended with:

License expiration checks

Online activation & validation

User-based access control (Admin / Cashier)


👩‍💻 Author

Hande Saglam
Software Engineering Student
