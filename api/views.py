from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, CourseRegistration
from .serializers import CourseRegistrationSerializer, CourseSerializer, UserSerializer
from .permissions import IsAdminOrReadOnly, IsStudent
from .exceptions import NotFoundException
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,    
)

from .models import User


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)

class UserView(APIView):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    def get(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            courses = Course.objects.filter(courseregistration__user=user).distinct()
            serializer = CourseSerializer(courses, many=True, context={'request', request})
            return Response(serializer.data)
        except Exception as e:
            raise NotFoundException('No such user found.')

# Courses API
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    @action(detail=True, methods=["get"])
    def students(self, request, pk=None):
        serializer = User
        try:
            course = Course.objects.get(pk=pk)
            students =  User.objects.filter(courses__courseregistration__course_id=course.id).distinct()
            serializer = UserSerializer(students, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            raise NotFoundException('Course Not Found')


class CourseRegistrationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsStudent)
    queryset = CourseRegistration.objects.all()
    serializer_class = CourseRegistrationSerializer