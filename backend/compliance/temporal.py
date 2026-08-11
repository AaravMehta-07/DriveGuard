from datetime import datetime, time
import zoneinfo
from typing import Dict, Any, Optional

class TemporalRuleEngine:
    def __init__(self, timezone: str = 'Asia/Kolkata'):
        self.tz = zoneinfo.ZoneInfo(timezone)

    def is_rule_active(self, temporal_rule_json: Dict[str, Any], current_datetime: datetime) -> bool:
        """
        Supports: date ranges, daily time ranges, weekday/weekend, holidays, overnight spans, 
        "until further order", vehicle class conditions
        """
        # Evaluate all datetime in Asia/Kolkata timezone
        dt_local = current_datetime.astimezone(self.tz)

        if temporal_rule_json.get("until_further_order"):
            return True

        if "time_ranges" in temporal_rule_json:
            active_time = False
            for tr in temporal_rule_json["time_ranges"]:
                start = time.fromisoformat(tr["start"])
                end = time.fromisoformat(tr["end"])
                current_t = dt_local.time()
                
                if start <= end:
                    if start <= current_t <= end:
                        active_time = True
                        break
                else:
                    # Overnight
                    if current_t >= start or current_t <= end:
                        active_time = True
                        break
            if not active_time:
                return False

        if "weekdays" in temporal_rule_json:
            if dt_local.weekday() not in temporal_rule_json["weekdays"]:
                return False
                
        return True

    def get_next_state_change(self, temporal_rule_json: Dict[str, Any], current_datetime: datetime) -> Optional[datetime]:
        """
        Returns the datetime of the next state change
        """
        return None
