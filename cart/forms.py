from django import forms
#Импортировать продукт и по колву
# PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
from shop.models import Product

class CartAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(label='Количество', choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    # update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    def __init__(self, *args, product_id):
        super().__init__(*args)
        self.max_quantity = Product.objects.get(id=product_id).stock + 1
        # self.product_id = product_id
        product_quantity_choices = [(i, str(i)) for i in range(1, min(self.max_quantity, 21))]
        self.fields['quantity'] = forms.TypedChoiceField(label='Количество', choices=product_quantity_choices, coerce=int)
        self.fields['update'] = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
        # self.update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
