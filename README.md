### 🚀 Purpose

This project automates the process of creating Jira issues from GitHub. When a developer comments `/jira` on a GitHub issue, a webhook triggers an AWS Lambda function that creates a corresponding issue in Jira — removing manual overhead and aligning development workflows across tools.

---

### 🛠️ Tooling & Architecture

#### ✅ GitHub
- **Webhook** configured to trigger on **issue comments**
- Payload is sent when a comment contains the `/jira` command

#### ✅ AWS API Gateway
- **HTTP API** used to expose a secure endpoint for the GitHub webhook
- Routes requests to the Lambda function

#### ✅ AWS Lambda
- Python-based function
- Parses GitHub event payload
- Authenticates using Jira API token from AWS Secrets Manager
- Posts a new issue to the correct Jira project

#### ✅ AWS Secrets Manager
- Securely stores:
  - Jira URL
  - Jira Email
  - Jira API Token
  - Jira Project Key
  - GitHub Token (optional for feedback comments)

#### ✅ Lambda Layer
- Used to bundle third-party dependencies like `requests`
- Must be zipped with folder structure named `python/` — **not a generic name like `requests.zip`** which caused issues initially

---

### ⚙️ System Flow

```
GitHub Issue Comment ("/jira")
        ↓
GitHub Webhook (issue_comment event)
        ↓
API Gateway (HTTP POST /{Endpoint})
        ↓
AWS Lambda
        ↓
AWS Secrets Manager (Jira credentials)
        ↓
Jira API (POST /rest/api/3/issue)
        ↓
Issue Created in Jira
```

---

### 🐛 Problems Faced

#### 🔐 Authentication Issues
- Initially passed correct email and token, but lacked permissions in the Jira project
- Solved via `GET /mypermissions` API to confirm `"CREATE_ISSUES"` permission


#### 🧱 Lambda Layer Naming
- Lambda layer zip must follow exact structure:
  - Folder name: `python/`
  - Zip file must contain `python/lib/site-packages/...` for it to work
- Using a custom folder name (e.g., `requests.zip`) broke the import of `requests`



#### 💬 HTML Errors from Jira
- A 404 HTML page from Jira meant wrong API path or unauthenticated calls
- Solved by adding `Accept: application/json` and validating `/rest/api/3/issue` vs `/rest/api/2/issue`

---

### ✅ Status

- 🔗 End-to-end integration works ✅
- 🛠️ Can create Jira issues via GitHub comment `/jira`
- 🔐 Credentials stored securely
- 🧰 Errors logged, and retry logic or Slack alerts can be added easily

---

### 💡 Future Enhancements

- [ ] Post a comment on GitHub with a link to the Jira issue
- [ ] Add Slack integration for success/failure notifications
- [ ] Extend to support `/jira bug`, `/jira story`, etc. with different issue types
- [ ] Implement IAC for full infrastructure automation

---
