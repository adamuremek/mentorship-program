\c mentorship_app

SELECT count(*) AS likeness,user_id as id,str_first_name,str_last_name FROM (
   SELECT DISTINCT t1.interest_id,t1.user_id AS user_id ,str_first_name,str_last_name
   FROM mentorship_program_app_user_interests AS t1, mentorship_program_app_user_interests AS t2,mentorship_program_app_user AS t3
   WHERE
      t2.user_id=22 AND t1.user_id <> t2.user_id AND t3.id = t1.user_id
)  GROUP BY user_id,str_first_name,str_last_name
ORDER BY likeness
LIMIT 4;
