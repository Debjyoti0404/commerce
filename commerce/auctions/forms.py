from django import forms

class BiddingForm(forms.Form):
    bid_amount = forms.FloatField(label="Bid here")

class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", max_length=300)

class ProductForm(forms.Form):
    prdct_name = forms.CharField(label="Product Name", widget=forms.Textarea(attrs={
        "class":"form-control border border-primary mb-2",
        "type":"text",
        "rows":"1"
    }), max_length=64)
    prdct_desc = forms.CharField(label="Description", widget=forms.Textarea(attrs={
        "class":"form-control border border-primary mb-2",
        "type":"text",
        "rows":"1"
    }), max_length=500)
    prdct_price = forms.FloatField(label="Initial Price", widget=forms.Textarea(attrs={
        "class":"form-control border border-primary mb-2",
        "type":"text",
        "rows":"1"
    }))
    prdct_img = forms.URLField(label="Product Picture", widget=forms.Textarea(attrs={
        "class":"form-control border border-primary mb-2",
        "type":"text",
        "rows":"1"
    }))
    prdct_category = forms.CharField(label="Category", widget=forms.Textarea(attrs={
        "class":"form-control border border-primary mb-2",
        "type":"text",
        "rows":"1"
    }), max_length=64)