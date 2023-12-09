SELECT idbill,  YM_start, YM_end, price_line
FROM
order_lines
JOIN orde ON idorder = id_order
WHERE idcont = $id_arendator


