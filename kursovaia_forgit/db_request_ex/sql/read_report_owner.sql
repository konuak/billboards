SELECT report_owner.id_bill ,summa,   id_ord
FROM report_owner
JOIN billboards ON (report_owner.id_bill = billboards.id_bill)
WHERE YEAR(date_or) = $year and   ido = $id_owner;


