from .reference import *
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

# changement de mot de passe

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


from datetime import datetime
# filtrage de date
from django.db.models.functions import ExtractMonth
from django.db.models import Q

# Create your views here.

@login_required(login_url='login')
def accueil(request):
    liste_facture = FactureFournisseur.objects.all()
    liste_facture_payer = FactureFournisseur.objects.filter(reste_a_payer=0)
    liste_facture_impayer = FactureFournisseur.objects.filter(status="IMPAYER")
    compt_facture_payer = liste_facture_payer.count()
    comp_facture = liste_facture.count()

    facture_impayer = liste_facture_impayer.count
    produits = TypeEmballage.objects.all()
    compte_produit = produits.count()
    nom_plus_vendu = ""
    nom_moins_vendu = ""
    total = 0
    v = []
    for i in produits:
        filtre_dans_vente = Vente.objects.filter(type_emballage=i.id)
        t = 0
        for j in filtre_dans_vente:
            t = t + int(j.quantite_vente)
        v = v + [t]
        if t >= max(v):
            nom_plus_vendu = str(i.produit)
        elif t <= min(v):
            nom_moins_vendu = str(i.produit)

        total = total + i.quantite_stock
    le_plus_vendu = str(max(v))
    le_moins_vendu = str(min(v))
    context = {
        'compte_produit': compte_produit,
        'total': total,
        'le_plus_vendu': le_plus_vendu,
        'le_moins_vendu': le_moins_vendu,
        'nom_plus_vendu': nom_plus_vendu,
        'nom_moins_vendu': nom_moins_vendu,
        'compt_facture_payer': compt_facture_payer,
        'facture_impayer':facture_impayer,
        'comp_facture': comp_facture,
        'liste_facture_impayer': liste_facture_impayer,
        'liste_facture_payer': liste_facture_payer,

    }

    return render(request, 'stock/index.html', context)

@login_required(login_url='login')
def liste_vente(request):
    vente = Vente.objects.order_by('-date_vente')
    context = {
        'vente': vente,

    }
    return render(request, 'vente/liste_vente.html', context)


@login_required(login_url='login')
def point_facture_vente(request):
    if 'boutton_recherche_vente' and request.method == 'POST':
        date_rechercher = request.POST.get('date_rechercher_vente')
        facture = Facture.objects.filter(date_facturation=date_rechercher)
        compte_facture = facture.count()
        point = 0
        for i in facture:
            point = point + i.montant_facture

    context = {
        'compte_facture': compte_facture,
        'point': point,
        'vente_par_date': facture,
    }
    return render(request, 'vente/point_vente.html', context)


@login_required(login_url='login')
def liste_produits(request):
    produits = TypeEmballage.objects.order_by('-date_creation')

    # pagination code
    pagination = Paginator(produits, 7)
    page = request.GET.get('page', 1)
    try:
        produits = pagination.page(page)
    except PageNotAnInteger:
        produits = pagination.page(1)
    except EmptyPage:
        produits = pagination.page(pagination.num_pages)

    if request.method == 'POST':
        if 'suppboutton':
            id_prod = request.POST.get('id_pour_supprimer')
            produit = TypeEmballage.objects.get(id=id_prod)
            produit.delete()
            messages.success(request, 'Supprimer avec succès')
    context = {
        'produits': produits
    }
    return render(request, 'produit/liste_produits.html', context)


@login_required(login_url='login')
def ajouter_produits(request):
    if request.method == 'POST':
        if 'ajouter_produit' in request.POST and request.FILES:

            designation = request.POST.get('designation')
            reference = request.POST.get('reference')
            categorie = request.POST.get('categorie')
            status = request.POST.get('status')
            image = request.FILES.get('image')

            # verifions si le produits existe déja
            produit = Produit.objects.filter(reference=reference)
            if not produit:
                Produit.objects.create(
                    designation=designation,
                    reference=reference,
                    categorie=categorie,
                    status=status,
                    image=image
                )

                messages.success(request, 'Enregistrer avec succès')
            else:
                messages.error(request, 'Veuillez svp entrez les informations correctes')

    produits = Produit.objects.all()
    if request.method == 'POST':
        if 'ajouter_prix' in request.POST:
            nom_produit = request.POST.get('nom_produit')
            produit = Produit.objects.get(id=nom_produit)
            type = request.POST.get('type')
            code_barre = request.POST.get('code_barre')
            prix_achat = request.POST.get('prix_achat')
            prix_vente = request.POST.get('prix_vente')
            nombre_unite = request.POST.get('nombre_unite')

            # verifions si le produits existe déja
            prix = TypeEmballage.objects.filter(code_barre=code_barre)
            if not prix:
                TypeEmballage.objects.create(
                produit=produit,
                libelle=type,
                code_barre=code_barre,
                prix_achat=prix_achat,
                prix_vente=prix_vente,
                nombre_unite=nombre_unite
                )
                messages.success(request, 'Enregistrer avec succès')
            else:
                messages.error(request, 'Veuillez svp entrez les informations correctes')

            return redirect('/liste_produits')

    context = {
        'produits':produits
    }
    return render(request, 'produit/ajouter_produits.html', context)


@login_required(login_url='login')
def liste_approvision(request):
    if request.method == 'POST':
        if 'button_rechercher':
            fournisseur = request.POST.get('fournisseur_rechercher')
            obj_fournisseur = Fournisseur.objects.get(id=fournisseur)
            date_rechercher = request.POST.get('date_rechercher')

            listes = Approvision.objects.filter(fournisseur=obj_fournisseur, date_renseigner=date_rechercher)

    elif 'voir_tous':
        listes = Approvision.objects.order_by('-date_renseigner')

        pagination = Paginator(listes, 10)
        page = request.GET.get('page', 1)
        try:
            listes = pagination.page(page)
        except PageNotAnInteger:
            listes = pagination.page(1)
        except EmptyPage:
            listes = pagination.page(pagination.num_pages)

    context = {
        'listes': listes
    }
    return render(request, 'produit/liste_approvision.html', context)


@login_required(login_url='login')
def ajouter_versement(request, pk):
    facture = FactureFournisseur.objects.get(id=pk)
    if request.method=='POST':
        if 'enregistrer_versement' in request.POST:

            facture_fournisseur = request.POST.get('reference')
            obj_facture = FactureFournisseur.objects.get(reference=facture_fournisseur)
            montant_verser = request.POST.get('montant_versement')
            date = request.POST.get('date_versement')

            if int(montant_verser) > obj_facture.reste_a_payer:
                montant_verser = obj_facture.reste_a_payer
            reste = obj_facture.reste_a_payer
            new_reste = float(reste) - float(montant_verser)
            if new_reste <= 0:
                obj_facture.reste_a_payer = 0
            else:
                obj_facture.reste_a_payer = new_reste
            if new_reste <= 0:
                obj_facture.status = 'SOLDE'
            else:
                obj_facture.status = 'IMPAYER'
            obj_facture.save()

            versement = Versement.objects.create(
                facture_fournisseur=obj_facture,
                montant_versement=montant_verser,
                date_versement=date,
            )
            return redirect('/voir_versement/' + str(pk) + '/')

    context = {
        'facture': facture,
    }
    return render(request, 'fournisseur/facture/ajouter_versement.html', context)


@login_required(login_url='login')
def enregistrer_facture_fournisseur(request, reference, id_four):

    fournisseurs = Fournisseur.objects.get(id=id_four)
    approv= Approvision.objects.filter(reference=reference)

    total = 0
    for i in approv:
        total += (i.quantite_approvision * i.prix_unitaire)

    print(total)

    if request.method == 'POST':
        if 'enregistrer':
            fournisseur = fournisseurs
            reference = reference
            montant_facture = total
            avance = request.POST.get('avance')
            reste_a_payer = int(montant_facture) - int(avance)
            if reste_a_payer == 0:
                status = "SOLDE"
            elif reste_a_payer > 0:
                status = "IMPAYER"
            else:
                status = " "
            date_facturation = request.POST.get('date_facturation')
            facture_fournisseur = FactureFournisseur.objects.filter(reference=reference, fournisseur=fournisseur)
            if not facture_fournisseur:
                FactureFournisseur.objects.create(
                    fournisseur=fournisseur,
                    reference=reference,
                    montant_facture=montant_facture,
                    avance=avance,
                    reste_a_payer = reste_a_payer,
                    status=status,
                    date_facturation=date_facturation,
                )
                messages.success(request,'Facture N° : ' + str(reference) + " à été enregistrer avec succès")
                return redirect('/approvision_produits/')
            else:
                messages.error(request,'La Facture existe déja')
    context = {
        'fournisseurs': fournisseurs,
        'total':total,
        'reference': reference

    }

    return render(request, 'fournisseur/facture/enregistrer_facture_fournisseur.html', context)


@login_required(login_url='login')
def liste_facture_fournisseur(request):
    if request.method == 'POST' and 'recherche' in request.POST:
        date_recherche = request.POST.get('date_recherche')

        factures = FactureFournisseur.objects.filter(date_facturation=date_recherche).order_by('-date_enregistrement')
        # pagination code
        pagination = Paginator(factures, 5)
        page = request.GET.get('page', 1)
        try:
            factures = pagination.page(page)
        except PageNotAnInteger:
            factures = pagination.page(1)
        except EmptyPage:
            factures = pagination.page(pagination.num_pages)
        if 'suppboutton' in request.POST:
            id_facture_fournisseur = request.POST.get('id_pour_supprimer')
            facture = FactureFournisseur.objects.get(id=id_facture_fournisseur)
            facture.delete()
    else:
        factures = FactureFournisseur.objects.order_by('-date_enregistrement')
        # pagination code
        pagination = Paginator(factures, 5)
        page = request.GET.get('page', 1)
        try:
            factures = pagination.page(page)
        except PageNotAnInteger:
            factures = pagination.page(1)
        except EmptyPage:
            factures = pagination.page(pagination.num_pages)
        if 'suppboutton' in request.POST:
            id_facture_fournisseur = request.POST.get('id_pour_supprimer')
            facture = FactureFournisseur.objects.get(id=id_facture_fournisseur)
            facture.delete()
            messages.success(request, 'Supprimer avec succès')
    context = {'factures': factures}
    return render(request, 'fournisseur/facture/liste_facture_fournisseur.html', context)


def voir_detail_facture_fournisseur(request, ref):
    facture_detail = Approvision.objects.filter(reference=ref)
    total_unitaire = 0
    for i in facture_detail:
        total_unitaire = int(i.quantite_approvision) * int(i.prix_unitaire)
    context = {
        'appro': facture_detail,
        'total': total_unitaire,
        'ref': ref
    }
    return render(request, 'fournisseur/facture/voir_detail_facture_fournisseur.html', context)


@login_required(login_url='login')
def approvision_produits(request):
    produits_list = TypeEmballage.objects.all()
    fournisseurs = Fournisseur.objects.all()

    if request.method =='POST':
        fournisseur = request.POST.get('fournisseur')
        fournisseur_obj = Fournisseur.objects.get(id=fournisseur)
        reference = request.POST.get('reference')
        date = request.POST.get('date_renseigner')
        save_by = request.user

        produit = request.POST.getlist('nom_produit')
        quantite = request.POST.getlist('quantite')
        prix_achat = request.POST.getlist('prix_achat')

        total = 0

        for j in range(len(produit)):
            # une ligne
            if quantite[j] == '' and prix_achat[j] == '':
                quant = 0
                prix_a = 0
            else:
                quant = int(quantite[j])
                prix_a = int(prix_achat[j])
            multiplication = quant * prix_a
            total += multiplication

        filtre_reference = Approvision.objects.filter(reference=reference)
        if not filtre_reference:
            for i in range(len(produits_list)):

                if quantite[i] == '' and prix_achat[i] == '':
                    quantites = 0
                    prix = 0
                else:
                    quantites = quantite[i]
                    prix = prix_achat[i]
                    produits = produit[i]

                    produit_obj = TypeEmballage.objects.get(id=produits)
                    stock_depart = produit_obj.quantite_stock
                    nouveau_stock = stock_depart + int(quantites)
                    produit_obj.quantite_stock = nouveau_stock
                    produit_obj.prix_achat = prix
                    produit_obj.save()

                    approvision = Approvision.objects.create(
                        type_emballage=produit_obj,
                        fournisseur=fournisseur_obj,
                        quantite_approvision=quantites,
                        reference=reference,
                        prix_unitaire=prix,
                        date_renseigner=date,
                        save_by=save_by,
                    )
            if approvision:
                messages.success(request, "Enregsitrer avec succès")
                return redirect('/enregistrer_facture_fournisseur/' +str(reference)+ '/'+str(fournisseur_obj.id)+'/' )

        else:
            messages.error(request, "La reference existe déjà")

    context = {
        'produits': produits_list,
        'fournisseurs': fournisseurs,
    }
    return render(request, 'produit/approvision_produits.html', context)


@login_required(login_url='login')
def ajouter_fournisseur(request):
    if request.method == 'POST':
        if 'ajouter_fournisseur' in request.POST:

            nom_prenom = request.POST.get('nom_prenom')
            adresse = request.POST.get('adresse')
            adresse_email = request.POST.get('adresse_email')
            contact = request.POST.get('contact')
            status = request.POST.get('status')

            # verifions si le produits existe déja
            fournisseur = Fournisseur.objects.filter(nom_prenom=nom_prenom)
            if not fournisseur:
                Fournisseur.objects.create(
                    nom_prenom=nom_prenom,
                    adresse=adresse,
                    adresse_email=adresse_email,
                    contact=contact,
                    status=status,
                )

                messages.success(request, 'Enregistrer avec succès')
            else:
                messages.error(request, 'Veuillez svp entrez les informations correctes')
        return redirect('/liste_fournisseur')

    return render(request, 'fournisseur/ajouter_fournisseur.html')


@login_required(login_url='login')
def liste_fournisseur(request):
    fournisseurs = Fournisseur.objects.order_by('-date_creation')

    # pagination code
    pagination = Paginator(fournisseurs, 5)
    page = request.GET.get('page', 1)
    try:
        fournisseurs = pagination.page(page)
    except PageNotAnInteger:
        fournisseurs = pagination.page(1)
    except EmptyPage:
        fournisseurs = pagination.page(pagination.num_pages)

    context = {'fournisseurs': fournisseurs}

    if request.method == 'POST':
        if 'suppboutton':
            id_fournisseur = request.POST.get('id_pour_supprimer')
            fournisseurs = Fournisseur.objects.get(id=id_fournisseur)
            fournisseurs.delete()
            messages.success(request, 'Supprimer avec succès')

    return render(request, 'fournisseur/liste_fournisseur.html', context)


@login_required(login_url='login')
def choisir_client(request):
    if request.method == 'POST':
        if 'ajout_client' in request.POST:
            client = request.POST.get('choix_client')
            facture_obj = Facture.objects.create(
             type_client=client,
            )
        return redirect('/espace_caisse/'+str(facture_obj.id)+'/')

    return render(request, 'vente/choisir_client.html')


# cette fonction creer aussi la vente et aussi fait les mouvvement dans le stock
@login_required(login_url='login')
def espace_caisse(request, pk):
    produits = TypeEmballage.objects.all()
    facture_obj = Facture.objects.get(id=pk)
    if 'creer_vente':
        if request.method == 'POST':
            facture = facture_obj
            produit = request.POST.get('produit_a_vendre')
            produit_obj = TypeEmballage.objects.get(id=produit)
            quantite_a_vendre = request.POST.get('quantite_a_vendre')
            save_by = request.user

            total_unitaire = int(produit_obj.prix_vente) * int(quantite_a_vendre)
            vente = Vente.objects.filter(type_emballage=produit_obj,facture=facture)
            if not vente:
                stock_depart = produit_obj.quantite_stock
                if stock_depart >= int(quantite_a_vendre):
                    nouveau_stock = stock_depart - int(quantite_a_vendre)
                    produit_obj.quantite_stock = nouveau_stock
                    produit_obj.save()
                    messages.success(request, 'Stock restant : ' + str(produit_obj.quantite_stock))

                    vente_creer = Vente.objects.create(
                        type_emballage=produit_obj,
                        facture=facture,
                        quantite_vente=quantite_a_vendre,
                        total_unitaire=total_unitaire,
                        save_by=save_by
                    )

                else:
                    messages.error(request, 'Stock insuffisant : '+ str(stock_depart))
            else:
                messages.error(request, 'Le produit existe déjà sur la facture.')

    vente_sur_factures = Vente.objects.filter(facture=facture_obj)

    compte_produits = vente_sur_factures.count()
    total_global = 0
    for i in vente_sur_factures:
        total_global = total_global + i.total_unitaire

    context = {
        'facture_obj':facture_obj,
        'produits': produits,
        'compte_produits': compte_produits,
        'vente_sur_factures': vente_sur_factures,
        'total_global': total_global
    }
    return render(request, 'vente/espace_caisse.html', context)


@login_required(login_url='login')
def payer_monnaie(request, pk):
    facture_obj = Facture.objects.get(id=pk)
    vente_sur_factures = Vente.objects.filter(facture=facture_obj)
    total_global = 0

    for i in vente_sur_factures:
        total_global = total_global + i.total_unitaire
    context = {
        'facture_obj': facture_obj,
        'total_global': total_global,
    }
    return render(request, 'vente/payer_et_monnaie.html', context)


@login_required(login_url='login')
def versement_fournisseur_impayer(request):
    factures = FactureFournisseur.objects.filter(status="IMPAYER")

    context = {
        'factures':factures,
    }
    return render(request, 'fournisseur/facture/versement_fournisseur_impayer.html', context)


@login_required(login_url='login')
def charges(request):
    liste_charges = Charges.objects.order_by('-date')
    if request.method == 'POST':
        if 'ajouter' in request.POST:
            nom1 = request.POST.get('nom_charges')
            verifie = Charges.objects.filter(nom=nom1)
            if not verifie:
                charge = Charges.objects.create(
                    nom=nom1,
                )
                if charge:
                    messages.success(request, 'ajouter avec succès !!!')
                else:
                    messages.error(request, 'Erreur !!!')
            else:
                messages.error(request, 'cette Charge existe déjà !!!')
    context = {
        'liste_charges': liste_charges
    }
    return render(request, 'charges_depenses/charges.html', context)


@login_required(login_url='login')
def depenses(request):
    charges = Charges.objects.all()
    if request.method =='POST':
        if 'ajouter_depense' in request.POST:
            nom_depense = request.POST['nom_depense']
            obj_charge = Charges.objects.get(id=nom_depense)
            montant_depense = request.POST['montant_depense']
            date_depense = request.POST['date_depense']
            save_by = request.user

            depense = Depenses.objects.create(
                charges=obj_charge,
                montant=montant_depense,
                date_enregistrer=date_depense,
                save_by=save_by,
            )
            if depense:
                messages.success(request, 'Dépense Ajouter avec succès !!!')
            else:
                messages.error(request, 'Erreur')

    liste_depense = Depenses.objects.all()
    total = 0
    for i in liste_depense:
        total += int(i.montant)

    context = {
        'charges': charges,
        'liste_depense': liste_depense,
        'total': total,
    }
    return render(request, 'charges_depenses/depenses.html', context)

@login_required(login_url='login')
def error404(request, exception):
    return render(request, 'page_erreur/404.html')


@login_required(login_url='login')
def voir_versement(request, pk):

    facture = FactureFournisseur.objects.get(id=pk)
    fact = facture.reference
    filtre_facture = Versement.objects.filter(facture_fournisseur=facture).order_by('-id')

    context = {
        'filtre_facture': filtre_facture,
        'facture': fact
    }
    return render(request, 'fournisseur/facture/voir_versement.html', context)


@login_required(login_url='login')
def comptabilite_accueil(request):
    now = datetime.today()
    date = "{}-{}-{}".format(now.year, now.month, now.day)
    produits = TypeEmballage.objects.all()
    liste_facture_impayer = FactureFournisseur.objects.filter(date_facturation=date, status="IMPAYER")
    liste_facture_client_creance = Facture.objects.filter(status='IMPAYER')
    depenses = Depenses.objects.all()
    total_creance = 0
    for non_payer in liste_facture_client_creance:
        total_creance += non_payer.reste_a_payer
    print(total_creance)
    total_valeur_stock = 0
    total_investi = 0
    total_dette = 0
    total_depense = 0
    benefice = 0
    for dep in depenses:
        total_depense += dep.montant

    for imp in liste_facture_impayer:
        total_dette += imp.reste_a_payer

    for prod in produits:
        total_valeur_stock += int(prod.prix_vente)
        total_investi += int(prod.prix_achat)
        benefice = total_valeur_stock - total_investi

    benefice_depense = benefice - total_depense


    context = {
        'total_valeur_stock': total_valeur_stock,
        'total_investi': total_investi,
        'total_dette': total_dette,
        'total_depense': total_depense,
        'benefice': benefice,
        'benefice_depense': benefice_depense,
        'total_creance': total_creance,

    }
    return render(request, 'comptabilite/comptabilite_accueil.html', context)


@login_required(login_url='login')
def creer_facture_client(request):
    clients = Client.objects.all()
    produit_list = TypeEmballage.objects.all()

    if request.method =='POST':
        client = request.POST.get('client')
        client_obj = Client.objects.get(id=client)
        ref = reference()
        save_by = request.user

        print(ref)
        produit = request.POST.getlist('nom_produit')
        quantite = request.POST.getlist('quantite')
        prix_vente = request.POST.getlist('prix_vente')

        total = 0

        for j in range(len(produit)):
            # une ligne
            if quantite[j] == '':
                quant = 0
                prix_v = 0
            else:
                quant = quantite[j]
                prix_v= prix_vente[j]
            multiplication = int(quant) * float(prix_v)
            total += multiplication
        print(total)
        vente = ''
        for i in range(len(produit_list)):

            if quantite[i] == '':
                quantites = 0
                prix = 0
            else:
                quantites = quantite[i]
                prix = prix_vente[i]
                produits = produit[i]
                produit_obj = TypeEmballage.objects.get(id=produits)
                stock_depart = produit_obj.quantite_stock
                if int(quantites) <= int(stock_depart):
                    total_unitaire = float(prix) * int(quantites)
                    nouveau_stock = stock_depart - int(quantites)
                    produit_obj.quantite_stock = nouveau_stock
                    produit_obj.save()

                    vente = Vente.objects.create(
                        type_emballage=produit_obj,
                        client=client_obj,
                        reference=ref,
                        quantite_vente=quantites,
                        total_unitaire=total_unitaire,
                        save_by=save_by,
                    )
                else:
                    messages.error(request, 'Stock insuffisant de ' + str(produit_obj))
        if vente:
            messages.success(request, "Enregsitrer avec succès")
            return redirect('/enregistrer_facture_client/' + str(ref) + '/' + str(client_obj.id)+'/')

    context = {
        'clients': clients,
        'produits': produit_list
    }

    return render(request, 'vente/creer_facture_client.html', context)


@login_required(login_url='login')
def enregistrer_facture_client(request, ref, id_clt):
    vente = Vente.objects.filter(reference=ref)
    client = Client.objects.get(id=id_clt)
    total = 0
    for ven in vente:
        total += ven.total_unitaire

    if request.method == 'POST':
        clients = client
        reference = ref
        montant_facture = request.POST.get('montant_facture')
        dates = request.POST.get('date')
        somme_recu = request.POST.get('somme_recu')
        print(somme_recu)
        print(montant_facture)
        reste = int(float(somme_recu)) - int(float(montant_facture))
        if reste >= 0:
            monnaie =reste
            status = "PAYER"
            reste_a_payer = 0
        else:
            status = "IMPAYER"
            monnaie = -1 * reste
            reste_a_payer = monnaie
        print(status, monnaie, reste_a_payer)
        save_by = request.user
        filtre_ref = Facture.objects.filter(reference_vente=ref)
        if not filtre_ref:
            Facture.objects.create(
                client=clients,
                reference_vente=reference,
                montant_facture=montant_facture,
                avance=somme_recu,
                monnaie=monnaie,
                reste_a_payer=reste_a_payer,
                date_facturation=dates,
                status=status,
                save_by=save_by,
            )
            messages.success(request, 'Facture N° ' + reference + ' a été enregistrer avec succès!!!')
            return redirect('/liste_facture/'+str(reference)+'/')
        else:
            messages.error(request, "erreur vueillez réessayer svp!!!")

    context = {
        'clients': client,
        'vente': vente,
        'total': total,
        'reference': ref,
    }
    return render(request, 'clients/enregistrer_facture_client.html',context)


@login_required(login_url='login')
def liste_clients(request):
    clients = Client.objects.order_by('-date')

    # pagination code
    pagination = Paginator(clients, 5)
    page = request.GET.get('page', 1)
    try:
        clients = pagination.page(page)
    except PageNotAnInteger:
        clients = pagination.page(1)
    except EmptyPage:
        clients = pagination.page(pagination.num_pages)

    context = {'clients': clients}

    if request.method == 'POST':
        if 'suppboutton':
            id_client = request.POST.get('id_pour_supprimer')
            clients = Client.objects.get(id=id_client)
            clients.delete()
            messages.success(request, 'Supprimer avec succès')

    return render(request, 'clients/liste_clients.html', context)


@login_required(login_url='login')
def ajouter_clients(request):
    if request.method == 'POST':
        if 'ajouter_clients' in request.POST:

            nom_prenom = request.POST.get('nom_prenom')
            adresse = request.POST.get('adresse')
            ville = request.POST.get('ville')
            contact = request.POST.get('contact')

            # verifions si le produits existe déja
            clients = Client.objects.filter(nom_prenom=nom_prenom)
            if not clients:
                Client.objects.create(
                    nom_prenom=nom_prenom,
                    adresse=adresse,
                    ville=ville,
                    contact=contact,
                )

                messages.success(request, 'Enregistrer avec succès')
            else:
                messages.error(request, 'Veuillez svp entrez les informations correctes')
        return redirect('/liste_clients')

    return render(request, 'clients/ajouter_clients.html')


@login_required(login_url='login')
def liste_facture(request, ref):
    vente = Vente.objects.filter(reference=ref)
    facture = Facture.objects.get(reference_vente=ref)
    status = facture.status
    total = 0

    for i in vente:
        total += i.total_unitaire


    context = {
        'status': status,
        'ventes': vente,
        'ref': ref,
        'total': total
    }
    return render(request, 'clients/liste_facture.html', context)


@login_required(login_url='login')
def imprimer_recu(request, ref):

    facture_obj = Facture.objects.filter(reference_vente=ref)
    vente_sur_factures = Vente.objects.filter(reference=ref)
    compte_produits = vente_sur_factures.count()
    total_global = 0
    montant_a_payer = request.POST.get('montant_a_payer')
    image = Image.objects.all()
    date = datetime.today()
    for vente in vente_sur_factures:
        total_unitaire = vente.total_unitaire
        total_global += total_unitaire
        client = vente.client
    for facture in facture_obj:
        reste_a_payer = facture.reste_a_payer
        monnaie = facture.monnaie
        somme_recu = facture.avance

    compte = vente_sur_factures.count()

    context = {
        'facture_obj': ref,
        'vente_sur_factures': vente_sur_factures,
        'total_global': total_global,
        'compte_produits': compte_produits,
        'reste_a_payer': reste_a_payer,
        'somme_recu': somme_recu,
        'montant_a_payer': montant_a_payer,
        'monnaie': monnaie,
        'date': date,
        'images': image,
        'compte': compte,
        'client': client
    }
    return render(request, 'vente/recu.html', context)


@login_required(login_url='login')
def liste_facture_client(request):
    date_recherche=''
    compte_facture = 0
    total = 0
    total_impayer = 0
    if 'recherche' in request.POST and request.method == 'POST':
        date_recherche = request.POST.get('date_recherche')
        toutes_facture_client = Facture.objects.filter(date_facturation=date_recherche)
        compte_facture = toutes_facture_client.count()
        for i in toutes_facture_client:
            total += i.montant_facture
            total_impayer += i.reste_a_payer

        # pagination code
        pagination = Paginator(toutes_facture_client, 5)
        page = request.GET.get('page', 1)
        try:
            toutes_facture_client = pagination.page(page)
        except PageNotAnInteger:
            toutes_facture_client = pagination.page(1)
        except EmptyPage:
            toutes_facture_client = pagination.page(pagination.num_pages)

    elif 'le_mois' in request.POST and request.method == 'POST':
        year = datetime.now().year
        month = datetime.now().month
        toutes_facture_client = Facture.objects.filter(Q(date_facturation__month=month))
        compte_facture = toutes_facture_client.count()
        for i in toutes_facture_client:
            total += i.montant_facture
            total_impayer += i.reste_a_payer
    else:
        toutes_facture_client = Facture.objects.all()
        compte_facture = toutes_facture_client.count()
        total = 0
        for i in toutes_facture_client:
            total += i.montant_facture
            total_impayer += i.reste_a_payer
        # pagination code
        pagination = Paginator(toutes_facture_client, 5)
        page = request.GET.get('page', 1)
        try:
            toutes_facture_client = pagination.page(page)
        except PageNotAnInteger:
            toutes_facture_client = pagination.page(1)
        except EmptyPage:
            toutes_facture_client = pagination.page(pagination.num_pages)

    context = {
        'toutes_facture_client': toutes_facture_client,
        'total': total,
        'compte_facture': compte_facture,
        'date_recherche': date_recherche,
        'total_impayer': total_impayer
    }
    return render(request, 'clients/liste_facture_client.html', context)


@login_required(login_url='login')
def liste_facture_client_impayer(request):
    facture_client_impayer = Facture.objects.filter(status='IMPAYER')

    context = {
        'facture_client_impayer' : facture_client_impayer,
    }
    return render(request, 'clients/liste_facture_client_impayer.html', context)


@login_required(login_url='login')
def ajouter_versement_client(request, pk):
    obj_facture = Facture.objects.get(id=pk)
    if request.method=='POST':
        if 'enregistrer_versement_client' in request.POST:

            facture_client = request.POST.get('reference')
            obj_facture = Facture.objects.get(reference_vente=facture_client)
            montant_verser = request.POST.get('montant_versement')
            date = request.POST.get('date_versement')

            if int(montant_verser) > obj_facture.reste_a_payer:
                montant_verser = obj_facture.reste_a_payer
            reste = obj_facture.reste_a_payer
            new_reste = float(reste) - float(montant_verser)
            if new_reste <= 0:
                obj_facture.reste_a_payer = 0
            else:
                obj_facture.reste_a_payer = new_reste
            if new_reste <= 0:
                obj_facture.status = 'SOLDE'
            else:
                obj_facture.status = 'IMPAYER'
            obj_facture.save()

            versement = VersementClient.objects.create(
                facture=obj_facture,
                montant_versement=montant_verser,
                date_versement=date,
            )
            return redirect('/voir_versement_client/' + str(pk) + '/')
    context = {
        'facture': obj_facture
    }
    return render(request, 'clients/ajouter_versement_client.html', context)


@login_required(login_url='login')
def voir_versement_client(request, pk):

    facture = Facture.objects.get(id=pk)
    fact = facture.reference_vente
    filtre_facture = VersementClient.objects.filter(facture=facture).order_by('-id')

    context = {
        'filtre_facture': filtre_facture,
        'facture': fact
    }
    return render(request, 'clients/voir_versement_client.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST' and 'change_password' in request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Modifier avec succès !!!')
            return redirect('login')
        else:
            messages.error(request, 'mot de passe trop court ou ne respecte pas les normes( un mot de passe doit contenir au moins 8 caractères composé de chiffres et de lettres). Merci!!!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'compte/change_password.html', {'form': form})
