
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', accueil, name='accueil'),
    path('liste_produits/', liste_produits, name='liste_produits'),
    path('ajouter_produits/', ajouter_produits, name='ajouter_produits'),
    path('ajouter_fournisseur/', ajouter_fournisseur, name='ajouter_fournisseur'),
    path('liste_fournisseur/', liste_fournisseur, name='liste_fournisseur'),
    path('liste_approvision/', liste_approvision, name='liste_approvision'),
    path('approvision_produits/', approvision_produits, name='approvision_produits'),
    path('espace_caisse/<str:pk>/', espace_caisse, name='espace_caisse'),
    path('imprimer_recu/<str:ref>', imprimer_recu, name='imprimer_recu'),
    path('enregistrer_facture_fournisseur/<str:reference>/<int:id_four>/', enregistrer_facture_fournisseur, name='enregistrer_facture_fournisseur'),
    path('enregistrer_facture_client/<str:ref>/<int:id_clt>/', enregistrer_facture_client, name='enregistrer_facture_client'),
    path('facture/liste_facture_fournisseur/', liste_facture_fournisseur, name='liste_facture_fournisseur'),
    path('liste_vente/', liste_vente, name='liste_vente'),
    path('point_facture_vente/', point_facture_vente, name='point_facture_vente'),
    path('payer_monnaie/<str:pk>/', payer_monnaie, name='payer_monnaie'),
    path('versement_fournisseur_impayer/', versement_fournisseur_impayer, name='versement_fournisseur'),
    path('voir_versement/<str:pk>/', voir_versement, name='voir_versement'),
    path('ajouter_versement/<str:pk>/', ajouter_versement, name='ajouter_versement'),
    path('charges_enregistrement/', charges, name='charges'),
    path('depenses_enregistrement/', depenses, name='depenses'),
    path('comptabilite_accueil/', comptabilite_accueil, name='comptabilite_accueil'),
    path('creer_facture_client/', creer_facture_client, name='creer_facture_client'),
    path('ajouter_clients/', ajouter_clients, name='ajouter_clients'),
    path('liste_clients/', liste_clients, name='liste_clients'),
    path('liste_facture/<str:ref>/', liste_facture, name='liste_facture'),
    path('liste_facture_client/', liste_facture_client, name='liste_facture_client'),
    path('liste_facture_client_impayer/', liste_facture_client_impayer, name='liste_facture_client_impayer'),
    path('ajouter_versement_client/<int:pk>/', ajouter_versement_client, name='ajouter_versement_client'),
    path('voir_versement_client/<int:pk>/', voir_versement_client, name='voir_versement_client'),
    path('voir_detail_facture_fournisseur/<str:ref>/', voir_detail_facture_fournisseur, name='voir_detail_facture_fournisseur'),
    path('compte/change_password/', change_password, name='change_password'),


]
