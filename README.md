# JIRA Reporting

Automate sprint reporting

## Getting started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
- Python 3.6
- [JIRA](https://www.atlassian.com/try/cloud/signup?bundle=jira-software&edition=free) project using the Scrum Template
- ID of the JIRA RapidView
    - Select Reports in the menu of your JIRA project
    - Select Sprint Report
    - The url should contains `RapidBoard.jspa?rapidView=3`. In this case, the ID of the rapid view is 3.
- A JIRA Token
    - Go to your JIRA account settings
    - Select `Security` in the menu
    - Under API Token, click on `Create and manage API tokens`
    - Click on the Create API button
    - Provide a label such as Python Project and click on `Create`

 
### Installing

Install the required packages
```
pip install -r requirements.txt
```

Create .env file at the root of the project
```
JIRA_SERVER= Add the url of your jira here
JIRA_API_TOKEN= Add your JIRA token
JIRA_USER= Add your jira user here
JIRA_RAPID_VIEW= Add the ID of the RapidView
```
Here is an example:
```
JIRA_SERVER=https://jakeperalta.atlassian.net
JIRA_API_TOKEN=BrOOkLyn99CaPTAiNHolT
JIRA_USER=jakeperalta@gmail.com
JIRA_RAPID_VIEW=3
```
