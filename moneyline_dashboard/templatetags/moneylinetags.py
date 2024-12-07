from django import template

register = template.Library()

@register.filter
def as_percent(prob):
    return format(prob, ".2%")

@register.filter
def as_percent_return(prob):
    if prob > 0:
        return '+' + format(prob, ".2%")
    else:
        return format(prob, ".2%")

@register.filter
def positive_negative_color(value):
    if value > 0:
        return " #258e25"
    else:
        return "#cc3300"

@register.filter
def convert_to_american_odds(decimal_odds):

    if decimal_odds >= 2.0:
        american_odds = 100*(decimal_odds-1)
        extra_str = '+'
    else:
        american_odds = -100/(decimal_odds-1)
        extra_str = ''

    return extra_str + format(american_odds,".0f")
