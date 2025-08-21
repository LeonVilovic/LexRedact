import os
import sys

def print_logo():
    ascii_art_logo = r"""
     _                  _____            _               _   
    | |                |  __ \          | |             | |  
    | |      ___ __  __| |__) | ___   __| |  __ _   ___ | |_ 
    | |     / _ \\ \/ /|  _  / / _ \ / _` | / _` | / __|| __|
    | |____|  __/ >  < | | \ \|  __/| (_| || (_| || (__ | |_ 
    |______|\___|/_/\_\|_|  \_\\___| \__,_| \__,_| \___| \__|
    """
    # Print in red
    print("\033[31m" + ascii_art_logo + "\033[0m")
def print_version():
    print("v 1.00")
def print_disclamer():
    print(
        "Nastavkom korišćenja ove aplikacije potvrđujete da ste pročitali i prihvatili Uslove korišćenja. Autor programa se odriče odgovornosti za eventualnu štetu nastalu korišćenjem aplikacije.")

def let_user_input_pdf_file_path():
    pdf_file_path = input("Enter the PDF file path: ")

    pdf_file_path = pdf_file_path.strip('"').strip("'")
    # Check if file exists and is a PDF
    if os.path.isfile(pdf_file_path) and pdf_file_path.lower().endswith(".pdf"):
        print("Valid PDF file:", pdf_file_path)
    else:
        print("Invalid file path or not a PDF. Exiting program.")
        sys.exit()
    return pdf_file_path

def let_user_filter_names(name_clusters):
    print("\n=== Spisak fizičkih lica ===")
    for i, name in enumerate(name_clusters.keys(), start=1):
        print(f"{i}) {name}")
    cluster_list = list(name_clusters.keys())
    while True:
        user_input = input("Ukucajte brojeve lica koje želite da cenzurišete, odvojene zapetama: ")
        try:
            selected_numbers = [int(num.strip()) for num in user_input.split(",")]
        except ValueError:
            print("Molimo unesite samo brojeve, odvojene zapetama.")
            continue
        if all(1 <= num <= len(cluster_list) for num in selected_numbers):
            break
        else:
            print(f"Brojevi moraju biti između 1 i {len(cluster_list)}. Pokušajte ponovo.")

    selected_names = [cluster_list[num - 1] for num in selected_numbers]
    print("Izabrana fizička lica:", selected_names)
    return selected_names