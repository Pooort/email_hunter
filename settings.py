import os

from decouple import config

PROJECTPATH = os.path.dirname(os.path.realpath(__file__))
SQLITEPATH = os.path.join(PROJECTPATH, 'data.db')
DBCONNECTION = 'sqlite:////{}'.format(SQLITEPATH)

COMPANYTYPE = config('COMPANYTYPE')
HUNTERAPIKEY=config('HUNTERAPIKEY')