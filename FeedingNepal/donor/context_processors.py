# donor/context_processors.py
from .models import Donor

def donor_context(request):
    donor = None
    donor_id = request.session.get('donor_id')
    if donor_id:
        try:
            donor = Donor.objects.get(id=donor_id)
        except Donor.DoesNotExist:
            donor = None
    return {'donor': donor}
