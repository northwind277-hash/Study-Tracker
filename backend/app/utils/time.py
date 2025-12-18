from datetime import date, datetime, timedelta
from typing import Optional


def get_today() -> date:
    """获取今天的日期"""
    return date.today()


def get_week_start(date_val: Optional[date] = None) -> date:
    """获取指定日期所在周的开始日期（周一）"""
    if date_val is None:
        date_val = get_today()
    
    # 获取星期几（0-6，周一=0，周日=6）
    weekday = date_val.weekday()
    
    # 计算周一的日期
    return date_val - timedelta(days=weekday)


def get_week_end(date_val: Optional[date] = None) -> date:
    """获取指定日期所在周的结束日期（周日）"""
    if date_val is None:
        date_val = get_today()
    
    # 获取星期几（0-6，周一=0，周日=6）
    weekday = date_val.weekday()
    
    # 计算周日的日期
    return date_val + timedelta(days=6 - weekday)


def get_month_start(date_val: Optional[date] = None) -> date:
    """获取指定日期所在月的开始日期"""
    if date_val is None:
        date_val = get_today()
    
    return date(date_val.year, date_val.month, 1)


def get_month_end(date_val: Optional[date] = None) -> date:
    """获取指定日期所在月的结束日期"""
    if date_val is None:
        date_val = get_today()
    
    # 计算下一个月的第一天
    if date_val.month == 12:
        next_month = date(date_val.year + 1, 1, 1)
    else:
        next_month = date(date_val.year, date_val.month + 1, 1)
    
    # 本月最后一天是下个月第一天减一天
    return next_month - timedelta(days=1)


def format_duration(minutes: int) -> str:
    """将分钟数格式化为小时和分钟的字符串"""
    hours = minutes // 60
    mins = minutes % 60
    
    if hours > 0:
        return f"{hours}小时{mins}分钟"
    else:
        return f"{mins}分钟"


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> date:
    """将字符串解析为日期对象"""
    return datetime.strptime(date_str, format_str).date()


def format_date(date_val: date, format_str: str = "%Y-%m-%d") -> str:
    """将日期对象格式化为字符串"""
    return date_val.strftime(format_str)


def get_date_range(days: int) -> tuple[date, date]:
    """获取过去N天的日期范围（包括今天）"""
    end_date = get_today()
    start_date = end_date - timedelta(days=days - 1)
    return start_date, end_date
