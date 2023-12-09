SELECT *
FROM billboards
WHERE (price <= $max_price) and (price >= $min_price);
