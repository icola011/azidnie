from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime
import os

# Fonction pour formater les montants en MAD
def format_mad(amount):
    if amount is None:
        return "0,00 MAD"
    return f"{amount:,.2f}".replace(",", " ").replace(".", ",") + " MAD"

# Fonction pour générer un PDF de facture
def generate_facture_pdf(facture, articles, total_ht, total_tva, total_ttc):
    # Créer le dossier pour les PDF s'il n'existe pas
    pdf_dir = os.path.join(os.getcwd(), "static", "pdf")
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Nom du fichier PDF
    pdf_filename = f"facture_{facture['numero']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    
    # Créer le document PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    
    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    
    # Contenu du PDF
    elements = []
    
    # Titre
    if facture["type"] == "client":
        title = "FACTURE CLIENT"
    else:
        title = "FACTURE FOURNISSEUR"
    
    elements.append(Paragraph(f"<font size=16><b>{title}</b></font>", styles['Center']))
    elements.append(Spacer(1, 20))
    
    # Informations de la facture
    elements.append(Paragraph(f"<b>Numéro de facture :</b> {facture['numero']}", styles['Normal']))
    elements.append(Paragraph(f"<b>Date :</b> {facture['date']}", styles['Normal']))
    elements.append(Paragraph(f"<b>{'Client' if facture['type'] == 'client' else 'Fournisseur'} :</b> {facture['nom_client_fournisseur']}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Tableau des articles
    data = [
        ["Article", "Quantité", "Prix unitaire", "TVA (%)", "Montant HT", "Montant TTC"]
    ]
    
    for article in articles:
        montant_ht = article["quantite"] * article["prix_unitaire"]
        montant_tva = montant_ht * (article["tva"] / 100)
        montant_ttc = montant_ht + montant_tva
        
        data.append([
            article["nom"],
            f"{article['quantite']:.2f}",
            format_mad(article["prix_unitaire"]),
            f"{article['tva']:.2f}%",
            format_mad(montant_ht),
            format_mad(montant_ttc)
        ])
    
    # Ajouter les totaux
    data.append(["" for _ in range(4)] + ["<b>Total HT</b>", format_mad(total_ht)])
    data.append(["" for _ in range(4)] + ["<b>Total TVA</b>", format_mad(total_tva)])
    data.append(["" for _ in range(4)] + ["<b>Total TTC</b>", format_mad(total_ttc)])
    
    # Créer le tableau
    table = Table(data, colWidths=[5*cm, 2*cm, 3*cm, 2*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -4), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Notes
    if facture.get("notes"):
        elements.append(Paragraph("<b>Notes :</b>", styles['Normal']))
        elements.append(Paragraph(facture["notes"], styles['Normal']))
    
    # Pied de page
    elements.append(Spacer(1, 30))
    elements.append(Paragraph(f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Right']))
    
    # Générer le PDF
    doc.build(elements)
    
    return pdf_path