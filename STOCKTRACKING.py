import tkinter as tk
from tkinter import messagebox, filedialog
import yfinance as yf
import json
import matplotlib.pyplot as plt

class StockPortfolioTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("500x600")

        # Portfolio dictionary to store stock symbols and their quantities
        self.portfolio = {}

        # UI Elements
        self.symbol_label = tk.Label(root, text="Stock Symbol:")
        self.symbol_label.pack()
        self.symbol_entry = tk.Entry(root)
        self.symbol_entry.pack()

        self.quantity_label = tk.Label(root, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.pack()

        self.add_button = tk.Button(root, text="Add Stock", command=self.add_stock)
        self.add_button.pack()

        self.remove_button = tk.Button(root, text="Remove Stock", command=self.remove_stock)
        self.remove_button.pack()

        self.track_button = tk.Button(root, text="Track Portfolio", command=self.track_portfolio)
        self.track_button.pack()

        self.save_button = tk.Button(root, text="Save Portfolio", command=self.save_portfolio)
        self.save_button.pack()

        self.load_button = tk.Button(root, text="Load Portfolio", command=self.load_portfolio)
        self.load_button.pack()

        self.graph_button = tk.Button(root, text="Show Performance Chart", command=self.show_performance_chart)
        self.graph_button.pack()

        self.output_box = tk.Text(root, height=10, width=60)
        self.output_box.pack()

    def add_stock(self):
        symbol = self.symbol_entry.get().upper()
        quantity = self.quantity_entry.get()

        if symbol and quantity.isdigit():
            self.portfolio[symbol] = int(quantity)
            messagebox.showinfo("Success", f"Added {quantity} shares of {symbol} to the portfolio.")
        else:
            messagebox.showerror("Error", "Please enter a valid stock symbol and quantity.")

    def remove_stock(self):
        symbol = self.symbol_entry.get().upper()

        if symbol in self.portfolio:
            del self.portfolio[symbol]
            messagebox.showinfo("Success", f"Removed {symbol} from the portfolio.")
        else:
            messagebox.showerror("Error", "Stock symbol not found in portfolio.")

    def track_portfolio(self):
        self.output_box.delete('1.0', tk.END)

        if not self.portfolio:
            self.output_box.insert(tk.END, "Portfolio is empty.\n")
            return

        total_value = 0
        for symbol, quantity in self.portfolio.items():
            stock = yf.Ticker(symbol)
            stock_price = stock.info['currentPrice']
            value = stock_price * quantity
            total_value += value
            self.output_box.insert(tk.END, f"{symbol}: {quantity} shares @ ${stock_price:.2f} = ${value:.2f}\n")

        self.output_box.insert(tk.END, f"\nTotal Portfolio Value: ${total_value:.2f}\n")

    def save_portfolio(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.portfolio, file)
            messagebox.showinfo("Success", "Portfolio saved successfully.")

    def load_portfolio(self):
        file_path = filedialog.askopenfilename(defaultextension=".json",
                                               filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.portfolio = json.load(file)
            messagebox.showinfo("Success", "Portfolio loaded successfully.")
            self.track_portfolio()

    def show_performance_chart(self):
        if not self.portfolio:
            messagebox.showerror("Error", "Portfolio is empty.")
            return

        symbols = list(self.portfolio.keys())
        quantities = list(self.portfolio.values())
        values = []

        for symbol in symbols:
            stock = yf.Ticker(symbol)
            stock_price = stock.info['currentPrice']
            values.append(stock_price)

        plt.figure(figsize=(10, 6))
        plt.bar(symbols, values, color='blue')
        plt.xlabel("Stock Symbol")
        plt.ylabel("Stock Price ($)")
        plt.title("Stock Performance")
        plt.show()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = StockPortfolioTracker(root)
    root.mainloop()
