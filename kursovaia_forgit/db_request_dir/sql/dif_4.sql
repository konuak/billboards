SELECT Id_cont, surname, phone, adress, business
FROM arendator
LEFT JOIN orde on Id_cont = idcont
WHERE idcont IS NULL;