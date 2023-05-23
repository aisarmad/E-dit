import tkinter as tk
from tkinter import messagebox
import PyPDF2


bookmarks = []  # Define the bookmarks list


def load_page(pdf_reader, page_num, book_text):
    try:
        page = pdf_reader.pages[page_num]
        content = page.extract_text()
        book_text.delete("1.0", tk.END)
        book_text.insert(tk.END, content)
    except IndexError:
        messagebox.showinfo("Error", "Invalid page number!")

def previous_page(pdf_reader, book_text, current_page):
    if current_page > 0:
        current_page -= 1
        load_page(pdf_reader, current_page, book_text)

def next_page(pdf_reader, book_text, current_page):
    if current_page < len(pdf_reader.pages) - 1:
        current_page += 1
        load_page(pdf_reader, current_page, book_text)

def zoom_in(book_text):
    # Get the current font size of the text widget
    font_size = int(book_text.cget("font").split()[1])

    # Increase the font size by 1 point
    new_font_size = font_size + 1

    # Set the font size of the text widget to the new value
    book_text.config(font=("Arial", new_font_size))

def zoom_out(book_text):
    # Get the current font size of the text widget
    font_size = int(book_text.cget("font").split()[1])

    # Decrease the font size by 1 point
    new_font_size = font_size - 1

    # Set the font size of the text widget to the new value
    book_text.config(font=("Arial", new_font_size))

def select_text(book_text):
    # Get the current selection in the text widget
    selection = book_text.get(tk.SEL_FIRST, tk.SEL_LAST)

    # If there is no selection, return
    if not selection:
        return

    # Copy the selection to the clipboard
    book_text.clipboard_clear()
    book_text.clipboard_append(selection)

def bookmark(book_text):
    # Get the current page number
    page_num = float(book_text.index(tk.END).split(".")[0])

    # Add the page number to the bookmarks list
    bookmarks.append(page_num)

    # Display a messagebox to confirm the bookmark
    messagebox.showinfo("Bookmark Added", "Page " + str(page_num) + " has been added to your bookmarks.")

def create_interface(pdf_reader):
    # Create the main application window
    window = tk.Tk()
    window.title("E-dit - E-book Reader")
    window.geometry("800x600")

    # Create a frame for the book content
    book_frame = tk.Frame(window)
    book_frame.pack(fill=tk.BOTH, expand=True)

    # Create a text widget to display the book content
    book_text = tk.Text(book_frame, wrap=tk.WORD, font=("Arial", 12))
    book_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a scrollbar for the book content
    scrollbar = tk.Scrollbar(book_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    book_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=book_text.yview)

    # Create a toolbar frame
    toolbar_frame = tk.Frame(window)
    toolbar_frame.pack(fill=tk.X)

    # Create toolbar buttons
    button_previous = tk.Button(toolbar_frame, text="Previous Page", command=lambda: previous_page(pdf_reader, book_text, current_page))
    button_previous.pack(side=tk.LEFT, padx=10, pady=5)
    button_next = tk.Button(toolbar_frame, text="Next Page",
                            command=lambda: next_page(pdf_reader, book_text, current_page))
    button_next.pack(side=tk.LEFT, padx=10, pady=5)

    button_zoom_in = tk.Button(toolbar_frame, text="Zoom In", command=lambda: zoom_in(book_text))
    button_zoom_in.pack(side=tk.LEFT, padx=10, pady=5)

    button_zoom_out = tk.Button(toolbar_frame, text="Zoom Out", command=lambda: zoom_out(book_text))
    button_zoom_out.pack(side=tk.LEFT, padx=10, pady=5)

    button_select_text = tk.Button(toolbar_frame, text="Select Text", command=lambda: select_text(book_text))
    button_select_text.pack(side=tk.LEFT, padx=10, pady=5)

    button_bookmark = tk.Button(toolbar_frame, text="Bookmark Page", command=lambda: bookmark(book_text))
    button_bookmark.pack(side=tk.LEFT, padx=10, pady=5)

    # Load the initial page
    current_page = 0
    load_page(pdf_reader, current_page, book_text)

    # Start the main event loop
    window.mainloop()
