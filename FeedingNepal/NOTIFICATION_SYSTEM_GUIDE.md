# Donor Notification System Guide

## Overview
This system provides a complete notification solution for the Feeding Nepal donor management system. It allows the backend to send notifications to specific donors and provides a frontend interface for donors to view their notifications in real-time.

## System Components

### 1. Database (MySQL - "feed" database)
The system uses the existing `feed` database with the following key models:
- **Donor**: Contains donor information including ID, name, phone, email
- **Notification**: Stores notifications with donor association

### 2. API Endpoint
**URL**: `http://127.0.0.1:8000/donor/api/notification/`

#### GET Request - Retrieve Notifications
Fetches notifications for a specific donor.

**Parameters**:
- `donor_id` (optional): Donor ID in query parameter. If not provided, uses session donor_id

**Example**:
```bash
curl -X GET "http://127.0.0.1:8000/donor/api/notification/?donor_id=1"
```

**Response**:
```json
{
  "success": true,
  "donor_id": 1,
  "donor_name": "sudip sapkota",
  "notifications": [
    {
      "id": 9,
      "number": "9843996625",
      "gmail": "sudip@gmail.com",
      "message": "API Test notification from curl",
      "created_at": "2025-07-10T03:31:43+00:00",
      "donor_id": 1,
      "donor_name": "sudip sapkota"
    }
  ]
}
```

#### POST Request - Create Notification
Creates a new notification for a donor.

**Body** (JSON):
```json
{
  "donor_id": 1,
  "message": "Your donation has been confirmed!"
}
```

**Example**:
```bash
curl -X POST "http://127.0.0.1:8000/donor/api/notification/" \
  -H "Content-Type: application/json" \
  -d '{"donor_id": 1, "message": "Your donation has been confirmed!"}'
```

### 3. Frontend Integration
The notification page (`/donor/notification/`) includes:
- **Real-time updates**: Auto-refreshes every 30 seconds
- **Manual refresh**: Refresh button for immediate updates
- **Interactive UI**: Dismiss notifications, loading states, status messages

## Implementation Details

### Backend (Django)
1. **notification_api view**: Handles both GET and POST requests
2. **Session support**: Can work with session-based authentication
3. **Error handling**: Proper error responses with status codes
4. **Database queries**: Optimized queries for donor-specific notifications

### Frontend (HTML/JavaScript)
1. **Auto-refresh**: Polls the API every 30 seconds
2. **Manual controls**: Refresh button and dismiss functionality
3. **Status notifications**: User feedback for actions
4. **Responsive design**: Works on desktop and mobile

## Usage Examples

### 1. Checking Notifications for a Specific Donor
When a donor logs in, their notifications are automatically displayed based on their donor login ID.

### 2. Sending Notifications to Donors
From the admin panel or other parts of the system:

```python
# In Django views or management commands
from adminpanel.models import Notification
from donor.models import Donor

# Send notification to specific donor
donor = Donor.objects.get(id=1)
notification = Notification.objects.create(
    number=donor.phone,
    gmail=donor.email,
    role='donor',
    message='Your donation request has been approved!',
    donor=donor
)
```

### 3. API Integration for External Systems
External systems can send notifications via API:

```python
import requests

response = requests.post('http://127.0.0.1:8000/donor/api/notification/', 
    json={
        'donor_id': 1,
        'message': 'Volunteer has been assigned to your donation'
    },
    headers={'Content-Type': 'application/json'}
)
```

## Security Features
1. **CSRF exempt**: API endpoint is exempt from CSRF for external integrations
2. **Session authentication**: Uses Django session for logged-in users
3. **Donor verification**: Validates donor exists before creating notifications
4. **Input validation**: Validates required fields and JSON format

## Database Schema
The notification system uses the existing `adminpanel_notification` table:

```sql
CREATE TABLE adminpanel_notification (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number VARCHAR(20),
    gmail VARCHAR(254),
    role VARCHAR(20),
    message TEXT,
    donor_id INT,
    volunteer_id INT,
    created_at DATETIME,
    FOREIGN KEY (donor_id) REFERENCES donor_donor(id),
    FOREIGN KEY (volunteer_id) REFERENCES volunteer_volunteer(id)
);
```

## Testing the System

### 1. Start the Django Server
```bash
cd "/Users/sudipsapkota/Desktop/Feeding Nepal/FeedingNepal"
python manage.py runserver 8000
```

### 2. Test API Endpoints
```bash
# Get notifications for donor ID 1
curl -X GET "http://127.0.0.1:8000/donor/api/notification/?donor_id=1"

# Create a new notification
curl -X POST "http://127.0.0.1:8000/donor/api/notification/" \
  -H "Content-Type: application/json" \
  -d '{"donor_id": 1, "message": "Test notification"}'
```

### 3. Test Frontend
1. Navigate to `http://127.0.0.1:8000/donor/notification/`
2. Click "Refresh" to load notifications
3. Open browser console and run `createTestNotification()` to test creating notifications

## Troubleshooting

### Common Issues:
1. **500 Error**: Check Django logs for database connection issues
2. **403 Error**: Ensure CSRF exempt is working or include CSRF token
3. **404 Error**: Verify URL patterns and Django server is running
4. **No notifications showing**: Check donor_id parameter and database data

### Debug Commands:
```bash
# Check database connection
python manage.py shell -c "from donor.models import Donor; print(Donor.objects.all())"

# View all notifications
python manage.py shell -c "from adminpanel.models import Notification; print(list(Notification.objects.all()))"
```

## Future Enhancements
1. **Real-time WebSocket**: Replace polling with WebSocket for instant updates
2. **Push notifications**: Add browser push notifications
3. **Email integration**: Send email notifications
4. **SMS integration**: Send SMS notifications using the phone numbers
5. **Notification categories**: Add different types of notifications
6. **Mark as read**: Track read/unread status
7. **Bulk notifications**: Send notifications to multiple donors at once

## System Requirements
- Django 3.x or higher
- MySQL database named "feed"
- Modern web browser with JavaScript enabled
- Internet connection for Font Awesome icons
