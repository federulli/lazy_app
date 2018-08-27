from rest_framework import generics
from django.http import JsonResponse
from ..models import Configuration


class ConfigurationView(generics.GenericAPIView):
    VALIDATIONS = {

    }

    def post(self, request):
        config_by_name = {config.name: config
                          for config in Configuration.objects.all()}
        for config, value in request.data.items():
            config_by_name[config].value = value
            config_by_name[config].save()

        return JsonResponse(request.data)

    def get(self, request):
        return JsonResponse(
            {config.name: config.value
             for config in Configuration.objects.all()}
        )
