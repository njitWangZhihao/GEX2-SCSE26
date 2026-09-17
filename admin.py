import json

def load_library(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

def save_library(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def find_book(books, search_text):
    query = str(search_text).strip().lower()

    if not query:
        return None

    for book_id, book in books.items():
        if str(book_id).strip().lower() == query:
            return book_id

        if str(book.get("title", "")).strip().lower() == query:
            return book_id

        if str(book.get("author", "")).strip().lower() == query:
            return book_id

    return None

def display_books(books):
    print("BOOK CATALOGUE")
    print("-" * 60)

    for book_id, book in books.items():
        status = "AVAILABLE" if book.get("available", False) else "ON LOAN"
        title = book.get("title", "")
        category = book.get("category", "")
        print(f"{book_id} | {title} | {category} | {status}")

def display_loans(loans, books):
    print("CURRENT LOANS")
    print("-" * 60)

    for loan in loans:
        book_id = loan.get("book_id", "")
        book = books.get(book_id, {})
        title = book.get("title", "Unknown")
        borrower = loan.get("borrower", "")
        print(f"{book_id} | {title} | Borrower: {borrower}")

def library_statistics(books):
    total = len(books)
    available = sum(1 for book in books.values() if book.get("available", False))
    borrowed = total - available
    return total, available, borrowed

def main():
    filename = "library.json"

    try:
        data = load_library(filename)
    except Exception:
        data = {
            "library": {},
            "categories": [],
            "books": {},
            "loans": []
        }

    library_info = data.get("library", {})
    categories = data.get("categories", [])
    books = data.get("books", {})
    loans = data.get("loans", [])

    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {library_info.get('name', '')}")
    print(f"Branch: {library_info.get('branch', '')}")
    print(f"Year: {library_info.get('year', '')}")
    print(f"Categories: {', '.join(categories)}")
    print()

    display_books(books)
    print()

    display_loans(loans, books)
    print()

    total, available, borrowed = library_statistics(books)

    print("STATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()
