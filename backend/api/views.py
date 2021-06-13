from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from backend.models import Awards
from backend.api.serializers import AwardsSerializer

from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


#THESE ARE FUNCTION BASED VIEWS
@csrf_exempt
def awards_api(request):
    if request.method == 'GET':
        awards = Awards.objects.all()
        serializers = AwardsSerializer(awards,many=True)
        return JsonResponse(serializers.data,safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializers = AwardsSerializer(data=data)
        if(serializers.is_valid()):
            serializers.save()
            return JsonResponse(serializers.data,status=201)
        else:
            return JsonResponse(serializers.errors,status=400)

#IF YOU WANT GET,POST LOOK AT THIS
@api_view(['GET','POST'])
def awards_apidec(request):
    if request.method == 'GET':
        awards = Awards.objects.all()
        serializers = AwardsSerializer(awards,many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        serializers = AwardsSerializer(data=request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializers.errors,status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def awards_details(request,pk):
    try:
        awards = Awards.objects.get(pk=pk)
    except Awards.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializers = AwardsSerializer(awards)
        return JsonResponse(serializers.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializers = AwardsSerializer(awards,data=data)
        if(serializers.is_valid()):
            serializers.save()
            return JsonResponse(serializers.data)
        else:
            return JsonResponse(serializers.errors)

    elif request.method == 'DELETE':
        awards.delete()
        return HttpResponse(status=204)


#IF YOU WANT GET,PUT DELETE LOOK AT THIS
@api_view(['GET','PUT','DELETE','POST'])
def awards_detailsdec(request,pk):
    try:
        awards = Awards.objects.get(pk=pk)
    except Awards.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializers = AwardsSerializer(awards)
        return Response(serializers.data)

    elif request.method == 'PUT':
        serializers = AwardsSerializer(awards,data=request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        awards.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#THESE ARE CLASS BASED VIEWS
#Class based views avoid repition
def start_command(update,context):
    update.message.reply_text('Type something you want to get started!')

def help_command(update,context):
    update.message.reply_text('If you need further help try visiting our Website!')

def handle_message(update,context):
    awardobj = Awards.objects.filter(id="4",facultyid="715518104060")
    for i in awardobj:
        fname=i.facultyname
        fid=i.facultyid
        fdept=i.department
        faward=i.awardname
        fdes=i.awarddescription
    text = str(update.message.text).lower()
    response = sample_responses(text)
    response1 = "Faculty Name :"+fname+"\n"+"Faculty id"+fid+"\n"+"Faculty Department : "+fdept+"\n"+"Award Name"+faward+"\n"
    update.message.reply_text(response1)

def error(update,context):
    print(f"Update {update} casued error {context.error}")

def main():
    updater = Updater(keys,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(MessageHandler(Filters.text,handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
