import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd

# Load dataset
try:
    import os
    csv_path = os.path.join(os.path.dirname(__file__), 'movies.csv')
    df = pd.read_csv(csv_path)

except:
    messagebox.showerror("Error", "Make sure movies.csv is in the same folder!")
    exit()

# App Class
class MovieRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movie Recommender System")
        self.root.geometry("850x650")
        self.root.configure(bg="#f8f9fa")

        title = tk.Label(root, text="Movie Recommender", font=("Helvetica", 24, "bold"), bg="#f8f9fa", fg="#333")
        title.pack(pady=20)

        self.create_filters()
        self.create_output()

    def create_filters(self):
        frame = tk.Frame(self.root, bg="#f8f9fa")
        frame.pack(pady=10)

        # Industry
        tk.Label(frame, text="Industry:", font=("Arial", 12), bg="#f8f9fa").grid(row=0, column=0, padx=10, pady=5)
        self.industry_var = tk.StringVar()
        industry_list = ['Any'] + sorted(df["industry"].dropna().unique())
        self.industry_menu = ttk.Combobox(frame, textvariable=self.industry_var, values=industry_list, state="readonly", width=18)
        self.industry_menu.grid(row=0, column=1, padx=10)
        self.industry_menu.current(0)

        # Genre
        tk.Label(frame, text="Genre:", font=("Arial", 12), bg="#f8f9fa").grid(row=0, column=2, padx=10)
        self.genre_var = tk.StringVar()
        genre_list = ['Any'] + sorted(df["genre"].dropna().unique())
        self.genre_menu = ttk.Combobox(frame, textvariable=self.genre_var, values=genre_list, state="readonly", width=18)
        self.genre_menu.grid(row=0, column=3, padx=10)
        self.genre_menu.current(0)

        # Rating
        tk.Label(frame, text="Min Rating:", font=("Arial", 12), bg="#f8f9fa").grid(row=1, column=0, padx=10, pady=5)
        self.rating_var = tk.DoubleVar(value=0)
        rating_scale = ttk.Scale(frame, from_=0, to=10, orient="horizontal", variable=self.rating_var, length=160)
        rating_scale.grid(row=1, column=1, padx=10)

        # Year Range
        tk.Label(frame, text="Year After:", font=("Arial", 12), bg="#f8f9fa").grid(row=1, column=2, padx=10)
        self.year_var = tk.IntVar(value=2000)
        year_spin = tk.Spinbox(frame, from_=1900, to=2050, textvariable=self.year_var, width=10)
        year_spin.grid(row=1, column=3, padx=10)

        # Button
        search_btn = tk.Button(self.root, text="🔍 Recommend", font=("Arial", 14), bg="#007bff", fg="white", command=self.recommend)
        search_btn.pack(pady=15)

    def create_output(self):
        self.result_box = scrolledtext.ScrolledText(self.root, height=20, width=100, font=("Consolas", 11))
        self.result_box.pack(pady=10)

    def recommend(self):
        industry = self.industry_var.get()
        genre = self.genre_var.get()
        min_rating = self.rating_var.get()
        min_year = self.year_var.get()

        result = df.copy()

        if industry != "Any":
            result = result[result["industry"] == industry]
        if genre != "Any":
            result = result[result["genre"] == genre]
        result = result[(result["rating"] >= min_rating) & (result["year"] >= min_year)]

        result = result.sort_values(by="rating", ascending=False).head(15)

        self.result_box.delete("1.0", tk.END)

        if result.empty:
            self.result_box.insert(tk.END, "❌ No results found. Try adjusting filters.\n")
            return

        self.result_box.insert(tk.END, f"✅ Found {len(result)} result(s):\n\n")
        for _, row in result.iterrows():
            info = (
                f"🎬 {row['title']} ({row['year']})\n"
                f"📽️ Genre: {row['genre']} | Industry: {row['industry']}\n"
                f"⭐ Rating: {row['rating']}\n"
                f"📖 Summary: {row['summary']}\n"
                f"{'-'*70}\n"
            )
            self.result_box.insert(tk.END, info)

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieRecommenderApp(root)
    root.mainloop()
