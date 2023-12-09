SELECT *
FROM billboards
WHERE (quality <= $max_quality) and (quality >= $min_quality);