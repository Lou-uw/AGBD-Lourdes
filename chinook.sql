--Consulta 1--
SELECT FirstName, LastName FROM employees 
ORDER BY FirstName, LastName DESC 

--Consulta 2--
SELECT name, Milliseconds FROM tracks
 JOIN albums ON tracks.AlbumId = albums.AlbumId 
 WHERE Title LIKE "Big Ones" ORDER BY Milliseconds DESC 

--Consulta 3--
SELECT Title, sum(UnitPrice) FROM tracks
JOIN albums ON tracks.AlbumId = albums.AlbumId
GROUP BY tracks.AlbumId
ORDER BY sum(UnitPrice) ASC LIMIT 10

--Consulta 4--
SELECT tracks.name, albums.Title,genres.Name FROM tracks
JOIN albums ON tracks.AlbumId = albums.AlbumId
JOIN genres ON tracks.GenreId = genres.GenreId
WHERE UnitPrice = 0.99

--Consulta 5--
SELECT tracks.name, tracks.Milliseconds, 
albums.Title, artists.Name FROM tracks
JOIN albums ON tracks.AlbumId = albums.AlbumId
JOIN artists ON albums.ArtistId = artists.ArtistId
WHERE UnitPrice = 0.99 
ORDER BY tracks.Milliseconds ASC LIMIT 20

--Consulta 6--
SELECT emp.LastName AS empleado, jefe.LastName AS jefes, emp.Title, count(SupportRepId) 
AS cant_clientes FROM employees emp
JOIN employees jefe ON emp.ReportsTo = jefe.EmployeeId
JOIN customers ON emp.EmployeeId = customers.SupportRepId
GROUP BY emp.EmployeeId ORDER BY cant_clientes DESC

--Consulta 7--
SELECT emp.FirstName AS Nombre_empleado, emp.LastName AS Apellido_empleado,
 clie.FirstName AS Nombre_cliente, clie.LastName AS Apellido_cliente
FROM employees emp
JOIN customers clie ON emp.EmployeeId = clie.SupportRepId

--Consulta 8--
SELECT clie.FirstName AS Nombre_cliente, clie.LastName AS Apellido_cliente, clie.Address,inv.InvoiceDate
FROM customers clie
JOIN invoices inv ON clie.CustomerId = inv.InvoiceId

--Consulta 9--
SELECT genres.name AS Genero, COUNT(tracks.TrackId) AS Total_canciones FROM genres 
JOIN tracks ON genres.GenreId = tracks.GenreId
GROUP BY genres.name ORDER BY Total_canciones DESC

--Consulta 10--
SELECT clie.FirstName AS Nombre_cliente, artists.name AS Nombre_artista FROM customers clie
JOIN invoices ON clie.CustomerId = invoices.CustomerId
JOIN invoice_items ON invoices.InvoiceId = invoice_items.InvoiceId
JOIN tracks ON invoice_items.TrackId = tracks.TrackId
JOIN albums ON tracks.AlbumId = albums.AlbumId
JOIN artists ON albums.ArtistId = artists.ArtistId
ORDER BY Nombre_cliente ASC

--Consulta 11--
SELECT clie.FirstName AS Nombre_cliente, 
 clie.City AS Ciudad_cliente, tracks.Name AS Nombre_cancion,
 genres.Name AS Genero_cancion  FROM customers clie
JOIN invoices ON clie.CustomerId = invoices.CustomerId
JOIN invoice_items ON invoices.InvoiceId = invoice_items.InvoiceId
JOIN tracks ON invoice_items.TrackId = tracks.TrackId
JOIN genres ON genres.GenreId = tracks.GenreId
ORDER BY Nombre_cliente ASC;

--Consulta 12--
SELECT * FROM customers
JOIN invoices ON customers.CustomerId = invoices.CustomerId
JOIN invoice_items ON invoices.InvoiceId = invoice_items.InvoiceId
JOIN tracks ON invoice_items.TrackId = tracks.TrackId
JOIN genres ON tracks.GenreId = genres.GenreId
JOIN media_types ON tracks.MediaTypeId = media_types.MediaTypeId
JOIN albums ON tracks.AlbumId = albums.AlbumId
JOIN artists ON albums.ArtistId = artists.ArtistId
JOIN employees ON customers.SupportRepId = employees.EmployeeId
JOIN playlist_track ON tracks.TrackId = playlist_track.TrackId
JOIN playlists ON playlist_track.PlaylistId = playlists.PlaylistId;

--TP: Integridad y Manipulación de Datos en Sistemas Relacionales
--Parte I: Investigación y Análisis Crítico

--1. El peligro del "Empty WHERE": Expliquen técnicamente qué sucede en la memoria y en el
-- almacenamiento de la base de datos cuando se ejecuta un UPDATE o un DELETE 
-- sin la cláusula WHERE.

--UPDATE: El usar update sin where es peligroso porque el update sirve para modificar tabla,
--si no le das especificamente donde modificar, lo que se entiende es que se modifiquen toda
--la tabla, lo cual provoca que se recorran todas la tabla fila por fila, modificando todas

--DELETE: Con un delete es lo mismo pero enves de modificar las tablas, se borran todas las filas
--porque la base de datos interpreta que te referis a todas. Esto hace un alto consumo de la memoria
--al tener que cargar todas la tabla


--2.Integridad Referencial: ¿Qué es una restricción de clave foránea (FOREIGN KEY constraint)
-- y cómo protege la consistencia de los datos al intentar usar DELETE?

--Es una restricción que permite vincular una columna de una tabla con la PRIMARY KEY
--de otra tabla. Su función es garantizar la integridad referencial, es decir, que los registros 
--hijos siempre apunten a un registro padre existente y no queden huérfanos si se borra(DELETE) o 
--modifica(UPDATE) el padre 


--RESTRICT (o NO ACTION): impide borrar/actualizar el padre si hay hijos que lo referencian. 
--Es la opción más segura por defecto en muchos motores.

--CASCADE: al borrar/actualizar el padre, propaga la operación a los hijos 
--(borra o actualiza la FK). Útil, pero requiere cuidado.

--SET NULL: al borrar/actualizar el padre, la FK del hijo se vuelve NULL
 --(la FK debe permitir NULL).

--SET DEFAULT: establece un valor por defecto en la FK del hijo 
--(esa columna debe tener DEFAULT válido).

--NO ACTION: similar a RESTRICT en la mayoría de motores; 
--la comprobación se difiere al final de la sentencia (no confundir con “no hacer nada”).


--Parte II: Implementación Práctica (Caso Chinook)

--1. Gestión de Catálogo (INSERT)

--Primero, inserten un nuevo artista en artists (ej: "Divididos").
INSERT INTO artists(ArtistId, Name)
VALUES(276,'Lisa')
-- Result: query executed successfully. Took 0ms, 1 rows affected
-- EXECUTING ALL IN 'SQL 1'

--Segundo, inserten un álbum para ese artista en albums.
INSERT INTO albums(AlbumId, Title, ArtistId)
VALUES(348,'Alter Ego', 276)
--Result: query executed successfully. Took 0ms, 1 rows affected
-- EXECUTING ALL IN 'SQL 1'


--Tercero, inserten al menos dos canciones en tracks.
INSERT INTO tracks(TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
VALUES(3504,'Lifestyle', 348, 1, 9, 'Bartolito',  161000, 6440000, 5.5),
      (3505,'Thunder', 348, 1, 9, 'Bartolito', 168000, 6720000, 5.5)
   
--Execution finished without errors.
--Result: query executed successfully. Took 0ms, 2 rows affected

--2. Mantenimiento y Precios (UPDATE)

--.Corrección de Datos: El empleado con EmployeeId = 3 cambió su domicilio. 
--Actualicen su dirección (Address) a "Av. Siempreviva 742" y su ciudad a "Springfield".

UPDATE employees SET Address = 'Av. Siempreviva 742', City = 'Springfield'
WHERE EmployeeId = 3
--Execution finished without errors.
--Result: query executed successfully. Took 0ms, 1 rows affected

--.Ajuste por Inflación: La gerencia decidió aumentar un 10% el precio de todas las canciones(tracks)
--que pertenecen al género "Jazz" (GenreId = 2). Realicen la actualización en una sola sentencia.

UPDATE tracks SET UnitPrice = UnitPrice * 1.10
WHERE GenreId = 2
--Execution finished without errors.
--Result: query executed successfully. Took 0ms, 130 rows affected

--3. Depuración de Registros (DELETE)

--.Baja de Prueba: Intenten eliminar el registro del artista "Queen" directamente 
--de la tabla artists.
 
DELETE FROM artists 
WHERE ArtistId = 51
--Execution finished with errors.
--Result: FOREIGN KEY constraint failed

 --Consigna: Copien el error que devuelve el motor y expliquen qué registros
   --deberían borrar primero para que la sentencia funcione.
                                    --Explicación--
--Para que funcione hay que borrar todos los registros que estan r
--elacionados con Queen

--.Eliminación Selectiva: Eliminen todos los registros de la tabla invoices (facturas) 
--que correspondan al año 2010.

DELETE FROM invoice_items
WHERE InvoiceId IN (
SELECT InvoiceId FROM invoices
WHERE InvoiceDate >= '2010-01-01' AND InvoiceDate < '2011-01-01' )
--Execution finished without errors.
--Result: query executed successfully. Took 3ms, 455 rows affected

-- At line 1:
DELETE FROM invoices 
WHERE InvoiceDate >= '2010-01-01' AND InvoiceDate < '2011-01-01'
-- Result: query executed successfully. Took 1ms, 83 rows affected


 