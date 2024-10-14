from django.contrib.sites import requests
from django.http import JsonResponse, HttpResponse


CANVAS_API_BASE_URL = "https://canvas.instructure.com/api/v1/"
CANVAS_API_TOKEN = '7~uCf4nvC7EWhy6waEwLCRQuYYwVXEuyHAG2f4PHDGaNRfQPGueGHuAwhzN2RTCQ3n'

def index(request):
    if request.method == "POST":

        course_id = request.POST.get('course_id', 'No course ID found')
        user_id = request.POST.get('user_id', 'No user ID found')

        if course_id == 'No course ID found' or user_id == 'No user ID found':
            return HttpResponse("Missing course_id or user_id", status=400)


        users = get_canvas_course_users(course_id)


        users_assignments = {}
        for user in users:
            user_id = user['id']
            assignments = get_user_assignments(course_id, user_id)
            users_assignments[user['name']] = assignments


        return JsonResponse({
            'course_id': course_id,
            'users': users_assignments
        })

    else:

        return HttpResponse("This endpoint only accepts POST requests.", status=405)


def get_canvas_course_users(course_id):

    url = f"{CANVAS_API_BASE_URL}courses/{course_id}/users"
    headers = {
        'Authorization': f'Bearer {CANVAS_API_TOKEN}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def get_user_assignments(course_id, user_id):

    url = f"{CANVAS_API_BASE_URL}courses/{course_id}/students/submissions"
    headers = {
        'Authorization': f'Bearer {CANVAS_API_TOKEN}'
    }
    params = {
        'student_ids[]': user_id
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []

