from dotenv import load_dotenv
import requests
import os
import json
load_dotenv()


SERVER = os.getenv('JIRA_SERVER')
USER = os.getenv('JIRA_USER')
TOKEN = os.getenv('JIRA_API_TOKEN')
RAPID_VIEW_ID = os.getenv('JIRA_RAPID_VIEW')


class Jira:

    def __init__(self, server=SERVER, user=USER, token=TOKEN, rapid_view_id=RAPID_VIEW_ID):
        self.server = server
        self.base_url = server + '/rest/greenhopper/latest/'
        self.user = user
        self.token = token
        self.rapid_view_id = rapid_view_id
        self.auth = (self.user, self.token)

    def set_rapid_view_id(self, id):
        self.rapid_view_id = id

    def get_raw_content_sprint_report(self, sprint: int):
        url = f'{self.base_url}rapid/charts/sprintreport?rapidViewId={self.rapid_view_id}&sprintId={str(sprint)}'
        r = requests.get(url=url, auth=self.auth)
        content = json.loads(r.content)
        return content.get('contents')


class SprintReport(Jira):

    def __init__(self, sprint: int, server=SERVER, user=USER, token=TOKEN, rapid_view_id=RAPID_VIEW_ID):
        Jira.__init__(self, server=server, user=user, token=token, rapid_view_id=rapid_view_id)
        self.raw_content = self.get_raw_content_sprint_report(sprint=sprint)
        self.issues_key_added_during_sprint = self.get_issues_key_added_during_sprint()
        self.completed_issues = self.get_completed_issues()
        self.issues_not_completed_in_sprint = self.get_issues_not_completed_in_sprint()

    def get_issues_key_added_during_sprint(self):
        list_of_issues = list()
        issues = self.raw_content.get('issueKeysAddedDuringSprint')
        if issues:
            for key, value in issues.items():
                if value is True:
                    list_of_issues.append(key)
        return list_of_issues

    def get_completed_issues(self):
        return self.raw_content.get('completedIssues')

    def get_issues_not_completed_in_sprint(self):
        return self.raw_content.get('issuesNotCompletedInCurrentSprint')
