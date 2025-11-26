from datetime import datetime

students = {}
librarian_account = {"admin": "12345"}  # default librarian account (username: admin, password: 12345)

books = {
    "1001": {"title": "Harry Potter", "available": True, "shelf": "Shelf A"},
    "1002": {"title": "Snow White", "available": False, "shelf": "Shelf B"},
    "1003": {"title": "Peter Pan", "available": True, "shelf": "Shelf A"},
    "1004": {"title": "Cinderella", "available": False, "shelf": "Shelf B"},
    "1005": {"title": "Little Red Riding Hood", "available": True, "shelf": "Shelf B"},
    "1006": {"title": "Hansel and Gretel", "available": False, "shelf": "Shelf C"},
    "1007": {"title": "The Witch Hunter", "available": True, "shelf": "Shelf C"},
    "1008": {"title": "The Chronicles of Narnia", "available": False, "shelf": "Shelf D"},
    "1009": {"title": "The God Father", "available": True, "shelf": "Shelf E"},
    "1010": {"title": "The Wizard of Oz", "available": False, "shelf": "Shelf A"}
}

borrowed_books = {}

# ---------------- STUDENT FUNCTIONS ----------------

def register_student():
    username = input("Enter username: ")
    password = input("Enter Password: ")
    if not username or not password:
        print("Please enter both username and password.\n")
        return
    if username in students:
        print("Account already exists!\n")
    else:
        students[username] = password
        print("students registered successfully!\n")

def login_student():
    username = input("Username: ")
    password = input("Enter Password: ")

    if username in students and students[username] == password:
        print("✅ Login successful!\n")
        student_menu(username)
    else:
        print("❌ Invalid credentials. Try again or register.\n")

def show_books():
    print("\n📚 Available Books:")
    print("------------------------------------------------------------")
    print("{:<8} {:<30} {:<12} {:<10}".format("ID", "Title", "Status", "Shelf"))
    print("------------------------------------------------------------")
    for book_id, info in sorted(books.items()):
        status = "Available" if info.get("available", False) else "Unavailable"
        shelf = info.get("shelf", "Unknown")
        print("{:<8} {:<30} {:<12} {:<10}".format(book_id, info.get("title", "Unknown Title"), status, shelf))
    print("------------------------------------------------------------\n")

def borrow_book(username):
    show_books()
    book_id = input("Enter Book ID to borrow (or type 'cancel' to go back): ")

    if not book_id:
        print("Please enter a Book ID.\n")
        return

    if book_id.lower() == "cancel":
        print("❌ Borrowing canceled.\n")
        return

    if book_id in books:
        if books[book_id]["available"]:
            confirm = input(f"Are you sure you want to borrow '{books[book_id]['title']}'? (yes/no): ").lower()
            if confirm != "yes":
                print("❌ Borrowing canceled.\n")
                return

            books[book_id]["available"] = False
            borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            borrowed_books.setdefault(username, []).append({
                "book_id": book_id,
                "borrow_date": borrow_date,
                "return_date": None
            })
            print(f"✅ You borrowed '{books[book_id]['title']}' on {borrow_date}\n")
        else:
            print("❌ Sorry, this book is already borrowed (Unavailable).\n")
    else:
        print("❌ Book not found.\n")

def return_book(username):
    user_borrowed = borrowed_books.get(username, [])
    if not user_borrowed:
        print("📭 You have no borrowed books.\n")
        return

    print("📘 Your borrowed books:")
    for record in user_borrowed:
        print(f"- {record['book_id']}: {books.get(record['book_id'], {}).get('title', 'Unknown Title')} (Borrowed: {record['borrow_date']})")
    print()

    book_id = input("Enter Book ID to return: ")
    if not book_id:
        print("Please enter a Book ID.\n")
        return

    for record in user_borrowed:
        if record["book_id"] == book_id and record["return_date"] is None:
            record["return_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            books[book_id]["available"] = True
            print(f"✅ You returned '{books[book_id]['title']}' on {record['return_date']}\n")
            return

    print("❌ Invalid Book ID (not in your borrowed list or already returned).\n")

def view_borrow_history(username):
    records = borrowed_books.get(username, [])
    if not records:
        print("📭 You haven't borrowed any books yet.\n")
        return

    print("\n📖 Borrow History:")
    print("----------------------------")
    for r in records:
        title = books.get(r["book_id"], {}).get("title", "Unknown Title")
        status = "✅ Returned" if r["return_date"] else "⏳ Not Returned"
        print(f"{r['book_id']} - {title}")
        print(f"   Borrowed: {r['borrow_date']}")
        print(f"   Re")