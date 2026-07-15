import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods

from practice.models import Item


@require_GET
def health(request):
    return JsonResponse({'status': 'ok', 'service': 'django', 'framework': 'Django'})


@require_http_methods(['POST'])
def create_item(request):
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'detail': 'Request body must be valid JSON.'}, status=400)

    name = payload.get('name')
    if not isinstance(name, str) or not name.strip():
        return JsonResponse({'detail': 'name is required.'}, status=400)

    item = Item.objects.create(name=name.strip())
    return JsonResponse(
        {
            'id': item.pk,
            'name': item.name,
            'created_at': item.created_at.isoformat(),
        },
        status=201,
    )


@require_GET
def read_item(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        return JsonResponse({'detail': 'Item not found.'}, status=404)

    return JsonResponse(
        {
            'id': item.pk,
            'name': item.name,
            'created_at': item.created_at.isoformat(),
        },
    )
