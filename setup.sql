player:
_sofifa_id_
_long_name_
overall -- The player's rating
wage_eur

nontechnical_attributes:
_sofifa_id_
_long_name_
age
dob
height_cm
weight_kg
nationality
club

-- PLAYERS ARE BASED OFF CLUB POSITION, NATIONAL TEAM DOES NOT HAVE ENOUGH INFO
-- Ignore subs, as they were not good enough to start on their own team, won't make
-- TOTY
goalkeepers:
_sofifa_id_
gk_diving
gk_handling
gk_kicking
gk_reflexes
gk_speed
gk_positioning

-- Check if position is in LB LWB LCB CB RCB RB RWB
defenders:
_sofifa_id_
defending
physic

-- Check if position is in CDM LDM RDM CAM RCM LCM CM LAM RAM LM RM
midfielders:
_sofifa_id_
pace
passing
dribbling
physic

-- Check if position are in CF LF LS RS LW RW RF ST
forwards:
_sofifa_id_
pace
shooting
passing
dribbling
