from django import forms
from django.contrib.auth import get_user_model

# from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from baseapp import utils


User = get_user_model()


class RegisterForm(UserCreationForm):
    """
    The default

    """

    email = forms.EmailField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
                "placeholder": "Email",
                "autocomplete": False,
            }
        ),
        label=False,
        required=True,
    )

    password1 = forms.CharField(
        max_length=30,
        min_length=6,
        label=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "autocomplete": False,
            }
        ),
    )
    password2 = forms.CharField(
        max_length=30,
        min_length=6,
        label=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Verify Password",
                "class": "form-control",
                "autocomplete": False,
            }
        ),
    )

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class CreateAcctForm(forms.ModelForm):
    """
    The default

    """

    email = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "hidden": True,
            }
        ),
        label=False,
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
        label=False,
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
        label=False,
        required=True,
    )

    phone_number = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "form-control",
                "placeholder": "Phone number",
                "autocomplete": False,
            }
        ),
        label=False,
        required=True,
    )

    date_of_birth = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "date",
                "class": "form-control",
                "placeholder": "Date of Birth",
                "autocomplete": False,
            }
        ),
        label=False,
        required=True,
    )

    gender = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Gender",
                "autocomplete": False,
            }
        ),
        label=False,
        required=True,
    )

    # next_of_kin = forms.CharField(
    #     max_length=80,
    #     widget=forms.TextInput(
    #         attrs={
    #             "type": "text",
    #             "class": "form-control",
    #             "placeholder": "Next of kin",
    #             "autocomplete": False,
    #         }
    #     ),
    #     label=False,
    #     required=True,
    # )

    address = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Address",
                "autocomplete": False,
            }
        ),
        label=False,
        required=True,
    )

    city = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "City",
                "autocomplete": False,
            }
        ),
        label=False,
        required=True,
    )

    state = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "State",
                "autocomplete": False,
            }
        ),
        label=False,
        required=True,
    )

    zipcode = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Zipcode",
                "autocomplete": False,
            }
        ),
        label=False,
        required=True,
    )

    country = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Country",
                "autocomplete": False,
            }
        ),
        label=False,
        required=True,
    )

    account_type = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Account type",
                "autocomplete": False,
            }
        ),
        label=False,
        required=True,
    )

    security_pin = forms.CharField(
        min_length=4,
        max_length=4,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "4 Digit Security pin",
            }
        ),
        label=False,
        required=True,
    )

    password = forms.CharField(
        max_length=30,
        min_length=6,
        label=False,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "hidden": True,
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "date_of_birth",
            "gender",
            # "next_of_kin",
            "address",
            "city",
            "state",
            "zipcode",
            "country",
            "account_type",
            "security_pin",
            "password",
        ]

    def save(self, commit=True):
        user = super(CreateAcctForm, self).save(commit=False)  # Get the form instance

        # Process and assign additional fields if needed
        user.username = utils.gen_random_number()
        # For example, hashing passwords before saving
        if user.password:
            user.set_password(user.password)

        # Save the user to the database if commit=True
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    username = forms.CharField(
        max_length=12,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Account Number",
            }
        ),
        label=False,
        required=True,
    )
    password = forms.CharField(
        max_length=10,
        min_length=6,
        label=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )

    def clean(self):
        if self.is_valid():
            if not authenticate(
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password"],
            ):
                raise forms.ValidationError("Invalid Account number or Password")
