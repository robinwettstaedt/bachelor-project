CREATE TABLE Payments (
    id SERIAL PRIMARY KEY,
    amount MONEY NOT NULL,
    payment_date DATE NOT NULL
);


CREATE TABLE Log (
    id SERIAL PRIMARY KEY
);
