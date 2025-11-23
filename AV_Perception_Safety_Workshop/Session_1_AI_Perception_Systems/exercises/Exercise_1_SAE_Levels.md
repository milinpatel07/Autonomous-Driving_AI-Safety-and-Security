# Exercise 1: Understanding SAE Automation Levels

**Session 1: AI-based Perception Systems**
**Difficulty:** Beginner

---

## 🎯 Learning Objectives

After completing this exercise, you will be able to:
- Classify real-world autonomous vehicles by SAE level
- Understand the difference between driver assistance and automation
- Identify the critical Level 2 → Level 3 transition
- Define appropriate Operational Design Domains (ODDs)

---

## Part A: Vehicle Classification

### Task 1: Classify by SAE Level

For each vehicle/system below, determine the **SAE automation level (0-5)**.

| # | System | Your Answer | Reasoning |
|---|--------|-------------|-----------|
| 1 | Tesla Model 3 with Autopilot (highway, driver monitoring) | | |
| 2 | Waymo autonomous taxi (Phoenix, AZ, no driver) | | |
| 3 | Mercedes-Benz S-Class with Drive Pilot (German highway, <60 km/h) | | |
| 4 | Honda Civic with Adaptive Cruise Control only | | |
| 5 | Cruise robotaxi (San Francisco, geofenced, no driver) | | |
| 6 | BMW 7 Series with Lane Keeping Assist + ACC | | |
| 7 | Traditional 2010 Toyota Camry (no ADAS features) | | |
| 8 | Audi A8 with Traffic Jam Pilot (never released to public) | | |

**Instructions:**
1. Fill in "Your Answer" column with level (0-5)
2. Write brief reasoning (1 sentence)
3. Check your answers in `solutions/exercise_1_solution.md` after completing

---

### Task 2: Critical Distinction - Level 2 vs Level 3

Answer these questions:

1. **What is the KEY difference between Level 2 and Level 3?**

   Your answer:
   ```


   ```

2. **Why is Level 3 considered "dangerous" by some manufacturers (e.g., Tesla, Waymo)?**

   Your answer:
   ```


   ```

3. **Who is legally responsible for a crash in:**
   - Level 2 system?
     ```

     ```
   - Level 3 system (during automated mode)?
     ```

     ```

---

## Part B: Operational Design Domain (ODD)

### Task 3: Define ODD for Campus Shuttle

**Scenario:** You are designing a **Level 4 autonomous shuttle** for a university campus.

**Define a safe and realistic ODD:**

| ODD Parameter | Your Definition | Justification |
|---------------|-----------------|---------------|
| **Geography** (where?) | | |
| **Road Types** | | |
| **Speed Limit** | | |
| **Weather** | | |
| **Time of Day** | | |
| **Excluded Scenarios** | | |

**Example:**
```
Geography: Campus roads within 2 km radius of student center
Road Types: Paved roads with speed bumps, pedestrian crossings
Speed Limit: Maximum 25 km/h
Weather: Clear, light rain only (no operation in heavy rain, snow, fog)
Time of Day: Daylight hours (8 AM - 6 PM), avoid darkness
Excluded Scenarios: No operation during large events (football games, graduation)
```

Now define your ODD above!

---

### Task 4: ODD Boundary Analysis

For your campus shuttle ODD:

1. **What happens if the shuttle encounters heavy fog?**

   Your answer:
   ```


   ```

2. **How should the system detect it's leaving the ODD?**

   Your answer:
   ```


   ```

3. **What is the safest action when exiting ODD?**

   Your answer:
   ```


   ```

---

## Part C: Real-World Examples (Bonus - 5 min)

### Task 5: Research Current Systems

Research one of these systems and complete the table:

| System | Tesla FSD | Mercedes Drive Pilot | Waymo One |
|--------|-----------|---------------------|-----------|
| **Official SAE Level** | | | |
| **ODD - Geography** | | | |
| **ODD - Weather** | | | |
| **ODD - Speed** | | | |
| **Driver Role** | | | |
| **Biggest Limitation** | | | |

**Sources:**
- Tesla FSD: https://www.tesla.com/autopilot
- Mercedes Drive Pilot: https://www.mercedes-benz.com/en/innovation/autonomous/drive-pilot/
- Waymo One: https://waymo.com/waymo-one/

---

## ✅ Self-Check

Before looking at solutions, verify:

- [ ] I can explain the difference between Levels 0, 1, 2, 3, 4, 5
- [ ] I understand why Level 2 → 3 is a critical jump
- [ ] I can define a realistic ODD for a given system
- [ ] I know why ODD boundaries matter for safety
- [ ] I can classify real-world vehicles by SAE level

---

## 💡 Discussion Questions

Think about or discuss with others:

1. **Why do Tesla and Waymo avoid Level 3?**
   - Tesla: Went straight from Level 2 to targeting Level 4/5
   - Waymo: Went straight from Level 2 to Level 4 (no Level 3)

2. **Is Level 5 realistic? When?**
   - What technical challenges remain?
   - What infrastructure is needed?

3. **Which level is safest?**
   - Level 0 (human control)?
   - Level 2 (human supervising)?
   - Level 4 (system control in ODD)?

---

## 📚 Additional Resources

- **SAE J3016 Standard:** https://www.sae.org/standards/content/j3016_202104/
- **NHTSA AV Policy:** https://www.nhtsa.gov/technology-innovation/automated-vehicles-safety
- **Mercedes Drive Pilot Approval:** https://www.mercedes-benz.com/en/innovation/autonomous/drive-pilot/

---

## ✏️ Solutions

Don't peek until you've tried! Solutions in: `solutions/exercise_1_solution.md`

---

*Exercise created by Milin Patel | Hochschule Kempten*
*Last updated: 2025-01-17*
