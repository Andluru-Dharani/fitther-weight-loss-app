# app.py - Streamlit Web Version (Access via browser link)
# Deploy on Streamlit Cloud for free via GitHub

import streamlit as st
from datetime import datetime
import json

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="FitHer - Weight Loss Tracker",
    page_icon="🌸",
    layout="wide"
)

# ==================== CONFIGURATION ====================
GOAL_START = 60.0
GOAL_TARGET = 50.0
DAILY_CALORIE_TARGET = 1400
WATER_TARGET = 3.0

# ==================== SESSION STATE ====================
if "water_count" not in st.session_state:
    st.session_state.water_count = 0.0
if "weight_log" not in st.session_state:
    st.session_state.weight_log = []
if "tasks_done" not in st.session_state:
    st.session_state.tasks_done = []

today = datetime.now().strftime("%Y-%m-%d")
day_name = datetime.now().strftime("%A")

# ==================== DATA ====================
DAILY_TASKS = {
    "🌅 Morning Routine (6:00 - 7:00 AM)": [
        "Wake up & drink warm lemon water (1 glass)",
        "Yoga/Stretching - 15 minutes",
        "Brisk Walking / Jogging - 30 minutes",
        "Core exercises (plank, crunches) - 10 minutes",
    ],
    "☀️ Mid-Day Activity (12:00 - 12:30 PM)": [
        "Post-lunch walk - 15 minutes",
        "Take stairs instead of elevator",
        "Deep breathing exercises - 5 minutes",
    ],
    "🌆 Evening Workout (5:00 - 6:00 PM)": [
        "Strength training / Bodyweight exercises - 20 min",
        "Cycling / Skipping rope - 15 minutes",
        "Cool-down stretching - 10 minutes",
    ],
    "🌙 Night Routine (9:00 - 10:00 PM)": [
        "Light walk after dinner - 10 minutes",
        "No screen time 30 min before bed",
        "Sleep by 10:30 PM (7-8 hrs sleep)",
    ],
}

WEEKLY_PLAN = {
    "Monday": "🏃 Cardio (Running/Cycling) + Core",
    "Tuesday": "💪 Upper Body Strength + Yoga",
    "Wednesday": "🔥 HIIT (20 min) + Stretching",
    "Thursday": "🦵 Lower Body Strength + Walking",
    "Friday": "🏋️ Full Body Workout + Core",
    "Saturday": "💃 Swimming / Dance / Zumba (Fun Day)",
    "Sunday": "🧘 Active Rest - Yoga + Light Walk",
}

MEAL_PLANS = {
    "Monday": {
        "6:00 AM - Early Morning": "Warm lemon water + 5 soaked almonds | 50 kcal",
        "8:00 AM - Breakfast": "Oats porridge with fruits + green tea | 250 kcal",
        "10:30 AM - Mid-Morning": "1 apple + 10 peanuts | 120 kcal",
        "1:00 PM - Lunch": "2 roti + dal + sabzi + salad + buttermilk | 400 kcal",
        "4:30 PM - Evening Snack": "Sprouts chaat + green tea | 150 kcal",
        "7:30 PM - Dinner": "Vegetable soup + 1 roti + grilled paneer | 350 kcal",
        "9:30 PM - Before Bed": "Warm turmeric milk (low-fat) | 80 kcal",
    },
    "Tuesday": {
        "6:00 AM - Early Morning": "Warm water + chia seeds (1 tsp) | 40 kcal",
        "8:00 AM - Breakfast": "Moong dal chilla (2) + mint chutney + tea | 270 kcal",
        "10:30 AM - Mid-Morning": "1 banana + few walnuts | 130 kcal",
        "1:00 PM - Lunch": "Brown rice (1 cup) + rajma + cucumber raita | 420 kcal",
        "4:30 PM - Evening Snack": "Roasted makhana + green tea | 100 kcal",
        "7:30 PM - Dinner": "Grilled chicken/tofu salad + 1 multigrain roti | 350 kcal",
        "9:30 PM - Before Bed": "Chamomile tea | 5 kcal",
    },
    "Wednesday": {
        "6:00 AM - Early Morning": "Warm water + apple cider vinegar (1 tsp) | 10 kcal",
        "8:00 AM - Breakfast": "Poha with peanuts + lemon + tea | 260 kcal",
        "10:30 AM - Mid-Morning": "Carrot + cucumber sticks with hummus | 110 kcal",
        "1:00 PM - Lunch": "2 roti + palak paneer + salad + curd | 430 kcal",
        "4:30 PM - Evening Snack": "1 boiled egg + green tea (or fruit) | 120 kcal",
        "7:30 PM - Dinner": "Vegetable khichdi + raita | 320 kcal",
        "9:30 PM - Before Bed": "Warm milk with cinnamon | 80 kcal",
    },
    "Thursday": {
        "6:00 AM - Early Morning": "Warm lemon + honey water | 30 kcal",
        "8:00 AM - Breakfast": "Idli (3) + sambar + coconut chutney | 280 kcal",
        "10:30 AM - Mid-Morning": "Papaya slices (1 cup) | 60 kcal",
        "1:00 PM - Lunch": "Quinoa pulao + curd + green salad | 400 kcal",
        "4:30 PM - Evening Snack": "Dhokla (2 pcs) + green tea | 140 kcal",
        "7:30 PM - Dinner": "Mushroom soup + grilled fish/paneer tikka | 350 kcal",
        "9:30 PM - Before Bed": "Jeera water | 5 kcal",
    },
    "Friday": {
        "6:00 AM - Early Morning": "Warm water + methi seeds (soaked) | 20 kcal",
        "8:00 AM - Breakfast": "Smoothie (banana, spinach, yogurt, flax seeds) | 250 kcal",
        "10:30 AM - Mid-Morning": "Handful of mixed dry fruits | 150 kcal",
        "1:00 PM - Lunch": "2 bajra roti + mixed veg + dal + salad | 420 kcal",
        "4:30 PM - Evening Snack": "Fruit chaat (no sugar) + tea | 100 kcal",
        "7:30 PM - Dinner": "Stuffed capsicum + tomato soup + 1 roti | 340 kcal",
        "9:30 PM - Before Bed": "Warm turmeric milk | 80 kcal",
    },
    "Saturday": {
        "6:00 AM - Early Morning": "Coconut water | 45 kcal",
        "8:00 AM - Breakfast": "Besan chilla (2) + curd + tea | 270 kcal",
        "10:30 AM - Mid-Morning": "1 orange + few cashews | 100 kcal",
        "1:00 PM - Lunch": "Chole + 1 roti + onion salad + buttermilk | 430 kcal",
        "4:30 PM - Evening Snack": "Puffed rice (murmura) chaat | 120 kcal",
        "7:30 PM - Dinner": "Egg bhurji/Paneer bhurji + 1 roti + salad | 350 kcal",
        "9:30 PM - Before Bed": "Fennel (saunf) water | 5 kcal",
    },
    "Sunday": {
        "6:00 AM - Early Morning": "Warm lemon water + soaked almonds | 60 kcal",
        "8:00 AM - Breakfast": "Whole wheat pancakes + honey + fruits | 300 kcal",
        "10:30 AM - Mid-Morning": "Buttermilk + roasted chana | 120 kcal",
        "1:00 PM - Lunch": "Rice (1 cup) + sambar + avial + papad | 440 kcal",
        "4:30 PM - Evening Snack": "Homemade veg sandwich (wheat bread) | 150 kcal",
        "7:30 PM - Dinner": "Clear soup + grilled veggies + 1 roti | 300 kcal",
        "9:30 PM - Before Bed": "Warm milk + nutmeg | 80 kcal",
    },
}

# ==================== HEADER ====================
st.markdown("""
<div style='background: linear-gradient(90deg, #FF69B4, #FF1493); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
    <h1 style='color: white; text-align: center; margin: 0;'>🌸 FitHer - Weight Loss Tracker</h1>
    <p style='color: white; text-align: center; margin: 5px 0 0 0;'>Your journey: 60kg → 50kg | Safe & Sustainable</p>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ Quick Stats")
    st.markdown(f"📅 **Today:** {datetime.now().strftime('%A, %B %d, %Y')}")
    st.markdown(f"🎯 **Goal:** {GOAL_TARGET} kg")
    st.markdown(f"🔥 **Daily Calories:** {DAILY_CALORIE_TARGET} kcal")
    st.markdown(f"💧 **Water Target:** {WATER_TARGET} L")
    st.markdown("---")
    st.markdown(f"### 🏋️ Today's Focus")
    st.markdown(f"**{WEEKLY_PLAN.get(day_name, 'Rest Day')}**")
    st.markdown("---")
    st.markdown("### 📊 Weekly Plan")
    for day, workout in WEEKLY_PLAN.items():
        marker = "👉 " if day == day_name else ""
        st.markdown(f"{marker}**{day}:** {workout}")

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard", "✅ Daily Tasks", "🍽️ Meal Plan",
    "💧 Water", "📈 Progress", "💡 Tips"
])

# --- TAB 1: DASHBOARD ---
with tab1:
    col1, col2, col3, col4 = st.columns(4)

    weights = st.session_state.weight_log
    current_weight = weights[-1]["weight"] if weights else GOAL_START
    lost = GOAL_START - current_weight
    remaining = current_weight - GOAL_TARGET
    progress_pct = (lost / (GOAL_START - GOAL_TARGET)) * 100 if (GOAL_START - GOAL_TARGET) > 0 else 0
    progress_pct = max(0, min(100, progress_pct))

    col1.metric("⚖️ Current Weight", f"{current_weight} kg")
    col2.metric("✅ Lost So Far", f"{lost:.1f} kg")
    col3.metric("🔥 Remaining", f"{remaining:.1f} kg")
    col4.metric("📈 Progress", f"{progress_pct:.1f}%")

    st.progress(progress_pct / 100)

    st.markdown("---")

    # Motivation
    import random
    quotes = [
        "💪 *The only bad workout is the one that didn't happen.*",
        "🌟 *Small daily improvements lead to stunning results.*",
        "🔥 *Don't wish for it, work for it.*",
        "🎯 *10 kg is just consistent weeks of dedication away!*",
        "✨ *Your body achieves what your mind believes.*",
        "💖 *Progress, not perfection.*",
    ]
    st.info(random.choice(quotes))

# --- TAB 2: DAILY TASKS ---
with tab2:
    st.markdown("### ✅ Complete Your Daily Tasks")
    st.markdown(f"*Check off each task as you complete it today ({day_name})*")

    total_tasks = 0
    done_tasks = 0

    for category, tasks in DAILY_TASKS.items():
        st.markdown(f"#### {category}")
        for task in tasks:
            total_tasks += 1
            key = f"{category}_{task}"
            checked = st.checkbox(task, key=key)
            if checked:
                done_tasks += 1

    st.markdown("---")
    completion = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0
    st.markdown(f"### 🏆 Today's Completion: **{done_tasks}/{total_tasks}** tasks ({completion:.0f}%)")
    st.progress(completion / 100)

    if completion == 100:
        st.balloons()
        st.success("🎉 Amazing! You completed ALL tasks today! Keep it up!")
    elif completion >= 75:
        st.success("👏 Great job! Almost there!")
    elif completion >= 50:
        st.warning("💪 Halfway done! Keep pushing!")

# --- TAB 3: MEAL PLAN ---
with tab3:
    st.markdown(f"### 🍽️ Today's Meal Plan — {day_name}")

    meals = MEAL_PLANS.get(day_name, MEAL_PLANS["Monday"])
    total_cal = 0

    for time_slot, meal_info in meals.items():
        cal = 0
        if "kcal" in meal_info:
            cal = int(meal_info.split("|")[-1].strip().replace("kcal", "").strip())
            total_cal += cal

        st.markdown(f"""
        <div style='background: #FFFACD; padding: 12px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #FF69B4;'>
            <strong>⏰ {time_slot}</strong><br>
            {meal_info}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"### 📊 Total: ~{total_cal} kcal / {DAILY_CALORIE_TARGET} kcal target")

    st.markdown("---")
    st.markdown("### 🚫 Foods to AVOID")
    avoid_items = [
        "Sugar, sweets, chocolates, pastries",
        "Fried foods (samosa, pakora, chips)",
        "Soft drinks, packaged juices",
        "White bread, maida products",
        "Excessive rice (limit to 1 cup/day)",
        "Late night snacking after 9 PM",
        "Alcohol and processed foods",
    ]
    for item in avoid_items:
        st.markdown(f"❌ {item}")

    st.markdown("---")
    st.markdown("### ✅ Super Foods to INCLUDE")
    super_foods = [
        "Green tea (2-3 cups/day) - boosts metabolism",
        "Protein (dal, eggs, paneer, chicken) - keeps you full",
        "Fiber (oats, vegetables, fruits) - aids digestion",
        "Healthy fats (almonds, walnuts, flaxseeds)",
        "Probiotics (curd, buttermilk) - gut health",
    ]
    for item in super_foods:
        st.markdown(f"✅ {item}")

# --- TAB 4: WATER TRACKER ---
with tab4:
    st.markdown("### 💧 Daily Water Intake")
    st.markdown(f"**Target:** {WATER_TARGET} Liters (12 glasses) per day")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Add 1 Glass (250ml)", use_container_width=True):
            st.session_state.water_count += 0.25
    with col2:
        if st.button("➕ Add 500ml", use_container_width=True):
            st.session_state.water_count += 0.5
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.water_count = 0.0

    water_pct = min(st.session_state.water_count / WATER_TARGET, 1.0)
    st.markdown(f"### 🥤 {st.session_state.water_count:.2f} L / {WATER_TARGET} L")
    st.progress(water_pct)

    glasses = int(st.session_state.water_count * 4)
    total_glasses = int(WATER_TARGET * 4)
    glass_display = "🥤" * glasses + "⬜" * (total_glasses - glasses)
    st.markdown(f"**Glasses:** {glass_display}")

    if st.session_state.water_count >= WATER_TARGET:
        st.success("🎉 You've reached your daily water goal!")

    st.markdown("---")
    st.markdown("### ⏰ Recommended Water Schedule")
    schedule = [
        "6:00 AM - 2 glasses (wake up, empty stomach)",
        "8:00 AM - 1 glass (before breakfast)",
        "10:30 AM - 1 glass",
        "12:30 PM - 1 glass (before lunch)",
        "2:30 PM - 1 glass",
        "4:30 PM - 1 glass",
        "6:00 PM - 1 glass (before workout)",
        "7:00 PM - 1 glass (before dinner)",
        "8:30 PM - 1 glass",
        "9:30 PM - 1 glass (before bed)",
    ]
    for s in schedule:
        st.markdown(f"💧 {s}")

# --- TAB 5: PROGRESS ---
with tab5:
    st.markdown("### 📈 Log Your Weight")

    col1, col2 = st.columns([1, 2])
    with col1:
        weight_input = st.number_input("Enter weight (kg)", min_value=35.0, max_value=100.0, value=60.0, step=0.1)
        if st.button("📝 Log Today's Weight"):
            st.session_state.weight_log.append({
                "date": today,
                "weight": weight_input
            })
            st.success(f"✅ Logged {weight_input} kg for today!")

    with col2:
        if st.session_state.weight_log:
            st.markdown("### 📋 Weight History")
            for entry in reversed(st.session_state.weight_log[-15:]):
                diff_from_goal = entry["weight"] - GOAL_TARGET
                st.markdown(f"📅 **{entry['date']}** → {entry['weight']} kg *({diff_from_goal:.1f} kg from goal)*")

# --- TAB 6: TIPS ---
with tab6:
    st.markdown("### 💡 Weight Loss Tips & Guidelines")

    tips_data = {
        "🔑 Golden Rules": [
            "Calorie deficit is KEY: Eat less than you burn",
            "Aim to lose 0.5-1 kg per week (healthy rate)",
            "Never go below 1200 kcal/day",
            "Consistency > Intensity",
            "Weight fluctuates daily — track weekly averages",
        ],
        "🥗 Nutrition Tips": [
            "Eat protein in every meal (dal, eggs, paneer, chicken)",
            "Fill half your plate with vegetables",
            "Eat slowly — take 20 minutes per meal",
            "Don't skip meals — it slows metabolism",
            "Cook at home — avoid outside food",
            "Use smaller plates to control portions",
        ],
        "🏃 Exercise Tips": [
            "150 min/week moderate exercise (minimum)",
            "Mix cardio + strength training",
            "Morning workouts boost metabolism all day",
            "Don't sit for more than 1 hour continuously",
            "10,000 steps/day is a great baseline goal",
        ],
        "😴 Lifestyle Tips": [
            "Sleep 7-8 hours — poor sleep causes weight gain",
            "Manage stress (cortisol increases belly fat)",
            "Drink water before meals (reduces appetite)",
            "No eating 2-3 hours before bed",
            "Track everything — what gets measured gets managed",
        ],
    }

    for category, tips in tips_data.items():
        with st.expander(category, expanded=True):
            for tip in tips:
                st.markdown(f"• {tip}")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px;'>
    🌸 FitHer - Made with ❤️ | Remember: Consistency is the key to transformation!<br>
    ⚠️ Consult a doctor/nutritionist before starting any weight loss program.
</div>
""", unsafe_allow_html=True)
