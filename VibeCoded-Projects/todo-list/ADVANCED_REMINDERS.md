# Advanced Reminder System

## Overview
This document outlines enhancements to the reminder system with more sophisticated notification scheduling and background processing.

## Enhanced Backend Implementation

### 1. Background Task Scheduler

Create `scheduler.py`:

```python
import schedule
import time
import threading
from datetime import datetime, timedelta
from app import app, db, Task
import smtplib
from email.mime.text import MIMEText
import requests

class ReminderScheduler:
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_scheduler)
            self.thread.daemon = True
            self.thread.start()
            print("Reminder scheduler started")
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _run_scheduler(self):
        # Schedule checks every minute
        schedule.every(1).minutes.do(self.check_reminders)
        
        while self.running:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
    
    def check_reminders(self):
        with app.app_context():
            now = datetime.utcnow()
            upcoming_reminders = Task.query.filter(
                Task.reminder_time <= now + timedelta(minutes=1),
                Task.reminder_time > now - timedelta(minutes=1),
                Task.completed == False,
                Task.reminder_sent != True  # Add this field to track sent reminders
            ).all()
            
            for task in upcoming_reminders:
                self.send_reminder(task)
                task.reminder_sent = True
                db.session.commit()
    
    def send_reminder(self, task):
        # Send web push notification
        self.send_web_push(task)
        
        # Send email notification (optional)
        # self.send_email_reminder(task)
        
        # Send webhook notification (for integrations)
        # self.send_webhook(task)
    
    def send_web_push(self, task):
        # Implementation for web push notifications
        # This would integrate with services like Firebase Cloud Messaging
        pass
    
    def send_email_reminder(self, task):
        # Email reminder implementation
        pass

# Initialize scheduler
scheduler = ReminderScheduler()
```

### 2. Web Push Notifications

Add to `app.py`:

```python
from pywebpush import webpush, WebPushException
import json

# Add these routes to app.py

@app.route('/api/subscribe', methods=['POST'])
def subscribe_to_notifications():
    subscription = request.get_json()
    
    # Store subscription in database
    # You'd create a Subscription model to store these
    
    return jsonify({'success': True})

@app.route('/api/send-notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    
    try:
        # Send web push notification
        webpush(
            subscription_info=data['subscription'],
            data=json.dumps({
                'title': 'Task Reminder',
                'body': data['message'],
                'icon': '/static/icon-192.png',
                'badge': '/static/icon-72.png'
            }),
            vapid_private_key="your-vapid-private-key",
            vapid_claims={
                "sub": "mailto:your-email@example.com"
            }
        )
        return jsonify({'success': True})
    except WebPushException as ex:
        return jsonify({'error': str(ex)}), 400
```

### 3. Enhanced Frontend Notifications

Create `static/notifications.js`:

```javascript
class NotificationManager {
    constructor() {
        this.registration = null;
        this.subscription = null;
    }
    
    async init() {
        if ('serviceWorker' in navigator && 'PushManager' in window) {
            try {
                this.registration = await navigator.serviceWorker.register('/static/sw.js');
                await this.setupPushNotifications();
            } catch (error) {
                console.error('Service Worker registration failed:', error);
            }
        }
    }
    
    async setupPushNotifications() {
        const permission = await Notification.requestPermission();
        
        if (permission === 'granted') {
            try {
                this.subscription = await this.registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: this.urlBase64ToUint8Array('YOUR_VAPID_PUBLIC_KEY')
                });
                
                // Send subscription to server
                await fetch('/api/subscribe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.subscription)
                });
            } catch (error) {
                console.error('Push subscription failed:', error);
            }
        }
    }
    
    urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/-/g, '+')
            .replace(/_/g, '/');
            
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }
    
    async scheduleLocalReminder(task) {
        if ('serviceWorker' in navigator && this.registration) {
            const reminderTime = new Date(task.reminder_time);
            const now = new Date();
            const delay = reminderTime.getTime() - now.getTime();
            
            if (delay > 0) {
                // Schedule using setTimeout for near-term reminders
                if (delay < 24 * 60 * 60 * 1000) { // Less than 24 hours
                    setTimeout(() => {
                        this.showLocalNotification(task);
                    }, delay);
                }
            }
        }
    }
    
    showLocalNotification(task) {
        if (Notification.permission === 'granted') {
            const notification = new Notification('Task Reminder', {
                body: `Don't forget: ${task.title}`,
                icon: '/static/icon-192.png',
                badge: '/static/icon-72.png',
                tag: `task-${task.id}`,
                data: { taskId: task.id },
                actions: [
                    {
                        action: 'complete',
                        title: 'Mark Complete'
                    },
                    {
                        action: 'snooze',
                        title: 'Snooze 10min'
                    }
                ]
            });
            
            notification.onclick = () => {
                window.focus();
                // Navigate to task
                const taskElement = document.querySelector(`[data-task-id="${task.id}"]`);
                if (taskElement) {
                    taskElement.scrollIntoView({ behavior: 'smooth' });
                }
            };
        }
    }
}

// Initialize notification manager
const notificationManager = new NotificationManager();
```

### 4. Advanced Reminder Features

Add to task model and UI:

```python
# Add to Task model in app.py
class Task(db.Model):
    # ... existing fields ...
    reminder_sent = db.Column(db.Boolean, default=False)
    snooze_count = db.Column(db.Integer, default=0)
    recurrence_rule = db.Column(db.String(100))  # For recurring reminders
    
    def get_next_reminder(self):
        """Calculate next reminder time for recurring tasks"""
        if self.recurrence_rule and self.reminder_time:
            # Parse recurrence rule (daily, weekly, monthly)
            # Return next occurrence
            pass
```

### 5. Reminder Templates and Customization

```javascript
// Add to frontend
const reminderTemplates = {
    urgent: {
        title: '🚨 Urgent Task Reminder',
        sound: 'urgent-alert.mp3',
        vibrate: [200, 100, 200]
    },
    normal: {
        title: '📋 Task Reminder',
        sound: 'gentle-chime.mp3',
        vibrate: [100]
    },
    gentle: {
        title: '💭 Gentle Reminder',
        sound: 'soft-ping.mp3',
        vibrate: [50]
    }
};

function createCustomReminder(task, template = 'normal') {
    const config = reminderTemplates[template];
    
    return new Notification(config.title, {
        body: task.title,
        icon: `/static/priority-${task.priority}.png`,
        sound: `/static/sounds/${config.sound}`,
        vibrate: config.vibrate,
        tag: `task-${task.id}-${template}`
    });
}
```

## Additional Features

### 1. Smart Reminder Timing
- Machine learning to suggest optimal reminder times
- Consider user's active hours and task completion patterns
- Adaptive snoozing based on user behavior

### 2. Multiple Reminder Channels
- Browser notifications
- Email reminders
- SMS notifications (via Twilio)
- Slack/Discord webhook integrations
- Desktop notifications (Electron app)

### 3. Reminder Escalation
- Multiple reminders with increasing urgency
- Escalate to different channels if not acknowledged
- Smart snoozing with decreasing intervals

### 4. Team Reminders
- Assign tasks to team members
- Reminder delegation and escalation
- Group notifications for shared deadlines

## Installation Requirements

```bash
pip install schedule pywebpush APScheduler celery redis
```

## Configuration

1. Set up VAPID keys for web push notifications
2. Configure email SMTP settings
3. Set up background task queue (Celery + Redis)
4. Configure webhook endpoints for integrations

This enhanced reminder system provides enterprise-level notification capabilities while maintaining simplicity for individual users.
