-- This function takes as an input the id for a player and guesses the
-- worth in N years
DELIMITER !
CREATE FUNCTION guess_future_worth (id INT, N int) 
    RETURNS DOUBLE DETERMINISTIC
BEGIN
    DECLARE age INT DEFAULT 0;
    DECLARE wage INT DEFAULT 0;
    IF id NOT IN (SELECT id FROM player)
    THEN RETURN 0; -- They can't be worth anything if they aren't in the db
    ELSE
        SET age = (SELECT age FROM player NATURAL JOIN nontechnical_attributes 
                    WHERE player.id = id);
        SET wage = (SELECT wage FROM player WHERE player.id = id);

        -- The wage tends to decrease for the players past the age of 30, they
        -- tend to increase until the player is in their "prime", which is 
        -- around 30.
        IF age + N > 36
        THEN 
            RETURN 0; -- 99% of players retire by 36, so E[wage] is roughly 0
        ELSEIF (age + N > 30) THEN
            -- Wage tends to proportionally diminish every year past 30
            RETURN ((36 - AGE - N) / 6) * wage;
        ELSE 
            -- Wage tends to increase proportionally until 30, where it doubles
            RETURN ((30 - AGE - N) / (30 - AGE)) * WAGE + WAGE;
    END IF;
END !
DELIMITER ;


-- This function takes as an input a player and computers a projected rating
-- that is more precise than the FIFA rating. This allows for easier comparison
-- between two players of the same position. If the player is not found, then
-- return -1
DELIMITER !
CREATE FUNCTION compute_rating (play_id INT) 
    RETURNS DOUBLE DETERMINISTIC
BEGIN
    DECLARE rating DOUBLE DEFAULT 0;
    IF (play_id IN SELECT id FROM goalkeepers) -- Goalkeepers
        THEN
        -- Most important attributes are diving, reflexes, and positioning in
        -- that order so these are emphasized
        SET rating = (SELECT (1.5 * diving + 1.4 * reflexes + 1.4 * positioning 
            + handling + kicking + speed) FROM goalkeepers WHERE id = play_id);
    ELSEIF (play_id IN SELECT id FROM defenders) -- Defenders
        THEN
        -- Defending is more important than physical, so emphasize it more
        SET rating = (SELECT (1.5 * defending + 1.2 * physical) FROM defenders
            WHERE id = play_id);
    ELSEIF (play_id IN SELECT id FROM midfielders) -- Midfielders
        THEN
        -- Most important are passing, dribbling, and pace, in that order
        SET rating = ((SELECT (1.5 * passing + 1.4 * dribbling + 
            1.1 * pace + physical) FROM midfielders WHERE id = play_id);
    ELSEIF (play_id IN SELECT id FROM forwards) -- Forwards       
        THEN
        -- Most important are pace, dribbling, and shooting, in that order
        SET rating = ((SELECT (1.5 * dribbling + 1.4 * shooting + 
            1.4 * pace + passing) FROM forwards WHERE id = play_id);
    ELSE
        -- Positions are different
        RETURN -1;
    END IF;
    RETURN rating;
END !
DELIMITER ;


-- Given an input of two players, return 1 if the first player 
-- has a predicted higher ranking than the other, 0 for equality and -1 
-- otherwise. Returns 2 if positions are different
-- Calls the above function compute_rating
DELIMITER !
CREATE FUNCTION compute (fst_id INT, snd_id INT) 
    RETURNS DOUBLE DETERMINISTIC
BEGIN
    DECLARE fst_rating INT DEFAULT 0;
    DECLARE snd_rating INT DEFAULT 0;
    -- Check if the two players play the same position
    IF ((fst_id IN SELECT id FROM goalkeepers) AND 
            (snd_id IN SELECT id FROM goalkeepers)) OR
        ((fst_id IN SELECT id FROM defenders) AND 
            (snd_id IN SELECT id FROM defenders)) OR 
        ((fst_id IN SELECT id FROM midfielders) AND 
            (snd_id IN SELECT id FROM midfielders)) OR
        ((fst_id IN SELECT id FROM forwards) AND 
            (snd_id IN SELECT id FROM forwards))
    THEN
        SET fst_rating = compute_rating (fst_id);
        SET snd_rating = compute_rating (snd_id);
        IF fst_rating = snd_rating THEN RETURN 0;
        ELSEIF fst_rating < snd_rating THEN RETURN -1;
        ELSE RETURN 1;
        END IF;
    ELSE -- Positions are different
        RETURN 2;
    END IF;
END !
DELIMITER ;


-- Given id, name, and rating, insert a predicted wage (based on 
-- other entries) with a player with a new id of MAX(id)+1
DELIMITER !
CREATE PROCEDURE insert_predicted_wage (id INT, name VARCHAR(100), overall INT)
BEGIN
    DECLARE predicted INT DEFAULT 0;
    DECLARE new_id INT DEFAULT 0;

    SET new_id = (SELECT MAX(id) + 1 FROM player);

    -- Other players do not have this rating
    IF overall NOT IN (SELECT rating FROM player WHERE rating = overall)
    THEN
        IF overall < (SELECT MIN(rating) FROM player)
        THEN SET predicted = 0;
        ELSE IF overall > (SELECT MAX(rating) FROM player)
        THEN 
            SET predicted = 
                (SELECT CAST(1.1 * wage AS INT) FROM player, 
                    (SELECT MAX(rating) AS rating FROM player) AS t
                WHERE player.rating = t.rating);
    ELSE -- Other players have this rating
        SET predicted = 
            (SELECT AVG(wage) FROM player WHERE rating = rating);
    END IF;
    INSERT INTO players
    VALUES (new_id, name, overall, predicted);
END !
DELIMITER ;

DROP TRIGGER IF EXISTS redo_wage;

-- If a player is inserted into the player table, insert a "copy" with 
-- the predicted wage. This makes it more convenient for managers and clients
-- to see the predicted wage as time progresses based on the stats
DELIMITER !
CREATE TRIGGER redo_wage AFTER INSERT ON player FOR EACH ROW
BEGIN
    CALL insert_predicted_wage (NEW.id, NEW.name, NEW.rating);  
END !
DELIMITER ;
