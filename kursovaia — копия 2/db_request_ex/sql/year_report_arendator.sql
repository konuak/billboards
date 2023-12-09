SELECT DISTINCT YEAR(date_or) AS date_m
FROM report_arendator
JOIN arendator ON (report_arendator.id_cont = arendator.Id_cont)
WHERE arendator.Id_cont = $id_arendator;


