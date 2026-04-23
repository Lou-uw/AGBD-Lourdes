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
JOIN tracks  ON genres.GenreId = tracks.GenreId
GROUP BY genres.name ORDER BY Total_canciones DESC

--Consulta 10--
SELECT clie.FirstName AS Nombre_cliente, artists.name AS Nombre_artista FROM customers clie
JOIN invoices ON clie.CustomerId = invoices.CustomerId
JOIN invoice_items ON invoices.InvoiceId = invoice_items.InvoiceId
JOIN tracks ON invoice_items.TrackId = tracks.TrackId
JOIN albums ON tracks.AlbumId = albums.AlbumId
JOIN artists ON albums.ArtistId = artists.ArtistId
ORDER BY Nombre_cliente ASC









 