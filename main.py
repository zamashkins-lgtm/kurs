
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "port_data.json"

class PortMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Monitor Demo")
        self.root.geometry("980x620")
        self.data = self.load_data()

        top = ttk.Frame(root, padding=12)
        top.pack(fill="x")
        ttk.Label(top, text="Мониторинг порта", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(top, text=f"Обновлено: {self.data['updated_at']}").pack(anchor="w")

        cards = ttk.Frame(root, padding=12)
        cards.pack(fill="x")
        self.kpi_vars = {}
        for i, (label, key, suffix) in enumerate([
            ("Грузооборот", "cargo_turnover_tpd", " т/сутки"),
            ("Глубина", "depth_m", " м"),
            ("Ветер", "wind_speed_ms", " м/с"),
            ("Прибытия", "arrivals_today", ""),
        ]):
            f = ttk.LabelFrame(cards, text=label, padding=12)
            f.grid(row=0, column=i, padx=6, sticky="nsew")
            v = tk.StringVar(value=f"{self.data['summary'][key]}{suffix}")
            self.kpi_vars[key] = (v, suffix)
            ttk.Label(f, textvariable=v, font=("Segoe UI", 15, "bold")).pack()
            cards.columnconfigure(i, weight=1)

        btns = ttk.Frame(root, padding=(12,0,12,0))
        btns.pack(fill="x")
        ttk.Button(btns, text="Обновить", command=self.refresh).pack(side="left")
        ttk.Button(btns, text="Показать рекомендации", command=self.show_recommendations).pack(side="left", padx=8)

        table_frame = ttk.Frame(root, padding=12)
        table_frame.pack(fill="both", expand=True)
        cols = ("name","type","berth","arrival","departure","status")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        headers = ["Судно","Тип","Причал","Прибытие","Отправление","Статус"]
        for c, h in zip(cols, headers):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=120, anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.fill_table()

    def load_data(self):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def fill_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for s in self.data["ship_schedule"]:
            self.tree.insert("", "end", values=(s["name"], s["type"], s["berth"], s["arrival"], s["departure"], s["status"]))

    def refresh(self):
        self.data = self.load_data()
        for key, (var, suffix) in self.kpi_vars.items():
            var.set(f"{self.data['summary'][key]}{suffix}")
        self.fill_table()

    def show_recommendations(self):
        messagebox.showinfo(
            "Рекомендации",
            "1. Снизить нагрузку на Причал 5.\n"
            "2. Использовать Причал 4 как резервный.\n"
            "3. При ветре > 8 м/с предупреждать маломерные суда."
        )

if __name__ == "__main__":
    root = tk.Tk()
    try:
        from tkinter import ttk
    except Exception:
        pass
    app = PortMonitorApp(root)
    root.mainloop()
