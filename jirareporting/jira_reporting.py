from jirareporting import Config, env
import requests
import json


class Jira:

    def __init__(self, server=Config.JIRA_SERVER, user=Config.JIRA_USER, token=Config.JIRA_API_TOKEN,
                 rapid_view_id=Config.JIRA_RAPID_VIEW):
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

    def __init__(self, sprint: int, server=Config.JIRA_SERVER, user=Config.JIRA_USER, token=Config.JIRA_API_TOKEN,
                 rapid_view_id=Config.JIRA_RAPID_VIEW):
        Jira.__init__(self, server=server, user=user, token=token, rapid_view_id=rapid_view_id)
        self.raw_content = self.get_raw_content_sprint_report(sprint=sprint)
        self.issues_key_added_during_sprint = self.get_issues_key_added_during_sprint()
        self.completed_issues = self.get_completed_issues()
        self.issues_not_completed = self.get_issues_not_completed()
        self.issues_group_by_epic = self.get_issues_group_by_epic()

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

    def get_issues_not_completed(self):
        return self.raw_content.get('issuesNotCompletedInCurrentSprint')

    @staticmethod
    def get_distinct_epics(issues):
        epics = list()
        for issue in issues:
            epic = issue.get('epic')
            if epic and epic not in epics:
                epics.append(epic)

    def get_issues_group_by_epic(self):
        epics = dict()
        for issue in self.completed_issues:

            # Get epic name of the issue, if no epic then categorize under a 'Miscellaneous' epic
            epic_field = issue.get('epicField')
            if epic_field:
                epic_name = epic_field.get('text')
            else:
                epic_name = 'Miscellaneous'

            # Verify if the epic exists in the epics dictionary. If not, add it
            if not epics.get(epic_name):
                epics[epic_name] = list()

            # Append the issue to corresponding epic
            epics[epic_name].append(issue)

        return epics

    def print_report(self):
        template = env.get_template('sprint_report.txt')
        return print(template.render(epics=self.get_issues_group_by_epic()))
