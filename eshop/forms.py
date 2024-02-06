from .models import Order, Item
from django import forms

class OrderModelForm(forms.ModelForm):


    class Meta:
        model = Order
        exclude = ["user"]
        # fields = "__all__"
        widgets = {
            "number": forms.NumberInput(
                attrs={
                    "placeholder": "Number of items",
                    "min": 1,
                    "initial": 1
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "placeholder":"Shipping address"
                }
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Your email address"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(OrderModelForm, self).__init__(*args, **kwargs)
        print(args, kwargs)

        def set_initials_inited(init, item="", description="", size=""):
            if not item:
                item = Item.objects.all().first()
                print("ITEM:", item)
                description = item.description
                size= item.size
                item = item.item
            descriptions = Item.objects.filter(item=item).values_list('description').distinct().order_by('description')
            self.fields['description'].choices = [(desc[0], desc[0]) for desc in descriptions]
            sizes = Item.objects.filter(item=item, description=description).values_list('size').distinct()
            self.fields['size'].choices = [(s[0], s[0]) for s in sizes]
            max_items = Item.objects.filter(item=item, description=description, size=size).count()
            self.fields['number'].widget.attrs['max'] = max_items
            if init:
                # set initials in case no item is passed before
                self.fields['item'].initial = item
                self.fields['description'].initial = description
                self.fields['size'].initial = size
            
            self.fields['number'].initial = 1

        if 'item' in self.initial:
            print("FORMINIT")
            item = self.initial['item']
            description = self.initial['description']
            size = self.initial['size']
            set_initials_inited(False, item, description, size)
        else:
            set_initials_inited(True)

