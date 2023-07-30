from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):

    full_name_invoice = forms.CharField(widget=forms.TextInput
                                 (attrs={'placeholder': 'e.g: Full name '}))
    address_invoice = forms.CharField(widget=forms.TextInput
                              (attrs={'placeholder': 'e.g:  xyz ,Maharashtra , India '}))
    GST_invoice = forms.CharField(widget=forms.TextInput
                                (attrs={'placeholder': 'e.g:  27AGSPC7785J1ZM'}))
    particular_invoice = forms.CharField(widget=forms.Textarea
                                   (attrs={'placeholder': 'e.g:  xyz for 4 Weeks' ,'rows': 1, 'cols': 40}))
    amount_invoice = forms.DecimalField(
        max_digits=20,
        decimal_places=4,
         min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g:  10000.00'})
    )
    any_discount_invoice = forms.DecimalField(
        max_digits=20,
        decimal_places=4,
         min_value=0,
         initial=0 ,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g:  1000.00'})
    )
    cgst = forms.IntegerField(initial=9 , widget=forms.NumberInput(attrs={'placeholder': 'e.g. 9'}))
    sgst = forms.IntegerField(initial=9 , widget=forms.NumberInput(attrs={'placeholder': 'e.g. 9'}))
    igst = forms.IntegerField(initial=0 , widget=forms.NumberInput(attrs={'placeholder': 'e.g. 18'}))

    class Meta:
        model = Invoice
        fields = ('full_name_invoice', 'address_invoice', 'GST_invoice', 'invoice_number',
                   'coaching_type_course_invoice', 'particular_invoice',
                  'amount_invoice', 'any_discount_invoice' ,'cgst','sgst' ,'igst' )

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['address_invoice'].widget.attrs['rows'] = 1
        self.fields['address_invoice'].widget.attrs['columns'] = 1
        self.fields['address_invoice'].required = False
        self.fields['GST_invoice'].required = False
        self.fields['any_discount_invoice'].required = False
        self.fields['particular_invoice'].required = True

        self.fields['full_name_invoice'].label = ""
        self.fields['address_invoice'].label = ""
        self.fields['GST_invoice'].label = ""
        self.fields['particular_invoice'].label = ""
        self.fields['coaching_type_course_invoice'].label = ""
        self.fields['amount_invoice'].label = ""
        self.fields['any_discount_invoice'].label = ""
        self.fields['cgst'].label = ""
        self.fields['sgst'].label = ""
        self.fields['igst'].label = ""
        
        self.fields['coaching_type_course_invoice'].empty_label = "Select type of coaching"
    