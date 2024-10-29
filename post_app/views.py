from django.shortcuts import render
from post_app.models import Posts
from post_app.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# 순서2 - url요청이 들어왔을때 요청의 HTTP방식을 확인해서 해당 방식에 맞는 DB 데이터(모델) 제어
@api_view(['GET', 'POST'])
def posts(request):

# 들어온 요청이 GET방식일때는 기존의 모델데이터를 JSON형태로 직렬화해서 프론트로 전달
  if request.method == 'GET':
    posts = Posts.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
  
  # 들어온 요청이 POST 방식일때는 클라이언트로부터 받은 데이터를 역직렬화해서 모델저장
  elif request.method == 'POST':
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)    

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)