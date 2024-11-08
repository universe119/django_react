from django.shortcuts import render
from post_app.models import Posts
from post_app.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q

# 순서2 - url요청이 들어왔을때 요청의 HTTP방식을 확인해서 해당 방식에 맞는 DB 데이터(모델) 제어
@api_view(['GET', 'POST'])
def posts(request):

# 들어온 요청이 GET방식일때는 기존의 모델데이터를 JSON형태로 직렬화해서 프론트로 전달
  if request.method == 'GET':
    posts = Posts.objects.all().order_by("-id")
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
  
  # 들어온 요청이 POST 방식일때는 클라이언트로부터 받은 데이터를 역직렬화해서 모델저장
  elif request.method == 'POST':
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)    

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
# 상세페이지에서 요청받을 GET, PUT, DELETE요청처럼 함수 추가
@api_view(['GET','PUT','DELETE'])
def posts_detail(request, slug):
  # 자바스크립트에 트라이캐칭이라하고 파이썬에선 트라이익셉트
  # 파라미터로 같이 전달된 slug에 매칭되는 모델 데이터를 찾음
  try:
    post = Posts.objects.get(slug=slug)
  # 만약 매칭되는 데이터가 없으면 404에러 반환
  except Posts.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  # 요청 방식이 'GET'이면 찾아놓은 모델데이터를 직렬화해서 클라이언트 응답처리
  if request.method=='GET':
    serializer = PostSerializer(post)
    return Response(serializer.data)
  
  # 요청 방식이 'PUT'이면 찾아놓은 모델데이터를 수정해서 다시 저장
  elif request.method=='PUT':
    # 클라이언트로부터 전달받은 데이터를 반영해서 기존 모델 구조를 변경한뒤 다시 역직렬화
    serializer = PostSerializer(post, data=request.data)

    # 유효성 검사에 성공하면
    if serializer.is_valid():
      # 모델에 저장 성공 응답 반환
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    # 수정 실패하면 실패 응답 반환
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  # 요청 방식이 'DELETE'이면 찾아놓은 모델데이터를 DB 테이블에서 제거, 제거응답 상태 전송
  elif request.method=='DELETE':
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def posts_search(request):
  # 프론트쪽 url요청시 search란 항목의 params 쿼리정보 가져옴
  query = request.query_params.get("search")
  
  # Q메서드를 이용해 title필드에서 대소문자 구분없이 query가 포함된 문자값이 있으면 true반환 없으면 false반환
  # 아래 코드 해석 클라이언트로부터 전달된 쿼리정보가 title필드 항목에 있거나 혹은 body필드 항목에 있거나 혹은 category필드 항목에 매칭되는게 하나라도 있으면 해당 모델을 모두 필터링해서 반환
  posts = Posts.objects.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(category__icontains=query))
  
  serializer = PostSerializer(posts, many=True)
  
  return Response(serializer.data, status=status.HTTP_200_OK)