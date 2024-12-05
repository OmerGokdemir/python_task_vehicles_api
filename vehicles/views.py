from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import requests
import csv
from .serializers import DummySerializer

class VehicleAPIView(GenericAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = DummySerializer

    def get_queryset(self):
        return []
    
    def get_access_token(self):
        """Get access token for the external API."""
        auth_url = "https://api.baubuddy.de/index.php/login"
        auth_headers = {
            "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
            "Content-Type": "application/json"
        }
        auth_payload = {"username": "365", "password": "1"}
        auth_response = requests.post(auth_url, json=auth_payload, headers=auth_headers)
        if auth_response.status_code == 200:
            return auth_response.json().get("oauth", {}).get("access_token")
        raise ValueError("Could not retrieve access token. Check your credentials or API availability.")

    def get_vehicle_data(self, access_token):
        """Fetch active vehicle data from the external API."""
        vehicles_url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(vehicles_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        raise ValueError("Failed to fetch vehicle data. Check your access token or API endpoint.")

    def resolve_label_colors(self, label_ids, access_token):
        """Resolve color codes for given label IDs."""
        if not isinstance(label_ids, list):
            return []

        headers = {"Authorization": f"Bearer {access_token}"}
        colors = []
        for label_id in label_ids:
            label_url = f"https://api.baubuddy.de/dev/index.php/v1/labels/{label_id}"
            response = requests.get(label_url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                color_code = json_data.get("colorCode")
                if color_code:
                    colors.append(color_code)
            else:
                colors.append(None)  # Ek bir hata kontrolü
        return colors

    def post(self, request, *args, **kwargs):
        # Step 1: Get the CSV file and parse it
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "No file uploaded. Please provide a valid CSV file."}, status=400)

        try:
            csv_data = list(csv.DictReader(csv_file.read().decode('utf-8').splitlines()))
        except Exception as e:
            return Response({"error": f"Invalid CSV format: {str(e)}"}, status=400)

        # Step 2: Get access token and vehicle data
        try:
            access_token = self.get_access_token()
            vehicles_data = self.get_vehicle_data(access_token)
        except ValueError as e:
            return Response({"error": str(e)}, status=500)

        # Step 3: Filter vehicle data by `hu` field
        filtered_data = [vehicle for vehicle in vehicles_data if vehicle.get("hu")]

        # Step 4: Resolve label colors
        for vehicle in filtered_data:
            label_ids = vehicle.get("labelIds", [])
            vehicle["resolved_colors"] = self.resolve_label_colors(label_ids, access_token)

        # Step 5: Return filtered data
        return Response(filtered_data)
