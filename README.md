# Ram-on

Ramon is a good AI assistant. It streamlines tasks and boosts everyday efficiency.

## Setting up the Project

To set up the project, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/abuiles/ramon.git
```
2. Navigate to the project directory:
```bash
cd ramon
```
3. Install Just:
```bash
brew install just
```

4. Install uv: https://docs.astral.sh/uv/getting-started/installation/
```bash
brew install uv
```

5. Initialize the project:
```bash
just init
```
6. Start the cli in prompt mode:
```bash
just chat
```

## Environment Variables

The following environment variables need to be configured:

* `JIRA_SERVER`: The URL of your JIRA server instance
* `JIRA_EMAIL`: Your JIRA account email
* `JIRA_TOKEN`: Your JIRA API token for authentication
* `OPENAI_API_KEY`: Your OpenAI API key

## Getting Your Jira Token

To create the Jira API Key, follow these steps:
1. Log into Jira using the service account you created.
2. Click on the user profile icon in the top right corner.
3. Select "Manage Account" from the dropdown menu.
4. Navigate to the "Security" tab.
5. Click on "Create and manage API Tokens".
