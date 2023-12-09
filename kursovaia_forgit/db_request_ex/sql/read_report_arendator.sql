SELECT report_arendator.id_bill ,summa,  id_ord, date_or
FROM report_arendator
JOIN arendator ON (report_arendator.id_cont = arendator.Id_cont)
WHERE YEAR(date_or) = $year and   report_arendator.id_cont = $id_arendator;