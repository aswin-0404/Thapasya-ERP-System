from firebase_admin import messaging
from typing import List

def send_push_notification(tokens: List[str], title: str, body: str, data: dict = None):

    if not tokens:
        return None
        
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        tokens=tokens,
    )
    
    response = messaging.send_each_for_multicast(message)
    
    print(f"FCM: Successfully sent {response.success_count} messages.")
    return response