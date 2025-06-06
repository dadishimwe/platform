"""
Starlink API utilities for the Starlink Platform API.
"""
import requests
import time
from flask import current_app
from src.utils.auth import get_starlink_access_token

class StarlinkAPI:
    """Starlink API client."""
    
    def __init__(self):
        """Initialize Starlink API client."""
        self.base_url = current_app.config['STARLINK_API_URL']
        self.access_token = None
        self.token_expiry = 0
    
    def _ensure_token(self):
        """Ensure access token is valid."""
        current_time = time.time()
        if not self.access_token or current_time >= self.token_expiry:
            self.access_token = get_starlink_access_token()
            if self.access_token:
                # Token typically expires in 15 minutes, but we'll refresh after 14 minutes
                self.token_expiry = current_time + 14 * 60
            else:
                raise Exception("Failed to get Starlink access token")
    
    def get_telemetry(self, account_number, batch_size=1000, max_linger_ms=15000):
        """Get telemetry data from Starlink API."""
        try:
            self._ensure_token()
            
            response = requests.post(
                f"{self.base_url}/telemetry/stream/v1/telemetry",
                json={
                    "accountNumber": account_number,
                    "batchSize": batch_size,
                    "maxLingerMs": max_linger_ms
                },
                headers={
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'Authorization': f'Bearer {self.access_token}'
                }
            )
            
            if response.status_code == 401:
                # Token expired, clear it and retry
                self.access_token = None
                self.token_expiry = 0
                return self.get_telemetry(account_number, batch_size, max_linger_ms)
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Failed to get telemetry data: {str(e)}")
            return None
    
    def process_telemetry_data(self, telemetry_data):
        """Process telemetry data from Starlink API."""
        if not telemetry_data or 'data' not in telemetry_data:
            return None
        
        data = telemetry_data['data']
        metadata = telemetry_data.get('metadata', {})
        
        # Get column names by device type
        column_names_by_device_type = data.get('columnNamesByDeviceType', {})
        
        # Get values (rows of data)
        values = data.get('values', [])
        
        # Process each row of data
        processed_data = []
        for row in values:
            if not row or len(row) < 2:
                continue
            
            device_type = row[0]
            column_names = column_names_by_device_type.get(device_type, [])
            
            if not column_names or len(column_names) != len(row):
                continue
            
            # Create a dictionary for the row
            row_dict = {}
            for i, column_name in enumerate(column_names):
                row_dict[column_name] = row[i]
            
            processed_data.append(row_dict)
        
        return {
            'data': processed_data,
            'metadata': metadata
        }
    
    def get_user_terminal_telemetry(self, account_number):
        """Get user terminal telemetry data."""
        telemetry_data = self.get_telemetry(account_number)
        if not telemetry_data:
            return []
        
        processed_data = self.process_telemetry_data(telemetry_data)
        if not processed_data:
            return []
        
        # Filter for user terminal data
        user_terminal_data = [
            row for row in processed_data['data']
            if row.get('DeviceType') == 'u'
        ]
        
        return user_terminal_data
    
    def get_router_telemetry(self, account_number):
        """Get router telemetry data."""
        telemetry_data = self.get_telemetry(account_number)
        if not telemetry_data:
            return []
        
        processed_data = self.process_telemetry_data(telemetry_data)
        if not processed_data:
            return []
        
        # Filter for router data
        router_data = [
            row for row in processed_data['data']
            if row.get('DeviceType') == 'r'
        ]
        
        return router_data
    
    def get_ip_allocations(self, account_number):
        """Get IP allocation data."""
        telemetry_data = self.get_telemetry(account_number)
        if not telemetry_data:
            return []
        
        processed_data = self.process_telemetry_data(telemetry_data)
        if not processed_data:
            return []
        
        # Filter for IP allocation data
        ip_allocation_data = [
            row for row in processed_data['data']
            if row.get('DeviceType') == 'i'
        ]
        
        return ip_allocation_data

