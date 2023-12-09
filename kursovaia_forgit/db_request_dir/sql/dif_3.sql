SELECT *
FROM billboards
WHERE price = CASE
    WHEN $value = 'минимальная' THEN (SELECT MIN(price) FROM billboards)
    WHEN $value = 'максимальная' THEN (SELECT MAX(price) FROM billboards)
END;