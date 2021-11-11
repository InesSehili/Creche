# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.urls.conf import re_path  # add this
from factures.views import liste_factures_employe,ajouter_paiement_employe, supprimer_facture ,modifier_facture  ,valider_modifier_facture_employe ,paiement_employe
from employes.views import imprimer_facture_employer, ajouter_employee, supprimer_employe,modifier_employe,update_employee, liste_employe



from creches.views import ajouter_info_creche, changer_mot_de_passe
from supplement.views import supplement_page, formulaire_modifier_supplement, update_supplement, delete_supplement
from categoriesAbonnement.views import categorie_abonnement_page, formulaire_modifier_categorie_abonnement, update_categori_abonnement, delete_categorie_abonnement
from depenses.views import depense_page, formulaire_modifier_depense, update_depense, delete_depense
from classes.views import liste_classes , modifier_classe,update_classe ,supprimer_classes
from autorisations.views import autorisation_page, formulaire_modifier_autorisation, update_autorisation, delete_autorisation 
from enfants.views import liste_enfants , ajouter_enfant ,afficher_detail_enfant, valider_ajouter_enfant ,supprimer_enfant,modifier_enfant,valider_modifier_enfant


from stock.views import ajouter_article ,supprimer_stock  ,valider_modifier_stock ,modifier_stock
from besoin.views import liste_besoin ,ajouter_besoin ,supprimer_besoin ,valider_modifier_besoin ,modifier_besoin
from achats.views import  ajouter_achats   
from pointages.views import list_enfant_present ,list_enfant_absent ,pointage_enfant, supprimer_pointage_enfant, ajouter_pointage_enfant, ajouter_pointage_enfant, ajouter_pointage_employe,supprimer_pointage,pointage_employe,  list_employe_present,list_employe_absent
from depenses.views import dashboard

from prixsortie.views import liste_stock,liste_depenses ,ajouter_facture_depense,valider_ajouter_depense ,ajouter_liste_achats ,ajouter_achats_article ,supprimer_achats,modifier_achats ,valider_modifier_achats,ajouter_achats_besoin ,liste_achats ,valider_modifier_depense,modifier_depense_prix
from sectionsage.views import update_section_age, section_age_page, formulaire_modifier_section_age, delete_section_age

from factureenfants.views import print_pdf, imprimer_facture, liste_factures_touts_les_enfant, update_facture_enfant, formulaire_modifier_facture_enfant, add_new_facture_enfant, liste_factures_enfant, formulaire_ajouter_facture, delete_facture


from payement.views import formulaire_creation_payement , ajouter_payement ,supprimer_payement,modifier_payement ,valider_modifier_payement

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path('customers/', include("customers.urls")),  # Django customers route
    path("", include("app.urls")),  # UI Kits Html files
    path("", include("authentication.urls")),  # Auth routes - login / register
    path('changer_mot_de_passe', changer_mot_de_passe, name="changer_mot_de_passe"),
    path('print_pdf', print_pdf, name="print_pdf"),
    path('imprimer_facture_employer', imprimer_facture_employer, name="imprimer_facture_employer"),
    path('ajouter_employee', ajouter_employee, name="ajouter_employee"),
    path('update_section_age', update_section_age, name="update_section_age"),
    path('delete_section_age', delete_section_age, name="delete_section_age"),
    path('section_age_page', section_age_page, name="section_age_page"),
    path('formulaire_modifier_section_age', formulaire_modifier_section_age, name="formulaire_modifier_section_age"),    
    path('ajouter_paiement_employe', ajouter_paiement_employe, name="ajouter_paiement_employe"),
    path('liste_employe', liste_employe, name='liste_employe'),    
    path('supprimer_employe', supprimer_employe, name='supprimer_employe'),
    path('supprimer_facture', supprimer_facture, name='supprimer_facture'),
    path('modifier_employe',modifier_employe , name='modifier_employe'),
    path('modifier_classe',modifier_classe , name='modifier_classe'),
    path('update_employee',update_employee , name='update_employee'),
    path("Information_creche",ajouter_info_creche, name='information_creche'),
    path("supplement_page", supplement_page, name = 'supplement_page'),
    path("formulaire_modifier_supplement",formulaire_modifier_supplement, name = 'modifier_supplement'),
    path("update_supplement", delete_supplement, name = 'delete_supplement'),
    path("delete_supplement", update_supplement, name = 'update_supplement'),
    path("categorie_abonnement_page", categorie_abonnement_page, name = 'categorie_abonnement_page'),
    path("formulaire_modifier_categorie_abonnement", formulaire_modifier_categorie_abonnement, name = 'formulaire_modifier_categorie_abonnement'),
    path("update_categori_abonnement", update_categori_abonnement, name = 'update_categori_abonnement'),
    path("delete_categorie_abonnement", delete_categorie_abonnement, name = 'delete_categorie_abonnement'),
    path("depense_page", depense_page, name = 'depense_page'),
    path("formulaire_modifier_depense", formulaire_modifier_depense, name = 'formulaire_modifier_depense'),
    path("update_depense",update_depense, name = 'update_depense'),
    path("update_classe",update_classe, name = 'update_classe'),
    path("delete_depense", delete_depense, name = 'delete_depense'),
    path("liste_classes", liste_classes, name = 'liste_classes'),
    path("ajouter_pointage_employe",ajouter_pointage_employe,name='ajouter_pointage_employe'),
    path("autorisation_page",autorisation_page, name = 'autorisation_page'),
    path("formulaire_modifier_autorisation", formulaire_modifier_autorisation, name = 'formulaire_modifier_autorisation'),
    path("update_autorisation",update_autorisation, name = 'update_autorisation'),
    path("delete_autorisation",delete_autorisation, name = 'delete_autorisation'),
    path("liste_enfants",liste_enfants, name = 'liste_enfants'),
    path("ajouter_enfant",ajouter_enfant, name = 'ajouter_enfant'),
    path("afficher_detail_enfant",afficher_detail_enfant, name = 'afficher_detail_enfant'),
    path("valider_ajouter_enfant",valider_ajouter_enfant, name = 'valider_ajouter_enfant'),
    path("supprimer_enfant" , supprimer_enfant ,name="supprimer_enfant"),
    path("modifier_enfant" , modifier_enfant , name = "modifier_enfant"),
    path("valider_modifier_enfant" , valider_modifier_enfant , name = "valider_modifier_enfant"),
    path("supprimer_pointage", supprimer_pointage, name="supprimer_pointage"),
    path('list_employe_present', list_employe_present, name="list_employe_present"),
    path('list_employe_absent', list_employe_absent, name="list_employe_absent"),
    path('liste_factures_employe', liste_factures_employe, name="liste_factures_employe"),

    path('liste_factures_enfant', liste_factures_enfant, name="liste_factures_enfant"),
    path('formulaire_ajouter_facture', formulaire_ajouter_facture, name="formulaire_ajouter_facture"),
    path('add_new_facture_enfant', add_new_facture_enfant, name="add_new_facture_enfant"),
    path('delete_facture', delete_facture, name="delete_facture"),
    path('formulaire_modifier_facture_enfant', formulaire_modifier_facture_enfant, name="formulaire_modifier_facture_enfant"),
    path('update_facture_enfant', update_facture_enfant, name="update_facture_enfant"),
    path('liste_factures_touts_les_enfant', liste_factures_touts_les_enfant, name="liste_factures_touts_les_enfant"),
    path('imprimer_facture', imprimer_facture, name="imprimer_facture"),



    path('supprimer_classes', supprimer_classes, name="supprimer_classes"),
    path('ajouter_article', ajouter_article, name="ajouter_article"),
    path('liste_stock', liste_stock, name="liste_stock"),
    path('liste_besoin', liste_besoin, name="liste_besoin"),
    path('ajouter_besoin', ajouter_besoin, name="ajouter_besoin"),
    path('supprimer_besoin', supprimer_besoin, name="supprimer_besoin"),
    path('supprimer_stock', supprimer_stock, name="supprimer_stock"),
    path('liste_achats', liste_achats, name="liste_achats"),
    path('ajouter_achats', ajouter_achats, name="ajouter_achats"),
    path('ajouter_achats_besoin', ajouter_achats_besoin, name="ajouter_achats_besoin"),
    path('ajouter_liste_achats', ajouter_liste_achats, name="ajouter_liste_achats"),
    path('ajouter_achats_article', ajouter_achats_article, name="ajouter_achats_article"),
    path('valider_modifier_stock', valider_modifier_stock, name="valider_modifier_stock"),
    path('modifier_stock', modifier_stock, name="modifier_stock"),
    path('supprimer_achats', supprimer_achats, name="supprimer_achats"),
    path('modifier_besoin', modifier_besoin, name="modifier_besoin"),
    path('valider_modifier_besoin', valider_modifier_besoin, name="valider_modifier_besoin"),
    path('pointage_employe', pointage_employe, name="pointage_employe"),
    path('modifier_facture', modifier_facture, name="modifier_facture"),
    path('liste_depenses', liste_depenses, name="liste_depenses"),
    path("supprimer_pointage_enfant", supprimer_pointage_enfant, name="supprimer_pointage_enfant"),
    path('list_enfant_present', list_enfant_present, name="list_enfant_present"),
    path('list_enfant_absent', list_enfant_absent, name="list_enfant_absent"),
    path('pointage_enfant', pointage_enfant, name="pointage_enfant"),
    path("ajouter_pointage_enfant",ajouter_pointage_enfant,name='ajouter_pointage_enfant'),
    path("dashboard",dashboard,name='dashboard'),
    path("valider_modifier_facture_employe",valider_modifier_facture_employe,name='valider_modifier_facture_employe'),
    path("modifier_achats",modifier_achats,name='modifier_achats'),
    path("valider_modifier_achats",valider_modifier_achats,name='valider_modifier_achats'),
    path("valider_ajouter_depense",valider_ajouter_depense,name='valider_ajouter_depense'),
    path("ajouter_facture_depense",ajouter_facture_depense,name='ajouter_facture_depense'),
    path("valider_modifier_depense",valider_modifier_depense,name='valider_modifier_depense'),
    path("modifier_depense_prix",modifier_depense_prix,name='modifier_depense_prix'),
    path("paiement_employe",paiement_employe,name='paiement_employe'),
    path("formulaire_creation_payement",formulaire_creation_payement,name='formulaire_creation_payement'),
    path("ajouter_payement",ajouter_payement,name='ajouter_payement'),
    path("supprimer_payement",supprimer_payement,name='supprimer_payement'),
    path("modifier_payement",modifier_payement,name='modifier_payement'),
    path("valider_modifier_payement",valider_modifier_payement,name='valider_modifier_payement'),
    


    






    




    










   

]

if settings.DEVEL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
