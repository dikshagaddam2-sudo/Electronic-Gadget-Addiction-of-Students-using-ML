import os
import uuid
import joblib
import random
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import shap

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from .forms import (
    ParentSignUpForm,
    AddictionInputForm,
    EmailLoginForm,
    OTPVerificationForm
)
# ======================
# Paths to model files
# ======================
MODEL_PATH = r"C:\Users\Diksha\Desktop\final yearproject\phone_addiction_full\phone_addiction_full\xgb_mobile_addiction_model_new.pkl"

SCALER_PATH = r"C:\Users\Diksha\Desktop\final yearproject\phone_addiction_full\phone_addiction_full\scaler.pkl"

scaler = joblib.load(SCALER_PATH)

# ======================

# Load model
# ======================
xgb_model = None
scaler = None


try:

    if os.path.exists(MODEL_PATH):

        xgb_model = joblib.load(MODEL_PATH)

        print("Model loaded successfully.")

    if os.path.exists(SCALER_PATH):

        scaler = joblib.load(SCALER_PATH)

        print("Scaler loaded successfully.")

except Exception as e:

    print('Load error:', e)


# ======================
# SEND OTP EMAIL
# ======================

def send_otp_email(email, otp):

    send_mail(

        subject='📱 Phone Addiction Tracker OTP',

        message=f'''
Your OTP verification code is:

{otp}

Do not share this OTP with anyone.

Phone Addiction Tracker
        ''',

        from_email=None,

        recipient_list=[email],

        fail_silently=False,
    )

# ======================
# User Registration
# ======================
# ======================
# USER REGISTRATION WITH OTP
# ======================

def register_view(request):

    if request.method == 'POST':

        form = ParentSignUpForm(request.POST)

        if form.is_valid():

            # ==========================
            # GET FORM DATA
            # ==========================

            email = form.cleaned_data['email']

            password = form.cleaned_data['password1']
            
                        # ==========================
            # CHECK EXISTING ACCOUNT
            # ==========================

            if User.objects.filter(username=email).exists():

                messages.error(

                    request,

                    'Email already registered. Please login instead.'
                )

                return redirect('main:login')

            # ==========================
            # GENERATE OTP
            # ==========================

            otp = str(
                random.randint(100000, 999999)
            )

            # ==========================
            # STORE DATA IN SESSION
            # ==========================

            request.session['otp'] = otp

            request.session['email'] = email

            request.session['password'] = password

            # ==========================
            # SEND OTP EMAIL
            # ==========================

            send_otp_email(email, otp)

            # ==========================
            # REDIRECT TO OTP PAGE
            # ==========================

            return redirect('main:verify_otp')

    else:

        form = ParentSignUpForm()

    return render(
        request,
        'main/register.html',
        {'form': form}
    )


# ======================
# OTP VERIFICATION VIEW
# ======================

def verify_otp_view(request):

    if request.method == 'POST':

        form = OTPVerificationForm(request.POST)

        if form.is_valid():

            entered_otp = form.cleaned_data['otp']

            saved_otp = request.session.get('otp')

            # ==========================
            # CHECK OTP
            # ==========================

            if entered_otp == saved_otp:

                email = request.session.get('email')

                password = request.session.get('password')

                # ==========================
                # CREATE USER
                # ==========================

                # ==========================
                # CHECK IF USER EXISTS
                # ==========================

                if User.objects.filter(username=email).exists():

                    messages.error(
                        request,
                        'Account already exists. Please login.'
                    )

                    return redirect('main:login')

                # ==========================
                # CREATE USER
                # ==========================

                user = User.objects.create_user(

                    username=email,

                    email=email,

                    password=password
                )

                # ==========================
                # LOGIN USER
                # ==========================

                login(request, user)
                            # ==========================
            # SEND WELCOME EMAIL
            # ==========================

                send_mail(

                    subject='🎉 Registration Successful',

                    message=f'''

    Hello Parent,

    Your account has been successfully created
    on Phone Addiction Tracker.

    You can now:

    - Predict addiction levels
    - View AI analysis
    - Receive high-risk alerts
    - Monitor smartphone behavior

    Thank you for registering.

    Phone Addiction Tracker Team
                    ''',

                    from_email=None,

                    recipient_list=[user.email],

                    fail_silently=True
                )

                # ==========================
                # CLEAR SESSION
                # ==========================

                request.session.pop('otp', None)

                request.session.pop('email', None)

                request.session.pop('password', None)

                messages.success(
                    request,
                    'OTP verification successful.'
                )

                return redirect('main:predict')

            else:

                messages.error(
                    request,
                    'Invalid OTP.'
                )

    else:

        form = OTPVerificationForm()

    return render(

        request,

        'main/verify_otp.html',

        {'form': form}
    )

# ======================
# Login View
# ======================
# class ParentLoginView(LoginView):
#     template_name = 'main/login.html'


# ======================
# Email Login View
# ======================
def email_login_view(request):

    form = EmailLoginForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():

            user = form.cleaned_data['user']

            login(request, user)
            # ==========================
            # LOGIN ALERT EMAIL
            # ==========================

            send_mail(

                subject='🔐 Login Alert',

                message=f'''

Hello Parent,

Your account was just logged into successfully.

If this was you, no action is needed.

If you did NOT login,
please reset your password immediately.

Phone Addiction Tracker Team
                ''',

                from_email=None,

                recipient_list=[user.email],

                fail_silently=True
            )

            messages.success(request, 'Login successful.')

            return redirect('main:home')

    return render(request, 'main/login.html', {
        'form': form
    })


# ======================
# Home Page
# ======================
def home(request):

    # send_mail(
    #     subject='Django Email Test',
    #     message='Your Django Gmail integration is working successfully.',
    #     from_email=None,
    #     recipient_list=['honeysheth8@gmail.com'],
    #     fail_silently=False,
    # )

    return render(request, 'main/home.html')


# ======================
# SHAP Helpers
# ======================
def _ensure_shap_dir():
    shap_dir = os.path.join(settings.MEDIA_ROOT, 'shap_images')
    os.makedirs(shap_dir, exist_ok=True)
    return shap_dir

def _save_matplotlib_figure(fig, filename):
    fig.tight_layout()
    fig.savefig(filename, bbox_inches='tight', dpi=150)
    plt.close(fig)

# def _generate_simple_plot(model, input_df):
#     """
#     Generate a simple horizontal bar plot showing how each feature contributes
#     to the predicted score.
#     """
#     try:
#         shap_dir = os.path.join(settings.MEDIA_ROOT, 'shap_images')
#         os.makedirs(shap_dir, exist_ok=True)

#         # Compute contribution as (feature value * model feature importance)
#         # Get feature importance from XGBoost
#         importances = model.feature_importances_
#         features = input_df.columns
#         values = input_df.iloc[0].values

#         contributions = values * importances  # simple weighted contribution

#         # Sort descending
#         sorted_idx = np.argsort(np.abs(contributions))
#         sorted_features = features[sorted_idx]
#         sorted_contributions = contributions[sorted_idx]

#         # Plot
#         fig, ax = plt.subplots(figsize=(8, max(3, len(features) * 0.4)))
#         ax.barh(range(len(sorted_features)), sorted_contributions, color="#4f46e5")
#         ax.set_yticks(range(len(sorted_features)))
#         ax.set_yticklabels(sorted_features)
#         ax.set_xlabel("Feature contribution")
#         ax.set_title("Prediction Feature Contributions")
#         for i, v in enumerate(sorted_contributions):
#             ax.text(v, i, f"{v:.2f}", va='center', color='black')

#         # Save
#         fname = f"simple_{uuid.uuid4().hex[:8]}.png"
#         save_path = os.path.join(shap_dir, fname)
#         fig.tight_layout()
#         fig.savefig(save_path, bbox_inches='tight', dpi=150)
#         plt.close(fig)

#         media_url = getattr(settings, 'MEDIA_URL', '/media/')
#         if not media_url.endswith('/'):
#             media_url += '/'
#         return f"{media_url}shap_images/{fname}"

#     except Exception as e:
#         print("Simple plot generation error:", e)
#         return None
def _generate_shap_plot(model, input_df):

    try:

        shap_dir = os.path.join(
            settings.MEDIA_ROOT,
            'shap_images'
        )

        os.makedirs(shap_dir, exist_ok=True)

        # ==========================
        # SIMPLE FEATURE IMPORTANCE
        # ==========================

        importances = model.feature_importances_

        features = input_df.columns

        values = input_df.iloc[0].values

        contributions = values * importances

        # ==========================
        # SORT
        # ==========================

        sorted_idx = np.argsort(np.abs(contributions))

        sorted_features = features[sorted_idx]

        sorted_contributions = contributions[sorted_idx]

        # ==========================
        # PLOT
        # ==========================

        fig, ax = plt.subplots(figsize=(10, 7))

        ax.barh(

            range(len(sorted_features)),

            sorted_contributions,

            color='#4f46e5'
        )

        ax.set_yticks(range(len(sorted_features)))

        ax.set_yticklabels(sorted_features)

        ax.set_xlabel('Feature Contribution')

        ax.set_title(
            'Explainable AI Feature Analysis'
        )

        # ==========================
        # VALUE LABELS
        # ==========================

        for i, v in enumerate(sorted_contributions):

            ax.text(

                v,

                i,

                f'{v:.2f}',

                va='center'
            )

        # ==========================
        # SAVE IMAGE
        # ==========================

        fname = f"shap_{uuid.uuid4().hex[:8]}.png"

        save_path = os.path.join(
            shap_dir,
            fname
        )

        fig.tight_layout()

        fig.savefig(

            save_path,

            bbox_inches='tight',

            dpi=150
        )

        plt.close(fig)

        media_url = getattr(
            settings,
            'MEDIA_URL',
            '/media/'
        )

        if not media_url.endswith('/'):
            media_url += '/'

        return f"{media_url}shap_images/{fname}"

    except Exception as e:

        print(
            "SHAP generation error:",
            e
        )

        return None




# ======================
# Prediction View
# ======================
@login_required
def predict_view(request):

    if request.method == 'POST':

        form = AddictionInputForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data
                        # ==========================
            # CONVERT DROPDOWN STRINGS
            # ==========================

            data['Gender'] = int(data['Gender'])

            data['Parental_Control'] = int(
                data['Parental_Control']
            )

            data['Phone_Usage_Purpose'] = int(
                data['Phone_Usage_Purpose']
            )

            input_df = pd.DataFrame([data])

            # ==========================
            # PREDICTION
            # ==========================

            try:

                # pred = float(
                #     xgb_model.predict(input_df)[0]
                # )
                scaled_input = scaler.transform(input_df)
                pred = float(
                    xgb_model.predict(scaled_input)[0]
                )
                pred = max(0, min(pred, 10))

            except Exception as e:

                print("Prediction error:", e)

                pred = min(
                    data.get('Daily_Usage_Hours', 0)
                    + data.get('Time_on_Social_Media', 0)
                    + data.get('Time_on_Gaming', 0),
                    10
                )

            # ==========================
            # RISK LABEL
            # ==========================

            if pred < 4:

                label = 'Low Risk — You are not addicted.'

            elif 4 <= pred < 7:

                label = 'Moderate Risk — Try reducing phone usage.'

            else:

                label = 'High Risk — Excessive phone usage detected.'

            # ==========================
            # SEND EMAIL IF HIGH RISK
            # ==========================

            if pred >= 7:

                try:

                    send_mail(

                        subject='⚠ High Phone Addiction Alert',

                        message=f'''
Hello Parent,

Our AI system detected a HIGH mobile addiction risk.

Predicted Addiction Score: {round(pred, 2)} / 10

Recommendations:
- Reduce daily screen time
- Encourage outdoor activities
- Improve sleep schedule
- Increase family interaction
- Encourage exercise and study balance

Phone Addiction Tracker
                        ''',

                        from_email=None,

                        recipient_list=[request.user.email],

                        fail_silently=False,
                    )

                    print("High addiction alert email sent successfully.")

                except Exception as email_error:

                    print("Email sending failed:", email_error)

            # ==========================
            # SHAP IMAGE
            # ==========================

            shap_image = None

            if xgb_model:

                # shap_image = _generate_simple_plot(
                #     xgb_model,
                #     input_df
                # )
                shap_image = _generate_shap_plot(
                    xgb_model,
                    input_df
                ) if xgb_model else None

            # ==========================
            # RESULT PAGE
            # ==========================

            return render(

                request,

                'main/result.html',

                {
                    'score': round(pred, 2),
                    'label': label,
                    'shap_image': shap_image
                }
            )

    else:

        form = AddictionInputForm()

    return render(
        request,
        'main/predict.html',
        {'form': form}
    )



# ======================
# XAI (SHAP) Gallery
# ======================
def xai_view(request):
    shap_dir = _ensure_shap_dir()
    media_url = getattr(settings, 'MEDIA_URL', '/media/')
    if not media_url.endswith('/'):
        media_url += '/'
    shap_files = []

    try:
        for f in sorted(os.listdir(shap_dir), reverse=True):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                shap_files.append(os.path.join(media_url, 'shap_images', f).replace('\\', '/'))
    except Exception as e:
        print("Error listing SHAP files:", e)

    return render(request, 'main/xai.html', {'shap_files': shap_files})


# ======================
# Logout View
# ======================
def logout_view(request):
    logout(request)
    return redirect('main:login')
