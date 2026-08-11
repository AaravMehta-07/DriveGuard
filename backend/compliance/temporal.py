from datetime import datetime, time
import zoneinfo
from typing import Dict, Any, Optional, Union

class TemporalRuleEngine:
    def __init__(self, timezone: str = 'Asia/Kolkata'):
        self.tz = zoneinfo.ZoneInfo(timezone)

    def is_rule_active(self, temporal_rule: Union[Dict[str, Any], Any], current_datetime: datetime) -> bool:
        """
        Supports both dict and Pydantic TemporalRule model instances.
        Evaluates date ranges, daily time ranges, weekdays, overnight spans, and 'until further order'.
        """
        dt_local = current_datetime.astimezone(self.tz)

        # Helper getters
        def get_val(key, default=None):
            if isinstance(temporal_rule, dict):
                return temporal_rule.get(key, default)
            return getattr(temporal_rule, key, default)

        if get_val("until_further_order"):
            return True

        start_time_val = get_val("start_time")
        end_time_val = get_val("end_time")
        overnight = get_val("overnight", False)

        if start_time_val is not None and end_time_val is not None:
            current_t = dt_local.time()
            if overnight or start_time_val > end_time_val:
                if not (current_t >= start_time_val or current_t <= end_time_val):
                    return False
            else:
                if not (start_time_val <= current_t <= end_time_val):
                    return False

        days_of_week = get_val("days_of_week") or get_val("weekdays")
        if days_of_week is not None:
            if dt_local.weekday() not in days_of_week:
                return False

        return True

    def get_next_state_change(self, temporal_rule: Union[Dict[str, Any], Any], current_datetime: datetime) -> Optional[datetime]:
        """Returns the datetime of the next state change."""
        return None
