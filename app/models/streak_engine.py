from datetime import date, timedelta

def update_streak(streak_obj):
    today = date.today()

    if streak_obj.last_action_date is None:
        streak_obj.current_streak = 1
        streak_obj.last_action_date = today
        return streak_obj.current_streak

    if streak_obj.last_action_date == today:
        return streak_obj.current_streak

    if streak_obj.last_action_date == today - timedelta(days=1):
        streak_obj.current_streak += 1
    else:
        streak_obj.current_streak = 1

    streak_obj.last_action_date = today
    return streak_obj.current_streak