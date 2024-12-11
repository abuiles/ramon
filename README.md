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
3. Install uv: https://docs.astral.sh/uv/getting-started/installation/

4. Initialize the project:

```bash
just init
```

5. Run the project:

```bash
uv run python -m ramon
```

## Environment Variables

The following environment variables need to be configured:

* `JIRA_SERVER`: The URL of your JIRA server instance
* `JIRA_EMAIL`: Your JIRA account email
* `JIRA_TOKEN`: Your JIRA API token for authentication
* `OPENAI_API_KEY`: Your OpenAI API key
