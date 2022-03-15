DROP TABLE IF EXISTS goalkeepers;
DROP TABLE IF EXISTS defenders;
DROP TABLE IF EXISTS midfielders;
DROP TABLE IF EXISTS forwards;
DROP TABLE IF EXISTS nontechnical_attributes;
DROP TABLE IF EXISTS player;

-- A table representing the basic information of a player
CREATE TABLE player (
    id INT UNIQUE, -- A unique identifier for the player in the game
    name VARCHAR(100), -- The full name of the player (i.e. Eden Hazard)
    rating INT NOT NULL, -- The player's rating on FIFA 20
    wage INT NOT NULL, -- The salary of the player in euros
    PRIMARY KEY (id, name)
);

-- A table representing the nontechnical attributes of a player are more 
-- specific
CREATE TABLE nontechnical_attributes (
    id INT UNIQUE,
    name VARCHAR(100),
    age INT NOT NULL,
    dob DATE NOT NULL, -- When the player was born
    height INT NOT NULL, -- The height of the player in cm
    weight INT NOT NULL, -- The weight of the palyer in kilograms 
    nationality VARCHAR(50) NOT NULL, -- Where the player is from
    club VARCHAR(50) NOT NULL, -- What team the player plays for
    PRIMARY KEY (id, name),
    FOREIGN KEY (id, name) REFERENCES player(id, name)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- A table representing the players that are goalkeepers as well as their 
-- corresponding attributes
CREATE TABLE goalkeepers (
    id INT UNIQUE,
    diving INT NOT NULL, -- How good they are at saves involving diving
    handling INT NOT NULL, -- How good they are with the ball (hands and feet)
    kicking INT NOT NULL, -- How good their distribution is (passing, etc.)
    reflexes INT NOT NULL, -- How fast their reflexes are
    speed INT NOT NULL, -- How rapid they are
    positioning INT NOT NULL, -- How well they position themselves on the field
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES player(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- A table that represents players that are defenders as well as their relevant
-- attributes. Defenders are any player that play LB, LWB, LCB, CB, RCB, RB,
-- or RWB
CREATE TABLE defenders (
    id INT PRIMARY KEY,
    position VARCHAR(3) NOT NULL,
    defending INT NOT NULL,
    physical INT NOT NULL,
    CHECK (position IN ('LB', 'LWB', 'LCB', 'CB', 'RCB', 'RB', 'RWB')),
    FOREIGN KEY (id) REFERENCES player(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- A table that represents players that are midfielders as well as their 
-- relevant attributes. Midfielders are any player that play CDM, LDM, RDM, 
-- CAM, RCM, LCM, CM, LAM, RAM, LM, or RM
CREATE TABLE midfielders (
    id INT PRIMARY KEY,
    position VARCHAR(3) NOT NULL, 
    pace INT NOT NULL,
    passing INT NOT NULL,
    dribbling INT NOT NULL,
    physical INT NOT NULL,
    CHECK (position IN ('CDM', 'LDM', 'RDM', 'CAM', 'RCM', 'LCM', 'CM', 'LAM',
            'RAM', 'LM', 'RM')),
    FOREIGN KEY (id) REFERENCES player(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- A table that represents players that are forwards as well as their 
-- relevant attributes. Forwards are any player that play CF, LF, LS, RS, LW, 
-- RW, RF, or ST
CREATE TABLE forwards (
    id INT PRIMARY KEY,
    position VARCHAR(3) NOT NULL,
    pace INT NOT NULL,
    shooting INT NOT NULL,
    passing INT NOT NULL,
    dribbling INT NOT NULL,
    CHECK (position IN ('CF', 'LF', 'LS', 'RS', 'LW', 'RW', 'RF', 'ST')),
    FOREIGN KEY (id) REFERENCES player(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Create an indices for attributes that will be frequently used when 
-- evaluating the TOTY
CREATE INDEX value ON player (rating, wage);
CREATE INDEX player_desc ON nontechnical_attributes (age, nationality);
