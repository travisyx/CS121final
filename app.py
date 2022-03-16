# Names: Travis Xiang, Rohan Iyer
# Emails: txiang@caltech.edu, riiyer@caltech.edu

import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. Set to False when done testing.
DEBUG = True


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='appadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',
          password='adminpw',
          database='totydb'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def select_given_id():
    """
    Select the name, club, nationality, wage, and rating for a player given
    the id.
    """
    play_id = input("Enter the player id: ").strip()
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = """
SELECT name, club, nationality, wage, rating 
FROM player NATURAL JOIN nontechnical_attributes
WHERE id = \'%s\';
""" % (play_id, )
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("The id does not exist!")
        else:
            row = rows[0]
            print("Name: " + str(row[0]))
            print("Club: " + str(row[1]))
            print("Nationality: " + str(row[2]))
            print("Wage: " + str(row[3]))
            print("Rating: " + str(row[4]))
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("""An error occurred, please email txiang@caltech.edu or 
                            riiyer@caltech.edu!""")


def compare_players():
    """
    Given two player ids, compare them.
    """
    play_one = input("Enter the first player's id: ").strip()
    play_two = input("Enter the second player's id: ").strip()
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = """
SELECT compare (%s, %s);
""" % (play_one, play_two, )
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("Something went wrong...")
        else:
            row = int(rows[0][0])
            if row == 1:
                print("The first player is predicted to be better!")
            elif row == 0:
                print("The two players are predicted to be equivalent!")
            elif row == -1:
                print("The second player is predicted to be better!")
            else:
                print("The two players play different positions!")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("""An error occurred, please email txiang@caltech.edu or 
                            riiyer@caltech.edu!""")


def get_TOTY():
    """
    Select a team of the year given the nationality
    """
    inp = input("Enter a nation: ").strip().lower().split(" ")
    nation = ""
    for j in range(len(inp)):
        i = inp[j]
        nation += i[0].upper() + i[1:]
        if j != len(inp)-1:
            nation += " "
    cursor = conn.cursor()
    sqlgk = """
SELECT name FROM 
    (SELECT name, id, compute_rating(id) AS rating
        FROM goalkeepers NATURAL JOIN nontechnical_attributes
        WHERE nationality = \'%s\' ORDER BY rating DESC LIMIT 1) AS t;
""" % (nation, )
    sqldef = """
SELECT name FROM 
    (SELECT name, id, compute_rating(id) AS rating
        FROM defenders NATURAL JOIN nontechnical_attributes
        WHERE nationality = \'%s\' ORDER BY rating DESC LIMIT 4) AS t;
""" % (nation, )
    sqlmid = """
SELECT name FROM 
    (SELECT name, id, compute_rating(id) AS rating
        FROM midfielders NATURAL JOIN nontechnical_attributes
        WHERE nationality = \'%s\' ORDER BY rating DESC LIMIT 3) AS t;
""" % (nation, )
    sqlfor = """
SELECT name FROM 
    (SELECT name, id, compute_rating(id) AS rating
        FROM forwards NATURAL JOIN nontechnical_attributes
        WHERE nationality = \'%s\' ORDER BY rating DESC LIMIT 3) AS t;
""" % (nation, )
    try:
        # Select the goalkeeper
        cursor.execute(sqlgk)
        rowsgk = cursor.fetchall()

        # Select the 4 defenders
        cursor.execute(sqldef)
        rowsdef = cursor.fetchall()

        # Select the 3 midfielders
        cursor.execute(sqlmid)
        rowsmid = cursor.fetchall()

        # Select the 3 forwards
        cursor.execute(sqlfor)
        rowsfor = cursor.fetchall()

        num_players = len(rowsgk) + len(rowsdef) + len(rowsmid) + len(rowsfor)
        if num_players == 0:
            print(f"No player from the nation {nation} exists in the db!")
        elif num_players < 11:
            print("""There are not enough players from this 
                        #nation to form a TOTY!""")
            print(f"There are only {num_players} players!")
        else:
            print(f"\nThe TOTY for {nation} is: ")
            for row in rowsgk:
                print("Goalkeeper: " + str(row[0]))
            for row in rowsdef:
                print("Defender: " + str(row[0]))
            for row in rowsmid:
                print("Midfielder: " + str(row[0]))
            for row in rowsfor:
                print("Forward: " + str(row[0]))
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("""An error occurred, please email txiang@caltech.edu or 
                            riiyer@caltech.edu!""")
    

def insert_player():
    """
    Insert a new player into the database
    """
    goalkeepers = ['GK']
    defenders = ['LB', 'LWB', 'LCB', 'CB', 'RCB', 'RB', 'RWB']
    midfielders = ['CDM', 'LDM', 'RDM', 'CAM', 'RCM', 'LCM', \
                        'CM', 'LAM','RAM', 'LM', 'RM']
    forwards = ['CF', 'LF', 'LS', 'RS', 'LW', 'RW', 'RF', 'ST']

    print('Create a new player!\n')
    player_name = input('Enter a new player: \n').strip()
    nation = input("Enter the player's nationality: \n").strip()
    position = input("Enter the player's position: \n").strip()
    age = input("Enter the player's age: \n").strip()
    dob = input("Enter the player's date of birth (YYYY-MM-DD): \n").strip()
    height = input("Enter the player's height in cm: \n").strip()
    weight = input("Enter player's weight in kg: \n").strip()
    overall = input("Enter player's overall rating: \n").strip()
    club = input("Enter player's club: \n").strip()
    position_dict = {'goalkeepers': goalkeepers, 'defenders': defenders, \
                        'midfielders': midfielders, 'forwards': forwards}

    #Check if the position is a valid position. Else exit
    position_table = ''
    for key in position_dict:
        if position in position_dict[key]:
            position_table = key
    if position_table == '':
        print('The position you entered is not valid')
        sys.exit(1)

    cursor = conn.cursor()
    get_next_id = "SELECT MAX(id)+1 AS next_id FROM player;" # get the next id
    cursor.execute(get_next_id)
    next_id = cursor.fetchall()[0][0]

    get_predicted_wage = """
SELECT get_predicted_wage(%s, \'%s\', %s);
""" % (next_id, player_name, overall,)
    cursor.execute(get_predicted_wage)
    pred_wage = cursor.fetchall()[0][0]

    insert_player_table = """
INSERT INTO player VALUES (%s, \'%s\', %s, %s);
""" % (next_id, player_name, pred_wage, overall,)
    cursor.execute(insert_player_table)
    conn.commit()

    insert_nontech_table = """
INSERT INTO nontechnical_attributes(age, dob, height, weight, nation, club) 
VALUES (%s,\'%s\', %s, %s, \'%s\', \'%s\';
""" % (age, dob, height, weight, nation, club,)
    cursor.execute(insert_nontech_table)
    conn.commit()

    if position_table == 'goalkeepers':
        insert_pos_table = """
INSERT INTO \'%s\' (diving, handling, kicking, reflexes, speed, positioning) 
VALUES (%s, %s, %s, %s, %s, %s)
""" % (position_table, overall, overall, overall, overall, overall, overall,)
    elif position_table == 'defenders':
        insert_pos_table = """
INSERT INTO \'%s\' (defending, physical) VALUES (%s, %s)
""" % (position_table, overall, overall,)
    elif position_table == 'midfielders':
        insert_pos_table = """
INSERT INTO \'%s\' (pace, passing, physical, dribbling) 
VALUES (%s, %s, %s, %s)
""" % (position_table, overall, overall, overall, overall,)
    else:
        insert_pos_table = """
INSERT INTO \'%s\' (pace, shooting, dribbling, passing) 
VALUES (%s, %s, %s, %s)
""" % (position_table, overall, overall, overall, overall,)
    cursor.execute(insert_pos_table)
    conn.commit()
    print('Inserted Succesfully!')


# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
def login():
    """
    A function to log users in given usernames and passwords login
    """
    username = input("Enter username: ")
    password = input("Enter password: ") # In the future, hide this text
    cursor = conn.cursor()
    sql = """ SELECT authenticate(\'%s\', \'%s\'); """ % (username, password, )
    try:
        # Select the goalkeeper
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("Your account does not exist!")
        else:
            row = rows[0]
            if row[0] == 1:
                print("Success!\n")
                show_options()
            else:
                print("Incorrect password or your account does not exist!\n")
                show_options()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("""An error occurred, please email txiang@caltech.edu or 
                            riiyer@caltech.edu!""")


def create_user():
    """
    A function to create a new user for the database. Assumes that the account
    does not exist. Crashes if it does.
    """
    username = input("Enter username: ")
    password = input("Enter password: ") # In the future, hide this text
    cursor = conn.cursor()
    sql = """ CALL sp_add_user(\'%s\', \'%s\'); """ % (username, password, )
    try:
        # Select the goalkeeper
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("Success!")
        show_options()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr("""An error occurred, please email txiang@caltech.edu or 
                            riiyer@caltech.edu!""")


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('What would you like to do? ')
    print('  (c) - Create a new account')
    print('  (l) - Login')
    print('  (i) - Get information on a player by id')
    print('  (m) - Compare two players')
    print('  (n) - Get the TOTY given a nationality')
    print('  (p) - Enter a password to access admin (for convenience)')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'i':
        select_given_id()
    elif ans == 'm':
        compare_players()
    elif ans == 'n':
        get_TOTY()
    elif ans == 'l':
        login()
    elif ans == 'c':
        create_user()
    elif ans == 'p':
        inp = input("Enter the password: ")
        if inp.lower().strip() == 'knox':
            print("Success!")
            show_admin_options()
        else:
            print("Incorrect.")
            show_options()
    elif ans == '':
        pass    


# You may choose to support admin vs. client features in the same program, or
# separate the two as different client and admin Python programs using the same
# database.
def show_admin_options():
    """
    Displays options specific for admins, such as adding new data <x>,
    modifying <x> based on a given id, removing <x>, etc.
    """
    print('What would you like to do? ')
    print('  (c) - Create a new account')
    print('  (l) - Login')
    print('  (i) - Get information on a player by id')
    print('  (n) - Get the TOTY given a nationality')
    print('  (p) - Insert a player')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'i':
        select_given_id()
    elif ans == 'n':
        get_TOTY()
    elif ans == 'l':
        login()
    elif ans == 'c':
        create_user()
    elif ans == 'p':
        insert_player()
    elif ans == '':
        pass


def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    # This conn is a global object that other functinos can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
