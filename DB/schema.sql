-- Create the Supplier table
CREATE TABLE IF NOT EXISTS Supplier (
    SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
    SupplierName TEXT NOT NULL,
    SupplierPhoneNumber TEXT NOT NULL
);

-- Create the Drug table
CREATE TABLE IF NOT EXISTS Drug (
    DrugID INTEGER PRIMARY KEY AUTOINCREMENT,
    DrugName TEXT NOT NULL,
    PurchasePrice REAL NOT NULL,
    SellingPrice REAL NOT NULL,
    StockQuantity INTEGER NOT NULL
);

-- Create the Purchase table
CREATE TABLE IF NOT EXISTS Purchase (
    PurchaseID INTEGER PRIMARY KEY AUTOINCREMENT,
    SupplierID INTEGER NOT NULL,
    DrugID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    PurchaseDate DATE NOT NULL,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID),
    FOREIGN KEY (DrugID) REFERENCES Drug(DrugID)
);

-- Create the Customer table
CREATE TABLE IF NOT EXISTS Customer (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerName TEXT NOT NULL,
    CustomerPhoneNumber TEXT NOT NULL
);

-- Create the Sale table
CREATE TABLE IF NOT EXISTS Sale (
    SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER NOT NULL,
    DrugID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    SaleDate DATE NOT NULL,
    TotalPrice REAL NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (DrugID) REFERENCES Drug(DrugID)
);

-- Create the Fund table
CREATE TABLE IF NOT EXISTS Fund (
    FundID INTEGER PRIMARY KEY AUTOINCREMENT,
    CurrentAmount REAL NOT NULL
);

-- Create the Staff table
CREATE TABLE IF NOT EXISTS Staff (
    StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    PhoneNumber TEXT NOT NULL UNIQUE,
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL
);

-- Insert an example staff record
INSERT INTO Staff (Name, PhoneNumber, Username, Password)
VALUES ('Admin User', '1234567890', 'admin', 'admin123');


INSERT INTO Fund (CurrentAmount)
SELECT 100000.0
WHERE NOT EXISTS (SELECT 1 FROM Fund);

