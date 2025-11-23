from django.db.models import Q

def search(manager, search_value, search_fields):
    print(search_fields)
    print(search_value)
    if not search_value:
        return []
    query = Q()
    for field in search_fields:
        query |= Q(**{f"{field}__icontains" : search_value})
    return manager.filter(query).distinct()
    