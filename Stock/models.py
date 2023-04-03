from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Produit(models.Model):

    CAT = (
        ('VIN','VIN'),
        ('SUCRERIE','SUCRERIE'),
        ('BIERE','BIERE'),
        ('LIQUEUR','LIQUEUR'),
        ('EAU','EAU'),
        ('CHAMPAGNE','CHAMPAGNE'),
        ('ENERGIE','ENERGIE'),
    )
    STAT = (
        ('ACTIF', 'ACTIF'),
        ('INACTIF', 'INACTIF'),
    )
    designation = models.CharField(max_length=200, null=True, blank=True)
    reference = models.CharField(max_length=200, null=True, blank=True)
    categorie = models.CharField(max_length=200, null=True, choices=CAT, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STAT, blank=True)
    date_creation = models.DateField(auto_now_add=True, null=True, blank=True)
    image = models.ImageField(upload_to='./image/', null=True, blank=True)

    def __str__(self):
        return self.designation


class TypeEmballage(models.Model):
    LIBELLE = (
        ('DETAIL', 'DETAIL'),
        ('CARTON', 'CARTON'),
        ('DEMI', 'DEMI'),
        ('QUART', 'QUART'),
        ('PACK', 'PACK'),
    )
    produit = models.ForeignKey(Produit, max_length=200, on_delete=models.CASCADE, null=True, blank=True)
    libelle = models.CharField(max_length=200, choices=LIBELLE, null=True, blank=True)
    code_barre = models.CharField(max_length=200, null=True, blank=True)
    prix_achat = models.FloatField(max_length=200, null=True, blank=True)
    prix_vente = models.FloatField(max_length=200, null=True, blank=True)
    quantite_stock = models.FloatField(max_length=200, null=True, blank=True, default=0)
    nombre_unite = models.FloatField(max_length=200, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f"{self.produit.designation}_{self.libelle}"


class Client(models.Model):
    nom_prenom = models.CharField(max_length=300, null=True, blank=True)
    adresse = models.CharField(max_length=200, null=True, blank=True)
    ville = models.CharField(max_length=200, null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f"{self.nom_prenom}"


class Fournisseur(models.Model):
    STAT = (
        ('ACTIF', 'ACTIF'),
        ('INACTIF', 'INACTIF'),
    )
    nom_prenom = models.CharField(max_length=200, null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    adresse = models.CharField(max_length=200, null=True, blank=True)
    adresse_email = models.EmailField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STAT, blank=True)
    date_creation = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.nom_prenom


"""class LigneFActure(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    reference = models.CharField(max_length=200, null=True, blank=True)
    montant_facture = models.FloatField(max_length=200, null=True, blank=True)
    avance = models.FloatField(max_length=200, null=True, blank=True)
"""


class FactureFournisseur(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    reference = models.CharField(max_length=200, null=True, blank=True)
    montant_facture = models.FloatField(max_length=200, null=True, blank=True)
    avance = models.FloatField(max_length=200, null=True, blank=True)
    reste_a_payer = models.FloatField(max_length=200, null=True, blank=True)
    date_facturation = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    date_enregistrement = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.reference}"


class Versement(models.Model):
    facture_fournisseur = models.ForeignKey(FactureFournisseur, on_delete=models.CASCADE, null=True, blank=True)
    montant_versement = models.FloatField(max_length=200, null=True, blank=True)
    date_versement = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.facture_fournisseur.reference}"


class Approvision(models.Model):
    type_emballage = models.ForeignKey(TypeEmballage, on_delete=models.CASCADE, null=True, blank=True)
    reference=models.CharField(max_length=200, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    quantite_approvision = models.FloatField(max_length=200, null=True, blank=True)
    prix_unitaire = models.FloatField(max_length=200, null=True, blank=True)
    date_approvision = models.DateField(auto_now_add=True, null=True, blank=True)
    date_renseigner = models.DateField(null=True, blank=True)
    save_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.fournisseur}"


class Image(models.Model):
    logo = models.ImageField(upload_to='./image/', null=True, blank=True)


class Vente(models.Model):
    type_emballage = models.ForeignKey(TypeEmballage, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    reference = models.CharField(max_length=200, null=True, blank=True)
    quantite_vente = models.FloatField(max_length=200, null=True, blank=True)
    total_unitaire = models.FloatField(max_length=200, null=True, blank=True)
    date_vente = models.DateField(auto_now_add=True, null=True, blank=True)
    save_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.type_emballage}"


class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,  null=True, blank=True)
    reference_vente = models.CharField(max_length=200, null=True, blank=True)
    montant_facture = models.FloatField(max_length=200, null=True, blank=True)
    avance = models.FloatField(max_length=200, null=True, blank=True)
    reste_a_payer = models.FloatField(max_length=200, null=True, blank=True)
    monnaie = models.FloatField(max_length=200, null=True, blank=True)
    date_facturation = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    date_facture = models.DateField(auto_now_add=True, null=True, blank=True)
    save_by = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True)
    def __str__(self):
        return f"{self.reference_vente}"


# class Remise(models.Model):
#     ref_facture = models.ForeignKey(Facture, on_delete=models.CASCADE, null=True, blank=True)
#     montant_remise = models.FloatField(max_length=200, null=True, blank=True)


class VersementClient(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, null=True, blank=True)
    montant_versement = models.FloatField(max_length=200, null=True, blank=True)
    date_versement = models.DateField(null=True, blank=True)


class Charges(models.Model):
    nom = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.nom}"


class Depenses(models.Model):
    charges = models.ForeignKey(Charges, on_delete=models.CASCADE, max_length=200, null=True, blank=True)
    montant = models.FloatField(max_length=200, null=True, blank=True)
    date_enregistrer = models.DateField(null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    save_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.charges}"
