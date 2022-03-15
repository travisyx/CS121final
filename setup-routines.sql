-- This function takes as an input the id for a player and guesses the
-- worth in N years
DELIMITER !
CREATE FUNCTION guess_future_worth (id INT, N int) 
    RETURNS VARCHAR(20) DETERMINISTIC
BEGIN

END !
DELIMITER ;


-- This function takes as an input two players and returns 1 if the first
-- has a projected higher ranking than the other and 0 otherwise.
DELIMITER !
CREATE FUNCTION compare (first_id INT, second_id INT) 
    RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    -- Goalkeepers

    -- Defenders

    -- Midfielders

    -- Forwards
END !
DELIMITER ;


-- Insert into player given id and wage, a predicted rating (based on other 
-- entries)
DELIMITER !
CREATE PROCEDURE insert_predicted_rating (id INT, wage INT)
BEGIN

END !
DELIMITER ;


-- If a player is inserted into a table again, replace the wage with the 
-- predicted wage
DELIMITER !
CREATE TRIGGER redo_wage AFTER INSERT ON player FOR EACH ROW
BEGIN

END !
DELIMITER ;
