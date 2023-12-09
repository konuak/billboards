SELECT id_bill,address, SUM(MONTH(YM_end)-MONTH(YM_start)) as count_months
FROM billboards JOIN schedules on (billboards.id_bill = schedules.idbills)
WHERE (YEAR(YM_end)) = $name_1  and (YEAR(YM_start)) = $name_1
GROUP BY id_bill;