import tkinter as tk
from tkinter import messagebox

# ---------------- DATE LOGIC ----------------

def شمسی_به_عیسوی(jy, jm, jd):
    jy -= 979
    jm -= 1
    jd -= 1

    j_day_no = 365 * jy + jy // 33 * 8 + (jy % 33 + 3) // 4
    for i in range(jm):
        j_day_no += 31 if i < 6 else 30
    j_day_no += jd

    g_day_no = j_day_no + 79
    gy = 1600 + 400 * (g_day_no // 146097)
    g_day_no %= 146097

    leap = True
    if g_day_no >= 36525:
        g_day_no -= 1
        gy += 100 * (g_day_no // 36524)
        g_day_no %= 36524
        if g_day_no < 365:
            leap = False
        else:
            g_day_no += 1

    gy += 4 * (g_day_no // 1461)
    g_day_no %= 1461

    if g_day_no >= 366:
        leap = False
        g_day_no -= 1
        gy += g_day_no // 365
        g_day_no %= 365

    gd = g_day_no + 1
    months = [31, 29 if leap else 28, 31, 30, 31, 30,
              31, 31, 30, 31, 30, 31]

    gm = 0
    while gd > months[gm]:
        gd -= months[gm]
        gm += 1

    return gy, gm + 1, gd


def عیسوی_به_شمسی(gy, gm, gd):
    gy -= 1600
    gm -= 1
    gd -= 1

    g_day_no = 365 * gy + (gy + 3)//4 - (gy + 99)//100 + (gy + 399)//400
    for i in range(gm):
        g_day_no += [31,28,31,30,31,30,31,31,30,31,30,31][i]

    if gm > 1 and ((gy+1600)%4==0 and ((gy+1600)%100!=0 or (gy+1600)%400==0)):
        g_day_no += 1

    g_day_no += gd

    j_day_no = g_day_no - 79
    j_np = j_day_no // 12053
    j_day_no %= 12053

    jy = 979 + 33*j_np + 4*(j_day_no//1461)
    j_day_no %= 1461

    if j_day_no >= 366:
        jy += (j_day_no - 1)//365
        j_day_no = (j_day_no - 1)%365

    jm = 0
    while jm < 11 and j_day_no >= (31 if jm < 6 else 30):
        j_day_no -= 31 if jm < 6 else 30
        jm += 1

    return jy, jm + 1, j_day_no + 1

# ---------------- GUI ----------------

def convert_jalali():
    try:
        y,m,d = map(int, j_entry.get().split("-"))
        gy,gm,gd = شمسی_به_عیسوی(y,m,d)
        result.set(f"{gy}-{gm:02}-{gd:02}")
    except:
        messagebox.showerror("Error", "Invalid Jalali date")

def convert_gregorian():
    try:
        y,m,d = map(int, g_entry.get().split("-"))
        jy,jm,jd = عیسوی_به_شمسی(y,m,d)
        result.set(f"{jy}-{jm:02}-{jd:02}")
    except:
        messagebox.showerror("Error", "Invalid Gregorian date")

root = tk.Tk()
root.title("Jalali ↔ Gregorian Converter")
root.geometry("420x240")
root.resizable(False, False)

tk.Label(root, text="Jalali (YYYY-MM-DD)").pack()
j_entry = tk.Entry(root, justify="center")
j_entry.pack()

tk.Button(root, text="Convert to Gregorian", command=convert_jalali).pack(pady=5)

tk.Label(root, text="Gregorian (YYYY-MM-DD)").pack()
g_entry = tk.Entry(root, justify="center")
g_entry.pack()

tk.Button(root, text="Convert to Jalali", command=convert_gregorian).pack(pady=5)

result = tk.StringVar()
tk.Entry(root, textvariable=result, justify="center", state="readonly").pack(pady=10)

root.mainloop()
