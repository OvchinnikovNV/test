CREATE TABLE company(companyId integer PRIMARY KEY,
                    companyName text,
                    companyCountry text
);
CREATE TABLE phone(phoneId integer PRIMARY KEY,
                    phoneModel text,
                    price integer,
                    companyId integer, 
                    FOREIGN KEY (companyId) REFERENCES company(companyId)
);

INSERT INTO company VALUES(1,'Apple','USA');
INSERT INTO company VALUES(2,'SAMSUNG','China');
INSERT INTO company VALUES(3,'BQ','Spain');
INSERT INTO company VALUES(4,'NOKIA','China');

INSERT INTO phone VALUES(1,'iPhone 12',89000,1);
INSERT INTO phone VALUES(2,'iPhone 11',69000,1);
INSERT INTO phone VALUES(3,'iPhone X',59000,1);
INSERT INTO phone VALUES(4,'iPhone 12 Plus',109000,1);

INSERT INTO phone VALUES(5,'A10',59000,2);
INSERT INTO phone VALUES(6,'A9',49000,2);
INSERT INTO phone VALUES(7,'M10',69000,2);
INSERT INTO phone VALUES(8,'M9',55000,2);

INSERT INTO phone VALUES(9,'Aquaris X5',21000,3);
INSERT INTO phone VALUES(10,'Aquaris 5',19000,3);
INSERT INTO phone VALUES(11,'Aquaris X4',16000,3);
INSERT INTO phone VALUES(12,'Aquaris 4',10000,3);

INSERT INTO phone VALUES(13,'NOK1',49000,4);
INSERT INTO phone VALUES(14,'NOK2',39000,4);
INSERT INTO phone VALUES(15,'NOK3',29000,4);

SELECT companyName, avgPrice
FROM
    company INNER JOIN
        (
        SELECT companyId,
            AVG(price) AS avgPrice
        FROM phone
        GROUP BY companyId
        ) prices
    USING(companyId)
WHERE avgPrice = (
        SELECT MAX(avgPrice)
        FROM (
            SELECT AVG(price) AS avgPrice
            FROM phone
            GROUP BY companyId
        ) a
    );


SELECT COUNT(phoneId) AS Китайских_товаров
FROM
    company LEFT JOIN phone
    USING(companyId)
WHERE companyCountry = 'China'
GROUP BY company.companyCountry;


SELECT companyName AS Производитель,
    phoneModel AS Самая_дорогая_модель
FROM company, phone,
    (
    SELECT companyId,
        MAX(price) AS maxPrice
    FROM phone
    GROUP BY companyId
    ) prices
WHERE company.companyId = phone.companyId AND
     phone.companyId = prices.companyId AND
     phone.price = prices.maxPrice;
    