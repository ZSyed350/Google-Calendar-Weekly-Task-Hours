# Fetch Weekly Task Hours from Google Calendar

This script retrieves and calculates the total hours spent on a specified task from a Google Calendar for the current week (Monday to Friday). This can help you refine your time blocking, analyze where your time is going, or help you gain a realistic perspective on your plans, ensuring your schedule is achievable. It uses the Google Calendar API and requires a service account for authentication.

## Prerequisites
- Python 3.7 or higher
- A Google Cloud project with the Google Calendar API enabled
- Service account credentials JSON file

---

## Setup Instructions

### 1. Enable Google Calendar API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Log in with your Google account.
3. Create a new project or select an existing project:
   - Click the project selector dropdown → **New Project** → Enter a name → **Create**.
4. In the left-hand menu, go to **APIs & Services** → **Library**.
5. Search for "Google Calendar API" and click on it.
6. Click **Enable**.

### 2. Create a Service Account
1. In the Cloud Console, go to **APIs & Services** → **Credentials**.
2. Click **+ Create Credentials** → **Service Account**.
3. Provide a service account name (e.g., "calendar-access") → Click **Create and Continue**.
4. (Optional) Assign roles if needed → Click **Done**.
5. In the **Service Accounts** section, find the newly created service account and click on it.
6. Go to the **Keys** tab → Click **Add Key** → **Create New Key**.
7. Choose JSON format → Click **Create**.
8. A JSON file will be downloaded (this is your credentials file). Be careful, and keep it secure!

### 3. Add Credentials to Environment Variables
1. Move the `credentials.json` file to a secure location.
2. Add this path to your environment variables as `GOOGLE_APPLICATION_CREDENTIALS`

### 4. Share Your Calendar with the Service Account
1. Open [Google Calendar](https://calendar.google.com/).
2. Click the three dots next to the calendar you want to share → **Settings and sharing**.
3. Under **Share with specific people**, add the service account email (found in the credentials JSON file under `client_email`).
4. Set permissions to **See all event details**.
5. Save the changes.

### 5. Install Required Python Libraries
Install the necessary libraries:
```pip install -r requirements.txt```

---

### Running the Script

#### Command-Line Arguments
- `--task` (`-t`): Task name to filter calendar events (case-insensitive).
- `--calendar_id` (`-c`): The ID of the calendar to query.

#### Example Usage
```cmd
python gethours.py -t "study" -c "primary"
```