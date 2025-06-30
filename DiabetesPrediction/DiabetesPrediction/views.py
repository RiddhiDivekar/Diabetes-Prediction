from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import numpy as np
import joblib
import random  # <-- Import random for puzzle selection

# Load the trained model
model = joblib.load(
    "C:/Users/Riddhi Divekar/OneDrive/Desktop/Diabetes Project/diabetes_model.pkl"
)

# -------------------- User Authentication Views --------------------

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")

# -------------------- Main Views (Require Login) --------------------

@login_required(login_url='login')
def home(request):
    return render(request, "home.html", {"username": request.user.username})


@login_required(login_url='login')
def bmi_calculator(request):
    return render(request, "bmi.html")


@login_required(login_url='login')
def predict(request):
    return render(request, "predict.html")


@login_required(login_url='login')
def result(request):
    try:
        val1 = float(request.GET['n1'])  # Pregnancies
        val2 = float(request.GET['n2'])  # Glucose
        val3 = float(request.GET['n3'])  # Blood Pressure
        val4 = float(request.GET['n4'])  # Skin Thickness
        val5 = float(request.GET['n5'])  # Insulin
        val6 = float(request.GET['n6'])  # BMI
        val7 = float(request.GET['n7'])  # Diabetes Pedigree Function
        val8 = float(request.GET['n8'])  # Age

        # Predict
        input_data = np.array([[val1, val2, val3, val4, val5, val6, val7, val8]])
        pred = model.predict(input_data)
        result1 = "Positive" if pred[0] == 1 else "Negative"

        # Save data for chart
        request.session['chart_data'] = {
            "Positive": 1 if result1 == "Positive" else 0,
            "Negative": 1 if result1 == "Negative" else 0
        }
        request.session['result_label'] = result1

        # BMI & Health Recommendations
        recommendations = []
        if val6 < 18.5:
            recommendations.append(
                "Your BMI is low. Include healthy fats like nuts, seeds, and avocados."
            )
        elif 18.5 <= val6 < 25:
            recommendations.append(
                "Your BMI is normal. Maintain this with a balanced diet and daily activity."
            )
        elif 25 <= val6 < 30:
            recommendations.append(
                "You are overweight. Consider reducing sugar and carbs, and increasing exercise."
            )
        else:
            recommendations.append(
                "You are in the obese category. Adopt a structured diet and consult a nutritionist."
            )

        if result1 == "Positive":
            recommendations.append(
                "Since your prediction is Positive, limit processed sugar and refined carbs."
            )
            recommendations.append(
                "Exercise regularly — at least 30 minutes daily (walking, cycling, yoga)."
            )
            recommendations.append(
                "Stay hydrated and follow up with a healthcare provider."
            )

        return render(
            request,
            "result.html",
            {"result2": result1, "recommendations": recommendations},
        )

    except Exception as e:
        messages.error(request, f"Something went wrong: {e}")
        return redirect("predict")


@login_required(login_url='login')
def chart_view(request):
    chart_data = request.session.get(
        'chart_data',
        {"Positive": 0, "Negative": 0, "lt30": 0, "between30_50": 0, "gt50": 0}
    )
    return render(
        request,
        "chart.html",
        {"chart_data": chart_data, "result": request.session.get('result_label', "Unknown")},
    )


@login_required(login_url='login')
def meal_plan_view(request):
    result = request.session.get('result_label', "Unknown")

    if result == "Positive":
        meal_plan = [
            "✅ Breakfast: Oatmeal with almonds and strawberries.",
            "✅ Snack: Apple with a teaspoon of peanut butter.",
            "✅ Lunch: Grilled chicken salad with olive oil dressing.",
            "✅ Snack: Greek yogurt with walnuts.",
            "✅ Dinner: Steamed vegetables and baked salmon.",
        ]
    else:
        meal_plan = [
            "✅ Breakfast: Whole-grain toast with avocado.",
            "✅ Snack: Carrot sticks with hummus.",
            "✅ Lunch: Brown rice with vegetables and tofu.",
            "✅ Snack: A handful of almonds.",
            "✅ Dinner: Grilled chicken with quinoa and steamed broccoli.",
        ]

    return render(
        request,
        "meal_plan.html",
        {"result": result, "meal_plan": meal_plan},
    )


@login_required(login_url='login')
def what_if_food(request):
    food_name = None
    portion = None
    impact = None
    alternative = None

    if request.method == "POST":
        food_name = request.POST.get('food_name')
        portion = request.POST.get('portion')

        unhealthy_foods = {
            "pizza": ("High glycemic impact 🍕 → Consider swapping with salad 🥗", "salad"),
            "burger": ("High glycemic impact 🍔 → Consider swapping with grilled chicken bowl 🐔", "grilled chicken bowl"),
            "cake": ("Very sugary 🍰 → Consider swapping with Greek yogurt with berries 🍓", "Greek yogurt with berries")
        }

        food_name_lower = food_name.lower()
        if food_name_lower in unhealthy_foods:
            impact, alternative = unhealthy_foods[food_name_lower]
        else:
            impact = "Looks like a diabetic-friendly choice! ✅"
            alternative = None

    return render(
        request,
        "what_if_food.html",
        {"food_name": food_name, "portion": portion, "impact": impact, "alternative": alternative},
    )


@login_required(login_url='login')
def puzzle_view(request):
    puzzles = [
        {
            "question": "🤔 What is the healthiest beverage for people with diabetes?",
            "options": ["Fruit Juice", "Regular Soda", "Water 💧", "Sweet Tea"],
            "correct": "Water 💧"
        },
        {
            "question": "🤔 Which of these foods is a whole grain option?",
            "options": ["White Bread", "Brown Rice 🍚", "French Fries", "Candy"],
            "correct": "Brown Rice 🍚"
        },
        {
            "question": "🤔 What is a recommended exercise for diabetic patients?",
            "options": ["Sitting all day", "Watching TV", "Walking 🚶‍♂️", "Smoking"],
            "correct": "Walking 🚶‍♂️"
        },
        {
            "question": "🤔 Which is a low-glycemic fruit?",
            "options": ["Watermelon 🍉", "Mango 🥭", "Strawberries 🍓", "Pineapple 🍍"],
            "correct": "Strawberries 🍓"
        },
        {
            "question": "🤔 What is a good breakfast option for diabetes control?",
            "options": ["Sugary cereal", "Pancakes with syrup", "Oatmeal 🥣 with almonds", "Donuts"],
            "correct": "Oatmeal 🥣 with almonds"
        }
    ]

    # Initialize score if not present
    if "score" not in request.session:
        request.session["score"] = 0

    puzzle = random.choice(puzzles)
    score = request.session["score"]

    return render(request, "puzzle.html", {"puzzle": puzzle, "score": score})

from django.http import JsonResponse

@login_required(login_url='login')
def update_score(request):
    if request.method == "POST":
        # increment score in session
        request.session["score"] = request.session.get("score", 0) + 1
        return JsonResponse({"new_score": request.session["score"]})
    return JsonResponse({"error": "Invalid method"}, status=400)
