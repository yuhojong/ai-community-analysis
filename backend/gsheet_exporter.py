import gspread
from oauth2client.service_account import ServiceAccountCredentials # type: ignore
import os

class GoogleSheetExporter:
    def __init__(self, json_keyfile_path: str):
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, self.scope)
        self.client = gspread.authorize(self.creds)

    def export_data(self, sheet_name: str, data: list):
        try:
            sheet = self.client.open(sheet_name).sheet1
        except gspread.SpreadsheetNotFound:
            sheet = self.client.create(sheet_name).sheet1

        # Assume data is a list of lists [Date, Platform, Channel, Content, Author]
        sheet.append_rows(data)
        return sheet.url
