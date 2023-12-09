SELECT DISTINCT surname
FROM arendator
LEFT JOIN orde on Id_cont=idcont
LEFT JOIN (
SELECT *
FROM order_lines)as MEOW on (orde.id_order = MEOW.idorder)
WHERE (YM_start NOT LIKE $date ) OR YM_start IS NULL ;
