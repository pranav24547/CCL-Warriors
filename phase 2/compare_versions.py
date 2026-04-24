v5 = {1:5104, 2:5800, 3:5638, 4:11432, 5:1444, 6:688, 7:723, 8:5543, 9:7385, 10:7969, 11:606, 12:1622, 13:396, 14:9159, 15:634, 16:446, 17:821, 18:129, 19:2220, 20:1602}
v6 = {1:5150, 2:5776, 3:5720, 4:13903, 5:1397, 6:652, 7:723, 8:4900, 9:8646, 10:8062, 11:657, 12:1553, 13:391, 14:10019, 15:649, 16:454, 17:774, 18:129, 19:2451, 20:1623}
v61 = {1:6362, 2:5756, 3:5471, 4:14079, 5:1448, 6:636, 7:722, 8:4644, 9:7155, 10:7708, 11:668, 12:1621, 13:385, 14:9771, 15:645, 16:444, 17:767, 18:126, 19:2545, 20:1556}
p1 = {1:8010, 5:2136, 6:1990, 15:479, 16:316, 19:5928}
p1_desk = 27337

names = {1:'WiFi AP Indoor', 2:'SW 8P PoE+ Fiber', 3:'RTR Branch LTE', 4:'Phone Desk_1', 5:'SW Ind 8P PoE', 6:'RTR Edge Fiber', 7:'SW 24P UPOE', 8:'Phone Video', 9:'Phone Desk_2', 10:'Phone Desk_3', 11:'SW 24P HP PoE', 12:'SW Ind 8P Eth', 13:'SW DC Modular', 14:'SW 8P Ethernet', 15:'NGFW_1', 16:'NGFW_2', 17:'SW Ind 24P Eth', 18:'SW DC 400G', 19:'RTR 4P PoE', 20:'RTR LTE Wireless'}

print("COMPREHENSIVE VERSION COMPARISON: v5.0 vs v6.0 vs v6.1 vs Phase 1 Actuals")
print("=" * 115)
print(f"{'#':>2} {'Product':<20} {'v5.0':>7} {'v6.0':>7} {'v6.1':>7} {'P1 Act':>7} | {'v5 Err':>8} {'v6 Err':>8} {'v61 Err':>8} | {'v6->v61':>8}")
print("-" * 115)

v61_total_abs_err = 0
v6_total_abs_err = 0
v5_total_abs_err = 0
n_match = 0

for i in range(1, 21):
    actual = p1.get(i, None)
    v5e = f"{(v5[i]-actual)/actual*100:+.1f}%" if actual else "   -"
    v6e = f"{(v6[i]-actual)/actual*100:+.1f}%" if actual else "   -"
    v61e = f"{(v61[i]-actual)/actual*100:+.1f}%" if actual else "   -"
    delta = f"{v61[i]-v6[i]:+,}"
    act_str = f"{actual:,}" if actual else "   -"
    
    if actual:
        v5_total_abs_err += abs(v5[i]-actual)/actual*100
        v6_total_abs_err += abs(v6[i]-actual)/actual*100
        v61_total_abs_err += abs(v61[i]-actual)/actual*100
        n_match += 1
    
    print(f"{i:>2} {names[i]:<20} {v5[i]:>7,} {v6[i]:>7,} {v61[i]:>7,} {act_str:>7} | {v5e:>8} {v6e:>8} {v61e:>8} | {delta:>8}")

print("-" * 115)
print(f"   {'TOTAL':<20} {sum(v5.values()):>7,} {sum(v6.values()):>7,} {sum(v61.values()):>7,}")
print()
print("ACCURACY ON KNOWN PRODUCTS (Phase 1 Actuals):")
print(f"  v5.0 avg abs error: {v5_total_abs_err/n_match:.1f}%")
print(f"  v6.0 avg abs error: {v6_total_abs_err/n_match:.1f}%")
print(f"  v6.1 avg abs error: {v61_total_abs_err/n_match:.1f}%")
print()

# Cisco accuracy (max(0, 1 - |fc-act|/act))
print("CISCO ACCURACY (max(0, 1-|err|/actual)) on known products:")
for label, d in [("v5.0", v5), ("v6.0", v6), ("v6.1", v61)]:
    accs = []
    for pid, actual in p1.items():
        cisco_acc = max(0, 1 - abs(d[pid] - actual)/actual)
        accs.append(cisco_acc)
        print(f"  {label} #{pid} {names[pid]:<20}: {cisco_acc*100:.1f}%")
    print(f"  {label} AVG: {sum(accs)/len(accs)*100:.1f}%")
    print()

print("IP Phone Desk Aggregate (P1 actual = 27,337):")
for label, d in [("v5.0", v5), ("v6.0", v6), ("v6.1", v61)]:
    total = d[4] + d[9] + d[10]
    err = (total - p1_desk) / p1_desk * 100
    cisco_acc = max(0, 1 - abs(total - p1_desk)/p1_desk)
    print(f"  {label}: {total:>7,} (err: {err:+.1f}%, Cisco acc: {cisco_acc*100:.1f}%)")
