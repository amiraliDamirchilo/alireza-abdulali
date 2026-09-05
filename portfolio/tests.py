from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import Inquiry, Project, Service, SiteText, WorkCategory


class PortfolioTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("portfolio:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "MOTION")

    def test_public_pages_render(self):
        for route_name in ("work", "about", "services", "contact"):
            with self.subTest(route=route_name):
                response = self.client.get(reverse(f"portfolio:{route_name}"))
                self.assertEqual(response.status_code, 302)

    def test_navigation_uses_real_routes(self):
        response = self.client.get(reverse("portfolio:home"))
        self.assertContains(response, 'href="#work"')
        self.assertContains(response, 'href="#about"')
        self.assertContains(response, 'href="#services"')
        self.assertContains(response, 'href="#contact"')
        self.assertNotContains(response, "scroll-map")

    def test_gsap_is_loaded(self):
        response = self.client.get(reverse("portfolio:home"))
        self.assertContains(response, "gsap.min.js")

    def test_admin_project_appears_on_work_page(self):
        category = WorkCategory.objects.get(slug="motion")
        Project.objects.create(title_en="Test Film", title_fa="فیلم تست", slug="test-film", category=category, video_url="https://youtu.be/dQw4w9WgXcQ")
        response = self.client.get(reverse("portfolio:home"))
        self.assertContains(response, "Test Film")
        self.assertContains(response, "youtube-nocookie.com/embed/dQw4w9WgXcQ")

    def test_youtube_url_formats_are_embedded(self):
        self.assertEqual(Project.youtube_video_id("https://www.youtube.com/watch?v=abc123"), "abc123")
        self.assertEqual(Project.youtube_video_id("https://youtube.com/shorts/abc123"), "abc123")

    def test_admin_managed_copy_is_sent_to_the_public_page(self):
        text = SiteText.objects.get(key="heroTitleOne")
        text.text_en = "STORIES"
        text.save()
        response = self.client.get(reverse("portfolio:home"))
        self.assertContains(response, "STORIES")
        self.assertContains(response, 'id="site-copy-data"')

    def test_site_text_character_limit_protects_layout(self):
        text = SiteText.objects.get(key="heroTitleOne")
        text.text_en = "X" * (text.character_limit + 1)
        with self.assertRaises(ValidationError):
            text.full_clean()

    def test_service_cards_are_admin_managed(self):
        self.assertEqual(Service.objects.count(), 4)
        Service.objects.create(
            title_en="Sound design", title_fa="طراحی صدا", slug="sound-design",
            description_en="Sound with a clear narrative purpose.",
            description_fa="صدا با هدف روایی روشن.", order=50,
        )
        response = self.client.get(reverse("portfolio:home"))
        self.assertContains(response, "Sound design")
        self.assertContains(response, "طراحی صدا")

    def test_ajax_inquiry_is_saved(self):
        response = self.client.post(
            reverse("portfolio:submit_inquiry"),
            {
                "name": "Alex",
                "email": "alex@example.com",
                "company": "Vanta",
                "service": "motion",
                "budget": "$3k — $7k",
                "message": "We need a kinetic launch film.",
                "website": "",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertEqual(Inquiry.objects.count(), 1)

    def test_honeypot_rejects_spam(self):
        response = self.client.post(
            reverse("portfolio:submit_inquiry"),
            {
                "name": "Bot",
                "email": "bot@example.com",
                "service": "other",
                "message": "Spam",
                "website": "https://spam.example",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_non_ajax_inquiry_redirects_to_contact(self):
        response = self.client.post(
            reverse("portfolio:submit_inquiry"),
            {
                "name": "Alex",
                "email": "alex@example.com",
                "service": "motion",
                "message": "A multi-page portfolio project.",
                "website": "",
            },
        )
        self.assertRedirects(response, "/?sent=1#contact", fetch_redirect_response=False)
