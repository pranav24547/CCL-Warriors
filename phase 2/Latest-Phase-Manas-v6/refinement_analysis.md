# v6.0 Refinement Analysis: What the Data Tells Us

## The Honest Assessment

After implementing v6.0 and running the verification, **3 of 7 changes clearly helped, 2 are neutral, and 2 actually hurt**. Here's the breakdown:

---

## What the Backtest Reveals

### Changes That WORKED ✅

| Change | Evidence |
|--------|----------|
| **Damped equal weights** (replaces acc³) | V6.0 closer to expert consensus on 11/20 products, more stable under perturbation. **Keep.** |
| **Removing dominant expert rule** | Same reasoning — combination beats selection across decades of research. **Keep.** |
| **Growth floor bug fix (#8)** | Objectively correct. Product #8 dropped from 5,543→4,900 (closer to Decline trajectory). **Keep.** |

### Changes That Are NEUTRAL ≈

| Change | Evidence |
|--------|----------|
| **Linear interpolation** (replaces step function) | Barely changes anything — differences are <2% on any product. Harmless. **Keep.** |
| **Bias threshold 8%** | Slightly changes a few products. Neither clearly better nor worse. **Keep.** |

### Changes That HURT ❌

| Change | Evidence |
|--------|----------|
| **Q2 seasonal avg replacing MA4** | **Backtest shows MA4 was better on 8 products, Q2 avg on only 3.** Products #2, #3, #5, #6, #17, #18 all degraded. v5 structural avg accuracy 49.9% vs v6 42.3%. **Revert.** |
| **Pattern-based overrides removing Product #9 anchor** | Product #9 jumped from 7,385→8,646 (+17%). The v5.0 Q2-history anchor was keeping it sensible. Without it, the damped-equal expert blend of 12,618 is too high. **Needs fix.** |

---

## The 4 Critical Findings

### 1. 🔴 Revert Signal 3: Keep MA4, Not Q2 Seasonal Avg

The backtest conclusively shows MA4 outperforms Q2 seasonal average as the 3rd structural signal:
- **v5 structural MASE = 1.040** (barely worse than naive)
- **v6 structural MASE = 1.174** (significantly worse than naive)

Why? MA4 smooths across recent quarters, catching recent trajectory shifts. Q2 seasonal avg only uses Q2 history (3 points), which is too sparse and misses recent momentum changes.

> [!IMPORTANT]
> **Recommendation:** Revert Signal 3 back to MA4. The Q2 seasonal avg was already available as a "validation signal" — it should stay there. The structural median should be: Q2/Q1 ratio, YoY Q2, **MA4**.

### 2. 🟡 Product #4: The +21.6% Shift Is Too Aggressive

Product #4 (IP Phone Desk_1) went from v5=11,432 to v6=13,903. This happened because:
- v5.0 had the dominant expert rule anchoring 80% on DP (9,500, accuracy 88%)
- v6.0 uses damped equal weights, giving DS (22,593, accuracy 68%) more influence

The damped-equal weighting is *theoretically correct*, but **the magnitude of shift is a risky bet**:
- Expert average = 14,823
- v6.0 = 13,903 (6.2% below expert avg — reasonable)
- v5.0 = 11,432 (22.9% below expert avg — aggressive bet ON DP)

> [!TIP]
> Actually, v6.0 is **closer to expert consensus** here (+6.2% vs -22.9%). The v5.0 number was the aggressive one. **Keep v6.0 for Product #4** — it's the more principled choice.

### 3. 🔴 Both Versions Fail to Beat Seasonal Naive (MASE > 1)

This is the most important finding:

```
Seasonal Naive avg accuracy:  53.5%
v5.0 structural avg accuracy: 49.9%
v6.0 structural avg accuracy: 42.3%
```

**Neither model's structural component adds value over "just use last Q2."** This means:

1. The structural signals are net-negative — they introduce more noise than signal
2. The expert forecasts are where all the value is
3. **We should increase expert weight across the board**

> [!WARNING]  
> **Recommendation:** Increase the expert weight floor. Currently the linear interpolation maps [20%-95% acc] → [25%-85% expert weight]. Since structural signals fail to beat naive, shift to [35%-90% expert weight]. This anchors more on experts and reduces the damage from structural noise.

### 4. 🟡 Consider a "Seasonal Naive Safety Net"

From the M4/M5 competition research: winning strategies always anchor to strong baselines before adding complexity. We should guard against our structural signals being WORSE than just using last year's Q2:

```python
# After computing structural_median, clamp it toward seasonal naive
seasonal_naive = fy25q2  # Q2 this year = Q2 last year
if structural_median > 0 and seasonal_naive > 0:
    deviation = abs(structural_median - seasonal_naive) / seasonal_naive
    if deviation > 0.40:  # If structural deviates >40% from naive
        # Shrink back toward naive
        structural_median = structural_median * 0.70 + seasonal_naive * 0.30
```

This prevents the structural signals from making extreme bets that are worse than doing nothing.

---

## Recommended v6.1 Patch (3 Targeted Fixes)

| Fix | What | Lines to Change |
|-----|------|:---:|
| **A** | Revert Signal 3 to MA4 | `ind_signals = [ratio_fc, yoy_fc, ma4_fc]` |
| **B** | Shift expert weight range to [35%-90%] | `clamp(0.35 + ... * (0.90 - 0.35) / ...)` |
| **C** | Add seasonal naive safety net | New 4-line guard after structural median |

### Expected Impact of v6.1
- ✅ Keeps damped equal weights (the biggest, most-supported improvement)
- ✅ Keeps no dominant expert rule
- ✅ Keeps growth floor bug fix
- ✅ Reverts the one change that backtest proved was wrong (Q2 avg → MA4)
- ✅ Increases expert anchoring (since structural fails to beat naive)
- ✅ Adds a safety net against extreme structural deviations

---

## Risk-Tiered Product Strategy

Based on all our analysis, here's how confident we should be in each product:

### 🟢 High Confidence (tight consensus, stable)
Products: #5, #7, #12, #13, #15, #18, #20
- All experts agree (±15%), structural consistent
- v5→v6 shift was minor (<10%)
- **Leave alone — these are fine**

### 🟡 Medium Confidence (some divergence)  
Products: #2, #3, #6, #10, #11, #16, #17
- Moderate expert disagreement or structural divergence
- **v6.1 fixes should stabilize these**

### 🔴 Low Confidence (big bets)
Products: #1, #4, #8, #9, #14, #19
- Major expert disagreement and/or large v5→v6 shifts
- **These need the most scrutiny:**

| Product | Key Risk | Strategy |
|---------|----------|----------|
| **#1 WiFi AP** | Q2 spike product; experts badly under-forecast | Keep structural-heavy (Rule C fires correctly) |
| **#4 IP Phone Desk_1** | DP says 9.5K, DS says 22.6K | v6.0's 13,903 is closer to expert avg — keep |
| **#8 IP Phone Video** | Decline product, bug fixed | v6.0's 4,900 is correct direction |
| **#9 IP Phone Desk_2** | +17% shift, needs Q2 stability anchor | v6.1 increased expert weight should help |
| **#14 Switch 8P Eth** | Hockey-stick growth, hard to forecast | Trust expert consensus (8,734 avg) |
| **#19 Router 4P PoE** | In freefall, only DS reliable | Exclusion of DP/MK (<10%) is correct |

---

## Bottom Line

> v6.0 made 7 changes. 5 were right, 2 were wrong. A targeted v6.1 patch (revert MA4, boost expert weights, add naive safety net) would give us **the best of both worlds**: the research-backed improvements from v6.0 with the structural accuracy from v5.0.

Should I implement the v6.1 patch?
