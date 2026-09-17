from admin import (
    find_book,
    load_library,
    save_library
)

def books_in_category(books, category):
    query = str(category).strip().lower()

    if not query:
        return []

    result = []

    for book_id, book in books.items():
        if str(book.get("category", "")).strip().lower() == query:
            result.append(book_id)

    return result

def search_by_title(books, search_text):
    query = str(search_text).strip().lower()

    if not query:
        return []

    result = []

    for book_id, book in books.items():
        if query in str(book.get("title", "")).lower():
            result.append(book_id)

    return result

def borrow_book(books, loans, search_text, borrower):
    book_id = find_book(books, search_text)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if borrower is None or str(borrower).strip() == "":
        return "EMPTY_NAME"

    if not books[book_id].get("available", False):
        return "NOT_AVAILABLE"

    books[book_id]["available"] = False
    loans.append({
        "book_id": book_id,
        "borrower": str(borrower).strip()
    })

    return "OK"

def return_book(books, loans, book_title, borrower):
    book_id = find_book(books, book_title)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    if borrower is None or str(borrower).strip() == "":
        return "EMPTY_NAME"

    borrower_clean = str(borrower).strip().lower()
    matching_loan = None

    for loan in loans:
        if (
            loan.get("book_id") == book_id
            and str(loan.get("borrower", "")).strip().lower() == borrower_clean
        ):
            matching_loan = loan
            break

    if matching_loan is None:
        return "NOT_ON_LOAN"

    books[book_id]["available"] = True
    loans.remove(matching_loan)

    return "OK"

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

    books = data.get("books", {})
    loans = data.get("loans", [])

    print("LIBRARY USER SYSTEM")
    print("=" * 60)

    while True:
        print("\nMenu:")
        print("1. Search by title")
        print("2. Search by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")

        try:
            choice = input("Select an option: ").strip()
        except EOFError:
            break

        if choice == "1":
            search_text = input("Enter title search text: ").strip()
            results = search_by_title(books, search_text)

            if results:
                for book_id in results:
                    book = books.get(book_id, {})
                    status = "AVAILABLE" if book.get("available", False) else "ON LOAN"
                    print(
                        f"{book_id} | {book.get('title', '')} | "
                        f"{book.get('category', '')} | {status}"
                    )
            else:
                print("No books found.")

        elif choice == "2":
            category = input("Enter category: ").strip()
            results = books_in_category(books, category)

            if results:
                for book_id in results:
                    book = books.get(book_id, {})
                    status = "AVAILABLE" if book.get("available", False) else "ON LOAN"
                    print(
                        f"{book_id} | {book.get('title', '')} | "
                        f"{book.get('category', '')} | {status}"
                    )
            else:
                print("No books found.")

        elif choice == "3":
            search_text = input("Enter book ID/title/author: ").strip()
            borrower = input("Enter borrower name: ").strip()
            result = borrow_book(books, loans, search_text, borrower)
            print(result)

        elif choice == "4":
            search_text = input("Enter book ID/title/author: ").strip()
            borrower = input("Enter borrower name: ").strip()
            result = return_book(books, loans, search_text, borrower)
            print(result)

        elif choice == "5":
            data["books"] = books
            data["loans"] = loans

            try:
                save_library(data, filename)
            except Exception:
                pass

            print("Goodbye!")
            break

        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()
