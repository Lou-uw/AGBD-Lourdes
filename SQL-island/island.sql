    
    SELECT * FROM INHABITANT 
    --Selecciona todos de la tabla inhabitant

    SELECT * FROM INHABITANT 
    WHERE state LIKE “FRIENDLY” 
   --Selecciona todos de la tabla inhabitant que sean amigables(friendly)

    SELECT * FROM INHABITANT 
    WHERE state LIKE "FRIENDLY" AND job = "weaponsmith" 
  --Selecciona todos de la tabla inhabitant que sean amigables(friendly)
  --y trabajan de weaponsmith

    SELECT * FROM INHABITANT 
    WHERE state LIKE "FRIENDLY" AND job LIKE "%smith" 
  --Selecciona todos de la tabla inhabitant que sean amigables(friendly)
  --y su trabajo termina en  de smith

    SELECT personid FROM INHABITANT 
    WHERE name LIKE "stranger" 
  --Selecciona la columna personid de la tabla inhabitant 
  --donde el nombre sea "stranger"

    SELECT gold FROM INHABITANT 
    WHERE name LIKE "stranger" 
  --Selecciona la columna gold de la tabla inhabitant 
  --donde el nombre sea "stranger"

    SELECT * FROM ITEM 
    WHERE OWNER IS NULL 
  --Selecciona todo de la tabla ITEM 
  --donde el dueño sea null(nulo/no hay)

    UPDATE item SET owner = 20 
    WHERE OWNER IS NULL 
 --Actualiza item y cambia su dueño al 20 
 --donde el dueño es null

    SELECT * FROM ITEM 
    WHERE owner = 20 
  --Selecciona todo de la tabla ITEM 
  --donde el dueño es 20

    SELECT * FROM INHABITANT 
    WHERE state LIKE "friendly" AND job = "dealer" OR job ="merchant" 
  --Selecciona todos de la tabla inhabitant que sean amigables(friendly)
  --y trabajan de dealer o merchant

    UPDATE item set owner = 15 
  --Actualiza item y cambia su dueño al 15

    UPDATE INHABITANT SET name = "Jorgito" 
    WHERE personid = 20 
  --Actualiza INHABITANT y cambia su nombre a Jorgito 
  --donde el personid es 20 

    SELECT * FROM INHABITANT  
    WHERE job = "baker" ORDER BY gold DESC 
  --Selecciona todos de la tabla inhabitant que trabajan de baker, 
  --ordenado desde el que tiene mas oro al que menos tiene

    SELECT * FROM INHABITANT  
    WHERE job = "pilot"  
  --Selecciona todos de la tabla inhabitant que trabajan de piloto

    SELECT inhabitant.name FROM village 
    JOIN inhabitant ON village.chief = inhabitant.personid 
    WHERE village.name = “Onionville” 
 --Selecciona el nombre del habitante 
 --que es el jefe

    SELECT COUNT(*) FROM inhabitant, village 
    WHERE village.villageid = inhabitant.villageid 
    AND village.name = "Onionville" AND inhabitant.gender = "f" 
--Cuenta cuantas mujeres vviven en Onionville

    SELECT name FROM inhabitant 
    WHERE gender = "f" AND villageid = "3" 
--Selecciona el nombre de las mujeres del pueblo en el id 3

    SELECT SUM(gold) FROM INHABITANT 
    WHERE job LIKE "baker" or job LIKE "dealer" or job LIKE "merchant" 
--Calcula la suma de las personas que trabajan de dealer o baker o merchant

    SELECT state, AVG(inhabitant.gold) FROM inhabitant 
    GROUP BY state ORDER BY AVG(inhabitant.gold)  
--Selecciona el estado y el promedio de oro de las personas en este,
--ordenado del menor al mayor

    DELETE FROM inhabitant 
    WHERE name = "Dirty Diane" 
--Elimina de la tabla inhabitant
--donde el nombre sea Dirty Diane

    UPDATE inhabitant SET state = "friendly" 
    WHERE personid = 8 
 --Actualiza inhabitant en el state pone friendly 
 --donde el personid es 8

 