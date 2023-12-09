SELECT *
FROM billboards
WHERE 1=1
 and id_bill IN ($item_ids);
