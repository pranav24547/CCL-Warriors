# Deep Analysis of CFL FY26 Q2 Demand Forecasting Project

## 1. Project Overview & Context
The project represents a demand forecasting engine for 30 Cisco products for FY26 Q2. Currently, there are multiple assets in the project directory:
- **[forecast.py](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py)**: The main forecasting engine script executing the multi-step methodology.
- **[forecast_dashboard.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast_dashboard.html)**: The UI dashboard presenting the data produced by the engine ([forecast_data.json](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast_data.json)).
- **[forecasting_step_by_step_guide.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecasting_step_by_step_guide.html)**: A learning module/guide intended to explain the underlying forecasting methodology.
- **[plan_coherence_audit.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/plan_coherence_audit.html)**: An audit report that explicitly evaluates a prior plan and suggests fixes.

## 2. Identified Inconsistencies

During the analysis, I cross-referenced the Python implementation ([forecast.py](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py)), the UI output ([forecast_dashboard.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast_dashboard.html)), the [plan_coherence_audit.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/plan_coherence_audit.html), and the Step-by-Step Guide ([forecasting_step_by_step_guide.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecasting_step_by_step_guide.html)). Several significant inconsistencies were found:

### A. Lifecycle Blending Formulas Mismatch
The blending weights differ across project files, creating a contradictory "source of truth":
- **[forecast.py](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py) & [forecast_dashboard.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast_dashboard.html)**: 
  - Sustaining: 25% WMA + 25% Trend + 50% Ensemble
  - Decline: 40% WMA + 30% Trend + 30% Ensemble  (Wait, [forecast.py](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py) has Decline as 40 WMA, 30 Trend, 30 Ens).
  - NPI-Ramp: 10% WMA + 5% Trend + 85% Ensemble
- **[forecasting_step_by_step_guide.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecasting_step_by_step_guide.html)**:
  - Sustaining: 35% WMA + 65% Ensemble (Misses Trend component entirely).
  - Decline: 35% Trend + 35% WMA + 30% Ensemble.
  - NPI-Ramp: 15% WMA + 85% Ensemble (Misses Trend component entirely).
- **[plan_coherence_audit.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/plan_coherence_audit.html)**:
  - Recommends using the 3-component formula everywhere: 25/25/50 for Sustaining, 30/40/30 for Decline, and 10/5/85 for NPI. 

### B. Linear Trend & Seasonality Use "Dirty" Big Deal Data
The [plan_coherence_audit.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/plan_coherence_audit.html) explicitly cites removing big deals (cleaning) from data so forecasts aren't distorted. However, there are bugs in [forecast.py](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py):
- In [forecast.py](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py), [compute_wma](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py#186-226) properly accepts a clean baseline without big deals.
- However, `trend = compute_trend(actuals)` passes `actuals` (the uncleaned, raw numbers containing big deal outliers). This heavily skews linear regression over the 12 quarters for products with large deals.
- Similarly, `seasonally_adjusted` relies on [compute_seasonal_index(actuals)](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py#413-441), meaning the Q2 seasonal multipliers are calculated on completely raw data. If a massive big deal landed in a historical Q2, the seasonality multiplier will be falsely inflated.

### C. Outdated Examples in the Step-By-Step Guide
The interactive examples and static worked examples in the Step-by-Step guide ([forecasting_step_by_step_guide.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecasting_step_by_step_guide.html)) do not match the real output in [forecast.py](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py) or the [forecast_dashboard.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast_dashboard.html) for "Product 1". 
- **Guide**: Mentions a final forecast of ~15,528 based on old blending logic.
- **Dashboard/Engine**: Output is actually 15,647 with an intermediate raw blend of 15,276.
- The guide's calculator tool requires users to input [(wma, ens)](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py#545-718) for Sustaining and misses the [trend](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py#232-272) parameter entirely.

## 3. Recommended Plan to Remove Inconsistencies

To unify the project and ensure that the documented methodology perfectly matches the mathematical implementation, we should execute the following plan:

### Part 1: Fix the Python Engine ([forecast.py](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py))
1. **Apply Cleaned Baseline to All Methods**:
   Pass the `merged` clean dictionary (which contains `clean_baseline` for the past 8 quarters and raw actuals for the prior 4) into [compute_trend()](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py#232-272) and [compute_seasonal_index()](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py#413-441), rather than the raw `actuals`, for products where `has_bd` is true.
2. **Re-run the Engine**:
   Execute [forecast.py](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py) to regenerate [forecast_output.csv](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast_output.csv) and [forecast_data.json](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast_data.json) so the dashboard matches the repaired math. 

### Part 2: Update the Step-by-Step Guide ([forecasting_step_by_step_guide.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecasting_step_by_step_guide.html))
1. **Unify Blending Logic**: Update Step 5 of the guide to document the exact same 3-component formula currently implemented in the engine and dashboard:
   - Sustaining: 25% WMA + 25% Trend + 50% Ensemble
   - Decline: 40% WMA + 30% Trend + 30% Ensemble
   - NPI-Ramp: 10% WMA + 5% Trend + 85% Ensemble
2. **Fix the JS Calculator**: Modify the JavaScript functions [calcBlend()](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecasting_step_by_step_guide.html#427-449) and the inputs (`<input>`) in the guide to accept and parse the [trend](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py#232-272) variable for all three lifecycle types instead of just "Decline", and update the text in "Step 5" to reflect the actual weights.
3. **Update Product 1 Example Numbers**: Reflect the correct Step 3 (WMA), Step 4 (Ensemble), Step 5 (Blend), and Step 6 (Final) numbers for Product 1 derived after fixing the big-deal issue in part 1. 

### Part 3: Synchronize UI and Audit Context
1. Update [plan_coherence_audit.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/plan_coherence_audit.html) (if necessary) to make sure its recommended Decline blend matches [forecast.py](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast.py) (40% WMA + 30% Trend + 30% Ensemble) rather than `30/40/30` which is ambiguous.
2. Make sure [forecast_dashboard.html](file:///c:/Users/shaha/Downloads/CCL%2726/New%20folder%20v1/New%20folder%20v1/New%20folder/forecast_dashboard.html)'s methodology modal matches the exact implementation.

By applying this plan, the mathematical logic, the dashboard statistics, the methodology documentation, and the interactive training guide will all be 100% consistent.
