SELECT DISTINCT YEAR(date_or) AS date_m
FROM report_owner
JOIN billboards ON (report_owner.id_bill = billboards.id_bill)
WHERE ido = $id_owner;


