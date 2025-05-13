import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import difflib
import shutil
import os

def hash_ol(fayl_nomi):
    h = hashlib.sha256()
    with open(fayl_nomi, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def farqni_korsat(eski_fayl, yangi_fayl):
    with open(eski_fayl, 'r', encoding='utf-8') as f1, open(yangi_fayl, 'r', encoding='utf-8') as f2:
        eski = f1.readlines()
        yangi = f2.readlines()
    diff = difflib.unified_diff(eski, yangi, fromfile='Backup', tofile='Yangi', lineterm='')
    diff_matn = ''.join(diff)

    oynacha = tk.Toplevel(oyna)
    oynacha.title("Farqlar")
    text = tk.Text(oynacha, wrap="word")
    text.insert(tk.END, diff_matn)
    text.pack(expand=True, fill='both')

def faylni_tiklash(asl_fayl, backup_fayl):
    shutil.copy(backup_fayl, asl_fayl)
    messagebox.showinfo("✅ Tiklandi", "Fayl backup’dan qayta tiklandi.")

def tekshir_fayl():
    fayl_nomi = filedialog.askopenfilename(title="Faylni tanlang")
    if not fayl_nomi:
        return

    papka = os.path.dirname(fayl_nomi)
    fayl_nomi_short = os.path.basename(fayl_nomi)
    backup_nomi = os.path.join(papka, fayl_nomi_short + "_backup.txt")
    hash_nomi = os.path.join(papka, fayl_nomi_short + ".hash")

    # Faylni ilk marta tanlaganda: backup va hash yaratish
    if not os.path.exists(backup_nomi) or not os.path.exists(hash_nomi):
        shutil.copy(fayl_nomi, backup_nomi)
        hash_qiymat = hash_ol(fayl_nomi)
        with open(hash_nomi, 'w') as f:
            f.write(hash_qiymat)
        messagebox.showinfo("🔐 Saqlandi", "Backup va hash yaratildi.")
        return

    # Oldingi hashni o‘qish
    with open(hash_nomi, 'r') as f:
        eski_hash = f.read().strip()
    yangi_hash = hash_ol(fayl_nomi)

    if eski_hash == yangi_hash:
        messagebox.showinfo("✅ Natija", "Fayl o‘zgarmagan.")
    else:
        javob = messagebox.askyesno("⚠️ Diqqat", "Fayl o‘zgargan!\nFarqni ko‘rasizmi?")
        if javob:
            farqni_korsat(backup_nomi, fayl_nomi)

        tiklash = messagebox.askyesno("♻️ Tiklash", "Faylni backup’dan tiklashni xohlaysizmi?")
        if tiklash:
            faylni_tiklash(fayl_nomi, backup_nomi)

# GUI oyna
oyna = tk.Tk()
oyna.title("Fayl Butunligi Nazoratchisi")
oyna.geometry("400x200")

btn = tk.Button(oyna, text="📂 Fayl tanlash va tekshirish", command=tekshir_fayl)
btn.pack(pady=50)

oyna.mainloop()
