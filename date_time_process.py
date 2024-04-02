from datetime import datetime, timedelta

def get_dates():
    # Get today's date
    today = datetime.today()
    # Calculate the date 3 months ago
    three_months_ago = today - timedelta(days=3*30)  # Assuming 30 days per month for simplicity
    return {
        "end" : today.strftime('%Y-%m-%d'),
        "start" : three_months_ago.strftime('%Y-%m-%d')
    }

def format_time(duration_minutes):
    hours = duration_minutes // 60
    minutes = duration_minutes % 60
    return f"{hours}h {minutes}m"
