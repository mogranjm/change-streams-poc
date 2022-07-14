CREATE TABLE Customers (
    CustomerID INT64 NOT NULL,
    fname STRING(1024),
    lname STRING(1024),
    username STRING(1024),
    phone STRING(1024),
    email STRING(1024),
    addr_street STRING(1024),
    addr_city STRING(1024),
    addr_state STRING(1024),
    addr_country STRING(1024),
    addr_pc STRING(1024),
    registered DATE DEFAULT (CURRENT_DATE()),
    subscribed BOOL
) PRIMARY KEY (CustomerID);

CREATE CHANGE STREAM test_stream
    FOR Customers
