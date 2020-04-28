from django.test import TestCase
from .models import Item


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': '신규 작업 아이템'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')


    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': '신규 작업 아이템'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)



class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "첫 번째 아이템"
        first_item.save()

        second_item = Item()
        second_item.text = "두 번째 아이템"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "첫 번째 아이템")
        self.assertEqual(second_saved_item.text, "두 번째 아이템")