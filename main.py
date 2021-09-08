import os
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class Book:
    title: str
    author: str
    genre: str


def log_sign() -> str:
    log_action = input("[Log In] or [Sign Up]\n> ").title()
    while not val_login(log_action):
        print("invalid action")
        log_action = input("[Log In] or [Sign Up]\n> ").title()
    if val_login(log_action):
        if log_action == "Log In":
            user = login()
        else:
            user = signup()
    return user


def val_login(log_action: str) -> bool:
    return log_action == "Log In" or log_action == "Sign Up"


def signup() -> str:
    name = input("Username: ")
    line = find_user(name)
    while line is not None:
        print("This account already exists")
        action = input("[sign up] or [log in]\n> ").title()
        if action == "Sign Up":
            name = input("Username: ")
            line = find_user(name)
        elif action == "Log In":
            user = login()
            return user
        else:
            print("Invalid action")
    password = input("Password: ")
    validate = input("Re-enter password: ")
    while password != validate:
        print("Passwords do not match.")
        password = input("Password: ")
        validate = input("Re-enter password: ")
    with open("users.txt", "a") as users_file:
        users_file.write(name + " " + password)
    return name


def login() -> str:
    line = None
    name = input("Username: ")
    password = input("Password: ")
    line = find_user(name)
    while line is None:
        print("Invalid username or password")
        print("[Try] again or [sign] up.")
        action = input("> ").title()
        if action == "Try":
            name = input("Username: ")
            password = input("Password: ")
            line = find_user(name)
        else:
            user = signup()
            return user
    username, userpass = line.split()
    while password != userpass:
        print("Invalid password")
        password = input("Password: ")
    return username


def find_user(name: str) -> Optional[str]:
    with open("users.txt", "r") as users_file:
        lines = users_file.readlines()
        for line in lines:
            a, b = line.split()
            if name == a:
                return line
    return None


def genre_inp() -> str:
    genre = input(
        "\nChoose a Genre:\nFiction\nNon-Fiction\nHorror\nAction\nRomance\nSci-Fi\nDrama\nComedy\n\nInput Book Genre: "
    ).title()
    while not val_genre(genre):
        print("Invalid genre")
        genre = input("> ").title()
    return genre


def val_genre(genre: str) -> bool:
    genres = [
        "Horror",
        "Non-Fiction",
        "Fiction",
        "Action",
        "Romance",
        "Drama",
        "Comedy",
        "Sci-Fi",
    ]
    if genre in genres:
        return True
    return False


def add(books: Dict[str, Book]):
    title = input("Input Book Title or [back] to cancel: ")
    if title != "back":
        author = input("Author Name: ")
        books_file = open("books.txt")
        lines = books_file.readlines()
        for line in lines:
            a, b, c = line.split(" - ")
            while title == a and author == b:
                print("This book is already in the system.")
                title = input("Input Book Title: ")
                author = input("Author Name: ")
        genre = genre_inp()
        with open("books.txt", "a+") as books_file:
            books_file.write(f"\n{title} - {author} - {genre}")
        books[title] = Book(title, author, genre)


def all_books() -> None:
    try:
        with open("books.txt") as books_file:
            print("\n")
            for line in books_file:
                print(line.strip())
            print("\n")
    except FileNotFoundError:
        print("No books in system")


def view(user: str, books: Dict[str, Book]) -> None:
    by = input(
        "View by [all], view by [author], view by [genre], view by [title], view by [tag], or go [back]\n> "
    ).title()
    while by != "Back":
        if by == "All":
            all_books()
        elif by == "Author":
            author()
        elif by == "Genre":
            by_genre()
        elif by == "Title":
            title()
        elif by == "Tag":
            view_tag(user)
        else:
            print("Invalid action")
        by = input(
            "View by [all], view by [author], view by [genre], view by [title], view by [tag], or go [back]\n> "
        ).title()


def view_tag(user):
    tag = input("What tag would you like to view? [back] to cancel\n> ")
    if tag != "back":
        try:
            with open(f"{user}/{tag}.txt", "r") as tag_file:
                for line in tag_file:
                    print(line)
        except FileNotFoundError:
            print("This tag does not exist... Yet")


def author():
    author = input("Which author are you looking for? [back] to cancel\n> ")
    if author != "back":
        is_books = False
        with open("books.txt") as books_file:
            print("\n")
            for line in books_file:
                if author in line:
                    print(line.strip())
                    is_books = True
            if is_books == False:
                print("There are no books with this author listed")
            print("\n")


def by_genre() -> None:
    genre = input("Genre: ")
    is_genre = False
    with open("books.txt") as books_file:
        print("\n")
        for line in books_file:
            if genre in line:
                print(line.strip())
                is_genre = True
        if is_genre == False:
            print("There are no books with this genre listed")
        print("\n")


def title() -> None:
    title = input("Book Title or [back] to cancel: ")
    if title != "back":
        is_title = False
        with open("books.txt") as books_file:
            print("\n")
            for line in books_file:
                if title in line:
                    print(line.strip())
                    is_title = True
            if is_title == False:
                print("There are no books with this title listed")
            print("\n")


def opts() -> str:
    while True:
        action = input(
            "What would you like to do? [add] a book, [delete] a book, [view] by, add a [tag], [Log Out], or [quit]\n> "
        ).title()
        if val_act(action):
            return action
        else:
            print("This is not a valid action!")


def val_act(action: str) -> bool:
    actions = [
        "Add", "All", "View", "Tag", "Delete", "Update", "Log Out", "Quit"
    ]
    if action in actions:
        return True
    return False


def tag(user: str, books: Dict[str, Book]) -> None:
    try:
        os.mkdir(user)
    except FileExistsError:
        pass
    action = input(
        "Would you like to [create] a tag, [delete] a tag, [edit] a tag, or [add] to a tag, or go [back]?\n> "
    ).title()
    while action != "Back":
        if action == "Create":
            create_tag(user, books)
        elif action == "Add":
            add_tag(user, books)
        elif action == "Delete":
            delete_tag(user, books)
        elif action == "Edit":
            edit_tag(user, books)
        else:
            print("Invalid action")
        action = input(
            "Would you like to [create] a tag, [delete] a tag, [edit] a tag, or [add] to a tag?\n> "
        ).title()


def delete_tag(user: str, books: Dict[str, Book]) -> None:
    tag = input("Which tag would you like to remove? [back] to cancel\n> ")
    if tag != "back":
        try:
            with open(f"{user}/{tag}.txt"):
                pass
            final = input(f"Are you sure you want to delete {tag} [Y/N]?\n> ")
            if final == "Y":
                os.remove(f"{user}/{tag}.txt")
            else:
                print(f"{tag} tag was not deleted.")
        except FileNotFoundError:
            print("This tag list does not exist.")


def edit_tag(user: str, books: Dict[str, Book]) -> None:
    action = input(
        "Would you like to [rename] the file or edit the [list]?\n> ").title()
    if val_edit(action):
        if action == "Rename":
            edit_tag_name(user, books)
        elif action == "List":
            edit_tag_list(user, books)
    else:
        print("This is not a valid action!")


def edit_tag_list(user: str, books: Dict[str, Book]) -> None:
    tag = input("Which tag's list are you editing?\n> ")
    if os.path.exists(f"{user}/{tag}.txt"):
        with open(f"{user}/{tag}.txt", "r") as tfile:
            lines = tfile.readlines()
            for book in lines:
                print(book)
        which_book = input(
            "Which Book are you removing from this tag's list?\n> ").title()
        file = open(f"{user}/{tag}.txt", "w")
        file.close()
        with open(f"{user}/{tag}.txt", "a+") as tag_file:
            for line in lines:
                a, b, c = line.split(" - ")
                if which_book == a:
                    lines.remove(line)
                else:
                    tag_file.write(line)
                    print(line)
    else:
        print("This tag does not exist!")


def edit_tag_name(user: str, books: Dict[str, Book]):
    tag = input("What tag are you renaming?\n> ")
    if os.path.exists(f"{user}/{tag}.txt"):
        new = input("New tag name?\n> ")
        os.rename(fr"{user}/{tag}.txt", fr"{user}/{new}.txt")
    else:
        print("This tag does not exist!")


def val_edit(action: str) -> bool:
    acts = ["Rename", "List"]
    if action in acts:
        return True
    else:
        return False


def create_tag(user: str, books: Dict[str, Book]) -> None:
    tag = input("Name the tag: ")
    with open(f"{user}/{tag}.txt", "a+") as tfile:
        tfile.write("")
        add_to_tag(user, books, tag)
    print("\n")


def add_tag(user: str, books: Dict[str, Book]) -> None:
    tag = input("Which tag would you like to add to? [back] to cancel.\n> ")
    while True:
        if os.path.exists(f"{user}/{tag}.txt"):
            add_to_tag(user, books, tag)
            break
        elif tag == "back":
            break
        else:
            print("This tag does not exist yet!")
            tag = input("Which tag would you like to add to?\n> ")


def add_to_tag(user: str, books: Dict[str, Book], tag: str) -> None:
    adding = input("Type a book title or [Q]uit.\n> ")
    while adding != "Q":
        if val_add(adding, user, tag, books):
            with open(f"{user}/{tag}.txt", "a+") as tfile:
                tfile.write(books[adding].title + " - " +
                            books[adding].author + " - " + books[adding].genre)
        else:
            if adding not in books:
                print("This book is not in the system.")
            else:
                print("This book already exists in this tag!")
        adding = input("Type a book title or [Q]uit.\n> ")


def val_add(adding: str, user: str, tag: str, books: Dict[str, Book]) -> bool:
    file = open(f"{user}/{tag}.txt", "r")
    lines = file.readlines()
    file.close()
    if adding in books:
        double = False
        for line in lines:
            a, b, c = line.split(" - ")
            if adding == a:
                double = True
        if double == True:
            return False
        else:
            return True
    return False


def delete_book(books: Dict[str, Book]) -> None:
    books_file = open("books.txt")
    lines = books_file.readlines()
    title = input("Which book would you like to delete? [back] to cancel\n> ")
    if title != "back":
        is_valid = False
        for line in lines:
            a, b, c = line.split(" - ")
            if title == a:
                with open("books.txt", "a+"):
                    lines.remove(line)
                    is_valid = True
                    del books[title]
        with open("books.txt", "w") as books_file:
            for line in lines:
                books_file.write(line)
        if is_valid == False:
            print("This book does not exist")


def main() -> None:
    books: Dict[str, Book] = {}
    with open("books.txt", "r") as books_file:
        lines = books_file.readlines()
        for line in lines:
            a, b, c = line.split(" - ")
            books[a] = Book(a, b, c)
    user = log_sign()
    while True:
        action = opts()
        if action == "Add":
            add(books)
        elif action == "View":
            view(user, books)
        elif action == "Tag":
            tag(user, books)
        elif action == "Delete":
            delete_book(books)
        elif action == "Log Out":
            print("\nYou have successfuly logged out!\n")
            user = log_sign()
        elif action == "Quit":
            break
        else:
            print("Invalid action")


if __name__ == "__main__":
    main()
