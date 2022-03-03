from posts.models import Comment, Group, Post, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')
        ref_name = 'ReadOnlyUsers'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = ('slug',)

    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError(
                'Заголовок не должен совпадать с описанием группы.'
            )
        return data


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(),
                                               required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date',)
        read_only_fields = ('author', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post', 'created',)
