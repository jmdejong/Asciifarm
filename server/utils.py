


def clamp(val, lower, upper):
    """ val if it's between lower and upper, else the closest of the two"""
    return min(max(val, lower), upper)
