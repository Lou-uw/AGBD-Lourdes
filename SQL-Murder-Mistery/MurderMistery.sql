SELECT * FROM crime_scene_report 
--selecciona todo el contenido de la tabla crime_scene_report

SELECT * FROM crime_scene_report WHERE type LIKE "murder" and city LIKE "sql city" and date = 20180115
--selecciona todo de la tabla en donde el tipo sea asesinato, la ciudad sql city y la fecha el 15 de enero de 2018

SELECT * FROM person WHERE address_street_name LIKE "Northwestern dr" ORDER BY address_number DESC
--selecciona todo de la tabla person en donde el nombre de calle sea Northwestern dr ordenado por numero de casa
de forma descendente (el mayor a menor)

SELECT * FROM interview WHERE person_id = 14887
--selecciona todo de la tabla interview y entrevista a quien tiene el person_id 148887 
--(uno de los testigos, el que vive en northwesten dr)

SELECT * FROM get_fit_now_member WHERE id LIKE "48Z%" AND membership_status = "gold";
--selecciona todo de la tabla en donde el id empiece con 48Z y sea un miembro gold

SELECT person.name FROM drivers_license JOIN person ON drivers_license.id = person.license_id 
WHERE drivers_license.plate_number LIKE "%H42W%" AND drivers_license.gender = "male";
--Selecciona el nombre de la persona, une la tabla de licencias con la de personas usando el ID,
--y busca las patentes que contienen "H42W" y que sean hombres.

SELECT person.name, interview.transcript FROM person JOIN interview ON person.id = interview.person_id
WHERE person.name = "Jeremy Bowers" OR person.name = "Tushar Chandra"
--Selecciona el nombre de la persona y su testimonio, toma los datos de la tabla person, 
--la une con la tabla interview usando el ID de la persona,
-- y busca a las personas que se llaman "Jeremy Bowers" o "Tushar Chandra".