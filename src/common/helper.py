from decimal import Decimal


def json_serializer(obj: object):
    if isinstance(obj, Decimal):
        return float(obj)
