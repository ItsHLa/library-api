from django.db.models import Q
class SearchAndFilteration:
    
    @staticmethod
    def search(manager, search_value, search_fields):
        print(search_fields)
        if not search_value:
            return manager.none()
        query = Q()
        for field in search_fields:
            query |= Q(**{f"{field}__icontains" : search_value})
        return manager.filter(query)