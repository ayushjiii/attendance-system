from django import template

register = template.Library()

@register.filter
def format_hours(value):
    """
    Converts decimal hours to human readable format.
    0.75 -> '45 min'
    4.75 -> '4 hr 45 min'
    4.0  -> '4 hr'
    """
    if not value:
        return '-'
    
    try:
        total_minutes = round(float(value) * 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60

        if hours == 0:
            return f'{minutes} min'
        elif minutes == 0:
            return f'{hours} hr'
        else:
            return f'{hours} hr {minutes} min'
    except (ValueError, TypeError):
        return '-'