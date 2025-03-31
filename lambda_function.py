import json
import os
import requests
import boto3

def get_jira_credentials():
    secret_name = os.getenv("secret_name")
    region_name = os.getenv("region")
    
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    secrets = json.loads(response["SecretString"])

    return (
            secrets["JIRA_URL"],
            secrets["JIRA_EMAIL"],
            secrets["JIRA_API_TOKEN"],
            secrets["JIRA_PROJECT_KEY"]
        )

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    try:
        body = json.loads(event["body"])
    except Exception as e:
        print("Failed to parse event body:", str(e))
        return {"statusCode": 400, "body": "Invalid JSON in request body"}

    # Extract GitHub comment
    comment = body.get("comment", {}).get("body", "")
    if "/jira" not in comment:
        print("No Jira command found in comment.")
        return {"statusCode": 200, "body": "No action needed"}

    issue_title = body.get("issue", {}).get("title", "No title provided")
    issue_description = body.get("issue", {}).get("body", "No description provided")

    try:
        JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY = get_jira_credentials()

        # Jira API setup
        jira_api_url = f"{JIRA_URL}"
        headers = {
            "Authorization": f"Basic {requests.auth._basic_auth_str(JIRA_EMAIL, JIRA_API_TOKEN)}",
            "Content-Type": "application/json"
        }
        payload = {
            "fields": {
                "project": {"key": JIRA_PROJECT_KEY},
                "summary": issue_title,
                "description": issue_description,
                "issuetype": {"name": "Task"}
            }
        }

        print("Sending payload to Jira:", json.dumps(payload))

        response = requests.post(jira_api_url, headers=headers, json=payload)
        print("Jira response:", response.status_code, response.text)

        if response.status_code == 201:
            return {"statusCode": 201, "body": "Jira issue created successfully"}
        else:
            return {"statusCode": response.status_code, "body": response.text}

    except Exception as e:
        print("Unexpected error occurred:", str(e))
        return {"statusCode": 500, "body": "Internal Server Error"}
