import subprocess, time, requests,os
import MongoDB
import MongoDB.main
from dotenv import load_dotenv
load_dotenv()

CONNECTION_ID = os.getenv("CONNECTION_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET =os.getenv("CLIENT_SECRET")
AIRBYTE_API_URL = "https://api.airbyte.com/v1"


def get_access_token():
    response = requests.post(
        "https://api.airbyte.com/v1/applications/token",
        json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
    )
    response.raise_for_status()
    return response.json()["access_token"]
AIRBYTE_API_KEY=get_access_token()

def trigger_airbyte_sync():
    # headers = {"Authorization": f"Bearer {AIRBYTE_API_KEY}"}
    url = f"https://api.airbyte.com/v1/connections/{CONNECTION_ID}"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {AIRBYTE_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    # print(response.text)

def wait_for_sync():
    url = "https://api.airbyte.com/v1/jobs"
    payload = { "jobType": "sync","connectionId":CONNECTION_ID }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {AIRBYTE_API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)

    # return response.text["jobId"]

def run_dbt():
    subprocess.run(["dbt", "run"], cwd="./chatbotProject", check=True)

def main():
    print("Generating synthetic data...")
    MongoDB.main.start()

    print("Triggering Airbyte sync...")
    trigger_airbyte_sync()
    wait_for_sync()
    time.sleep(120)
    print("Running dbt...")
    run_dbt()

if __name__ == "__main__":
    main()
