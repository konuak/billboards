SELECT id_report , summa,  id_ord, date_or, id_cont
FROM report_arendator
WHERE YEAR(date_or) = $year ;


