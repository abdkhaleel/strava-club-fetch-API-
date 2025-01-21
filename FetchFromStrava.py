import requests
import json
from datetime import datetime
import pandas as pd

class StravaAPI:
    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.base_url = "https://www.strava.com/api/v3"
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        auth_url = "https://www.strava.com/oauth/token"
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        response = requests.post(auth_url, data=payload)
        return response.json().get('access_token')

    def get_club_details(self, club_id):
        endpoint = f"{self.base_url}/clubs/{club_id}"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get(endpoint, headers=headers)
        return response.json()

    def get_club_activities(self, club_id, per_page=30):
        endpoint = f"{self.base_url}/clubs/{club_id}/activities"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'per_page': per_page}
        response = requests.get(endpoint, headers=headers, params=params)
        return response.json()

    def get_club_members(self, club_id, per_page=30):
        endpoint = f"{self.base_url}/clubs/{club_id}/members"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'per_page': per_page}
        response = requests.get(endpoint, headers=headers, params=params)
        return response.json()

def process_activities(activities):
    processed_activities = []
    for activity in activities:
        activity_copy = activity.copy()
        if 'athlete' in activity_copy and isinstance(activity_copy['athlete'], dict):
            activity_copy['athlete_name'] = f"{activity_copy['athlete'].get('firstname', '')} {activity_copy['athlete'].get('lastname', '')}".strip()
            del activity_copy['athlete']
        processed_activities.append(activity_copy)
    return processed_activities

def process_members(members):
    processed_members = []
    for member in members:
        member_copy = member.copy()
        member_copy['full_name'] = f"{member_copy.get('firstname', '')} {member_copy.get('lastname', '')}".strip()
        processed_members.append(member_copy)
    return processed_members

def main():
    # Strava API credentials
    CLIENT_ID = 'your_client_id'
    CLIENT_SECRET = 'your_client_secret'
    REFRESH_TOKEN = 'your_refresh_token'
    CLUB_ID = 'your_club_id'

    strava = StravaAPI(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

    # Fetch data
    club_details = strava.get_club_details(CLUB_ID)
    club_activities = strava.get_club_activities(CLUB_ID, per_page=200)
    club_members = strava.get_club_members(CLUB_ID, per_page=200)

    # Process and convert to DataFrames
    club_details_df = pd.DataFrame([club_details])

    if isinstance(club_activities, list):
        processed_activities = process_activities(club_activities)
        club_activities_df = pd.DataFrame(processed_activities)
    else:
        club_activities_df = pd.DataFrame()

    if isinstance(club_members, list):
        processed_members = process_members(club_members)
        club_members_df = pd.DataFrame(processed_members)
    else:
        club_members_df = pd.DataFrame()
    
    if not club_activities_df.empty:
        cols = list(club_activities_df.columns)
        cols.remove('athlete_name')
        cols.insert(1, 'athlete_name')
        club_activities_df = club_activities_df[cols]

    # Export to Excel
    excel_file = 'strava_club_data.xlsx'
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        club_details_df.to_excel(writer, sheet_name='Club Details', index=False)
        club_activities_df.to_excel(writer, sheet_name='Club Activities', index=False)
        club_members_df.to_excel(writer, sheet_name='Club Members', index=False)

        # Format Excel sheets
        workbook = writer.book
        for sheet in ['Club Details', 'Club Activities', 'Club Members']:
            worksheet = writer.sheets[sheet]
            for col_num, value in enumerate(eval(f"{sheet.lower().replace(' ', '_')}_df").columns.values):
                worksheet.write(0, col_num, value)

    # Export activities to CSV
    club_activities_df.to_csv('club_activities.csv', index=False)
    
    print(f"Data exported successfully to '{excel_file}' and 'club_activities.csv'!")

if __name__ == "__main__":
    main() 