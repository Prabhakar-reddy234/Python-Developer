from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests

# Account View
class AccountListCreateView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

# Destination View
class DestinationListCreateView(ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

# Incoming Data Handler
class IncomingDataHandler(APIView):
    def post(self, request):
        # Check for app secret token in header
        app_secret_token = request.headers.get('CL-X-TOKEN')
        if not app_secret_token:
            return Response({'error': 'Un Authenticate'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get account by secret token
        try:
            account = Account.objects.get(app_secret_token=app_secret_token)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get JSON data
        data = request.data
        if not isinstance(data, dict):
            return Response({'error': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)

        # Send data to all destinations of the account
        errors = []
        for destination in account.destinations.all():
            headers = destination.headers
            method = destination.http_method
            url = destination.url

            # Send data based on HTTP method
            try:
                if method == 'GET':
                    response = requests.get(url, headers=headers, params=data)
                elif method == 'POST':
                    response = requests.post(url, headers=headers, json=data)
                elif method == 'PUT':
                    response = requests.put(url, headers=headers, json=data)
                elif method == 'DELETE':
                    response = requests.delete(url, headers=headers)

                # Check if the destination responded successfully
                if response.status_code not in range(200, 300):
                    errors.append(f'Failed to send to {url} (status code: {response.status_code})')

            except Exception as e:
                errors.append(f'Failed to send to {url}: {str(e)}')

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'Data pushed successfully'}, status=status.HTTP_200_OK)
