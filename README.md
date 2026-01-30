# 🕹️ Pac-Man Capture the Flag — Multi-Agent Artificial Intelligence

This project implements a **two-agent adversarial AI system** for the Pac-Man Capture the Flag environment, developed as the final project for **CSE 140: Artificial Intelligence** at the University of California, Santa Cruz.

The goal was to design intelligent agents capable of **real-time decision-making** in a competitive, partially observable environment with strict time constraints.

---

## 🧠 Project Overview

The system consists of two cooperating agents:

- **Offensive Agent**  
  Focuses on efficient food collection while dynamically balancing risk, safety, and return timing.

- **Defensive Agent**  
  Protects home territory by detecting invaders, prioritizing threats, and intercepting opponents before food is stolen.

Both agents operate using **feature-based evaluation functions** with manually tuned weights, allowing fast, reactive behavior without expensive search.

---

## ⚙️ Technical Approach

- **Feature-Based Evaluation**  
  Each possible action is scored using a linear combination of state features such as:
  - Distance to food
  - Distance to enemies
  - Number of invaders
  - Safety (home vs. enemy side)
  - Game score and remaining time

- **Dynamic Return Logic (Offense)**  
  The offensive agent switches from exploration to safety based on:
  - Amount of food carried
  - Proximity to enemy ghosts
  - Current score and time remaining

- **Threat-Based Prioritization (Defense)**  
  Defensive behavior is driven by a custom threat metric that accounts for:
  - Distance to invaders
  - Proximity of invaders to defended food
  - Patrol stability and oscillation prevention

- **Reactive Architecture**  
  The agents evaluate only successor states, ensuring decisions are made well within the 3-second action limit.

---

## 📊 Results & Evaluation

- **9/10 average performance** against baseline autograder agents  
- **38 / 56 final tournament score**  
- Zero timeouts under competition constraints  
- Consistent success against baseline and simpler adversarial strategies

---

## 🛠 Skills & Concepts Gained

Through this project, I developed hands-on experience with:

- **Multi-Agent Systems & Adversarial AI**
- **Heuristic Design & Feature Engineering**
- **Real-Time Decision Making under Constraints**
- **Risk–Reward Tradeoff Modeling**
- **Manual Weight Tuning & Performance Evaluation**
- **Debugging Emergent Agent Behavior**
- **Collaborative AI Development in Team Settings**

This project strengthened my ability to translate **theoretical AI concepts** into **practical, performant systems**.

---

## 🧰 Technologies Used

- **Language:** Python  
- **Concepts:** Artificial Intelligence, Multi-Agent Systems, Heuristic Evaluation  
- **Techniques:** Feature Engineering, Adversarial Reasoning, Reactive Control

---

## 📄 Report

A detailed technical report describing the system design, feature selection, weight tuning, and evaluation results is included in the `report/` directory.

---
