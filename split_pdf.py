import PyPDF2
import os

def split_pdf(input_pdf_path, output_folder, n):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开PDF文件
    with open(input_pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        total_pages = len(reader.pages)

        for start_page in range(0, total_pages, n):
            writer = PyPDF2.PdfWriter()
            end_page = min(start_page + n, total_pages)
            for page_number in range(start_page, end_page):
                current_page = reader.pages[page_number]
                writer.add_page(current_page)

            output_filename = f"{output_folder}/pages_{start_page + 1}_to_{end_page}.pdf"
            with open(output_filename, 'wb') as output_pdf_file:
                writer.write(output_pdf_file)
            print(f"Pages {start_page + 1} to {end_page} saved as {output_filename}")

# 示例使用
input_pdf_path = 'USMTXML\\usmtdoc.pdf'
output_folder = 'USMTXML\\toc_split'
pages_per_split = 31  # 每5页拆分一个PDF文件
split_pdf(input_pdf_path, output_folder, pages_per_split)