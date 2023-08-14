from .models import *
from .serializers import *

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from django.contrib.auth import authenticate
from django.core.paginator import Paginator

# Create your views here.

@api_view(['GET','POST','PUT' ])
def index(request):
    courses={
            'course_name':"python",
            'learn':['flask','Django','FastAPI'],
            'course_provider':"Scalar"
        }
    if request.method=='GET':
        print(request.GET.get('search')) 
        print("**GET**")
        return Response(courses,status=status.HTTP_202_ACCEPTED)
    elif request.method=='POST':
        
        data=request.data
        print(data)
        print("**POST**")
        return Response(courses)
    elif request.method=='PUT':
        print("**PUT**")
        return Response(courses,status=status.HTTP_202_ACCEPTED)


@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method=='GET':
        objs=Person.objects.filter(color__isnull=False)
        serializer =PeopleSerializer(objs,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors )
    elif request.method=='PUT':
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors )
    elif request.method=='PATCH':
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=PeopleSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors )
    else:
        data=request.data
        print("**delete**")
        obj=Person.objects.get(id=data['id'])
        obj.delete()
        return Response({"message":"Person deleted"})
    
@api_view(['POST'])
def login(request):
    data=request.data
    serializer=LoginSerializer(data=data)
    if serializer.is_valid():
        data=serializer.validated_data
        #do something
        return Response({"message":"Success"})
    return Response(serializer.errors)


class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    def get(self,request):
        try:
            objs=Person.objects.filter(color__isnull=False)
            # objs=Person.objects.all()
            page=request.GET.get('page',1)
            page_size=2
            paginator=Paginator(objs,page_size)
            
            # serializer =PeopleSerializer(objs,many=True)
            serializer =PeopleSerializer(paginator.page(page),many=True)
            print(request.user)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'status':False,
                'message':'Invalid page'
            })
    def post(self,request):
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors )
    def put(self,request):
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors )
    def patch(self,request):
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=PeopleSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors )
    def delete(self,request):
        data=request.data
        obj=Person.objects.get(id=data['id'])
        obj.delete()
        return Response({"message":"Person deleted"})
    
    
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class=PeopleSerializer
    print(Person.objects.get(id=4))
    if Person.objects.all().exists():   
        queryset=Person.objects.all()
        
    def list(self,request):
        search=request.GET.get('search')
        queryset=self.queryset
        if search:
            queryset=queryset.filter(name__startswith=search)
        serializer=PeopleSerializer(queryset,many=True)
        return Response({'status':200,'data':serializer.data},status=status.HTTP_202_ACCEPTED)
    
class RegisterAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
            'status':False,
            'message':serializer.errors,

            },status.HTTP_400_BAD_REQUEST)
            
        serializer.save()
        return Response({
            'status':True,
            'message':"User created"
        },status.HTTP_201_CREATED)

class LoginAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
            'status':False,
            'message':serializer.errors,

            },status.HTTP_400_BAD_REQUEST)
        user=authenticate(username=serializer.data['username'],password=serializer.data['password'])
        
        if not user:
            return Response({
                'status':False,
                'message':"Invalid credentials",

            },status.HTTP_400_BAD_REQUEST)
        
        token,_=Token.objects.get_or_create(user=user)
        return Response({
            'status':True,
            'message':"usr login",
            'token':str(token)
        },status=status.HTTP_202_ACCEPTED)



