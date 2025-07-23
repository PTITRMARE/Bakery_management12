import pandas as pd 
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class BakeryOrderManagement:
    def __init__(self):
        self.orders = pd.DataFrame(columns=["Customer Name", "Item", "Quantity", "Order Date"])
        self.inventory = {"Bread": 50, "Cake": 30, "Pastry": 40, "Cookies": 100}  # Example stock

    def add_order(self):
        try:
            customer_name = input("Enter customer name: ").strip()
            item = input(f"Enter item ({', '.join(self.inventory.keys())}): ").strip().title()
            quantity = int(input("Enter quantity: "))

            if item not in self.inventory:
                print("Item not in inventory.")
                return

            if quantity > self.inventory[item]:
                print(f"Only {self.inventory[item]} {item}s available in stock.")
                return

            order_date = datetime.now().strftime("%Y-%m-%d")

            new_order = {
                "Customer Name": customer_name,
                "Item": item,
                "Quantity": quantity,
                "Order Date": order_date
            }

            self.orders = pd.concat([self.orders, pd.DataFrame([new_order])], ignore_index=True)
            self.inventory[item] -= quantity
            print("Order added and inventory updated.")

        except ValueError:
            print("Invalid input. Quantity must be a number.")

    def view_orders(self):
        if self.orders.empty:
            print("No orders available.")
        else:
            print("\nCurrent Orders:")
            print(self.orders.reset_index().rename(columns={'index': 'Order ID'}))

    def update_order(self):
        try:
            self.view_orders()
            order_id = int(input("Enter Order ID to update: "))

            if 0 <= order_id < len(self.orders):
                old_item = self.orders.at[order_id, "Item"]
                old_qty = self.orders.at[order_id, "Quantity"]

                item = input("Enter new item: ").strip().title()
                quantity = int(input("Enter new quantity: "))

                if item not in self.inventory:
                    print("Item not in inventory.")
                    return

                available_qty = self.inventory[item] + old_qty
                if quantity > available_qty:
                    print(f"Only {available_qty} {item}s available (after rollback).")
                    return

                self.orders.at[order_id, "Item"] = item
                self.orders.at[order_id, "Quantity"] = quantity

                self.inventory[old_item] += old_qty
                self.inventory[item] -= quantity
                print("Order updated and inventory adjusted.")

            else:
                print("Order ID not found.")
        except ValueError:
            print("Invalid input.")

    def delete_order(self):
        try:
            self.view_orders()
            order_id = int(input("Enter Order ID to delete: "))

            if 0 <= order_id < len(self.orders):
                item = self.orders.at[order_id, "Item"]
                qty = self.orders.at[order_id, "Quantity"]
                self.inventory[item] += qty

                self.orders = self.orders.drop(order_id).reset_index(drop=True)
                print("Order deleted and inventory restored.")
            else:
                print("Order ID no found.")
        except ValueError:
            print("Invalid input.")

    def search_orders(self):
        keyword = input("Enter customer name or item to search: ").strip().lower()
        results = self.orders[self.orders.apply(
            lambda row: keyword in row["Customer Name"].lower() or keyword in row["Item"].lower(),
            axis=1
        )]

        if results.empty:
            print("No matching orders found.")
        else:
            print("\nSearch Results:")
            print(results.reset_index().rename(columns={'index': 'Order ID'}))

    def view_inventory(self):
        print("\nCurrent Inventory:")
        for item, stock in self.inventory.items():
            print(f"{item}: {stock} remaining")

    def generate_invoice(self):
        try:
            self.view_orders()
            order_id = int(input("Enter Order ID to generate invoice: "))
            if 0 <= order_id < len(self.orders):
                order = self.orders.loc[order_id]
                filename = f"invoice_order_{order_id}.pdf"
                c = canvas.Canvas(filename, pagesize=letter)
                c.setFont("Helvetica", 12)

                c.drawString(100, 750, f"Invoice for Order #{order_id}")
                c.drawString(100, 730, f"Customer Name: {order['Customer Name']}")
                c.drawString(100, 710, f"Item: {order['Item']}")
                c.drawString(100, 690, f"Quantity: {order['Quantity']}")
                c.drawString(100, 670, f"Order Date: {order['Order Date']}")
                c.drawString(100, 650, "Thank you for your order!")

                c.save()
                print(f"Invoice generated: {filename}")
            else:
                print("Order ID not found.")
        except ValueError:
            print("Invalid input.")

    def save_to_excel(self):
        self.orders.to_excel("bakery_orders.xlsx", index=False)
        print("Orders saved to 'bakery_orders.xlsx'.")

def main():
    order_system = BakeryOrderManagement()

    actions = {
        '1': order_system.add_order,
        '2': order_system.view_orders,
        '3': order_system.update_order,
        '4': order_system.delete_order,
        '5': order_system.search_orders,
        '6': order_system.view_inventory,
        '7': order_system.generate_invoice,
        '8': order_system.save_to_excel
    }

    while True:
        print("\nMENU")
        print("1. Add Order\n2. View Orders\n3. Update Order\n4. Delete Order")
        print("5. Search Orders\n6. View Inventory\n7. Generate Invoice PDF\n8. Save to Excel\n9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '9':
            print("Exiting Bakery Order Management. Goodbye!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
