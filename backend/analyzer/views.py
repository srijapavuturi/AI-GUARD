from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import JobAnalysis
import json


# ==========================================
# HOME
# ==========================================

@login_required(login_url="/login/")
def home(request):
    return render(request, "analyzer/index.html")


# ==========================================
# SIGNUP
# ==========================================

def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(
                request,
                "analyzer/signup.html",
                {
                    "error": "Please enter username and password."
                }
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "analyzer/signup.html",
                {
                    "error": "Username already exists."
                }
            )

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("/login/")

    return render(request, "analyzer/signup.html")


# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/")

        return render(
            request,
            "analyzer/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "analyzer/login.html")


# ==========================================
# LOGOUT
# ==========================================

@login_required(login_url="/login/")
def logout_view(request):

    logout(request)

    return redirect("/login/")


# ==========================================
# ANALYZE JOB
# ==========================================

@csrf_exempt
@login_required(login_url="/login/")
def analyze_job(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Only POST requests are allowed"
            },
            status=405
        )

    try:

        data = json.loads(request.body)

        description = data.get(
            "description",
            ""
        ).lower()

        risk_score = 0
        red_flags = []


        # ==========================================
        # PAYMENT RELATED SCAMS
        # ==========================================

        if (
            "registration fee" in description
            and "no registration fee" not in description
        ):
            risk_score += 30

            red_flags.append(
                "Job asks for a registration fee."
            )


        if (
            "training fee" in description
            and "no training fee" not in description
        ):
            risk_score += 25

            red_flags.append(
                "Job asks candidates to pay a training fee."
            )


        if (
            (
                "pay upfront" in description
                or "pay a fee" in description
                or "advance payment" in description
            )
            and "no payment" not in description
        ):
            risk_score += 25

            red_flags.append(
                "Job asks the candidate to make an upfront or advance payment."
            )


        if (
            "security deposit" in description
            and "no security deposit" not in description
        ):
            risk_score += 25

            red_flags.append(
                "Job asks for a security deposit."
            )


        if (
            "processing fee" in description
            and "no processing fee" not in description
        ):
            risk_score += 25

            red_flags.append(
                "Job asks for a processing fee."
            )


        if "interview fee" in description:
            risk_score += 25

            red_flags.append(
                "Job appears to charge a fee for an interview."
            )


        # ==========================================
        # FAKE JOB PROMISES
        # ==========================================

        if "guaranteed job" in description:
            risk_score += 20

            red_flags.append(
                "Job claims employment is guaranteed."
            )


        if "100% placement" in description:
            risk_score += 20

            red_flags.append(
                "Job promises 100% placement."
            )


        if "guaranteed income" in description:
            risk_score += 20

            red_flags.append(
                "Job promises guaranteed income."
            )


        if "easy money" in description:
            risk_score += 15

            red_flags.append(
                "Job promises easy money."
            )


        if (
            "work from home" in description
            and (
                "easy money" in description
                or "high salary" in description
            )
        ):
            risk_score += 20

            red_flags.append(
                "Job promises easy money or high salary through work from home."
            )


        if "no interview" in description:
            risk_score += 15

            red_flags.append(
                "Job claims that no interview is required."
            )


        # ==========================================
        # SALARY RELATED SCAMS
        # ==========================================

        if (
            "earn 50000" in description
            or "earn 100000" in description
            or "₹50,000" in description
            or "₹100,000" in description
            or "50,000 per month" in description
            or "1 lakh per month" in description
        ):
            risk_score += 20

            red_flags.append(
                "The advertised salary may be unusually high."
            )


        # ==========================================
        # EXPERIENCE
        # ==========================================

        if (
            "no experience" in description
            or "no prior experience" in description
        ):
            risk_score += 5

            red_flags.append(
                "Job emphasizes that little or no experience is required."
            )


        # ==========================================
        # URGENCY
        # ==========================================

        if (
            "limited slots" in description
            or "limited time" in description
            or "apply now" in description
            or "urgent hiring" in description
            or "urgently hiring" in description
            or "hurry" in description
            or "act now" in description
        ):
            risk_score += 10

            red_flags.append(
                "Job uses urgency-based language."
            )


        # ==========================================
        # OTP AND VERIFICATION
        # ==========================================

        if (
            "otp" in description
            or "verification code" in description
        ):
            risk_score += 20

            red_flags.append(
                "Job appears to request an OTP or verification code."
            )


        # ==========================================
        # FINANCIAL INFORMATION
        # ==========================================

        if (
            "bank account" in description
            or "bank details" in description
            or "credit card" in description
            or "debit card" in description
            or "upi" in description
            or "upi id" in description
        ):
            risk_score += 20

            red_flags.append(
                "Job appears to request sensitive financial information."
            )


        # ==========================================
        # IDENTITY DOCUMENTS
        # ==========================================

        if (
            "aadhaar" in description
            or "aadhar" in description
            or "passport" in description
            or "identity proof" in description
            or "id proof" in description
            or "pan card" in description
        ):
            risk_score += 15

            red_flags.append(
                "Job requests identity documents; verify the employer before sharing them."
            )


        # ==========================================
        # COMMUNICATION RED FLAGS
        # ==========================================

        if (
            "whatsapp only" in description
            or "telegram only" in description
        ):
            risk_score += 10

            red_flags.append(
                "Job relies heavily on messaging apps instead of official communication."
            )


        if "whatsapp" in description:
            risk_score += 5

            red_flags.append(
                "Job uses WhatsApp for communication; verify the employer independently."
            )


        if "telegram" in description:
            risk_score += 5

            red_flags.append(
                "Job uses Telegram for communication; verify the employer independently."
            )


        if "personal email" in description:
            risk_score += 10

            red_flags.append(
                "Job appears to use a personal email instead of an official company email."
            )


        # ==========================================
        # INVESTMENT / MONEY TRANSFER
        # ==========================================

        if (
            "invest money" in description
            or "deposit money" in description
            or "transfer money" in description
            or "send money" in description
        ):
            risk_score += 25

            red_flags.append(
                "Job asks the candidate to invest or transfer money."
            )


        # ==========================================
        # QUICK MONEY
        # ==========================================

        if (
            "quick money" in description
            or "quick income" in description
            or "get rich quick" in description
            or "instant income" in description
        ):
            risk_score += 15

            red_flags.append(
                "Job promises quick or instant income."
            )


        # ==========================================
        # CRYPTO / INVESTMENT
        # ==========================================

        if (
            "crypto investment" in description
            or "cryptocurrency investment" in description
            or "investment opportunity" in description
        ):
            risk_score += 20

            red_flags.append(
                "Job appears to involve an investment opportunity."
            )


        # ==========================================
        # PERSONAL INFORMATION
        # ==========================================

        if (
            "password" in description
            or "login details" in description
            or "account password" in description
        ):
            risk_score += 25

            red_flags.append(
                "Job appears to request sensitive login information."
            )


        # ==========================================
        # KEEP SCORE BETWEEN 0 AND 100
        # ==========================================

        risk_score = min(
            risk_score,
            100
        )


        # ==========================================
        # RISK LEVEL
        # ==========================================

        if risk_score >= 70:
            risk_level = "High Risk 🚨"

        elif risk_score >= 40:
            risk_level = "Medium Risk ⚠️"

        else:
            risk_level = "Low Risk ✅"


        # ==========================================
        # SAFETY RECOMMENDATION
        # ==========================================

        if risk_score >= 70:

            recommendation = (
                "Do not proceed with this job until the employer is independently verified. "
                "Never pay upfront fees or share OTPs, passwords, bank details, "
                "or sensitive information."
            )

        elif risk_score >= 40:

            recommendation = (
                "Be careful before proceeding. Verify the employer, company website, "
                "official email address, and job details before sharing personal information."
            )

        else:

            recommendation = (
                "The job appears to have a low number of detected warning signs. "
                "Still verify the employer before sharing personal or financial information."
            )


        # ==========================================
        # SAVE RESULT FOR LOGGED-IN USER
        # ==========================================

        JobAnalysis.objects.create(
            user=request.user,
            job_description=description,
            risk_score=risk_score,
            risk_level=risk_level,
            warning_signs="\n".join(red_flags),
            recommendation=recommendation
        )


        # ==========================================
        # RETURN RESULT
        # ==========================================

        return JsonResponse(
            {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "red_flags": red_flags,
                "recommendation": recommendation
            }
        )


    except Exception as e:

        return JsonResponse(
            {
                "error": str(e)
            },
            status=400
        )


# ==========================================
# HISTORY
# ==========================================

@login_required(login_url="/login/")
def history(request):

    analyses = JobAnalysis.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )


    high_count = analyses.filter(
        risk_level__contains="High Risk"
    ).count()


    medium_count = analyses.filter(
        risk_level__contains="Medium Risk"
    ).count()


    low_count = analyses.filter(
        risk_level__contains="Low Risk"
    ).count()


    return render(
        request,
        "analyzer/history.html",
        {
            "analyses": analyses,
            "high_count": high_count,
            "medium_count": medium_count,
            "low_count": low_count
        }
    )


# ==========================================
# DELETE ANALYSIS
# ==========================================

@login_required(login_url="/login/")
def delete_analysis(request, id):

    if request.method == "POST":

        analysis = JobAnalysis.objects.get(
            id=id,
            user=request.user
        )

        analysis.delete()

    return redirect("/history/")

