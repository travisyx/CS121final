-- Query 1: choose the name, nationality, club, and average statistic of the 
-- best goalkeeper (the keeper with the maximum of the average of the stats).
-- This matches RA #1.
WITH t AS 
    (SELECT name, nationality, club, 
        (diving + handling + kicking + reflexes + speed + positioning)/6 
        AS avg_rating 
    FROM goalkeepers NATURAL JOIN player NATURAL JOIN nontechnical_attributes 
    ORDER BY avg_rating DESC) 
SELECT name, nationality, club, avg_rating FROM t NATURAL RIGHT JOIN 
    (SELECT MAX(avg_rating) AS avg_rating FROM t) AS b;

-- Query 2: select the names, passing statistic, and pace of the 5 midfielders 
-- who have the highest passing statistic that are at least twice as fast 
-- (pace) as the slowest midfielder
WITH t AS 
    (SELECT MIN(pace) AS slow FROM midfielders)
SELECT name, passing, pace, FROM midfielders NATURAL JOIN player
WHERE pace > 2 * (SELECT slow FROM t) ORDER BY passing DESC LIMIT 5;

-- Query 3: It is not an impossibility that a goalkeeper and the reserve 
-- goalkeeper on a team are both ineligible for a match (red card, injury, etc)
-- Insert into goalkeeper the fastest forward. Make sure that they have stats 
-- that are all 1s. This matches RA #3.
WITH t AS (SELECT id FROM forwards NATURAL JOIN player WHERE pace = (SELECT MAX(pace) FROM forwards))
INSERT INTO goalkeepers VALUES SELECT id,1,1,1,1,1,1 FROM t;


