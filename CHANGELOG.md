## 2024-12-13
### Move to gpt-4o-mini
Move to gpt-4o-mini. At one point, mini was hallucinating, but recent
changes to the prompt might have helped address that.

## 2024-12-12
### Reduce tokens
I noticed my OpenAI credits were burning quickly because I was sending
more tokens than necessary. I implemented several changes to address
this:

1. Only load non-completed tasks when requesting tasks.
2. Introduced a new file for archived documents to store tasks I no
   longer need in my current context. Eventually, these could be
   migrated to a vector DB for querying past tasks.
3. Kept the option to load archived tasks if needed.
4. Expanded the prompt to instruct the system to remove descriptions
   from tasks once they are created in Jira. After all, the
   information is already in Jira, and it might be redundant to keep
   it in memory. Though this could affect future searches, it helps
   keep tokens low now.

### New Jira capabilities: load comments, add comments, open Jira in a browser
Ramon can load or add new comments to a Jira ticket. If you want to
open the ticket in a browser, just say "open ticket."
