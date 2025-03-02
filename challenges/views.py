from django.shortcuts import render

# Create your views here.
import csv
import io
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            return HttpResponseBadRequest("No csv_file provided in the request.")

        csv_file = request.FILES['csv_file']

        try:
            decoded_file = csv_file.read().decode('utf-8')
        except Exception as e:
            return HttpResponseBadRequest(f"Error decoding file: {e}")

        csv_data = io.StringIO(decoded_file)
        reader = csv.DictReader(csv_data) 

        challenges = []
        for row in reader:
            try:
                row['ChallengeID'] = int(row.get('ChallengeID', 0))
                row['ChallengeSucessRate'] = int(row.get('ChallengeSucessRate', 0))
            except ValueError:
                pass
            challenges.append(row)

        return JsonResponse(challenges, safe=False)
    else:
        return JsonResponse({"error": "POST request required."}, status=405)
