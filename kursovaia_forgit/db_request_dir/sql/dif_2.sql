SELECT surname, date_ord, id_order
FROM order_lines JOIN `rk6_schema`.`orde` on (id_order = idorder)
JOIN arendator  on (id_cont = idcont)
WHERE YEAR(date_ord)=YEAR($date) AND MONTH(date_ord)=MONTH($date) AND surname=$surname;