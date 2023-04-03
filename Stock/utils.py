import serial
from escpos.printer import Usb

def generate_receipt_content(contenu):
    # générer le contenu du reçu
    content = ""
    content += "SHALOM'COM & EVENTS CAVE\n"
    content += "Sis FAYA à 200 m\n"
    content += "Du super marché Bon Prix\n"
    content += "Tél: (+225) 07-00-00-00-00\n"
    content += "Date et heure: {}\n"
    content += "Articles achetés:\n"
    content += "--------------------------------\n"
    for item in contenu:
        content += "{}x {:<20} {:>7.2f}$\n"
    content += "--------------------------------\n"
    content += "Total:               {:>7.2f}$\n"
    content += "--------------------------------\n"
    content += "Les marchandises vendues ne sont ni\n"
    content += "échangés ni reprises. Merci et à bientot\n"

    return content


def print_receipt(content):
    reception_contenu = generate_receipt_content(content)

    p = Usb(0x0416, 0x5011)

    p.text(reception_contenu)

    p.cut()

    p.close()
