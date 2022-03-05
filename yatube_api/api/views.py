from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Comment, Group, Post, User
from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, GroupSerializer, PostSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for working with User objects. Information about each
    user is not changable.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class APIGroupList(APIView):
    """
    Displays a list of all groups on the social net.
    """
    def get(self, request):
        """
        Displays a list of all groups on the social net.
        """
        if request.method == 'GET':
            groups = Group.objects.all()
            serializer = GroupSerializer(groups, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIGroup(APIView):
    """
    Displays a current group.
    """

    def get(self, request, pk):
        """
        Displays a current group from the social net.
        """
        if request.method == 'GET':
            current_group = get_object_or_404(Group, id=pk)
            serializer = GroupSerializer(current_group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    """
    Allowed requests: GET, POST. Get a list of all the posts all over the
    social net or create a new one.
    Also:
    Allowed requests: GET, PUT, PATCH, DELETE. Getting, editing or deleting
    exact post by its id.
    """
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """
        The function gets user's data and input it in data for creating
        posts as an author'd identity.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset for CRUD (GET, PUT, PATCH, DELETE) of a requested Comment objects.
    Allowed requests: GET, POST. Get a list of all the comments or create a
    new one which are related to the chosen post.
    Also:
    Allowed requests: GET, PUT, PATCH, DELETE. Getting, editing or deleting
    a requested Comment object of the chosen post by its id.
    """
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Returns new queryset by exact id post."""
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        """
        The function gets user's data and input it in data for creating
        comments as an author's identity.
        """
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)
        return post.comments.all()
