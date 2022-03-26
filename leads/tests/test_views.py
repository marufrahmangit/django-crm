from django.test import TestCase
from django.shortcuts import reverse


class LandingPageTest(TestCase):

    # def test_status_code(self):
    #     response = self.client.get(reverse('landing-page'))
    #     self.assertEqual(response.status_code, 200)

    def test_get(self):
        response = self.client.get(reverse('landing-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="landing.html")

    # def test_template_name(self):
    #     # check the name of the template
    #     response = self.client.get(reverse('landing-page'))
    #     self.assertTemplateUsed(response, template_name="landing.html")

