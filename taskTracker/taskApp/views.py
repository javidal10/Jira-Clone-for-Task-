from datetime import timezone
from tokenize import Comment
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Count
from .models import Assignee, Issue, Member, Project, User, List
from .serializers import CommentSerializer, IssueSerializer, ListSerializer, MemberSerializer, ProjectSerializer, UserSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['POST'])
    def register(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('pwd')
            if User.objects.filter(email=email).exists():
                return Response({'message': 'User with this email already exists'}, status=status.HTTP_409_CONFLICT)
            user = User.objects.create_user(username=email, email=email, password=password)
            serialized_user = UserSerializer(user)
            return Response(serialized_user.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('pwd')
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response({'message': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
            
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
            return Response(data=data)

        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})

    @action(detail=False, methods=['PUT'])
    def change_password(self, request):
        try:
            user = request.user
            old_password = request.data.get('oldPwd')
            new_password = request.data.get('newPwd')
            if not user.check_password(old_password):
                return Response({'message': 'Old password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'})
        except Exception as e:
            print(e)
            return Response({'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        try:
            q = request.query_params.get('q', '')
            users = User.objects.filter(username__icontains=q)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'])
    def get_authenticated_user(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['PUT'])
    def update_authenticated_user(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'])
    def delete_authenticated_user(self, request):
        try:
            user = request.user
            password = request.data.get('pwd')
            if not check_password(password, user.password):
                return Response({'message': 'password is incorrect :('}, status=status.HTTP_401_UNAUTHORIZED)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, pk=None):
        try:
            print(pk)
            user = User.objects.filter(id=pk).first()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=['POST'])
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return self.queryset.filter(members__user_id=user_id)

    @action(detail=True, methods=['POST'])
    def leave_project(self, request, pk=None):
        project_id = pk
        user_id = request.data.get('user_id')
        member_id = request.data.get('member_id')

        try:
            member = Member.objects.get(id=member_id, project_id=project_id, user_id=user_id)
            assignees = Assignee.objects.filter(project_id=project_id, user_id=user_id)
            related_issues = Issue.objects.filter(list__project_id=project_id, user_id=user_id)

            member.delete()
            assignees.delete()
            related_issues.delete()

            return Response({'message': 'You left from this project successfully'})

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MemberViewSet(viewsets.ViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    @action(detail=True, methods=['POST'])
    def get_members_in_project(self, pk=None):
        try:
            project_id = pk
            members = self.queryset.objects.filter(project_id=project_id).order_by('created_at')
            serialized_members = self.serializer_class(members, many=True).data
            return Response(serialized_members)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def add_member(self, request, pk=None):
        try:
            project_id = pk
            user_id = request.data.get('user_id')
            member = Member.objects.create(user_id=user_id, project_id=project_id)
            project = Project.objects.get(id=project_id)
            project.updated_at = timezone.now()
            project.save()
            serialized_member = MemberSerializer(member).data
            return Response(serialized_member, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def remove_member(self, request, pk=None):
        try:
            project_id = pk
            member_id = request.data.get('member_id')
            user_id = request.data.get('user_id')

            Member.objects.filter(id=member_id, project_id=project_id, user_id=user_id).delete()
            Assignee.objects.filter(project_id=project_id, user_id=user_id).delete()

            project = Project.objects.get(id=project_id)
            project.updated_at = timezone.now()
            project.save()

            return Response({'message': 'Member removed successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ListViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['GET'])
    def get_lists_in_project(self, pk=None):
        try:
            project_id = pk
            lists = List.objects.filter(project_id=project_id).order_by('order')
            serialized_lists = ListSerializer(lists, many=True).data
            return Response(serialized_lists)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['POST'])
    def create_list(self, pk=None):
        try:
            project_id = pk
            order = List.objects.filter(project_id=project_id).count() + 1
            list_data = {'project_id': project_id, 'order': order}
            serializer = ListSerializer(data=list_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def update_list(self, request, pk=None):
        try:
            list_id = pk
            list_instance = List.objects.get(id=list_id)
            serializer = ListSerializer(list_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def delete_list(self, request, pk=None):
        try:
            list_id = pk
            List.objects.get(id=list_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def reorder_lists(self, request, pk=None):
        try:
            data = request.data
            list_id = data.get('id')
            order = data.get('order')
            new_order = data.get('newOrder')
            project_id = data.get('project_id')

            # Call the same_container_reorder function from the ListSerializer
            ListSerializer.same_container_reorder(list_id, order, new_order, project_id)
            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class IssueViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['POST'])
    def get_issues_in_project(self, request, project_id=None):
        try:
            user_id = request.query_params.get('userId', None)
            list_issues = Issue.objects.filter(list__project_id=project_id).order_by('list__order').annotate(
                comments_count=Count('comments')
            ).select_related('list').prefetch_related('assignees__user')

            if user_id:
                list_issues = list_issues.filter(assignees__user_id=user_id)

            issues_data = {}
            for issue in list_issues:
                list_id = issue.list_id
                issues_data.setdefault(list_id, []).append({
                    'id': issue.id,
                    'order': issue.order,
                    'priority': issue.priority,
                    'type': issue.type,
                    'summary': issue.summary,
                    'descr': issue.descr,
                    'created_at': issue.created_at,
                    'updated_at': issue.updated_at,
                    'comments_count': issue.comments_count,
                    'assignees': [{'id': assignee.user_id, 'username': assignee.user.username} for assignee in issue.assignees.all()]
                })

            return Response(issues_data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def create_issue(self, request, project_id=None):
        try:
            list_id = request.data.get('listId')
            assignees = request.data.get('assignees', [])
            order = Issue.objects.filter(list_id=list_id).count() + 1
            issue_data = {
                'list_id': list_id,
                'order': order,
                'priority': request.data.get('priority'),
                'type': request.data.get('type'),
                'summary': request.data.get('summary'),
                'descr': request.data.get('descr'),
            }
            issue_serializer = IssueSerializer(data=issue_data)
            if issue_serializer.is_valid():
                issue = issue_serializer.save()
                # create assignee rows with new issue id
                Assignee.objects.bulk_create([
                    Assignee(issue_id=issue.id, user_id=user_id, project_id=project_id)
                    for user_id in assignees
                ])
                return Response({'msg': 'Issue is created'}, status=status.HTTP_201_CREATED)
            else:
                return Response(issue_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def update_issue(self, request, pk=None):
        try:
            issue_id = pk
            update_type = request.data.get('type')
            value = request.data.get('value')
            project_id = request.data.get('projectId')

            if update_type == 'listId':
                list_issues = Issue.objects.filter(list_id=value)
                order = list_issues.count() + 1
                Issue.objects.filter(id=issue_id).update(list_id=value, order=order)
            elif update_type == 'addAssignee':
                Assignee.objects.create(issue_id=issue_id, user_id=value, project_id=project_id)
                self.updated_at(issue_id)
            elif update_type == 'removeAssignee':
                Assignee.objects.filter(issue_id=issue_id, user_id=value).delete()
                self.updated_at(issue_id)
            else:
                Issue.objects.filter(id=issue_id).update(**{update_type: value})

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def delete_issue(self, request, pk=None):
        try:
            issue_id = pk
            issue = Issue.objects.get(id=issue_id)
            issue.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def reorder_issues(self, request, pk=None):
        try:
            data = request.data
            issue_id = data.get('id')
            source_id = data['s']['sId']
            order = data['s']['order']
            dest_id = data['d']['dId']
            new_order = data['d']['newOrder']

            if source_id == dest_id:
                # Call the same_container_reorder function from the IssueSerializer
                IssueSerializer.same_container_reorder(issue_id, order, new_order, source_id)
            else:
                # Call the diff_container_reorder function from the IssueSerializer
                IssueSerializer.diff_container_reorder(data)

            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def updated_at(self, issue_id):
        try:
            Issue.objects.filter(id=issue_id).update(updated_at=timezone.now())
        except Exception as e:
            print(e)


class CommentViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['GET'])
    def get_comments(self, issue_id=None):
        try:
            comments = Comment.objects.filter(issue_id=issue_id)
            serialized_comments = CommentSerializer(comments, many=True).data
            return Response(serialized_comments)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def create_comment(self, request, issue_id=None):
        try:
            comment_data = { 'issue_id': issue_id, **request.data }
            serializer = CommentSerializer(data=comment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def delete_comment(self, request, comment_id=None):
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return Response({'message': 'The comment is deleted successfully'})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)