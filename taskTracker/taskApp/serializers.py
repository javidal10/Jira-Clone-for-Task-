from rest_framework import serializers
from django.db.models import F
from .models import User, Project, Member, List, Issue, Assignee, Comment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignee
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    assignees = AssigneeSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'
    
    def same_container_reorder(self, issue_id, order, new_order, list_id):
        SameContainerReorderSerializer.reorder(Issue, issue_id, order, new_order, list_id)
    
    def diff_container_reorder(self, id, source_list_id, source_order, dest_list_id, new_order):
        try:
            ste = new_order > source_order
            if ste:
                Issue.objects.filter(list_id=source_list_id, order__gt=source_order).update(order=F('order') - 1)
                Issue.objects.filter(list_id=dest_list_id, order__gte=new_order).update(order=F('order') + 1)
            else:
                Issue.objects.filter(list_id=source_list_id, order__gte=source_order).update(order=F('order') + 1)
                Issue.objects.filter(list_id=dest_list_id, order__lt=new_order).update(order=F('order') - 1)
            Issue.objects.filter(id=id).update(list_id=dest_list_id, order=new_order)
        except Exception as e:
            print(e)


class ListSerializer(serializers.ModelSerializer):
    issues = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = '__all__'
    
    def same_container_reorder(self,issue_id, order, new_order, where_config, model):
        SameContainerReorderSerializer.reorder(Issue,issue_id, order, new_order, where_config, model)


class SameContainerReorderSerializer:
    @staticmethod
    def reorder(model, issue_id, order, new_order, list_id):
        try:
            ste = new_order > order
            if ste:
                model.objects.filter(list_id=list_id, order__gt=order, order__lte=new_order).update(order=F('order') - 1)
            else:
                model.objects.filter(list_id=list_id, order__lt=order, order__gte=new_order).update(order=F('order') + 1)
            model.objects.filter(id=issue_id).update(order=new_order)
        except Exception as e:
            print(e)


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True, read_only=True)
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.email
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email']