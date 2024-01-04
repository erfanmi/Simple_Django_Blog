from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from django.shortcuts import reverse


class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_user')
        cls.post1 = Post.objects.create(
            title="test title",
            author=cls.user,
            text="test text",
            status=Post.STATUS_CHOICES[0][0],
        )
        cls.post2 = Post.objects.create(
            title="test draft title",
            author=cls.user,
            text="test text draft",
            status=Post.STATUS_CHOICES[1][0],
        )

    def test_post_str(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_post_list_by_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_title_on_blog_page(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)

    def test_post_detail_by_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_details(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_status_404_if_post_does_not_exist(self):
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_not_showing_draft(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'post title',
            'text': 'some text here',
            'status': 'pub',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'post title')
        self.assertEqual(Post.objects.last().text, 'some text here')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id]), {
            'title': 'title updated',
            'text': 'text.updated',
            'status': 'pub',
            'author': self.post2.author.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'title updated')
        self.assertEqual(Post.objects.last().text, 'text.updated')

    def test_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post1.id]))
        self.assertEqual(response.status_code, 302)


