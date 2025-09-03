from bs4 import BeautifulSoup
import subprocess

def extract_text_from_pdf(pdf_path):
    try:
        # Convert PDF to HTML using pdftohtml
        html_output = subprocess.check_output(["pdftohtml", "-s", "-stdout", pdf_path])
        soup = BeautifulSoup(html_output, "html.parser")
        text = soup.get_text()
        return text
    except subprocess.CalledProcessError as e:
        print(f"Error converting PDF to HTML: {e}")
        return None

if __name__ == "__main__":
    pdf_file = "/home/ubuntu/sge.maracanau.ce.gov.br/livros/BCM_Introdu%C3%A7%C3%A3o_.pdf"
    extracted_text = extract_text_from_pdf(pdf_file)
    if extracted_text:
        print(extracted_text)
    


