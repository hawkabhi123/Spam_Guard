from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import User, Contact, SpamReport
from .serializers import UserSerializer, ContactSerializer, SpamReportSerializer
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ContactListView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SpamReportView(generics.CreateAPIView):
    serializer_class = SpamReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        phone_number = serializer.validated_data['phone_number']
       
        if SpamReport.objects.filter(phone_number=phone_number, reported_by=self.request.user).exists():
            self.response = Response({"detail": "You have already reported this number."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(reported_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if hasattr(self, 'response'):
            return self.response
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SearchByNameView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return User.objects.filter(
            Q(username__istartswith=query) | Q(username__icontains=query)
        ).annotate(
            spam_count=Count('spamreport')
        ).order_by('-spam_count')

class SearchByPhoneNumberView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        phone_number = self.request.query_params.get('phone_number', '')
        queryset = User.objects.filter(phone_number=phone_number).annotate(
            spam_count=Count('spamreport'))

        if queryset.exists():
            user = queryset.first()
            
            if not Contact.objects.filter(owner=self.request.user, phone_number=user.phone_number).exists():
                queryset = queryset.values('id', 'username', 'phone_number', 'spam_count')  
        return queryset
