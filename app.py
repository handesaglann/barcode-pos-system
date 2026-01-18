import sqlite3
import tkinter as tk

# ---------------- KASA ----------------

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

    # stok düş (satış ENGELLENMEZ)
    c.execute("UPDATE products SET stock = stock - 1 WHERE barcode=?", (barcode,))
    conn.commit()
    conn.close()

    listbox.insert(
        tk.END,
        f"{name} - {price:.2f} TL | stok: {stock-1}"
    )
    total.set(total.get() + price)

    status.config(text="✔ Okutuldu", fg="green")
    entry.delete(0, tk.END)

def finish():
    listbox.delete(0, tk.END)
    total.set(0)
    status.config(text="🧾 Satış bitti", fg="blue")

# ---------------- STOK GÖRÜNTÜLEME ----------------

def show_stock():
    win = tk.Toplevel(root)
    win.title("📦 Stok Durumu")
    win.geometry("450x400")

    lb = tk.Listbox(win, font=("Arial", 11))
    lb.pack(fill="both", expand=True, padx=10, pady=10)

    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT barcode, name, stock FROM products")
    rows = c.fetchall()
    conn.close()

    for barcode, name, stock in rows:
        if stock < 0:
            lb.insert(tk.END, f"{barcode} | {name} | Stok: {stock} ❗")
            lb.itemconfig(tk.END, fg="red")
        elif stock == 0:
            lb.insert(tk.END, f"{barcode} | {name} | Stok: 0 ⚠️")
            lb.itemconfig(tk.END, fg="orange")
        else:
            lb.insert(tk.END, f"{barcode} | {name} | Stok: {stock}")

# ---------------- ADMIN PANEL ----------------

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

        # ilk stok boşsa 0 kabul et
        if stock_e.get().strip() == "":
            initial_stock = 0
        else:
            try:
                initial_stock = int(stock_e.get())
            except:
                admin_status.config(text="❌ Stok sayısal olmalı", fg="red")
                return

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
            admin_status.config(
                text=f"✔ Ürün eklendi (ilk stok: {initial_stock})",
                fg="green"
            )
        except:
            admin_status.config(text="❌ Hata / Barkod zaten var", fg="red")

    def update_price():
        try:
            conn = sqlite3.connect("market.db")
            c = conn.cursor()
            c.execute(
                "UPDATE products SET price=? WHERE barcode=?",
                (float(price_e.get()), barcode_e.get())
            )
            conn.commit()
            conn.close()
            admin_status.config(text="✔ Fiyat güncellendi", fg="blue")
        except:
            admin_status.config(text="❌ Hata", fg="red")

    def delete_product():
        conn = sqlite3.connect("market.db")
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE barcode=?", (barcode_e.get(),))
        conn.commit()
        conn.close()
        admin_status.config(text="🗑️ Ürün silindi", fg="orange")

    def add_stock():
        if not barcode_e.get() or not add_stock_e.get():
            admin_status.config(text="❌ Barkod ve stok miktarı gir", fg="red")
            return
        try:
            conn = sqlite3.connect("market.db")
            c = conn.cursor()
            c.execute(
                "UPDATE products SET stock = stock + ? WHERE barcode=?",
                (int(add_stock_e.get()), barcode_e.get())
            )
            conn.commit()

            if c.rowcount == 0:
                admin_status.config(text="❌ Barkod bulunamadı", fg="red")
            else:
                admin_status.config(text="✔ Stok güncellendi", fg="green")

            conn.close()
        except:
            admin_status.config(text="❌ Hatalı stok değeri", fg="red")

    tk.Button(admin, text="➕ Ürün Ekle", command=add_product).pack(pady=4)
    tk.Button(admin, text="✏️ Fiyat Güncelle", command=update_price).pack(pady=4)
    tk.Button(admin, text="🗑️ Ürün Sil", command=delete_product).pack(pady=4)
    tk.Button(admin, text="➕ Stok Ekle", command=add_stock).pack(pady=6)

# ---------------- GUI ----------------

root = tk.Tk()
root.title("KASA")
root.geometry("400x560")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Barkod:", font=("Arial", 12)).pack(anchor="w")

entry = tk.Entry(frame, font=("Arial", 12))
entry.pack(fill="x", pady=5)
entry.focus()
entry.bind("<Return>", scan)

listbox = tk.Listbox(frame, height=10)
listbox.pack(fill="both", pady=10)

total = tk.DoubleVar(value=0)
tk.Label(frame, textvariable=total, font=("Arial", 16)).pack()

tk.Button(frame, text="Satışı Bitir", command=finish).pack(pady=4)
tk.Button(frame, text="📦 Stokları Gör", command=show_stock).pack(pady=4)
tk.Button(frame, text="🔐 Admin Panel", command=open_admin_panel).pack(pady=4)

status = tk.Label(frame, text="")
status.pack()

root.mainloop()
