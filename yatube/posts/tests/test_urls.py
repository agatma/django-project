from http import HTTPStatus
from django.test import Client
from posts.tests.set_up_tests import PostTestSetUpMixin, PostPagesLocators


class PostURLTests(PostTestSetUpMixin):
    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.response_404 = HTTPStatus.NOT_FOUND
        self.response_200 = HTTPStatus.OK
        self.response_302 = HTTPStatus.FOUND

    def test_post_urls_for_guest_exists_at_desired_location(self):
        """Проверяем общедоступные страницы."""
        self.check_url_response(PostPagesLocators.GUEST_PAGES)

    def test_post_urls_for_user_exists_at_desired_location(self):
        """Проверяем доступность страницы создания и редактирования поста"""
        self.check_url_response(
            PostPagesLocators.CREATE_EDIT_PAGES, authorized=True
        )

    def test_post_urls_404_page_exists_at_desired_location(self):
        """Проверяем неизвестный адрес, который должен вернуть 404 статус."""
        response = self.guest_client.get(PostPagesLocators.PAGE_404)
        self.assertEqual(
            response.status_code,
            self.response_404,
        )

    def test_post_urls_authorized_client_uses_correct_template(self):
        """URL-адрес страниц для авторизованного пользователя
        в urls использует соответствующий шаблон."""
        for template, url in PostPagesLocators.templates_url_names:
            with self.subTest(url=url):
                response_authorized = self.authorized_client.get(url)
                self.assertTemplateUsed(response_authorized, template)

    def test_post_urls_guest_client_uses_correct_template(self):
        """URL-адрес страниц для неавторизованного пользователя
        в urls использует соответствующий шаблон."""
        for template, url in PostPagesLocators.templates_url_name_guest:
            with self.subTest(url=url):
                response_guest = self.guest_client.get(url)
                self.assertTemplateUsed(response_guest, template, )

    def test_post_urls_for_user_redirect_anonymous_on_login(self):
        """Редирект страниц для неавторизованного пользователя
        post_create, post_edit, follow_index, follow, unfollow, ."""
        self.check_url_response(
            PostPagesLocators.REDIRECT_PAGES, redirect=True
        )
