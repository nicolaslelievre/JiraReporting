import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    JIRA_SERVER = os.environ.get('JIRA_SERVER')
    JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN')
    JIRA_USER = os.environ.get('JIRA_USER')
    JIRA_RAPID_VIEW = os.environ.get('JIRA_RAPID_VIEW')
