import configparser
import os
import pathlib

import dotenv

ROOT_FOLDER = pathlib.Path(__file__).parent.parent
ENV_FILENAME = 'prod.env'
env_ = ROOT_FOLDER / ENV_FILENAME
dotenv.load_dotenv(env_)
config = configparser.ConfigParser()
config.add_section('general')
config['general'] = os.environ
environ = config['general']

EMAILS_FOLDER = ROOT_FOLDER / 'emails'

MYSQL_HOST: str = environ['MYSQL_HOST']
MYSQL_PORT: int = environ.getint('MYSQL_PORT')
MYSQL_USER: str = environ['MYSQL_USER']
MYSQL_PASSWORD: str = environ['MYSQL_PASSWORD']
MYSQL_DB: str = environ['MYSQL_DB']
