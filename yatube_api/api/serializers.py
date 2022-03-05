from posts.models import Comment, Group, Post, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(many=True,
                                         allow_null=True,
                                         read_only=True,
                                         slug_field='posts')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')
        ref_name = 'ReadOnlyUsers'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'
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
        fields = '__all__'
        read_only_fields = ('author', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post', 'created',)
