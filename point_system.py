#point_system.py

from pathlib import Path
import numpy as np
import pandas as pd

def get_balance(userid):
    points = pd.read_csv(Path('points.csv'))
    points = points.set_index('uid')
    return points.loc[userid]['bal']

def create_entry(userid, balance):
    """
    Creates an entry in points.csv.
    """
    points = pd.read_csv(Path('points.csv'))
    entry = {'uid': userid,
             'bal': balance}
    penis = points.append(entry, ignore_index=True)
    penis.to_csv('points.csv', index=False)

def update_entry(userid, balance):
    """
    Updates a user's balance by a set amount. If entry for user does not exist, create a new entry.
    """
    points = pd.read_csv(Path('points.csv'))
    if userid not in points['uid'].values:
        create_entry(userid, balance)
    else:
        points = points.set_index('uid')
        before = get_balance(userid)
        after = int(before) + int(balance)
        points.loc[userid] = pd.Series({'bal': after})
        points = points.reset_index()
        points.to_csv('points.csv', index=False)

def set_entry(userid, balance):
    """
    Set a user's balance to specified amount. If entry for user does not exist, create a new entry.
    """
    points = pd.read_csv(Path('points.csv'))
    if userid not in points['uid'].values:
        create_entry(userid, balance)
    else:
        points = points.set_index('uid')
        points.loc[userid] = pd.Series({'bal': balance})
        points = points.reset_index()
        points.to_csv('points.csv', index=False)

if __name__ == '__main__':
    print('Creating/updating user entry')
    print()
    uid = input('User ID: ')
    bal = input('Balance: ')
    update_entry(uid, bal)