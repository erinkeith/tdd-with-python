from django.test import TestCase

from lists.forms import (ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm)
from lists.models import Item, List

class ItemFormTest(TestCase):

	def test_form_renders_text_input(self):
		form = ItemForm(data={'text': ''})
		
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

	def test_form_save_handles_saving_to_a_list(self):
		list_ = List.objects.create()
		form = ItemForm(data={'text': 'do me'})
		new_item = form.save(for_list=list_)

		self.assertEqual(new_item, Item.objects.first())
		self.assertEqual(new_item.text, 'do me')
		self.assertEqual(new_item.list, list_)

	def test_form_validation_for_duplicate_items(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='no twins!')
		form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})

		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
