SELECT
    staff_id, vgroup
FROM
 staff
WHERE
    login = $login
    AND
    password = $password