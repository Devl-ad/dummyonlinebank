from django import forms
from account.models import Account
from baseapp.utils import ref_code
from user.models import InternationalDetails, Transactions
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


class CreateTXOBSerializer(forms.ModelForm):
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "placeholder": "Recepient Email",
            }
        ),
        label="Recepient  Email",
        required=True,
    )

    first_name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "First name",
                "autocomplete": False,
            }
        ),
        label="Recepient First Name",
        required=True,
    )

    last_name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Last Name",
                "autocomplete": False,
            }
        ),
        label="Recepient Last Name",
        required=True,
    )

    ben_account_number = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Recepient Account Number",
                "autocomplete": False,
            }
        ),
        label="Recepient Account Number",
    )

    bank_name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Recepient Bank Name",
                "autocomplete": False,
            }
        ),
        label="Recepient Bank Name",
    )
    route_num = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Bank Route Number",
                "autocomplete": False,
            }
        ),
        label="Recepient Bank Route Number",
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
        fields = [
            "first_name",
            "last_name",
            "email",
            "ben_account_number",
            "bank_name",
            "route_num",
            "amount",
            "purpose",
            "type",
        ]

    def __init__(self, sender, *args, **kwargs):
        self.sender = sender
        super(CreateTXOBSerializer, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        transaction = super(CreateTXOBSerializer, self).save(commit=False)

        transaction.sender = self.sender
        transaction.purpose = self.cleaned_data["purpose"]
        transaction.bank_name = self.cleaned_data["bank_name"]
        transaction.type = "Domestic transfer"
        transaction.invoiceRef = ref_code()
        transaction.amount = self.cleaned_data["amount"]
        transaction.ben_acct = self.cleaned_data["ben_account_number"]
        transaction.route_num = self.cleaned_data["route_num"]
        transaction.date = timezone.now()

        details = InternationalDetails.objects.create(
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
        )
        transaction.interDetail = details

        if commit:
            transaction.save()
            transaction.sender.balance -= int(transaction.amount)
            transaction.sender.save()

        return transaction


class CreateTXInSerializer(forms.ModelForm):
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "placeholder": "Email",
            }
        ),
        label=" Email",
        required=True,
    )
    first_name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "First name",
                "autocomplete": False,
            }
        ),
        label="First Name",
        required=True,
    )

    last_name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Last Name",
                "autocomplete": False,
            }
        ),
        label="Last Name",
        required=True,
    )

    ben_account_number = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Account Number",
                "autocomplete": False,
            }
        ),
        label="Account Number",
    )

    bank_name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Bank Name",
                "autocomplete": False,
            }
        ),
        label="Bank Name",
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

    swift_code = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "SWift Code",
            }
        ),
        label="SWift/BIC",
        required=True,
    )
    iban_number = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "IBAN Number",
            }
        ),
        label="IBAN Number",
        required=True,
    )

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "City",
            }
        ),
        label="City",
        required=True,
    )

    country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Country",
            }
        ),
        label="Country",
        required=True,
    )

    class Meta:
        model = Transactions
        fields = [
            "first_name",
            "last_name",
            "email",
            "ben_account_number",
            "bank_name",
            "swift_code",
            "iban_number",
            "city",
            "country",
            "amount",
            "purpose",
            "type",
        ]

    def __init__(self, sender, *args, **kwargs):
        self.sender = sender
        super(CreateTXInSerializer, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        transaction = super(CreateTXInSerializer, self).save(commit=False)

        transaction.sender = self.sender
        transaction.purpose = self.cleaned_data["purpose"]
        transaction.bank_name = self.cleaned_data["bank_name"]
        transaction.type = "International"
        transaction.invoiceRef = ref_code()
        transaction.amount = self.cleaned_data["amount"]
        transaction.ben_acct = self.cleaned_data["ben_account_number"]
        transaction.date = timezone.now()

        details = InternationalDetails.objects.create(
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            country=self.cleaned_data["country"],
            city=self.cleaned_data["city"],
            iban_number=self.cleaned_data["iban_number"],
            bic_code=self.cleaned_data["swift_code"],
            email=self.cleaned_data["email"],
        )
        transaction.interDetail = details
        if commit:
            transaction.save()
            transaction.sender.balance -= int(transaction.amount)
            transaction.sender.save()

        return transaction


class ChangePinForm(forms.ModelForm):
    oldpin = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Old pin",
            }
        ),
        label="Old pin",
        required=True,
    )
    newpin = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "New pin",
            }
        ),
        label="New pin",
        required=True,
    )

    confirm_newpin = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Confirm New pin",
            }
        ),
        label="Confirm New pin",
        required=True,
    )

    class Meta:
        model = Account
        fields = ["oldpin", "newpin", "confirm_newpin"]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePinForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        oldpin = cleaned_data.get("oldpin")
        newpin = cleaned_data.get("newpin")
        confirm_newpin = cleaned_data.get("confirm_newpin")
        user = self.user

        if oldpin and user.security_pin != oldpin:
            self.add_error("oldpin", "Old Security pin doesn't match")

        if newpin and user.security_pin == newpin:
            self.add_error(
                "newpin", "New Security pin must be different from the old one"
            )

        if newpin and confirm_newpin and newpin != confirm_newpin:
            self.add_error("confirm_newpin", "New Security pin doesn't match")
