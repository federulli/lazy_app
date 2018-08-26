from rest_framework import generics
from django.http import JsonResponse
from ..tasks import (
    search_for_not_found_movies,
    search_for_not_found_chapters,
    download_subtitles,
)


class RefreshView(generics.GenericAPIView):
    TASK = {
        'MOVIE': search_for_not_found_movies,
        'TVSHOW': search_for_not_found_chapters,
        'SUBTITLES': download_subtitles,
    }

    def post(self, request):
        self.TASK[request.data['type']].delay()
        return JsonResponse(request.data)
