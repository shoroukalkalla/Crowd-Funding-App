from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
import datetime

register = template.Library()

@register.filter
def currency(dollars):
    if dollars:
        dollars = round(float(dollars), 2)
  
        return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])
    else:
        return '$0'
        

@register.filter
def remaining_days(given_date):
    remaining = (given_date.date() - datetime.datetime.now().date() ).days
    return remaining


@register.filter
def as_percentage_of(part, whole):
    if part :
        try:
            result = (float(part) / whole * 100)
            return 100 if result > 100 else int(result)
        except (ValueError, ZeroDivisionError):
            return ""
    else:
        return "0"

