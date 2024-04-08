-- this script is a query that returns how alike you are to a given user id in the database
-- the user id is set to 108 on line 6, replace it with the user id you want to query againts
-- and replace str_role with the role you want to filter your requests against
\c mentorship_app

SELECT DISTINCT t1.user_id AS id,str_first_name,str_last_name,COUNT(*) as likeness
   FROM mentorship_program_app_user_interests AS t1, mentorship_program_app_user_interests AS t2,mentorship_program_app_user AS tu
   WHERE t2.user_id=108 AND t1.interest_id = t2.interest_id AND t1.user_id = tu.id
         AND tu.str_role = 'Mentee'
   GROUP BY t1.user_id,tu.str_first_name,tu.str_last_name
   ORDER BY likeness DESC;
