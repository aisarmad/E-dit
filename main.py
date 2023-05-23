import PyPDF2
import interface

pdf_path = r'C:\Users\sohai\Downloads\Documents\Zafar Sulehri Greenhall Biology Notes.pdf'
with open(pdf_path, 'rb') as file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(file)

    # Call the create_interface function to create the user interface
    interface.create_interface(pdf_reader)
