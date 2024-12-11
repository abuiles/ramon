# Ram-on

Ramon is a good AI assistant that helps manage, prioritize, and streamline tasks. It tracks deadlines, facilitates collaborations, and integrates with systems like JIRA to automate workflows, enabling efficient task management and completion.

> **Note:** Ramon is currently in development mode. In the future, it will be available as a proper Python package. For now, you'll need to run it directly from the repository.

## Prerequisites

1. Install the following tools:
   - [Just](https://github.com/casey/just): `brew install just`
   - [uv](https://docs.astral.sh/uv/getting-started/installation/): `brew install uv`
   - [direnv](https://direnv.net/) (recommended): `brew install direnv`

## Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/abuiles/ramon.git
cd ramon
```

2. Create a `.envrc` file in the project directory with your environment variables:
```bash
# Jira configuration
export JIRA_SERVER="https://your-instance.atlassian.net"
export JIRA_EMAIL="your-email@company.com"
export JIRA_TOKEN="your-jira-token"  # See "Getting Your Jira Token" section below

# OpenAI configuration
export OPENAI_API_KEY="your-openai-key"

# Database configuration
export DB_DIR=~/ramon-db  # Or your preferred location

# Workflow customization
export PROMPT_EXTENSION="Jira project keys:
- RAM: Ramon-related tasks
- WORK: Work projects

### Team members
- Alice (Engineering Manager)
- Bob (Frontend)
- Charlie (Backend)

### Default owner
- Tasks are assigned to Alice unless specified otherwise"
```

3. Set up your task database:
```bash
mkdir -p $DB_DIR
cd $DB_DIR
git init  # Optional but recommended for version control
```

4. Initialize the project:
```bash
just init
```

5. Start using Ramon:
```bash
just chat
```

## Configuration Details

### Getting Your Jira Token

To create the Jira API token:
1. Log into Jira using your account
2. Click on your profile icon (top right)
3. Select "Manage Account"
4. Navigate to "Security" tab
5. Click "Create and manage API Tokens"

### Customizing the Assistant's Context

The `PROMPT_EXTENSION` environment variable helps Ramon understand your specific workflow. You can customize it with:
- Project-specific information
- Team members
- JIRA project keys
- Default task ownership
- Any other workflow-specific details

This context helps Ramon:
- Use the correct JIRA project keys
- Understand team member roles
- Set appropriate default task owners
- Make more contextually relevant decisions

### Task Storage

> **Note:** Currently using a simple JSON file for storage. A proper database implementation is planned for the future.

Tasks are stored in `$DB_DIR/tasks.json` with the following structure:
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

Since it's a JSON file, you can:
- Review task history through git
- Manually edit tasks (though using the CLI is recommended)
- Back up tasks by pushing to a remote repository
- Debug by examining file changes

> **Tip:** Using git in your `$DB_DIR` is recommended for tracking changes and backup.

## Roadmap

Ramon is actively being developed. Here are the key features planned for future releases:

### Database Improvements
- Replace JSON file storage with SQLite for better reliability and performance
- Add data migration tools for existing tasks
- Implement proper backup and restore functionality

### Web Interface
- Add a web dashboard for task management
- Provide visual task tracking and reporting
- Enable team collaboration features

### Smart Task Follow-ups
Ramon will be able to automatically follow up on tasks:
```bash
# Example future workflow
You: "Ramon, check with Amy why the landing page task isn't completed yet."

Ramon: "I'll start a conversation with Amy about the landing page task:
1. Send a Slack message to Amy
2. Wait for her response
3. Ask follow-up questions if needed
4. Provide you with a clear status update"
```

### Deployment

**Help Needed**: I'm punting on the deployment for now. If you have experience with cloud deployments or suggestions on how to automate the process for Ramon, please contribute your insights. The goal is to make Ramon easily deployable to any cloud provider.
