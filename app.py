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
    
# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------


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
    print('  (i) - Get information on a player by id')
    print('  (n) - Get the TOTY given a nationality')
    print('  (l) - Login')
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
    print('  (i) - Get information on a player by id')
    print('  (n) - Get the TOTY given a nationality')
    print('  (x) - yet another nifty thing')
    print('  (x) - more nifty things!')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'i':
        select_given_id()
    elif ans == 'n':
        get_TOTY()
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
