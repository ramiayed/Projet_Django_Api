from django.shortcuts import render
from django.contrib.auth.models import Group
from vehicules.models import Vehicule
from rendez_vous.models import RendezVous
from django.db.models import Sum, Count

def stats_view(request):
    # Nombre total de clients
    clients_group = Group.objects.get(name="Client")
    total_clients = clients_group.user_set.count()

    # Nombre total de mécaniciens
    mechanics_group = Group.objects.get(name="Mechanic")
    total_mechanics = mechanics_group.user_set.count()

    # Nombre total de véhicules
    total_vehicles = Vehicule.objects.count()

    # Rendez-vous par statut
    rendezvous_by_status = RendezVous.objects.values('status').annotate(count=Count('id'))

    # Total des paiements (basé sur le champ `cout`)
    total_paiements = RendezVous.objects.aggregate(Sum('cout'))['cout__sum'] or 0

    context = {
        'total_clients': total_clients,
        'total_mechanics': total_mechanics,
        'total_vehicles': total_vehicles,
        'rendezvous_by_status': {item['status']: item['count'] for item in rendezvous_by_status},
        'total_paiements': total_paiements,
    }

    return render(request, 'stats/stats.html', context)
