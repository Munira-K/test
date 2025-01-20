CREATE TABLE supermarket_data (
    Company VARCHAR(100),
    ReceiptDate DATETIME NOT NULL,
    ReceiptNumber INT NOT NULL,
    CashierNumber INT NOT NULL,
    TransactionNumber VARCHAR(100) NOT NULL,
    Cashier VARCHAR(100),
    ArticleNumber VARCHAR(100),
    Item VARCHAR(200),
    Quantity INT NOT NULL,
    Amount FLOAT NOT NULL,
    Discount INT
);
