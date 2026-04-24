"""Compute v7.0 accuracy against REAL Phase 2 actuals"""

# Phase 2 ACTUAL Q2 FY26 Bookings (from Phase2AccuracyCalculation.xlsx)
p2_actuals = {
    1: 6162, 2: 5243, 3: 10486, 4: 28011, 5: 1157, 6: 799, 7: 1036,
    8: 3936, 9: 6678, 10: 8312, 11: 1803, 12: 2201, 13: 415, 14: 9499,
    15: 758, 16: 402, 17: 1353, 18: 201, 19: 3251, 20: 4008
}

# Cost weights
cost_weights = {
    1: 0.08759, 2: 0.03262, 3: 0.18069, 4: 0.37524, 5: 0.00714, 6: 0.00518,
    7: 0.00755, 8: 0.01299, 9: 0.03490, 10: 0.04751, 11: 0.02579, 12: 0.01843,
    13: 0.00253, 14: 0.07015, 15: 0.00457, 16: 0.00142, 17: 0.01273, 18: 0.00132,
    19: 0.02280, 20: 0.04885
}

v7_preds = {
    1: 7598, 2: 5756, 3: 5471, 4: 13298, 5: 1998, 6: 1313, 7: 722,
    8: 4644, 9: 6758, 10: 7281, 11: 668, 12: 1621, 13: 385, 14: 9771,
    15: 512, 16: 348, 17: 767, 18: 126, 19: 4067, 20: 1556
}

v61_preds = {
    1: 6362, 2: 5756, 3: 5471, 4: 14079, 5: 1448, 6: 636, 7: 722,
    8: 4644, 9: 7155, 10: 7708, 11: 668, 12: 1621, 13: 385, 14: 9771,
    15: 645, 16: 444, 17: 767, 18: 126, 19: 2545, 20: 1556
}

v5_preds = {
    1: 5104, 2: 5800, 3: 5638, 4: 11432, 5: 1444, 6: 688, 7: 723,
    8: 5543, 9: 7385, 10: 7969, 11: 606, 12: 1622, 13: 396, 14: 9159,
    15: 634, 16: 446, 17: 821, 18: 129, 19: 2220, 20: 1602
}

names = {
    1: "WiFi AP Indoor", 2: "SW 8P PoE+ Fiber", 3: "RTR Branch LTE",
    4: "Phone Desk_1", 5: "SW Ind 8P PoE", 6: "RTR Edge Fiber",
    7: "SW 24P UPOE", 8: "Phone Video", 9: "Phone Desk_2",
    10: "Phone Desk_3", 11: "SW 24P HP PoE", 12: "SW Ind 8P Eth",
    13: "SW DC Modular", 14: "SW 8P Eth", 15: "NGFW_1",
    16: "NGFW_2", 17: "SW Ind 24P Eth", 18: "SW DC 400G",
    19: "RTR 4P PoE", 20: "RTR LTE Wireless"
}

def cisco_acc(fc, act):
    if act <= 0: return 0
    return max(0, 1 - abs(fc - act) / act)

print("=" * 120)
print("  PHASE 2 ACCURACY ANALYSIS — v7.0 vs REAL Q2 FY26 ACTUALS")
print("=" * 120)
print()
print(f"{'#':<3} {'Product':<22} {'P2 Actual':>9} {'v5.0':>7} {'v5 Acc':>7} {'v6.1':>7} {'v61 Acc':>8} {'v7.0':>7} {'v7 Acc':>7} {'CostWt':>7}")
print("-" * 100)

total_cw_v5 = total_cw_v61 = total_cw_v7 = 0
sum_acc_v5 = sum_acc_v61 = sum_acc_v7 = 0

for rk in range(1, 21):
    act = p2_actuals[rk]
    a5 = cisco_acc(v5_preds[rk], act)
    a61 = cisco_acc(v61_preds[rk], act)
    a7 = cisco_acc(v7_preds[rk], act)
    cw = cost_weights[rk]
    
    total_cw_v5 += a5 * cw
    total_cw_v61 += a61 * cw
    total_cw_v7 += a7 * cw
    sum_acc_v5 += a5
    sum_acc_v61 += a61
    sum_acc_v7 += a7
    
    flag = " <<<" if a7 < 0.50 else (" >>>" if a7 > 0.90 else "")
    print(f"{rk:<3} {names[rk]:<22} {act:>9,} {v5_preds[rk]:>7,} {a5*100:>6.1f}% {v61_preds[rk]:>7,} {a61*100:>7.1f}% {v7_preds[rk]:>7,} {a7*100:>6.1f}% {cw*100:>6.2f}%{flag}")

print("-" * 100)
print(f"{'':3} {'SIMPLE AVERAGE':22} {'':>9} {'':>7} {sum_acc_v5/20*100:>6.1f}% {'':>7} {sum_acc_v61/20*100:>7.1f}% {'':>7} {sum_acc_v7/20*100:>6.1f}%")
print(f"{'':3} {'COST-WEIGHTED':22} {'':>9} {'':>7} {total_cw_v5*100:>6.1f}% {'':>7} {total_cw_v61*100:>7.1f}% {'':>7} {total_cw_v7*100:>6.1f}%")

print()
print("=" * 80)
print("  TOP PERFORMERS (v7.0 Accuracy > 85%)")
print("=" * 80)
for rk in sorted(range(1,21), key=lambda r: cisco_acc(v7_preds[r], p2_actuals[r]), reverse=True):
    a = cisco_acc(v7_preds[rk], p2_actuals[rk])
    if a >= 0.85:
        print(f"  #{rk:<2} {names[rk]:<25} {a*100:.1f}% acc  (predicted {v7_preds[rk]:,} vs actual {p2_actuals[rk]:,})")

print()
print("=" * 80)
print("  BIGGEST MISSES (v7.0 Accuracy < 50%)")
print("=" * 80)
for rk in sorted(range(1,21), key=lambda r: cisco_acc(v7_preds[r], p2_actuals[r])):
    a = cisco_acc(v7_preds[rk], p2_actuals[rk])
    if a < 0.50:
        ratio = p2_actuals[rk] / v7_preds[rk] if v7_preds[rk] > 0 else 0
        print(f"  #{rk:<2} {names[rk]:<25} {a*100:.1f}% acc  (predicted {v7_preds[rk]:,} vs actual {p2_actuals[rk]:,}, actual was {ratio:.1f}x prediction)")

print()
print("=" * 80)
print("  P1 vs P2 ACTUALS COMPARISON (6 overlapping products)")
print("=" * 80)
p1_actuals = {1: 8010, 5: 2136, 6: 1990, 15: 479, 16: 316, 19: 5928}
for rk in sorted(p1_actuals):
    p1 = p1_actuals[rk]
    p2 = p2_actuals[rk]
    diff_pct = (p2 - p1) / p1 * 100
    v61_a = cisco_acc(v61_preds[rk], p2)
    v7_a = cisco_acc(v7_preds[rk], p2)
    print(f"  #{rk:<2} {names[rk]:<22} P1={p1:>6,} P2={p2:>6,} ({diff_pct:>+6.1f}%)  v6.1→P2:{v61_a*100:.1f}%  v7→P2:{v7_a*100:.1f}%  {'v6.1 better' if v61_a > v7_a else 'v7 better'}")

print()
total_v7 = sum(v7_preds.values())
total_actual = sum(p2_actuals.values())
print(f"  Portfolio Total: v7.0={total_v7:,} vs Actual={total_actual:,} ({(total_v7-total_actual)/total_actual*100:+.1f}%)")
