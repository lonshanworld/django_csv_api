from django.shortcuts import render

# Create your views here.
import csv
import io
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        # Check if the CSV file was provided in the POST data
        if 'csv_file' not in request.FILES:
            return HttpResponseBadRequest("No csv_file provided in the request.")

        csv_file = request.FILES['csv_file']

        try:
            # Read and decode the file (assuming UTF-8 encoding)
            decoded_file = csv_file.read().decode('utf-8')
        except Exception as e:
            return HttpResponseBadRequest(f"Error decoding file: {e}")

        # Use StringIO to treat the decoded string as a file
        csv_data = io.StringIO(decoded_file)
        reader = csv.DictReader(csv_data)  # Defaults to comma as delimiter

        challenges = []
        for row in reader:
            try:
                # Convert string numbers to integers, if applicable
                row['ChallengeID'] = int(row.get('ChallengeID', 0))
                row['ChallengeSucessRate'] = int(row.get('ChallengeSucessRate', 0))
            except ValueError:
                # Optionally, handle conversion errors here
                pass
            challenges.append(row)

        # Return the parsed data as JSON
        return JsonResponse(challenges, safe=False)
    else:
        # Only POST requests are allowed
        return JsonResponse({"error": "POST request required."}, status=405)
