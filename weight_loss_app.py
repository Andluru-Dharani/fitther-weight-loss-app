
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import os

# ==================== DATA & CONFIGURATION ====================

GOAL_START = 60.0  # kg
GOAL_TARGET = 50.0  # kg
DAILY_CALORIE_TARGET = 1400  # kcal (safe deficit for female)
WATER_TARGET = 3.0  # liters

# --- DAILY TASKS (Exercise Routine) ---
DAILY_TASKS = {
    "Morning Routine (6:00 - 7:00 AM)": [
        "☀️ Wake up & drink warm lemon water (1 glass)",
        "🧘 Yoga/Stretching - 15 minutes",
        "🏃 Brisk Walking / Jogging - 30 minutes",
        "💪 Core exercises (plank, crunches) - 10 minutes",
    ],
    "Mid-Day Activity (12:00 - 12:30 PM)": [
        "🚶 Post-lunch walk - 15 minutes",
        "🪜 Take stairs instead of elevator",
        "🧘 Deep breathing exercises - 5 minutes",
    ],
    "Evening Workout (5:00 - 6:00 PM)": [
        "🏋️ Strength training / Bodyweight exercises - 20 min",
        "🚴 Cycling / Skipping rope - 15 minutes",
        "🧘 Cool-down stretching - 10 minutes",
    ],
    "Night Routine (9:00 - 10:00 PM)": [
        "🚶 Light walk after dinner - 10 minutes",
        "📵 No screen time 30 min before bed",
        "😴 Sleep by 10:30 PM (7-8 hrs sleep)",
    ],
}

# --- WEEKLY EXERCISE PLAN ---
WEEKLY_PLAN = {
    "Monday": "Cardio (Running/Cycling) + Core",
    "Tuesday": "Upper Body Strength + Yoga",
    "Wednesday": "HIIT (20 min) + Stretching",
    "Thursday": "Lower Body Strength + Walking",
    "Friday": "Full Body Workout + Core",
    "Saturday": "Swimming / Dance / Zumba (Fun Day)",
    "Sunday": "Active Rest - Yoga + Light Walk",
}

# --- MEAL PLAN (7-Day Rotating) ---
MEAL_PLANS = {
    "Monday": {
        "Early Morning (6:00 AM)": "Warm lemon water + 5 soaked almonds | 50 kcal",
        "Breakfast (8:00 AM)": "Oats porridge with fruits + green tea | 250 kcal",
        "Mid-Morning (10:30 AM)": "1 apple + 10 peanuts | 120 kcal",
        "Lunch (1:00 PM)": "2 roti + dal + sabzi + salad + buttermilk | 400 kcal",
        "Evening Snack (4:30 PM)": "Sprouts chaat + green tea | 150 kcal",
        "Dinner (7:30 PM)": "Vegetable soup + 1 roti + grilled paneer | 350 kcal",
        "Before Bed (9:30 PM)": "Warm turmeric milk (low-fat) | 80 kcal",
    },
    "Tuesday": {
        "Early Morning (6:00 AM)": "Warm water + chia seeds (1 tsp) | 40 kcal",
        "Breakfast (8:00 AM)": "Moong dal chilla (2) + mint chutney + tea | 270 kcal",
        "Mid-Morning (10:30 AM)": "1 banana + few walnuts | 130 kcal",
        "Lunch (1:00 PM)": "Brown rice (1 cup) + rajma + cucumber raita | 420 kcal",
        "Evening Snack (4:30 PM)": "Roasted makhana + green tea | 100 kcal",
        "Dinner (7:30 PM)": "Grilled chicken/tofu salad + 1 multigrain roti | 350 kcal",
        "Before Bed (9:30 PM)": "Chamomile tea | 5 kcal",
    },
    "Wednesday": {
        "Early Morning (6:00 AM)": "Warm water + apple cider vinegar (1 tsp) | 10 kcal",
        "Breakfast (8:00 AM)": "Poha with peanuts + lemon + tea | 260 kcal",
        "Mid-Morning (10:30 AM)": "Carrot + cucumber sticks with hummus | 110 kcal",
        "Lunch (1:00 PM)": "2 roti + palak paneer + salad + curd | 430 kcal",
        "Evening Snack (4:30 PM)": "1 boiled egg + green tea (or fruit) | 120 kcal",
        "Dinner (7:30 PM)": "Vegetable khichdi + raita | 320 kcal",
        "Before Bed (9:30 PM)": "Warm milk with cinnamon | 80 kcal",
    },
    "Thursday": {
        "Early Morning (6:00 AM)": "Warm lemon + honey water | 30 kcal",
        "Breakfast (8:00 AM)": "Idli (3) + sambar + coconut chutney | 280 kcal",
        "Mid-Morning (10:30 AM)": "Papaya slices (1 cup) | 60 kcal",
        "Lunch (1:00 PM)": "Quinoa pulao + curd + green salad | 400 kcal",
        "Evening Snack (4:30 PM)": "Dhokla (2 pcs) + green tea | 140 kcal",
        "Dinner (7:30 PM)": "Mushroom soup + grilled fish/paneer tikka | 350 kcal",
        "Before Bed (9:30 PM)": "Jeera water | 5 kcal",
    },
    "Friday": {
        "Early Morning (6:00 AM)": "Warm water + methi seeds (soaked) | 20 kcal",
        "Breakfast (8:00 AM)": "Smoothie (banana, spinach, yogurt, flax seeds) | 250 kcal",
        "Mid-Morning (10:30 AM)": "Handful of mixed dry fruits | 150 kcal",
        "Lunch (1:00 PM)": "2 bajra roti + mixed veg + dal + salad | 420 kcal",
        "Evening Snack (4:30 PM)": "Fruit chaat (no sugar) + tea | 100 kcal",
        "Dinner (7:30 PM)": "Stuffed capsicum + tomato soup + 1 roti | 340 kcal",
        "Before Bed (9:30 PM)": "Warm turmeric milk | 80 kcal",
    },
    "Saturday": {
        "Early Morning (6:00 AM)": "Coconut water | 45 kcal",
        "Breakfast (8:00 AM)": "Besan chilla (2) + curd + tea | 270 kcal",
        "Mid-Morning (10:30 AM)": "1 orange + few cashews | 100 kcal",
        "Lunch (1:00 PM)": "Chole + 1 roti + onion salad + buttermilk | 430 kcal",
        "Evening Snack (4:30 PM)": "Puffed rice (murmura) chaat | 120 kcal",
        "Dinner (7:30 PM)": "Egg bhurji/Paneer bhurji + 1 roti + salad | 350 kcal",
        "Before Bed (9:30 PM)": "Fennel (saunf) water | 5 kcal",
    },
    "Sunday": {
        "Early Morning (6:00 AM)": "Warm lemon water + soaked almonds | 60 kcal",
        "Breakfast (8:00 AM)": "Whole wheat pancakes + honey + fruits | 300 kcal",
        "Mid-Morning (10:30 AM)": "Buttermilk + roasted chana | 120 kcal",
        "Lunch (1:00 PM)": "Rice (1 cup) + sambar + avial + papad | 440 kcal",
        "Evening Snack (4:30 PM)": "Homemade vegetable sandwich (wheat bread) | 150 kcal",
        "Dinner (7:30 PM)": "Clear soup + grilled veggies + 1 roti | 300 kcal",
        "Before Bed (9:30 PM)": "Warm milk + nutmeg | 80 kcal",
    },
}

# --- DATA FILE ---
DATA_FILE = "weight_tracker_data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"weight_log": [], "completed_tasks": {}, "water_log": {}}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ==================== MAIN APP ====================


class WeightLossApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 FitHer - Weight Loss Tracker (60kg → 50kg)")
        self.root.geometry("900x700")
        self.root.configure(bg="#FFF0F5")

        self.data = load_data()
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.day_name = datetime.now().strftime("%A")

        # --- Header ---
        header = tk.Frame(root, bg="#FF69B4", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🌸 FitHer - Daily Weight Loss Tracker",
            font=("Helvetica", 18, "bold"),
            bg="#FF69B4",
            fg="white",
        ).pack(pady=10)

        tk.Label(
            header,
            text=f"📅 {datetime.now().strftime('%A, %B %d, %Y')} | Goal: 60kg → 50kg",
            font=("Helvetica", 11),
            bg="#FF69B4",
            fg="white",
        ).pack()

        # --- Notebook (Tabs) ---
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), padding=[10, 5])

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Tabs
        self.create_dashboard_tab()
        self.create_tasks_tab()
        self.create_meals_tab()
        self.create_water_tab()
        self.create_progress_tab()
        self.create_tips_tab()

    # ==================== TAB 1: DASHBOARD ====================
    def create_dashboard_tab(self):
        tab = tk.Frame(self.notebook, bg="#FFF0F5")
        self.notebook.add(tab, text="📊 Dashboard")

        # Progress Summary
        frame = tk.LabelFrame(
            tab, text="Your Progress Summary", font=("Helvetica", 12, "bold"),
            bg="#FFF0F5", fg="#C71585", padx=20, pady=15
        )
        frame.pack(fill="x", padx=20, pady=10)

        # Calculate progress
        weights = self.data.get("weight_log", [])
        current_weight = weights[-1]["weight"] if weights else GOAL_START
        lost = GOAL_START - current_weight
        remaining = current_weight - GOAL_TARGET
        progress_pct = (lost / (GOAL_START - GOAL_TARGET)) * 100 if (GOAL_START - GOAL_TARGET) > 0 else 0
        progress_pct = max(0, min(100, progress_pct))

        info_text = (
            f"🏁 Start: {GOAL_START} kg  |  🎯 Target: {GOAL_TARGET} kg  |  "
            f"⚖️ Current: {current_weight} kg\n"
            f"✅ Lost: {lost:.1f} kg  |  🔥 Remaining: {remaining:.1f} kg  |  "
            f"📈 Progress: {progress_pct:.1f}%"
        )
        tk.Label(frame, text=info_text, font=("Helvetica", 11), bg="#FFF0F5", justify="left").pack(anchor="w")

        # Progress Bar
        pb_frame = tk.Frame(frame, bg="#FFF0F5")
        pb_frame.pack(fill="x", pady=10)
        tk.Label(pb_frame, text="Progress:", font=("Helvetica", 10), bg="#FFF0F5").pack(side="left")
        progress_bar = ttk.Progressbar(pb_frame, length=500, mode="determinate", value=progress_pct)
        progress_bar.pack(side="left", padx=10)
        tk.Label(pb_frame, text=f"{progress_pct:.1f}%", font=("Helvetica", 10, "bold"), bg="#FFF0F5").pack(side="left")

        # Today's Workout
        workout_frame = tk.LabelFrame(
            tab, text=f"🏋️ Today's Focus ({self.day_name})", font=("Helvetica", 12, "bold"),
            bg="#FFF0F5", fg="#C71585", padx=20, pady=15
        )
        workout_frame.pack(fill="x", padx=20, pady=10)

        workout = WEEKLY_PLAN.get(self.day_name, "Rest Day")
        tk.Label(workout_frame, text=f"💪 {workout}", font=("Helvetica", 12), bg="#FFF0F5").pack(anchor="w")

        # Motivational Quote
        quotes = [
            "\"The only bad workout is the one that didn't happen.\" 💪",
            "\"Your body can stand almost anything. It's your mind you have to convince.\"",
            "\"Small daily improvements lead to stunning results.\" 🌟",
            "\"Don't wish for it, work for it.\" 🔥",
            "\"10 kg is just 10 weeks of dedication away!\" 🎯",
        ]
        import random
        quote = random.choice(quotes)

        quote_frame = tk.LabelFrame(
            tab, text="💬 Today's Motivation", font=("Helvetica", 12, "bold"),
            bg="#FFF0F5", fg="#C71585", padx=20, pady=15
        )
        quote_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(quote_frame, text=quote, font=("Helvetica", 11, "italic"), bg="#FFF0F5", fg="#8B008B").pack()

    # ==================== TAB 2: DAILY TASKS ====================
    def create_tasks_tab(self):
        tab = tk.Frame(self.notebook, bg="#FFF0F5")
        self.notebook.add(tab, text="✅ Daily Tasks")

        # Scrollable frame
        canvas = tk.Canvas(tab, bg="#FFF0F5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#FFF0F5")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.task_vars = []
        completed_today = self.data.get("completed_tasks", {}).get(self.today, [])

        for category, tasks in DAILY_TASKS.items():
            frame = tk.LabelFrame(
                scroll_frame, text=category, font=("Helvetica", 11, "bold"),
                bg="#FFF8F0", fg="#C71585", padx=15, pady=10
            )
            frame.pack(fill="x", padx=20, pady=8)

            for task in tasks:
                var = tk.BooleanVar(value=(task in completed_today))
                cb = tk.Checkbutton(
                    frame, text=task, variable=var, font=("Helvetica", 10),
                    bg="#FFF8F0", activebackground="#FFF8F0",
                    command=self.save_tasks
                )
                cb.pack(anchor="w", pady=2)
                self.task_vars.append((task, var))

        # Save button
        btn_frame = tk.Frame(scroll_frame, bg="#FFF0F5")
        btn_frame.pack(pady=10)
        tk.Button(
            btn_frame, text="💾 Save Progress", font=("Helvetica", 11, "bold"),
            bg="#FF69B4", fg="white", command=self.save_tasks, padx=20, pady=5
        ).pack()

    def save_tasks(self):
        completed = [task for task, var in self.task_vars if var.get()]
        if "completed_tasks" not in self.data:
            self.data["completed_tasks"] = {}
        self.data["completed_tasks"][self.today] = completed
        save_data(self.data)

    # ==================== TAB 3: MEAL PLAN ====================
    def create_meals_tab(self):
        tab = tk.Frame(self.notebook, bg="#FFF0F5")
        self.notebook.add(tab, text="🍽️ Meal Plan")

        tk.Label(
            tab, text=f"🍽️ Today's Meal Plan ({self.day_name})",
            font=("Helvetica", 14, "bold"), bg="#FFF0F5", fg="#C71585"
        ).pack(pady=10)

        meals = MEAL_PLANS.get(self.day_name, MEAL_PLANS["Monday"])

        canvas = tk.Canvas(tab, bg="#FFF0F5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#FFF0F5")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        total_cal = 0
        for time_slot, meal_info in meals.items():
            frame = tk.Frame(scroll_frame, bg="#FFFACD", relief="ridge", bd=1)
            frame.pack(fill="x", padx=20, pady=5)

            tk.Label(
                frame, text=f"⏰ {time_slot}", font=("Helvetica", 10, "bold"),
                bg="#FFFACD", fg="#8B4513"
            ).pack(anchor="w", padx=10, pady=(5, 0))

            tk.Label(
                frame, text=f"   {meal_info}", font=("Helvetica", 10),
                bg="#FFFACD", fg="#333"
            ).pack(anchor="w", padx=10, pady=(0, 5))

            # Extract calories
            if "kcal" in meal_info:
                cal = int(meal_info.split("|")[-1].strip().replace("kcal", "").strip())
                total_cal += cal

        # Total calories
        tk.Label(
            scroll_frame,
            text=f"\n📊 Total Daily Calories: ~{total_cal} kcal (Target: {DAILY_CALORIE_TARGET} kcal)",
            font=("Helvetica", 12, "bold"), bg="#FFF0F5", fg="#C71585"
        ).pack(pady=10)

        # Foods to AVOID
        avoid_frame = tk.LabelFrame(
            scroll_frame, text="🚫 Foods to AVOID", font=("Helvetica", 11, "bold"),
            bg="#FFE4E1", fg="red", padx=15, pady=10
        )
        avoid_frame.pack(fill="x", padx=20, pady=10)

        avoid_items = [
            "❌ Sugar, sweets, chocolates, pastries",
            "❌ Fried foods (samosa, pakora, chips)",
            "❌ Soft drinks, packaged juices",
            "❌ White bread, maida products",
            "❌ Excessive rice (limit to 1 cup/day)",
            "❌ Late night snacking after 9 PM",
            "❌ Alcohol and processed foods",
        ]
        for item in avoid_items:
            tk.Label(avoid_frame, text=item, font=("Helvetica", 10), bg="#FFE4E1").pack(anchor="w")

    # ==================== TAB 4: WATER TRACKER ====================
    def create_water_tab(self):
        tab = tk.Frame(self.notebook, bg="#FFF0F5")
        self.notebook.add(tab, text="💧 Water")

        tk.Label(
            tab, text="💧 Daily Water Intake Tracker",
            font=("Helvetica", 14, "bold"), bg="#FFF0F5", fg="#1E90FF"
        ).pack(pady=15)

        tk.Label(
            tab, text=f"Target: {WATER_TARGET} Liters (12 glasses) per day",
            font=("Helvetica", 11), bg="#FFF0F5"
        ).pack()

        # Current water intake
        today_water = self.data.get("water_log", {}).get(self.today, 0)

        self.water_var = tk.DoubleVar(value=today_water)

        # Display
        self.water_label = tk.Label(
            tab, text=f"🥤 Today: {today_water:.1f} L / {WATER_TARGET} L",
            font=("Helvetica", 16, "bold"), bg="#FFF0F5", fg="#1E90FF"
        )
        self.water_label.pack(pady=20)

        # Glasses visual
        self.glasses_frame = tk.Frame(tab, bg="#FFF0F5")
        self.glasses_frame.pack(pady=10)
        self.update_glasses_display(today_water)

        # Buttons
        btn_frame = tk.Frame(tab, bg="#FFF0F5")
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame, text="+ 1 Glass (250ml)", font=("Helvetica", 11, "bold"),
            bg="#87CEEB", fg="black", command=lambda: self.add_water(0.25), padx=15, pady=5
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame, text="+ 500ml", font=("Helvetica", 11, "bold"),
            bg="#4682B4", fg="white", command=lambda: self.add_water(0.5), padx=15, pady=5
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame, text="Reset", font=("Helvetica", 11),
            bg="#FF6347", fg="white", command=self.reset_water, padx=15, pady=5
        ).pack(side="left", padx=10)

        # Water schedule
        schedule_frame = tk.LabelFrame(
            tab, text="⏰ Recommended Water Schedule", font=("Helvetica", 11, "bold"),
            bg="#F0F8FF", fg="#1E90FF", padx=15, pady=10
        )
        schedule_frame.pack(fill="x", padx=40, pady=20)

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
        for item in schedule:
            tk.Label(schedule_frame, text=f"  💧 {item}", font=("Helvetica", 10), bg="#F0F8FF").pack(anchor="w", pady=1)

    def update_glasses_display(self, liters):
        for widget in self.glasses_frame.winfo_children():
            widget.destroy()
        glasses_filled = int(liters * 4)  # 4 glasses per liter
        total_glasses = int(WATER_TARGET * 4)
        for i in range(total_glasses):
            color = "#1E90FF" if i < glasses_filled else "#D3D3D3"
            lbl = tk.Label(self.glasses_frame, text="🥤", font=("Helvetica", 14), bg="#FFF0F5", fg=color)
            lbl.grid(row=0, column=i, padx=2)

    def add_water(self, amount):
        if "water_log" not in self.data:
            self.data["water_log"] = {}
        current = self.data["water_log"].get(self.today, 0)
        current += amount
        self.data["water_log"][self.today] = current
        save_data(self.data)
        self.water_label.config(text=f"🥤 Today: {current:.1f} L / {WATER_TARGET} L")
        self.update_glasses_display(current)
        if current >= WATER_TARGET:
            messagebox.showinfo("🎉 Great!", "You've reached your daily water goal! Keep it up!")

    def reset_water(self):
        if "water_log" not in self.data:
            self.data["water_log"] = {}
        self.data["water_log"][self.today] = 0
        save_data(self.data)
        self.water_label.config(text=f"🥤 Today: 0.0 L / {WATER_TARGET} L")
        self.update_glasses_display(0)

    # ==================== TAB 5: PROGRESS (WEIGHT LOG) ====================
    def create_progress_tab(self):
        tab = tk.Frame(self.notebook, bg="#FFF0F5")
        self.notebook.add(tab, text="📈 Progress")

        tk.Label(
            tab, text="📈 Weight Progress Tracker",
            font=("Helvetica", 14, "bold"), bg="#FFF0F5", fg="#C71585"
        ).pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(tab, bg="#FFF0F5")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Today's Weight (kg):", font=("Helvetica", 11), bg="#FFF0F5").pack(side="left", padx=5)
        self.weight_entry = tk.Entry(input_frame, font=("Helvetica", 11), width=8)
        self.weight_entry.pack(side="left", padx=5)

        tk.Button(
            input_frame, text="📝 Log Weight", font=("Helvetica", 11, "bold"),
            bg="#FF69B4", fg="white", command=self.log_weight, padx=10
        ).pack(side="left", padx=10)

        # Weight History
        history_frame = tk.LabelFrame(
            tab, text="📋 Weight History (Last 30 entries)", font=("Helvetica", 11, "bold"),
            bg="#FFF8F0", fg="#C71585", padx=15, pady=10
        )
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview for history
        columns = ("Date", "Weight (kg)", "Change", "From Goal")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.refresh_weight_history()

        # Estimated timeline
        weights = self.data.get("weight_log", [])
        if len(weights) >= 2:
            first = weights[0]
            last = weights[-1]
            days_elapsed = (datetime.strptime(last["date"], "%Y-%m-%d") - datetime.strptime(first["date"], "%Y-%m-%d")).days
            if days_elapsed > 0:
                rate = (first["weight"] - last["weight"]) / days_elapsed  # kg per day
                if rate > 0:
                    remaining_kg = last["weight"] - GOAL_TARGET
                    est_days = int(remaining_kg / rate)
                    est_date = (datetime.now() + timedelta(days=est_days)).strftime("%B %d, %Y")
                    tk.Label(
                        tab,
                        text=f"📅 Estimated Goal Date: {est_date} (at current rate of {rate*7:.2f} kg/week)",
                        font=("Helvetica", 11, "bold"), bg="#FFF0F5", fg="#228B22"
                    ).pack(pady=5)

    def log_weight(self):
        try:
            weight = float(self.weight_entry.get())
            if weight < 30 or weight > 150:
                messagebox.showerror("Error", "Please enter a realistic weight (30-150 kg)")
                return

            if "weight_log" not in self.data:
                self.data["weight_log"] = []

            # Check if already logged today
            for entry in self.data["weight_log"]:
                if entry["date"] == self.today:
                    entry["weight"] = weight
                    save_data(self.data)
                    self.refresh_weight_history()
                    messagebox.showinfo("Updated", f"Today's weight updated to {weight} kg!")
                    return

            self.data["weight_log"].append({"date": self.today, "weight": weight})
            save_data(self.data)
            self.refresh_weight_history()
            self.weight_entry.delete(0, tk.END)
            messagebox.showinfo("Logged! ✅", f"Weight {weight} kg logged for today!")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def refresh_weight_history(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        weights = self.data.get("weight_log", [])[-30:]
        for i, entry in enumerate(reversed(weights)):
            change = ""
            if i < len(weights) - 1:
                prev = weights[len(weights) - 2 - i]["weight"]
                diff = entry["weight"] - prev
                change = f"{'🔻' if diff < 0 else '🔺'} {abs(diff):.1f} kg"

            from_goal = entry["weight"] - GOAL_TARGET
            self.tree.insert("", "end", values=(
                entry["date"], f"{entry['weight']:.1f}",
                change, f"{from_goal:.1f} kg away"
            ))

    # ==================== TAB 6: TIPS ====================
    def create_tips_tab(self):
        tab = tk.Frame(self.notebook, bg="#FFF0F5")
        self.notebook.add(tab, text="💡 Tips")

        canvas = tk.Canvas(tab, bg="#FFF0F5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#FFF0F5")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(
            scroll_frame, text="💡 Weight Loss Tips & Guidelines",
            font=("Helvetica", 14, "bold"), bg="#FFF0F5", fg="#C71585"
        ).pack(pady=10)

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
            "⚠️ Common Mistakes": [
                "Crash dieting (causes muscle loss + rebound)",
                "Skipping breakfast",
                "Relying only on cardio (add strength training!)",
                "Weighing daily and getting discouraged",
                "Drinking calories (juices, sugary coffee, soda)",
            ],
        }

        for category, tips in tips_data.items():
            frame = tk.LabelFrame(
                scroll_frame, text=category, font=("Helvetica", 11, "bold"),
                bg="#FFF8F0", fg="#8B008B", padx=15, pady=10
            )
            frame.pack(fill="x", padx=20, pady=8)

            for tip in tips:
                tk.Label(frame, text=f"  • {tip}", font=("Helvetica", 10), bg="#FFF8F0", anchor="w").pack(anchor="w", pady=1)


# ==================== RUN APP ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = WeightLossApp(root)
    root.mainloop()

