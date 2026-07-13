from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# =========================
# SIGNUP FORM
# =========================
class ParentSignUpForm(UserCreationForm):

    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your Gmail',
            'class': 'form-input'
        })
    )

    password1 = forms.CharField(
    label='Password',
    widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-input'
        })
    )

    password2 = forms.CharField(
    label='Confirm Password',
    widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-input'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if User.objects.filter(username=email).exists():

            raise forms.ValidationError(
                "This email is already registered. Please login or reset your password."
            )

        return email    
    
    def save(self, commit=True):
        user = super().save(commit=False)

        # Django still needs username internally
        user.username = self.cleaned_data['email']

        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


# =========================
# EMAIL LOGIN FORM
# =========================
class EmailLoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your Gmail',
            'class': 'form-input'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password',
            'class': 'form-input'
        })
    )

    def clean(self):

        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise forms.ValidationError(
                "Invalid email or password"
            )

        cleaned_data['user'] = user

        return cleaned_data

class OTPVerificationForm(forms.Form):

    otp = forms.CharField(

        max_length=6,

        widget=forms.TextInput(attrs={

            'placeholder': 'Enter 6-digit OTP',

            'class': 'form-input'
        })
    )

class AddictionInputForm(forms.Form):

    Age = forms.FloatField(

        min_value=10,
        max_value=20,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 15',
            'class': 'form-input'
        }),

        help_text='Enter age between 10 to 20 years'
    )

    Gender = forms.ChoiceField(

        choices=[

            (0, 'Female'),
            (1, 'Male'),
            (2, 'Other')
        ],

        widget=forms.Select(attrs={

            'class': 'form-input'
        })
    )

    Standard = forms.IntegerField(

        min_value=7,
        max_value=13,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 10th Standard',
            'class': 'form-input'
        }),

        help_text='Enter class/standard between 7 and 13'
    )

    Daily_Usage_Hours = forms.FloatField(

        min_value=0,
        max_value=24,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 6 hours',
            'class': 'form-input'
        }),

        help_text='Average phone usage per day'
    )

    Sleep_Hours = forms.FloatField(

        min_value=0,
        max_value=24,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 7',
            'class': 'form-input'
        }),

        help_text='Average sleep hours daily'
    )

    Academic_Performance = forms.FloatField(

        min_value=0,
        max_value=100,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Marks percentage (0-100)',
            'class': 'form-input'
        }),

        help_text='Academic score percentage'
    )

    Social_Interactions = forms.IntegerField(

        min_value=0,
        max_value=10,

        widget=forms.NumberInput(attrs={

            'placeholder': '0 to 10',
            'class': 'form-input'
        }),

        help_text='0 = very low social interaction'
    )

    Exercise_Hours = forms.FloatField(

        min_value=0,
        max_value=24,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 1 hour',
            'class': 'form-input'
        }),

        help_text='Average exercise hours daily'
    )

    Anxiety_Level = forms.FloatField(

        min_value=0,
        max_value=10,
        initial=5,

        widget=forms.NumberInput(attrs={

            'type': 'range',
            'min': '0',
            'max': '10',
            'step': '1',

            'class': 'slider-input',

            'oninput': 'this.nextElementSibling.value = this.value'
        }),

        help_text='0 = none, 10 = severe anxiety'
    )

    Depression_Level = forms.FloatField(

        min_value=0,
        max_value=10,
        initial=5,

        widget=forms.NumberInput(attrs={

            'type': 'range',
            'min': '0',
            'max': '10',
            'step': '1',

            'class': 'slider-input',

            'oninput': 'this.nextElementSibling.value = this.value'
        }),

        help_text='0 = none, 10 = severe depression'
    )

    Screen_Time_Before_Bed = forms.FloatField(

        min_value=0,
        max_value=10,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 2 hours',
            'class': 'form-input'
        }),

        help_text='Phone usage before sleeping'
    )

    Phone_Checks_Per_Day = forms.IntegerField(

        min_value=0,
        max_value=500,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 50',
            'class': 'form-input'
        }),

        help_text='How many times phone is checked daily'
    )

    Apps_Used_Daily = forms.IntegerField(

        min_value=0,
        max_value=100,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 15',
            'class': 'form-input'
        }),

        help_text='Total apps used daily'
    )

    Time_on_Social_Media = forms.FloatField(

        min_value=0,
        max_value=24,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 3 hours',
            'class': 'form-input'
        }),

        help_text='Daily social media usage'
    )

    Time_on_Gaming = forms.FloatField(

        min_value=0,
        max_value=24,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 2 hours',
            'class': 'form-input'
        }),

        help_text='Daily gaming time'
    )

    Time_on_Education = forms.FloatField(

        min_value=0,
        max_value=24,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 4 hours',
            'class': 'form-input'
        }),

        help_text='Educational phone usage'
    )

    Weekend_Usage_Hours = forms.FloatField(

        min_value=0,
        max_value=24,

        widget=forms.NumberInput(attrs={

            'placeholder': 'Example: 8 hours',
            'class': 'form-input'
        }),

        help_text='Phone usage during weekends'
    )

    Family_Communication = forms.IntegerField(

        min_value=0,
        max_value=10,

        widget=forms.NumberInput(attrs={

            'placeholder': '0 to 10',
            'class': 'form-input'
        }),

        help_text='Family communication quality'
    )

    Parental_Control = forms.ChoiceField(

        choices=[

            (0, 'No'),
            (1, 'Yes')
        ],

        widget=forms.Select(attrs={

            'class': 'form-input'
        })
    )

    Phone_Usage_Purpose = forms.ChoiceField(

        choices=[

            (0, 'Browsing'),
            (1, 'Education'),
            (2, 'Gaming'),
            (3, 'Other'),
            (4, 'Social Media')
        ],

        widget=forms.Select(attrs={

            'class': 'form-input'
        })
    )

    Self_Esteem = forms.FloatField(

        min_value=0,
        max_value=10,
        initial=5,

        widget=forms.NumberInput(attrs={

            'type': 'range',
            'min': '0',
            'max': '10',
            'step': '1',

            'class': 'slider-input',

            'oninput': 'this.nextElementSibling.value = this.value'
        }),

        help_text='0 = very low, 10 = very high self-esteem'
    )



