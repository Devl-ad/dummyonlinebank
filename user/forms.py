from django import forms
from account.models import Account
from baseapp.utils import ref_code
from user.models import Transactions
from django.utils import timezone


class CreateTXSBSerializer(forms.ModelForm):
    account_number = forms.CharField(
        max_length=10,
        min_length=10,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Account Number",
            }
        ),
        label="Reciever Account Number",
        required=True,
    )

    amount = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "number",
                "class": "form-control",
                "placeholder": "Amount",
                "min": 10,
            }
        ),
        label="Amount",
        required=True,
    )

    purpose = forms.CharField(
        max_length=100,
        min_length=5,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Purpose",
            }
        ),
        label="Purpose",
        required=True,
    )

    type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "hidden",
            }
        ),
        required=True,
    )

    class Meta:
        model = Transactions
        fields = ["account_number", "amount", "purpose", "type"]

    def __init__(self, sender, *args, **kwargs):
        self.sender = sender
        super(CreateTXSBSerializer, self).__init__(*args, **kwargs)

    def clean_account_number(self):
        acct_num = self.cleaned_data["account_number"]
        receiver = None
        try:
            receiver = Account.objects.get(username=acct_num)
        except Account.DoesNotExist:
            receiver = None

        if receiver is None:
            raise forms.ValidationError(
                {"account_number": "Account number is not valid"}
            )
        return acct_num

    def save(self, commit=True):
        transaction = super(CreateTXSBSerializer, self).save(commit=False)

        acct_num = self.cleaned_data["account_number"]
        receiver = Account.objects.get(username=acct_num)

        transaction.sender = self.sender
        transaction.receiver = receiver
        transaction.purpose = self.cleaned_data["purpose"]
        transaction.bank_name = "Heritage"
        transaction.type = "Local transfer"
        transaction.invoiceRef = ref_code()
        transaction.amount = int(self.cleaned_data["amount"])
        transaction.ben_acct = self.cleaned_data["account_number"]
        transaction.date = timezone.now()

        if commit:
            transaction.save()
            transaction.sender.balance -= int(transaction.amount)
            transaction.sender.save()
        return transaction
