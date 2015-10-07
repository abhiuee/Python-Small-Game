#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # Create connection and cursor
    conn = connect()
    cursor = conn.cursor()
    # Delete the matches table. Since only one tournament, reset wins and loses for all players
    cursor.execute("delete from matches")
    cursor.execute("update players set wins = 0, losses = 0")
    conn.commit()
    # Close connection
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    # Create connection and cursor
    conn = connect()
    cursor = conn.cursor();
    # Delete the players table.
    cursor.execute("delete from players")
    conn.commit()
    # Close connection
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    # Create connection and cursor
    conn = connect()
    cursor = conn.cursor()
    # SQL query to count the number of players and since only one row 
    # returned, therefore we use fetchone
    cursor.execute("select count(*) from players")
    rows = cursor.fetchone()
    # Close connection
    conn.close()
    return rows[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # Create connection and cursor
    conn = connect()
    cursor = conn.cursor()
    # Clean the name to prevent from script injection
    name = bleach.clean(name, strip=True)
    # Insert the player into players table
    cursor.execute("insert into players (name) values (%s)", (name,))
    conn.commit()
    # Close connection
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # Create connection and cursor
    conn = connect()
    cursor = conn.cursor()
    # Get all the players sorted by wins and then by least number of losses
    cursor.execute("select * from standings")
    # Create an empty tuple and then update the tuple with (id, name, wins, matches)
    posts = ()
    for row in cursor.fetchall():
        posts = posts + ((int(row[1]), str(row[0]), int(row[2]), int(row[2])+ int(row[3])),) 
    # Close connection
    conn.close()
    return posts 

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Create connection and cursor
    conn = connect()
    cursor = conn.cursor()
    # Insert the new match into the matches table
    cursor.execute("insert into matches(winner, looser) values (%s, %s)", (winner, loser))
    # Update the wins and losses for respective winners and losers
    cursor.execute("update players set wins = wins + 1 where id = %s", (winner,))
    cursor.execute("update players set losses = losses + 1 where id = %s", (loser,))
    conn.commit()
    # Close connection
    conn.close() 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Create connection and cursor
    conn = connect()
    cursor = conn.cursor()
    # Initialize the pairings tuple to an empty tuple and offset to 0
    pairings = ()
    offset = 0
    # Loop goes goes through the table two rows at a time and create pairings
    # Once no more pairings can be made the loop exits
    while True:
    	cursor.execute("select id,name from standings limit 2 offset %s", (offset, ))
    	rows = cursor.fetchall()
        if (len(rows) != 2):
	    break
        # Since there are only two rows returned from query we can directly create pairing using indices
	pairings = pairings + ((int(rows[0][0]), str(rows[0][1]), int(rows[1][0]), str(rows[1][1])),)
        offset = offset + 2
    # Close connection
    conn.close()
    # Return the pairings
    return pairings
    

