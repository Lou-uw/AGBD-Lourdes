SELECT FirstName, LastName FROM employees 
ORDER BY FirstName, LastName DESC 

SELECT name, Milliseconds FROM tracks
 JOIN albums ON tracks.AlbumId = albums.AlbumId 
 WHERE Title LIKE "Big Ones" ORDER BY Milliseconds DESC 

SELECT Title, sum(UnitPrice) FROM tracks
JOIN albums ON tracks.AlbumId = albums.AlbumId
GROUP BY tracks.AlbumId
ORDER BY sum(UnitPrice) ASC LIMIT 10

SELECT tracks.name, albums.Title,genres.Name FROM tracks
JOIN albums ON tracks.AlbumId = albums.AlbumId
JOIN genres ON tracks.GenreId = genres.GenreId
WHERE UnitPrice = 0.99

SELECT tracks.name, tracks.Milliseconds, 
albums.Title, artists.Name FROM tracks
JOIN albums ON tracks.AlbumId = albums.AlbumId
JOIN artists ON albums.ArtistId = artists.ArtistId
WHERE UnitPrice = 0.99 
ORDER BY tracks.Milliseconds ASC LIMIT 20

SELECT emp.LastName AS empleado, jefe.LastName AS jefes, emp.Title, count(SupportRepId) AS cant_clientes FROM employees emp
JOIN employees jefe ON emp.ReportsTo = jefe.EmployeeId
JOIN customers ON emp.EmployeeId = customers.SupportRepId
GROUP BY emp.EmployeeId ORDER BY cant_clientes DESC




 