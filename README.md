Barcode-Based Inventory and POS System

This project is a Python-based desktop inventory and point-of-sale (POS) application designed for small and medium-sized retail businesses such as grocery stores and local markets.
It provides fast product scanning using a barcode reader, automatic stock updates, and basic sales analysis.

Overview

The system allows users to manage products, track inventory levels, and process sales through a simple graphical user interface.
All data is stored locally using SQLite, making the application lightweight, portable, and suitable for offline use.

Features
Point of Sale (POS)

Barcode-based product scanning

Add products to cart automatically

Real-time total price calculation

Automatic stock reduction after each sale

Support for scanning the same product multiple times

Inventory Management

Add, update, and delete products

Store barcode, product name, price, and stock quantity

Real-time stock tracking

Prevents selling out-of-stock items

Data Visualization

Daily sales visualization using charts

Graph-based sales overview

Simple business insights for store owners

Database

SQLite-based local database

No external server required

Persistent and reliable data storage

Technologies Used
Technology	Description
Python	Core programming language
Tkinter	Desktop graphical user interface
SQLite3	Local database management
Matplotlib	Data visualization and charts
Datetime	Date-based transaction tracking
Project Structure
barcode_inventory_system/
│
├── app.py              # Main application file
├── market.db           # SQLite database
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── assets/             # Optional assets (icons, images)

Installation
Clone the Repository
git clone https://github.com/your-username/barcode_inventory_system.git
cd barcode_inventory_system

pip install matplotlib

Run the Application
python app.py

How It Works

A barcode scanner acts as a keyboard input device

When a barcode is scanned:

The product is searched in the database

If found, it is added to the cart

Stock quantity is reduced by one

The total price is updated instantly

All sales are recorded with date information

Sales data can be visualized using built-in charts

Use Cases

Small grocery stores

Local markets

Cafeterias

Educational or portfolio projects

Developers learning Python GUI applications

Licensing and Commercial Use

This project is suitable for:

Local license-based deployment

Monthly or yearly subscription models

Offline-first environments

The system can be extended with:

License expiration checks

Online activation and validation

User-based access control

Possible Enhancements

User authentication (admin / cashier roles)

Receipt printing support

QR code and mobile integration

Cloud synchronization

Advanced reporting (PDF or Excel export)

Author

Hande Saglam
Software Engineering Student
