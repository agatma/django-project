from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import Client, TestCase
from posts.models import Follow
from posts.tests.set_up_tests import UserLocators
from posts.tests.set_up_tests import PostLocators, PostTestSetUpMixin

User = get_user_model()


class PostModelTest(PostTestSetUpMixin):
    def setUp(self):
        self.post = PostModelTest.post

    def test_post_models_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        self.assertEqual(
            str(self.post), self.post.text[:settings.POST_SYMBOLS],
        )

    def test_post_models_have_correct_verbose_names(self):
        field_verbose = {
            'text': PostLocators.TEXT_VERBOSE,
            'pub_date': PostLocators.PUB_DATE_VERBOSE,
            'author': PostLocators.AUTHOR_VERBOSE_AND_HELP,
            'group': PostLocators.GROUP_VERBOSE,
        }
        self.check_correct_meta(field_verbose, verbose=True)

    def test_post_models_have_correct_help_text(self):
        field_help_text = {
            'text': PostLocators.TEXT_HELP_TEXT,
            'pub_date': PostLocators.PUB_DATE_HELP_TEXT,
            'author': PostLocators.AUTHOR_VERBOSE_AND_HELP,
            'group': PostLocators.GROUP_HELP_TEXT,
        }
        self.check_correct_meta(field_help_text, help_text=True)


class GroupModelTest(PostTestSetUpMixin):
    def test_group_models_have_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = GroupModelTest.group
        self.assertEqual(str(group), group.title, )


class CommentModelTest(PostTestSetUpMixin):
    def test_comment_models_have_correct_object_names(self):
        """Проверяем, что у модели Comment корректно работает __str__."""
        comment = GroupModelTest.comment
        self.assertEqual(str(comment), comment.text[:settings.POST_SYMBOLS], )


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username=UserLocators.USERNAME
        )
        cls.user_author = User.objects.create_user(
            username=UserLocators.USERNAME2
        )
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.user_author,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_comment_models_have_correct_object_names(self):
        """Проверяем, что у модели Follow корректно работает __str__."""
        follow = self.follow
        result = f'user - {self.user} author - {self.user_author}'
        self.assertEqual(str(follow), result, )
