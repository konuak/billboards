SELECT id_bill, 'size', price, address, date_build,  type_bill, approved
FROM
billboards
WHERE ido = $id_owner


