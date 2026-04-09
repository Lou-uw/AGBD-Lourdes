SELECT FirstName, LastName FROM employees 
ORDER BY FirstName, LastName DESC 

SELECT name, Milliseconds FROM tracks
 JOIN albums ON tracks.AlbumId = albums.AlbumId 
 WHERE Title LIKE "Big Ones" ORDER BY Milliseconds DESC 

SELECT name, sum(UnitPrice) FROM tracks
 JOIN albums ON tracks.AlbumId = albums.AlbumId
 WHERE Title LIKE "Big Ones"  
 ORDER BY UnitPrice ASC LIMIT 10

 