# Cisco Forecast League — Final Showcase Presentation Content (v3 — UPDATED)

> **Purpose**: Slide-by-slide content for 10-minute presentation to Senior Cisco Leaders  
> **Event**: CFL Final Showcase | April 10, 2026 | 10:30 AM – 12:30 PM  
> **Team**: Aarya, Manas, Pranav  

---

## SLIDE 1 — Team Introduction

**Title**: Team [Your Team Name] — Cisco Forecast League Finalists

**Content**:
- Headshots, full names, college name, and course of study for all 3 members
- Tagline: *"Data-driven demand forecasting through iterative model refinement"*

**Speaker**: Any (15 seconds)

---

## SLIDE 2 — Dream Team & The Challenge

**Title**: The Dream Team: 20 Products × FY26 Q2

**Content**:

**The Task**: Predict FY26 Q2 unit bookings for 20 Cisco products — Switches, Routers, IP Phones, Wireless APs, and Security Firewalls.

**Data We Had**:

| Data Source | What It Gave Us |
|-------------|----------------|
| Actual Bookings | 12 quarters of demand history (FY23Q2 → FY26Q1) |
| Expert Forecasts | DP, Marketing, DS team predictions for Q2 |
| Accuracy/Bias | 3-quarter track record per expert per product |
| Big Deal | Deal-level decomposition (8 quarters) |
| SCMS / VMS | Sales channel + industry vertical breakdowns |

**Key Challenge**: Products span different lifecycle stages — *Sustaining*, *Sustaining-Growth*, *Decline* — each needs a different forecasting approach.

**Speaker**: Pranav (~45 seconds)

**Talking Points**:
- "We had a rich, multi-dimensional dataset — actuals, expert forecasts with tracked accuracy, and channel-level segment data."
- "The core insight: this isn't one-size-fits-all. A WiFi AP with Q2 budget-flush spikes behaves completely differently from an IP Phone in decline."

---

## SLIDE 3 — Phase 1 Methodology (Condensed)

**Title**: Phase 1: The 6-Step Forecasting Engine (30 Products)

**Content**:

Our Phase 1 pipeline — a **6-step demand planning approach** aligned with Cisco's methodology:

| Step | What It Does |
|------|-------------|
| 1. WMA | Last 4 quarters, weights [1,2,3,4]/10 — 40% on most recent |
| 2. Big Deal Cleaning | If big deals >10% of total → use Avg Deals baseline |
| 3. Expert Ensemble | Bias-corrected blend of DP, MK, DS with outlier removal |
| 4. Lifecycle Blending | Sustaining: 25/25/50 · Decline: 40/30/30 · NPI: 10/5/85 |
| 5. Q2 Seasonal Index | Seasonal multiplier bounded [0.70, 1.40] |
| 6. Sanity Checks | Asymmetric loss penalty + QoQ bounds ±30% |

**Phase 1 v2 Key Innovations**:
- **Damped Trend**: Cut volatile-product error from 42.7% → 34.1% MAPE
- **Accuracy²-Weighted Ensemble**: Reduced ensemble error by 2.4pp
- **Recency-Weighted Seasonality**: 60% FY25Q2 + 30% FY24Q2 + 10% FY23Q2

**Speaker**: Pranav (~1 minute)

**Talking Points**:
- "Phase 1 was our foundation — a complete pipeline from WMA through lifecycle blending."
- "Two key innovations: damped trends (-8.6pp MAPE on volatile products) and accuracy-squared expert weighting (-2.4pp ensemble error)."

---

## SLIDE 4 — Phase 2 Evolution: Version Journey

**Title**: Phase 2: Disciplined Iteration (v5.0 → v6.1)

**Content**:

| Version | Author | Key Innovation |
|---------|--------|---------------|
| **v5.0** | Pranav | Forensic audit: dominant expert rule, acc³ weighting, 3 independent structural signals |
| **v6.0** | Manas | Research-backed: damped-equal weights (Clemen 1989), pattern-based rules |
| **v6.1** | Manas | Backtest-validated: MA4 revert, seasonal naive safety net |

**The Discipline**: Every change backed by academic research or backtesting — **never intuition alone**.

**Critical v6.1 Moment**: Backtest revealed 2 of v6.0's 7 changes *hurt* accuracy. We had the intellectual honesty to revert.

**Speaker**: Manas (~1.5 minutes)

**Talking Points**:
- "v5.0 found 8 flaws in v4.0 — including a 60% over-forecast on Product #4 from noisy acc² weighting."
- "v6.0 applied the 'forecast combination puzzle' from Clemen 1989 — 50+ years of research showing equal weights beat accuracy-based weights."
- "The pivotal moment: v6.1's backtest proved 2 changes hurt. We reverted. That discipline defines our approach."

---

## SLIDE 5 — Core Engine Deep-Dive

**Title**: The Engine: Expert-Anchored Ensemble with Structural Guardrails

**Content**:

```
┌──────────────────────────────────────────────────┐
│             EXPERT LAYER                         │
│  3 teams (DP, Marketing, DS) → Bias Correction   │
│  → Damped Equal Weights (60% equal + 40% acc¹)  │
│  → Outlier Cap (>2× median removed)             │
├──────────────────────────────────────────────────┤
│          STRUCTURAL LAYER                        │
│  Signal 1: Q2/Q1 Ratio × FY26Q1                 │
│  Signal 2: YoY Q2 Growth × FY25Q2               │
│  Signal 3: MA4 (last 4 quarters average)         │
│  → Median of 3 independent signals               │
│  → Decline caps / Growth floors                   │
├──────────────────────────────────────────────────┤
│     ADAPTIVE BLEND                               │
│  Expert weight = f(avg_accuracy) ∈ [35%, 90%]    │
│  final = expert × w + structural × (1-w)        │
└──────────────────────────────────────────────────┘
```

**Key Design Decisions**:
1. **Damped Equal Weights** (Clemen 1989) — accuracy estimates on 3 quarters are noisy; equal weights prevent amplifying that noise
2. **3 Independent Structural Signals** — forensic audit found 5 of 7 original signals were correlated; pruned to 3 truly independent ones
3. **Expert Weight [35%–90%]** — backtest showed structural signals barely beat seasonal naive (MASE ~1.04); experts add more value

**Speaker**: Aarya (~1.5 minutes)

**Talking Points**:
- "Two-layer system: experts anchor, structural signals guardrail."
- "We chose independence over volume — 5 of 7 signals were the same data repackaged. We pruned to 3."
- "The blend adapts per product — high-accuracy experts dominate; unreliable ones defer to structural signals."

---

## SLIDE 6 — Phase 1 Accuracy Results

**Title**: Phase 1 Results: Our Foundation Performance

**Content**:

**Phase 1 Accuracy** (30 products, v2 engine):

| Metric | Value |
|--------|-------|
| Overall Cisco Accuracy | **~77%** |
| Best products | Stable sustaining products with strong expert consensus |
| Weakest products | High-volatility NPI products with limited history |
| Key learning | Expert accuracy is the #1 predictor of forecast quality |

**What Phase 1 Taught Us**:
- Accuracy²-weighted ensemble outperformed equal weights by 2.4pp
- Damped trend was essential for volatile products (-8.6pp MAPE)
- Q2 seasonal spikes were systematically under-forecasted by experts
- Products with big deal concentration are inherently less predictable

**Speaker**: Pranav (~45 seconds)

---

## SLIDE 7 — Phase 2 Accuracy Results

**Title**: Phase 2 Results Against Real Q2 FY26 Actuals

**Content**:

**6 Products with >85% Accuracy**:

| # | Product | Forecast | Actual | Accuracy |
|---|---------|:-------:|:-----:|:--------:|
| 9 | Phone Desk_2 | 6,758 | 6,678 | **98.8%** |
| 14 | SW 8P Ethernet | 9,771 | 9,499 | **97.1%** |
| 13 | SW DC Modular | 385 | 415 | **92.8%** |
| 2 | SW 8P PoE+ Fiber | 5,756 | 5,243 | **90.2%** |
| 10 | Phone Desk_3 | 7,281 | 8,312 | **87.6%** |
| 16 | NGFW_2 | 348 | 402 | **86.6%** |

**Additional solid performers (70–85%)**:

| # | Product | Forecast | Actual | Accuracy |
|---|---------|:-------:|:-----:|:--------:|
| 8 | Phone Video | 4,644 | 3,936 | **82.0%** |
| 1 | WiFi AP Indoor | 7,598 | 6,162 | **76.7%** |
| 19 | RTR 4P PoE | 4,067 | 3,251 | **74.9%** |

**Pattern**: Best accuracy on products with **stable demand + strong expert consensus** — exactly what theory predicts.

**Speaker**: Aarya (~1 minute)

---

## SLIDE 8 — The Demand Surge: What Nobody Predicted

**Title**: Honest Analysis: The Q2 FY26 Demand Surge

**Content**:

Total actual = **95,711** vs predictions ~70K-75K. A **~30% surge** no model or expert predicted.

**The 4 "Black Swan" Products**:

| # | Product | Our Forecast | Actual | Surge |
|---|---------|:-----------:|:------:|:-----:|
| 4 | Phone Desk_1 | 13,298 | **28,011** | **2.1×** |
| 3 | RTR Branch LTE | 5,471 | **10,486** | **1.9×** |
| 11 | SW 24P HP PoE | 668 | **1,803** | **2.7×** |
| 20 | RTR LTE Wireless | 1,556 | **4,008** | **2.6×** |

Products #4 and #3 carry **55.6% of cost weight** — their 2× surge drove everyone's accuracy down.

**The Takeaway**: These surges represent event-driven demand (enterprise refresh deals, SD-WAN waves) that lies outside the predictable envelope of statistical forecasting.

**Speaker**: Manas (~1 minute)

**Talking Points**:
- "Products #4 and #3 experienced 2× demand surges nobody predicted — not us, not the expert teams."
- "Phone Desk_1 was labeled 'Decline' but hit 28,011 — higher than any Q2 in history. This is big-deal-driven demand."
- "Recognizing the boundary between forecastable and unforecastable demand is itself a critical skill."

---

## SLIDE 9 — Business Insights

**Title**: Business Insights from Our Analysis

**Content**:

### 1. IP Phone Portfolio: The Desk_1 Anomaly
- Desk_2: 98.8% accuracy | Desk_3: 87.6% accuracy | **Desk_1: 2× surge**
- The surge was concentrated in ONE product, not across the portfolio
- **Insight**: Likely a single massive enterprise refresh deal — not a market shift

### 2. WiFi6 AP: The Q2 Budget-Flush Cycle
- Q2 history: 2,284 → 6,651 → 8,293 — consistent Q2 spike
- Experts systematically under-forecast Q2 for this product
- **Insight**: Enterprise procurement cycles concentrate in Q2; experts miss the magnitude

### 3. Security Firewalls: Accelerating Contraction
- NGFW_1: 654 → 1,116 → 748 → 479 | NGFW_2: 610 → 512 → 659 → 316
- **Insight**: Cloud-native security (SASE, Umbrella) cannibalizing on-prem firewall demand

### 4. Expert Consensus = Best Predictor
- Products with strong expert agreement → 90%+ accuracy
- Products with expert disagreement → high uncertainty
- **Insight**: Expert consensus quality is the #1 predictor of forecast accuracy

**Speaker**: Pranav (~1 minute)

---

## SLIDE 10 — What Made Our Approach Robust

**Title**: Our Methodology Strengths

**Content**:

**1. Forensic Audit Discipline**
- Found 8 flaws in v4.0 including 60% over-forecast on Product #4
- Backtest revealed changes that hurt → reverted them

**2. Signal Independence**
- Pruned from 7 to 3 structural signals (5 were correlated)
- Clean signals → 90%+ accuracy on those products

**3. Adaptive Expert-Structural Blend**
- Automatically trusts experts more when reliable, structural more when not

**4. Complexity Discipline**
- Built a more complex version with extra features — rejected it
- M4/M5 research: simpler models generalize better

**Speaker**: Aarya (~45 seconds)

---

## SLIDE 11 — Summary & Closing

**Title**: What We Learned & What We'd Do Next

**Content**:

| Metric | Value |
|--------|-------|
| Products >85% accuracy | **6 out of 20** (30%) |
| Products >70% accuracy | **12 out of 20** (60%) |
| Best prediction | Phone Desk_2: **98.8%** |
| Biggest challenge | 2 products (55.6% cost weight) surged 2× |

**What We'd Do With More Time**:
1. **Demand decomposition** — separate base demand from big-deal demand
2. **Leading indicators** — use SCMS channel trends as forward-looking signals
3. **Scenario modeling** — generate upside/downside scenarios instead of point forecasts

**Closing**: *"Demand forecasting isn't about predicting the unpredictable — it's about maximizing accuracy on forecastable demand while being honest about limitations."*

**Speaker**: All three (30 seconds each)

---

# Q&A PREPARATION — Expected Questions & Answers

---

## Q1: "Your portfolio total was off by 22%. How do you explain that?"

**Answer**: Products #4 and #3 carry 55.6% of the cost weight. Both experienced 2× demand surges that nobody predicted — not our model, not the expert teams. Phone Desk_1 was labeled "Decline" and had been trending down for 2 years. Then Q2 FY26 hit 28,011 — the highest in three years. This is big-deal-driven demand that requires pipeline intelligence (deal registration data) not available in our dataset. Remove these two products and our remaining accuracy is significantly stronger.

---

## Q2: "Which products are you most proud of?"

**Answer**: Phone Desk_2 (#9) at **98.8%** — predicted 6,758 vs actual 6,678. This product had terrible expert agreement (DS forecasted 29,553, DP forecasted 6,500). Our system correctly identified DS as an outlier, leaned on structural signals, and produced near-perfect accuracy despite wildly divergent inputs. Also Switch 8P Ethernet (#14) at **97.1%** — a product with only 1 year of Q2 history that we handled by leaning on MK's 83% accuracy.

---

## Q3: "Why damped-equal weights instead of accuracy-based?"

**Answer**: The "forecast combination puzzle" (Clemen 1989) — 50+ years of research showing equal weights beat accuracy-based weights because accuracy estimates (measured on 3 quarters) are noisy. Our v5.0 used acc³ weighting and it caused a 60% over-forecast on Product #4 because DS (68% accuracy, 22,593 forecast) dominated. Our 60/40 damped-equal compromise captures skill differences without amplifying noise.

---

## Q4: "If structural signals barely beat seasonal naive, why use them?"

**Answer**: Two roles: (1) **Catching regime changes** — seasonal naive = FY25Q2, but when FY26Q1 drops 40%, last year's Q2 is stale. Q2/Q1 ratio uses current Q1 as base. (2) **Providing bounds** — structural signals set caps for decline products and floors for growth products, preventing extreme expert-driven forecasts.

---

## Q5: "What would you do differently knowing the actuals?"

**Answer**: (1) **Demand decomposition** — separate base demand from big-deal demand. Phone Desk_1's 28K was likely 13K base + 15K big deal. (2) **Scenario modeling** — generate upside scenarios instead of just point forecasts. (3) **Leading indicator overlay** — use SCMS channel data for forward-looking procurement momentum signals.

---

## Q6: "Can you walk through one product end-to-end?"

**Product #9 — Phone Desk_2 (98.8% accuracy):**

1. **History**: Q2 = 8,791 → 6,184 → 7,891. FY26Q1 = 6,871.
2. **Expert forecasts**: DP=6,500, MK=5,262, DS=29,553.
3. **Outlier cap**: DS >2× median → capped.
4. **Bias correction**: DP +33.5% bias → 6,064. MK -13.4% → 5,402.
5. **Expert blend** (damped equal): 7,717
6. **Structural**: ratio_fc=3,067, YoY=8,262, MA4=14,727 → median 6,438
7. **Blend**: 56% Expert + 44% Structural = 7,155, scaled to **6,758**
8. **Actual**: 6,678 → **98.8% accuracy**

---

## Q7: "How does Cisco Accuracy work?"

**Answer**: `Cisco Accuracy = max(0, 1 - |forecast - actual| / actual)`. 10% error = 90% accuracy. Over-forecasting >100% = 0%. The competition uses **cost-weighted accuracy** — higher-cost products have more impact.

---

## Q8: "Phone Desk_1 was labeled Decline but surged 2×. What does that tell us?"

**Answer**: The PLC label was correct based on history: 22,557 → 14,391 → 19,180. Then something happened — likely a major enterprise refresh or end-of-support migration. This highlights that lifecycle stages aren't permanent. A "Decline" product can be revived by a single large procurement decision. Our decline caps were correct methodology; this quarter, the market defied all signals.

---

## Q9: "What's the biggest lesson from this competition?"

**Answer**: Demand forecasting has a **forecastability boundary**. On one side — stable patterns, strong expert consensus — statistical models deliver 90%+ accuracy. On the other — big-deal-driven, event-driven demand — no model helps. The real value is building a system where every prediction has a documented rationale, a confidence level, and a traceable methodology.

---

## Business Insight Questions

## Q10: "What business insights did your analysis reveal?"

**Answer**: Four key insights:
1. **IP Phone Desk_1 surge was product-specific** — Desk_2 (98.8%) and Desk_3 (87.6%) were highly accurate. The surge was ONE product, not the portfolio. This points to a single mega-deal.
2. **WiFi AP has a structural Q2 budget-flush cycle** — Q2/Q1 ratio consistently >2.0×. Experts miss this every time. Supply chain should pre-position ahead of Q2.
3. **Firewall products are contracting** — both NGFW variants dropped sharply. This signals SASE/cloud-native security cannibalization.
4. **Expert consensus is the #1 accuracy predictor** — products with strong agreement hit 90%+, products with disagreement were our weakest.

---

## Key Numbers to Memorize

| Metric | Value |
|--------|-------|
| Portfolio total (ours) | **74,660** |
| Portfolio total (actual) | **95,711** |
| Products >85% accuracy | **6** (Desk_2 98.8%, SW8P 97.1%, DC Mod 92.8%, PoE+ 90.2%, Desk_3 87.6%, NGFW2 86.6%) |
| Products >70% accuracy | **12 out of 20** |
| #4 + #3 cost weight | **55.6%** (drove the under-forecast) |
| Model versions tested | **3** (v5.0 → v6.0 → v6.1) |
| Structural signals | **3** independent (Q2/Q1, YoY Q2, MA4) |
| Expert teams | **3** (DP, Marketing, DS) |

---

## Presentation Pacing Guide

| Slide | Time | Speaker | Focus |
|-------|------|---------|-------|
| 1 | 0:15 | Any | Team Introduction |
| 2 | 0:45 | Pranav | Dream Team + Challenge |
| 3 | 1:00 | Pranav | Phase 1 Methodology |
| 4 | 1:30 | Manas | Version Evolution |
| 5 | 1:30 | Aarya | Core Engine Deep-Dive |
| 6 | 0:45 | Pranav | Phase 1 Accuracy |
| 7 | 1:00 | Aarya | Phase 2 Accuracy |
| 8 | 1:00 | Manas | Demand Surge Analysis |
| 9 | 1:00 | Pranav | Business Insights |
| 10 | 0:45 | Aarya | Methodology Strengths |
| 11 | 0:30 | All | Summary & Closing |
| **Total** | **10:00** | | |

---

## Speaker Assignment
- **Pranav**: Dream Team + Phase 1 + Phase 1 Accuracy + Business Insights
- **Manas**: Version evolution + Demand surge honest analysis
- **Aarya**: Core engine + Phase 2 Accuracy + Methodology strengths + Closing
