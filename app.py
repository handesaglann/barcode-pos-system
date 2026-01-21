import sqlite3
import tkinter as tk
from datetime import date
import tkinter.font as tkFont
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox





cart = []  # [(barcode, name, price)]

# ---------------- KASA ----------------
print("🔥 YENİ KOD ÇALIŞIYOR 🔥")

def add_to_cart(barcode, name, price, stock):
    price = float(price)
    stock = int(stock)

    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute(
        "UPDATE products SET stock = stock - 1 WHERE barcode=?",
        (barcode,)
    )
    conn.commit()
    conn.close()

    cart.append((barcode, name, price))


    listbox.insert(
        tk.END,
        f"{name} - {price:.2f} TL "
    )

    listbox.see(tk.END)
    listbox.update_idletasks()

    total.set(total.get() + price)

    status.config(
    text=f"✔ {name} sepete eklendi",
    fg="green"
)





def scan(event=None):
    barcode = entry.get().strip()
    if not barcode:
        return

    conn = sqlite3.connect("market.db")
    c = conn.cursor()

    c.execute("SELECT name, price, stock FROM products WHERE barcode=?", (barcode,))
    row = c.fetchone()

    if not row:
        status.config(text="❌ Ürün yok", fg="red")
        entry.delete(0, tk.END)
        conn.close()
        return

    name, price, stock = row


    add_to_cart(barcode, name, price, stock)


    status.config(text="✔ Okutuldu", fg="green")
    entry.delete(0, tk.END)

def remove_selected():
    sel = listbox.curselection()
    if not sel:
        status.config(text="❌ Seçim yok", fg="red")
        return

    index = sel[0]
    barcode, name, price = cart.pop(index)


    # stok geri al
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("UPDATE products SET stock = stock + 1 WHERE barcode=?", (barcode,))
    conn.commit()
    conn.close()

    listbox.delete(index)
    total.set(total.get() - price)
    status.config(text="➖ Ürün silindi", fg="orange")

def finish():
    global cart
    if total.get() == 0:
        status.config(text="❌ Sepet boş", fg="red")
        return

    today = date.today().isoformat()

    conn = sqlite3.connect("market.db")
    c = conn.cursor()

    # Günlük toplam satış (özet)
    c.execute(
        "INSERT INTO sales (date, total) VALUES (?, ?)",
        (today, total.get())
    )

    # Satış detayları (ürün bazlı)
    for barcode, name, price in cart:
        c.execute("""
            INSERT INTO sale_items (sale_date, barcode, product_name, price)
            VALUES (?, ?, ?, ?)
        """, (today, barcode, name, price))

    conn.commit()
    conn.close()

    listbox.delete(0, tk.END)
    cart.clear()
    total.set(0)
    status.config(text="🧾 Satış kaydedildi", fg="blue")

    messagebox.showinfo(
    "Satış Tamamlandı",
    "Satış başarıyla kaydedildi."
)



from tkinter import messagebox

def show_day_detail(date_str):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()

    c.execute("""
        SELECT product_name, COUNT(*) 
        FROM sale_items
        WHERE sale_date = ?
        GROUP BY product_name
        ORDER BY COUNT(*) DESC
    """, (date_str,))

    rows = c.fetchall()
    conn.close()

    if not rows:
        messagebox.showinfo("Bilgi", "Bu tarihte satış yok.")
        return

    win = tk.Toplevel(root)
    win.title(f"{date_str} Satış Detayı")
    win.geometry("350x400")
    win.resizable(False, False)

    tk.Label(
        win,
        text=f"{date_str} Satış Detayı",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(pady=10)

    total_qty = 0
    for name, qty in rows:
        total_qty += qty
        tk.Label(
            frame,
            text=f"{name:<15} x {qty}",
            font=("Arial", 11),
            anchor="w"
        ).pack(anchor="w")

    tk.Label(win, text="----------------").pack(pady=10)

    tk.Label(
        win,
        text=f"Toplam ürün: {total_qty}",
        font=("Arial", 12, "bold")
    ).pack()

def show_day_detail(date_str):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()

    c.execute("""
        SELECT product_name, COUNT(*) 
        FROM sale_items
        WHERE sale_date = ?
        GROUP BY product_name
        ORDER BY COUNT(*) DESC
    """, (date_str,))

    rows = c.fetchall()
    conn.close()

    if not rows:
        messagebox.showinfo("Bilgi", "Bu tarihte satış yok.")
        return

    win = tk.Toplevel(root)
    win.title(f"{date_str} Satış Detayı")
    win.geometry("350x400")
    win.resizable(False, False)

    tk.Label(win, text=f"{date_str} Satış Detayı",
             font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(pady=10)

    total_qty = 0
    for name, qty in rows:
        total_qty += qty
        tk.Label(frame, text=f"{name} x {qty}",
                 font=("Arial", 11), anchor="w").pack(anchor="w")

    tk.Label(win, text="----------------").pack(pady=10)

    tk.Label(win, text=f"Toplam ürün: {total_qty}",
             font=("Arial", 12, "bold")).pack()



def show_daily_report():
    win = tk.Toplevel(root)
    win.title("📊 Gün Sonu Özeti")
    win.geometry("350x200")

    today = date.today().isoformat()

    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute(
        "SELECT COUNT(*), SUM(total) FROM sales WHERE date=?",
        (today,)
    )
    count, total_sum = c.fetchone()
    conn.close()

    count = count or 0
    total_sum = total_sum or 0.0

    tk.Label(win, text=f"📅 Tarih: {today}", font=("Arial", 12)).pack(pady=6)
    tk.Label(win, text=f"🧾 Toplam Satış: {count}", font=("Arial", 12)).pack(pady=6)
    tk.Label(win, text=f"💰 Günlük Ciro: {total_sum:.2f} TL",
             font=("Arial", 14, "bold")).pack(pady=10)
    
def show_report_by_date():
    win = tk.Toplevel(root)
    win.title("📅 Ciro Raporu")
    win.geometry("500x550")

    # --- Arama Alanı ---
    tk.Label(win, text="Tarih (YYYY-MM-DD):", font=font_normal).pack(pady=5)

    date_entry = tk.Entry(win, font=font_big)
    date_entry.pack(pady=5)

    result_label = tk.Label(win, text="", font=font_big)
    result_label.pack(pady=10)

    def fetch():
        selected_date = date_entry.get().strip()
        if not selected_date:
            result_label.config(text="❌ Tarih gir")
            return

        conn = sqlite3.connect("market.db")
        c = conn.cursor()
        c.execute(
            "SELECT COUNT(*), SUM(total) FROM sales WHERE date=?",
            (selected_date,)
        )
        count, total_sum = c.fetchone()
        conn.close()

        count = count or 0
        total_sum = total_sum or 0.0

        result_label.config(
            text=f"🧾 Satış: {count}   💰 Ciro: {total_sum:.2f} TL"
        )

    tk.Button(win, text="📊 Göster", command=fetch).pack(pady=5)

    # --- Liste Başlığı ---
    tk.Label(win, text="Son Günler", font=font_big).pack(pady=10)

    # --- Liste (Tablo) ---
    table = ttk.Treeview(
        win,
        columns=("date", "count", "total"),
        show="headings",
        height=10
    )

    table.heading("date", text="Tarih")
    table.heading("count", text="Satış")
    table.heading("total", text="Ciro (TL)")

    table.column("date", width=120, anchor="center")
    table.column("count", width=80, anchor="center")
    table.column("total", width=120, anchor="center")

    table.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Verileri Çek ---
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("""
        SELECT date, COUNT(*), SUM(total)
        FROM sales
        GROUP BY date
        ORDER BY date DESC
        LIMIT 14
    """)
    rows = c.fetchall()
    conn.close()

    for d, cnt, tot in rows:
        table.insert("", "end", values=(d, cnt, f"{tot:.2f}"))

    # --- DETAY BUTONU ---
    def show_detail_selected():
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen bir tarih seçin.")
            return

        date_str = table.item(selected[0])["values"][0]
        show_day_detail(date_str)

    tk.Button(
        win,
        text="📄 Detay Göster",
        font=font_big,
        command=show_detail_selected
    ).pack(pady=10)


def show_weekly_chart():
    win = tk.Toplevel(root)
    win.title("📊 Haftalık Ciro Grafiği")
    win.geometry("700x500")

    # --- Veriyi çek ---
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("""
        SELECT date, SUM(total)
        FROM sales
        GROUP BY date
        ORDER BY date DESC
        LIMIT 7
    """)
    rows = c.fetchall()
    conn.close()

    if not rows:
        tk.Label(win, text="Henüz satış yok", font=font_big).pack(pady=20)
        return

    # Grafikte soldan sağa eski → yeni olsun
    rows.reverse()
    dates = [r[0] for r in rows]
    totals = [r[1] for r in rows]

    # --- Matplotlib figure ---
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(dates, totals)
    ax.set_title("Son 7 Günlük Ciro")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("TL")

    # Değerleri bar üstüne yaz
    for i, v in enumerate(totals):
        ax.text(i, v, f"{v:.0f}", ha="center", va="bottom")

    fig.tight_layout()

    # --- Tkinter içine gömme ---
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)





# ---------------- STOK GÖRÜNTÜLEME ----------------

def show_stock():
    win = tk.Toplevel(root)
    win.title("📦 Stok Durumu")
    win.geometry("600x400")

    tk.Label(win, text="📦 Stok Durumu", font=font_big).pack(pady=5)

    table = ttk.Treeview(
        win,
        columns=("barcode", "name", "stock"),
        show="headings",
        height=15
    )

    table.heading("barcode", text="Barkod")
    table.heading("name", text="Ürün Adı")
    table.heading("stock", text="Stok")

    table.column("barcode", width=150, anchor="center")
    table.column("name", width=300, anchor="w")
    table.column("stock", width=100, anchor="center")

    table.pack(fill="both", expand=True, padx=10, pady=10)

    # VERİLERİ ÇEK
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT barcode, name, stock FROM products")
    rows = c.fetchall()
    conn.close()

    for barcode, name, stock in rows:
        tag = ""
        if stock < 0:
            tag = "negative"
        elif stock == 0:
            tag = "zero"

        table.insert(
            "",
            "end",
            values=(barcode, name, stock),
            tags=(tag,)
        )

    # RENKLER
    table.tag_configure("negative", foreground="red")
    table.tag_configure("zero", foreground="orange")

def show_product_list():
    win = tk.Toplevel(root)
    win.title("📋 Ürün Listesi")
    win.geometry("600x500")

    # --- Status ---
    list_status = tk.Label(win, text="", font=("Arial", 10))
    list_status.pack(pady=5)

    # --- Arama ---
    tk.Label(win, text="Ürün Ara:", font=font_normal).pack(pady=5)
    search_entry = tk.Entry(win, font=font_big)
    search_entry.pack(fill="x", padx=10)

    # --- Tablo ---
    table = ttk.Treeview(
        win,
        columns=("barcode", "name", "price", "stock"),
        show="headings",
        height=15
    )

    table.heading("barcode", text="Barkod")
    table.heading("name", text="Ürün")
    table.heading("price", text="Fiyat")
    table.heading("stock", text="Stok")

    table.column("barcode", width=120)
    table.column("name", width=250)
    table.column("price", width=80, anchor="center")
    table.column("stock", width=80, anchor="center")

    table.pack(fill="both", expand=True, padx=10, pady=10)

    def load_products(filter_text=""):
        for i in table.get_children():
            table.delete(i)

        conn = sqlite3.connect("market.db")
        c = conn.cursor()
        c.execute("""
            SELECT barcode, name, price, stock
            FROM products
            WHERE name LIKE ?
            ORDER BY name ASC
        """, (f"%{filter_text}%",))
        rows = c.fetchall()
        conn.close()

        for r in rows:
            table.insert("", "end", values=r)

    load_products()

    def on_search(event):
        load_products(search_entry.get())

    search_entry.bind("<KeyRelease>", on_search)

    def add_selected():
        sel = table.selection()
        if not sel:
            list_status.config(text="❌ Ürün seçilmedi", fg="red")
            return

        item = table.item(sel[0])["values"]
        barcode, name, price, stock = item

        add_to_cart(barcode, name, price, stock)

        list_status.config(
            text=f"✔ {name} sepete eklendi",
            fg="green"
        )

    # --- BUTON (KRİTİK) ---
    tk.Button(
        win,
        text="➕ Sepete Ekle",
        font=("Arial", 16, "bold"),
        command=add_selected
    ).pack(pady=10)





# ---------------- ADMIN PANEL ----------------
# (önceki admin panel kodun AYNEN duruyor, değişmedi)

def open_admin_panel():
    admin = tk.Toplevel(root)
    admin.title("Admin Panel - Ürün Yönetimi")
    admin.geometry("400x520")

    tk.Label(admin, text="Barkod").pack()
    barcode_e = tk.Entry(admin)
    barcode_e.pack(fill="x", padx=10)

    tk.Label(admin, text="Ürün Adı").pack()
    name_e = tk.Entry(admin)
    name_e.pack(fill="x", padx=10)

    tk.Label(admin, text="Fiyat").pack()
    price_e = tk.Entry(admin)
    price_e.pack(fill="x", padx=10)

    tk.Label(admin, text="İlk Stok (boş = 0)").pack()
    stock_e = tk.Entry(admin)
    stock_e.pack(fill="x", padx=10)

    tk.Label(admin, text="Eklenecek Stok").pack()
    add_stock_e = tk.Entry(admin)
    add_stock_e.pack(fill="x", padx=10)

    admin_status = tk.Label(admin, text="")
    admin_status.pack(pady=8)

    def add_product():
        if not barcode_e.get() or not name_e.get() or not price_e.get():
            admin_status.config(text="❌ Barkod, ürün adı ve fiyat zorunlu", fg="red")
            return

        initial_stock = int(stock_e.get()) if stock_e.get().strip() else 0

        try:
            conn = sqlite3.connect("market.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO products VALUES (?,?,?,?)",
                (
                    barcode_e.get(),
                    name_e.get(),
                    float(price_e.get()),
                    initial_stock
                )
            )
            conn.commit()
            conn.close()
            admin_status.config(text="✔ Ürün eklendi", fg="green")
        except:
            admin_status.config(text="❌ Barkod zaten var", fg="red")

    def update_price():
        conn = sqlite3.connect("market.db")
        c = conn.cursor()
        c.execute(
            "UPDATE products SET price=? WHERE barcode=?",
            (float(price_e.get()), barcode_e.get())
        )
        conn.commit()
        conn.close()
        admin_status.config(text="✔ Fiyat güncellendi", fg="blue")

    def delete_product():
        conn = sqlite3.connect("market.db")
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE barcode=?", (barcode_e.get(),))
        conn.commit()
        conn.close()
        admin_status.config(text="🗑️ Ürün silindi", fg="orange")

    def add_stock():
        conn = sqlite3.connect("market.db")
        c = conn.cursor()
        c.execute(
            "UPDATE products SET stock = stock + ? WHERE barcode=?",
            (int(add_stock_e.get()), barcode_e.get())
        )
        conn.commit()
        conn.close()
        admin_status.config(text="✔ Stok güncellendi", fg="green")

    tk.Button(admin, text="➕ Ürün Ekle", command=add_product).pack(pady=4)
    tk.Button(admin, text="✏️ Fiyat Güncelle", command=update_price).pack(pady=4)
    tk.Button(admin, text="🗑️ Ürün Sil", command=delete_product).pack(pady=4)
    tk.Button(admin, text="➕ Stok Ekle", command=add_stock).pack(pady=6)
    

def on_resize(event):
    new_size = max(10, int(event.width / 50))
    app_font.configure(size=new_size)

# ---------------- GUI ----------------

root = tk.Tk()

font_normal = tkFont.Font(family="Arial", size=14)
font_big = tkFont.Font(family="Arial", size=18, weight="bold")
font_total = tkFont.Font(family="Arial", size=28, weight="bold")


# ---- GLOBAL FONT ----
base_font_size = 14
app_font = tkFont.Font(family="Arial", size=base_font_size)


root.title("KASA")
root.geometry("520x800")
root.minsize(520, 700)


frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Barkod:", font=font_normal).pack(anchor="w")


entry = tk.Entry(frame, font=font_big)

entry.pack(fill="x", pady=5)
entry.focus()
entry.bind("<Return>", scan)

listbox = tk.Listbox(frame, height=10, font=font_big)

listbox.pack(fill="both", pady=10)

total = tk.DoubleVar(value=0)
tk.Label(frame, textvariable=total, font=font_total).pack(pady=10)


# ===============================
# KRİTİK BUTONLAR
# ===============================
action_frame = tk.Frame(frame)
action_frame.pack(fill="x", pady=25)

tk.Button(
    action_frame,
    text="➖ Seçili Ürünü Sil",
    command=remove_selected,
    font=("Arial", 20),
    padx=20,
    pady=15,
    relief="raised"
).pack(fill="x", pady=10)

tk.Button(
    action_frame,
    text="Satışı Bitir",
    command=finish,
    font=("Arial", 24, "bold"),
    padx=20,
    pady=18,
    bg="#f2f2f2",
    fg="#d32f2f",
    activebackground="#e0e0e0",
    activeforeground="#b71c1c",
    relief="raised"
).pack(fill="x", pady=15)



# ===============================
# DİĞER BUTONLAR
# ===============================
other_frame = tk.Frame(frame)
other_frame.pack(fill="x", pady=10)

tk.Button(
    other_frame,
    text="📋 Ürün Listesi",
    command=show_product_list
).pack(fill="x", pady=3)


tk.Button(other_frame, text="📦 Stokları Gör", command=show_stock)\
    .pack(fill="x", pady=3)

tk.Button(other_frame, text="🔐 Admin Panel", command=open_admin_panel)\
    .pack(fill="x", pady=3)

tk.Button(other_frame, text="📊 Gün Sonu Özeti", command=show_daily_report)\
    .pack(fill="x", pady=3)

tk.Button(other_frame, text="📅 Tarihe Göre Ciro", command=show_report_by_date)\
    .pack(fill="x", pady=3)

tk.Button(other_frame, text="📊 Haftalık Ciro Grafiği", command=show_weekly_chart)\
    .pack(fill="x", pady=3)





status = tk.Label(frame, text="")
status.pack()




root.mainloop()
