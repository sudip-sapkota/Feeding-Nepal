from django.db import connection

def volunteer_context(request):
    volunteer_data = {}
    email = request.session.get('volunteer_email')

    if email:
        with connection.cursor() as cursor:
            cursor.execute("SELECT full_name, email FROM volunteer WHERE email = %s", [email])
            user = cursor.fetchone()
            if user:
                full_name = user[0]
                volunteer_data = {
                    'name': full_name,
                    'email': user[1],
                    'initial': full_name[0].upper() if full_name else '?'
                }

    return {'user': volunteer_data}
