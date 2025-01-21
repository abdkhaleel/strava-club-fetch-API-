# Strava Club Data Exporter

This project provides Python scripts to fetch data from Strava clubs, including club details, activities, and members. The data is processed and exported to Excel and CSV files for further analysis.

## Features
- Fetch club details, activities, and members from Strava API.
- Process raw data to extract meaningful information.
- Export data to Excel and CSV formats.
- Easy-to-use Python scripts.

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- `requests` library
- `pandas` library
- `xlsxwriter` library

Install dependencies using:
```bash
pip install requests pandas xlsxwriter
```

## Setup Instructions

### Step 1: Get Strava API Credentials
1. Go to the [Strava Developers](https://www.strava.com/settings/api) page.
2. Create an application and obtain:
   - **Client ID**
   - **Client Secret**
   - **Refresh Token** (generated using the OAuth2 flow below)

### Step 2: Obtain Strava Refresh Token

Edit `OAuth2.py` and replace the placeholders with your Strava API credentials:

```python
client_id = 'your_client_id'
client_secret = 'your_client_secret'
params = {
    'client_id': client_id,
    'redirect_uri': 'http://localhost',
    'response_type': 'code',
    'scope': 'read_all,profile:read_all,activity:read_all'
}
```

Run the `OAuth2.py` script to get the refresh token:

```bash
python OAuth2.py
```

Follow these steps:
1. Open the URL displayed in the terminal.
2. Authorize the app and copy the redirected URL.
3. Paste the URL when prompted.
4. Copy the generated refresh token.

### Step 3: Configure API Credentials

Edit `FetchFromStrava.py` and replace the placeholders with your Strava API credentials:

```python
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REFRESH_TOKEN = 'your_refresh_token'
CLUB_ID = 'your_club_id'
```

### Step 4: Run the Script

Once configured, run the script to fetch and export club data:

```bash
python FetchFromStrava.py
```

The script will generate the following files:
- `strava_club_data.xlsx` (Excel file with club details, activities, and members)
- `club_activities.csv` (CSV file with activity data)

## Project Structure

```
|-- FetchFromStrava.py   # Main script to fetch and export Strava club data
|-- OAuth2.py            # Script to obtain Strava refresh token
|-- README.md            # Documentation
|-- requirements.txt     # List of dependencies
```

## Troubleshooting

- If you get an "Invalid Token" error, re-run `OAuth2.py` to get a new refresh token.
- Ensure you have the correct scopes set (`read_all, profile:read_all, activity:read_all`).
- Check if the club ID is correct.

## Contributions
Feel free to submit issues or pull requests to improve the project.

## License
This project is open-source and available under the MIT License.

