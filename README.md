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

## Database Setup

> **Note:** This is a temporary setup. In the future, we will use a database to store tasks.

Ramon uses a simple JSON file to store tasks, making it easy to version control and inspect changes. Here's how to set it up:

1. Create a directory for your task database:
```bash
mkdir ~/ramon-db
cd ~/ramon-db
git init
```

2. Set the `DB_DIR` environment variable to point to this directory:
```bash
# Add to your .bashrc, .zshrc, or equivalent
export DB_DIR=~/ramon-db
```

3. The tool will automatically create a `tasks.json` file in this directory when you add your first task.

### Version Control

Since the database is just a JSON file, you can use git to track changes:
```bash
cd ~/ramon-db
git add tasks.json
git commit -m "Task updates"
```

This allows you to:
- Review the history of your tasks
- Revert accidental changes
- Back up your tasks by pushing to a remote repository
- See exactly what the tool modified in each run

This is also useful for debugging and understanding the tool's behavior.

### Database Structure

Tasks are stored in `tasks.json` as a plain JSON array. Each task has the following structure:
```json
{
    "id": "task-1",
    "task": "Example task",
    "owner": "username",
    "priority": "high",
    "description": "Task description",
    "due_date": "2024-03-20",
    "completed_at": "",
    "metadata": "",
    "status": "to_do"
}
```

The JSON format makes it easy to manually edit tasks if needed, though it's recommended to use the CLI tool to ensure data consistency.