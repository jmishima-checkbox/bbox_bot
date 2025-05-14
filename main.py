import requests

# Endpoint para obtener clases
url = "https://www.briskbox.fit/api/clases"

# Cabeceras necesarias para autenticación
headers = {
    'Access-Token': '$2y$10$.ugT3Ie/X2H8J4RkAKTuFeNtf03aaJIqwJdUi49cQSqocPCR2kgvy',
    'User-Id': '82cfc5c9-2fd7-4fd4-96c7-51efa534955d'
}

# Handler para imprimir el resultado del POST
def on_post_complete(response, date):
    if response.ok:
        print(f"✅ Subscription succeeded for class on {date}")
    else:
        print(f"❌ Subscription failed for class on {date} — {response.status_code}: {response.text}")

# GET: obtener clases disponibles
response = requests.get(url, headers=headers)
lessons = response.json()

# Filtrar clases específicas
boxLessons = next(x for x in lessons['avalible_clases'] if x["name"] == "Nueva Cordoba")['clases_types']
activityLessons = next(x for x in boxLessons if x["name"] == "BriskBox X")

# Filtrar clases a las 18:00
lessonsIds = []
for lessons in activityLessons['dates']:
    for lesson in lessons['clases']:
        if lesson['name'].startswith('18:00'):
            lesson['date'] = lessons['date']
            lessonsIds.append(lesson)

# Endpoint para inscribirse
urlPost = 'https://www.briskbox.fit/api/inscribe'

# POST: inscribirse a las clases filtradas
for claseAInscribir in lessonsIds:
    classPayload = {
        "user_id": "82cfc5c9-2fd7-4fd4-96c7-51efa534955d",
        "trainee_id": "cf5b7bd7-f0dc-4e3e-aa87-b06e4cb3bfc9",
        "box_id": "37c327ea-5fb4-4d49-bfbd-59dcbfa7c42b",
        "clase_type_id": "e71622f4-c6b8-4113-a239-0da3fb1f62d7",
        "date": claseAInscribir['date'],
        "clase_id": claseAInscribir['id']
    }

    response = requests.post(urlPost, headers=headers, json=classPayload)
    on_post_complete(response, claseAInscribir['date'])
