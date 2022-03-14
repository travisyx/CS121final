DROP TABLE IF EXISTS goalkeepers;
DROP TABLE IF EXISTS defenders;
DROP TABLE IF EXISTS midfielders;
DROP TABLE IF EXISTS forwards;
DROP TABLE IF EXISTS outfield_attributes;
DROP TABLE IF EXISTS nontechnical_attributes;
DROP TABLE IF EXISTS player;

-- A table representing the basic information of a player
CREATE TABLE player (
    id INT UNIQUE, -- A unique identifier for the player in the game
    name VARCHAR(100), -- The full name of the player (i.e. Eden Hazard)
    overall INT NOT NULL, -- The player's rating on FIFA 20
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

-- A table representing the relevant technical attributes for outfield players,
-- which are players that are not goalkeepers. These are common attributes that
-- all outfield players have a metric for (but the importance of each attribute
-- varies by position)
CREATE TABLE outfield_attributes (
    id INT UNIQUE,
    pace INT NOT NULL, -- How fast the player is
    shooting INT NOT NULL, -- How good the player is at finishing
    passing	INT NOT NULL, -- How good the player is at passing
    dribbling INT NOT NULL, -- How good the player is at dribbling
    defending INT NOT NULL, -- How good the player is at defending
    physical INT NOT NULL, -- How strong the player is
    PRIMARY KEY (id, name),
    FOREIGN KEY (id) REFERNCES player(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- A table representing the players that are goalkeepers as well as their 
-- corresponding attributes. The attributes are not in outfield_attributes
-- as goalkeepers have unique attributes the other 10 players on the field 
-- do not need
CREATE TABLE goalkeepers (
    id INT UNIQUE,
    diving INT NOT NULL, -- How good they are at saves involving diving
    handling INT NOT NULL, -- How good they are with the ball (hands and feet)
    kicking INT NOT NULL, -- How good their distribution is (passing, etc.)
    reflexes INT NOT NULL, -- How fast their reflexes are
    speed INT NOT NULL, -- How rapid they are
    positioning INT NOT NULL, -- How well they position themselves on the field
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERNCES player(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- A table that represents players that are defenders as well as their relevant
-- attributes. Defenders are any player that play LB, LWB, LCB, CB, RCB, RB,
-- or RWB
CREATE TABLE defenders (
    id INT UNIQUE,
    position INT NOT NULL,
    defending INT NOT NULL,
    physical INT NOT NULL,
    CHECK (position IN ('LB', 'LWB', 'LCB', 'CB', 'RCB', 'RB', 'RWB')),
    PRIMARY KEY (id),
    FOREIGN KEY (position) REFERENCES outfield_attributes(position)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (defending) REFERENCES outfield_attributes(defending)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (physical) REFERENCES outfield_attributes(physical)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id) REFERNCES player(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- A table that represents players that are midfielders as well as their 
-- relevant attributes. Midfielders are any player that play CDM, LDM, RDM, 
-- CAM, RCM, LCM, CM, LAM, RAM, LM, or RM
CREATE TABLE midfielders (
    id INT UNIQUE,
    position INT NOT NULL, 
    pace INT NOT NULL,
    passing INT NOT NULL,
    dribbling INT NOT NULL,
    physical INT NOT NULL,
    CHECK (position IN ('CDM', 'LDM', 'RDM', 'CAM', 'RCM', 'LCM', 'CM', 'LAM',
            'RAM', 'LM', 'RM')),
    PRIMARY KEY (id),
    FOREIGN KEY (pace) REFERENCES outfield_attributes(pace)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (passing) REFERENCES outfield_attributes(passing)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (dribbling) REFERENCES outfield_attributes(dribbling)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (physical) REFERENCES outfield_attributes(physical)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id) REFERNCES player(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- A table that represents players that are forwards as well as their 
-- relevant attributes. Forwards are any player that play CF, LF, LS, RS, LW, 
-- RW, RF, or ST
CREATE TABLE forwards (
    id INT UNIQUE,
    position INT NOT NULL,
    pace INT NOT NULL,
    shooting INT NOT NULL,
    passing INT NOT NULL,
    dribbling INT NOT NULL,
    CHECK (position IN ('CF', 'LF', 'LS', 'RS', 'LW', 'RW', 'RF', 'ST')),
    FOREIGN KEY (pace) REFERENCES outfield_attributes(pace)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (shooting) REFERENCES outfield_attributes(shooting)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (passing) REFERENCES outfield_attributes(passing)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (dribbling) REFERENCES outfield_attributes(dribbling)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id) REFERNCES player(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
