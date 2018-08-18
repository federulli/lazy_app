from rest_framework import generics
from ..models import Torrent
from ..serializers import TorrentSerializer


class CreateTorrentView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Torrent.objects.all()
    serializer_class = TorrentSerializer
