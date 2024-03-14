# from weasyprint import HTML

# def html_to_pdf_weasyprint(html_file_path, output_pdf_path):
#     try:
#         HTML(html_file_path).write_pdf(output_pdf_path)
#         print(f"PDF generated successfully at {output_pdf_path}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# import os 

# html_file = 'C:\\Users\\LaWindhaus\\OneDrive - Pöppelmann GmbH & Co. KG\\20231130_json2pdf\\DatenStattDokumente\\index.html'
# output = 'output.pdf'

# if os.path.exists(html_file):
#     html_to_pdf_weasyprint(html_file, output)
# else:
#     print(f"File not found: {html_file}")



import pdfkit

html_file = './templates/document.html'

def convert_html_to_pdf(input_filename, output_filename):
    options = {
        'page-size': 'A4'
    }
    pdfkit.from_file(input_filename, output_filename, options=options)

# Example usage
convert_html_to_pdf(html_file, 'output.pdf')