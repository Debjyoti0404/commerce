from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", max_length=300)

class ProductForm(forms.Form):
    prdct_name = forms.CharField(label="Product Name", max_length=64)
    prdct_desc = forms.CharField(label="Description", max_length=200)
    prdct_price = forms.FloatField(label="Initial Price")
    prdct_img = forms.URLField(label="Product Picture")