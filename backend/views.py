from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf.urls import include, url
from django.urls import reverse
from django.contrib.auth.models import User, auth
from django.http import HttpResponse,HttpResponseRedirect
from .models import Awards,Personal,Evcon,Eveat
from backend import views
import os
import multiprocessing
#for audio
from .models import File
from .forms import MyfileUploadForm

def Audio1(request):
    context = {
        'form':MyfileUploadForm(),
    }
    if request.method == 'POST':
        form = MyfileUploadForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            files=form.cleaned_data['files_data']
            a=files.name
            File(my_file=files,file_name=a).save()
            return redirect('finalaudio')
        else:
            print(form.errors)
            return redirect('home')
    else:
        return render(request,'backend/audio.html',context)

"""def Audio_update(request):
    instance = get_object_or_404(Post,id=id)
    form = AudioForm(request.POST or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('home')
    context = {
    "form":form,
    }
    return redirect('audio')"""

def audio_list(request):
    userid=12
    aud = File.objects.all()
    if request.method == 'POST':
        for i in aud:
            if(str(i.id) in request.POST):
                request.session['aud']=[str(i.id),i.file_name]
                break
        return redirect("textpage")
    else:
        return render(request,'backend/stlist.html',{'aud':aud})

def textpage(request):
    if(request.method=='POST'):
        return redirect('audio')
    else:
        r=sr.Recognizer()
        url = 'media/'+request.session['aud'][1]
        with sr.AudioFile(url) as source:
            audio = r.listen(source)
            try:
                text=r.recognize_google(audio)
                print("Working on it")
                print(text)
            except:
                print('Sorry....run again')
        return render(request,'backend/final.html',{'data':text})

#Speech to Text
import speech_recognition as sr
def speechto_text(name):
    r=sr.Recognizer()
    url = 'media/'+name
    with sr.AudioFile(url) as source:
        audio = r.listen(source)
        try:
            text=r.recognize_google(audio)
            print("Working on it")
            print(text)
        except:
            print('Sorry....run again')


#for pdf
from io import BytesIO
from django.template.loader import get_template
from django.views.generic import View
from xhtml2pdf import pisa

#stuff required for html email
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#stuff required for html whatsapp
import os
from twilio.rest import Client
def whatsapp(request):
    if request.method == "POST":
        message= request.POST['message']
        to = request.POST['to']
        account_sid="#"
        token = "#"
        client = Client(account_sid,token)
        from_whatsapp_number ='#'
        to_whatsapp_number = '#
        print(to_whatsapp_number)
        client.messages.create(body=message,
                               from_=from_whatsapp_number,
                                to=to_whatsapp_number)
        return render(request,"backend/whatsapp.html",{'flag':True})
    else:
        return render(request,'backend/whatsapp.html')

def email(request):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        from_mail = '#'
        to_mail = request.POST['to_mail']
        send_mail(
            subject,
            message,
            from_mail,
            [to_mail],
            fail_silently=False
            )
        return render(request,'backend/email.html',{'flag1':True})
    else:
        return render(request,'backend/email.html')

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

def generate_pdf(request,*args,**kwargs):
    flag1=0
    flag2=0
    flag3=0
    flag4=0
    template = get_template('backend/submit.html')
    uc = request.user
    if('1' in request.session['checkboxr']):
        if Personal.objects.filter(facultyid="123").exists():
            flag1=1
            persobj = Personal.objects.filter(facultyid="#")
    if(len(request.session['checkboxevcon'])!=0):
        if Evcon.objects.filter(facultyid=uc).exists():
            flag2=1
            evconobj1=[]
            for i in request.session['checkboxevcon']:
                evconobj1+=[Evcon.objects.filter(id=i)]
    if(len(request.session['checkboxeveat'])!=0):
        if Eveat.objects.filter(facultyid=uc).exists():
            flag4=1
            evatobj1=[]
            for i in request.session['checkboxeveat']:
                evatobj1+=[Eveat.objects.filter(id=i)]
    if(len(request.session['checkboxaward'])!=0):
        if Awards.objects.filter(facultyid=uc).exists():
            flag3=1
            awardobj1=[]
            for i in request.session['checkboxaward']:
                awardobj1+=[Awards.objects.filter(id=i)]
    if(flag1==1):
        if(flag2==1):
            if(flag3==1):
                if(flag4==1):
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        "flag4":flag4,
                        'evconobj':evconobj1,
                        'awardobj':awardobj1,
                        'persobj':persobj,
                        'evatobj':evatobj1
                        }
                else:
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        'evconobj':evconobj1,
                        'awardobj':awardobj1,
                        'persobj':persobj
                        }
            else:
                if(flag4==1):
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        "flag4":flag4,
                        'evconobj':evconobj1,
                        'persobj':persobj,
                        'evatobj':evatobj1
                        }
                else:
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        'evconobj':evconobj1,
                        'persobj':persobj
                        }
        else:
            if(flag3==1):
                if(flag4==1):
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        "flag4":flag4,
                        'evatobj':evatobj1,
                        'awardobj':awardobj1,
                        'persobj':persobj
                        }
                else:
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        'awardobj':awardobj1,
                        'persobj':persobj
                        }
            else:
                if(flag4==1):
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        "flag4":flag4,
                        'evatobj':evatobj1,
                        'persobj':persobj
                        }
                else:
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        'persobj':persobj
                        }
    else:
        if(flag2==1):
            if(flag3==1):
                if(flag4==1):
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        "flag4":flag4,
                        'evatobj':evatobj1,
                        'evconobj':evconobj1,
                        'awardobj':awardobj1
                        }
                else:
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        'evconobj':evconobj1,
                        'awardobj':awardobj1
                        }
            else:
                if(flag4==1):
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        "flag4":flag4,
                        'evatobj':evatobj1,
                        'evconobj':evconobj1
                        }
                else:
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        'evconobj':evconobj1,
                        }
        else:
            if(flag3==1):
                if(flag4==1):
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        "flag4":flag4,
                        'evatobj':evatobj1,
                        'awardobj':awardobj1
                        }
                else:
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        'awardobj':awardobj1
                        }
            else:
                if(flag4==1):
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        'evatobj':evatobj1
                        }
                else:
                    context={
                        "flag1":flag1,
                        "flag2":flag2,
                        "flag3":flag3,
                        "flag4":flag4
                        }
    print(flag1,flag2,flag3,context)
    html = template.render(context)
    pdf = render_to_pdf('backend/submit1.html',context)
    if(request.session["genj"]==1):
        if pdf:
            return HttpResponse(pdf,content_type='application/pdf')
        else:
            return HttpResponse("Not Found")
    elif(request.session["gend"]==1):
        response = HttpResponse(pdf,content_type='application/pdf')
        filename = "Report_%s.pdf" %("1")
        content = "inline; filename='%s'" %(filename)
        download = True
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response

def first(request):
    request.session['a']=0
    return redirect('home')

def home(request):
    request.session['flagawards']=0
    request.session['flagevat']=0
    request.session['flagevcon']=0
    request.session['rep']=[]
    request.session['evecon']=[]
    request.session['eveat']=[]
    request.session['award']=[]
    request.session['c']=0
    request.session['d']=0
    request.session['e']=0
    request.session['z']=0
    request.session['evcon']=0
    if(request.session["a"]==0):
        return render(request,'backend/home.html')
    else:
        return redirect("personal")

def personal(request):
    request.session["b"]=1
    facultyid = request.user
    if Personal.objects.filter(facultyid=facultyid).exists():
        personalobj=Personal.objects.filter(facultyid=facultyid)
        for i in personalobj:
            facultyname=i.facultyname
            facultyid=i.facultyid
            annaid=i.annaid
            aicteid=i.aicteid
            emailid=i.emailid
            mobileno=i.mobileno
            dob=i.dob
            address=i.address
            bgroup=i.bgroup
            department=i.department
            aoi=i.aoi
            ugabout=i.ugabout
            ugyear=i.ugyear
            pgabout=i.pgabout
            pgyear=i.pgyear
            phdabout=i.phdabout
            phdyear=i.phdyear
            ac_name=i.ac_name
            ac_from=i.ac_from
            ac_to=i.ac_to
            re_name=i.re_name
            re_from=i.re_from
            re_to=i.re_to
            in_name=i.in_name
            in_from=i.in_from
            in_to=i.in_to
    if request.method == 'POST':
        if Personal.objects.filter(facultyid=facultyid).exists():
            checkbox = request.POST.getlist('checkbox')
            if request.POST['facultyname']!="":
                facultyname = request.POST['facultyname']
            if request.POST['facultyid']!="":
                facultyid = request.POST['facultyid']
            if request.POST['annaid']!="":
                annaid = request.POST['annaid']
            if request.POST['aicteid']!="":
                aicteid = request.POST['aicteid']
            if request.POST['emailid']!="":
                emailid = request.POST['emailid']
            if request.POST['mobileno']!="":
                mobileno = request.POST['mobileno']
            if request.POST['dob']!="":
                dob = request.POST['dob']
            if request.POST['address']!="":
                address = request.POST['address']
            if request.POST['bg']!="":
                bgroup = request.POST['bg']
            if request.POST['dept']!="":
                department = request.POST['dept']
            if request.POST['aoi']!="":
                aoi = request.POST['aoi']
            if('1' in checkbox):
                if request.POST['ugabout']!="":
                    ugabout = request.POST['ugabout']
                if request.POST['ugyear']!="":
                    ugyear = request.POST['ugyear']
            if('2' in checkbox):
                if request.POST['pgabout']!="":
                    pgabout =  request.POST['pgabout']
                if request.POST['pgyear']!="":
                    pgyear = request.POST['pgyear']
            if('3' in checkbox):
                if request.POST['phdabout']!="":
                    phdabout =  request.POST['phdabout']
                if request.POST['phdyear']!="":
                    phdyear = request.POST['phdyear']
        else:
            facultyname = request.POST['facultyname']
            facultyid = request.POST['facultyid']
            annaid = request.POST['annaid']
            aicteid = request.POST['aicteid']
            emailid = request.POST['emailid']
            mobileno = request.POST['mobileno']
            dob = request.POST['dob']
            address = request.POST['address']
            bgroup = request.POST['bg']
            department = request.POST['dept']
            checkbox = request.POST.getlist('checkbox')
            aoi = request.POST['aoi']
            ugabout =  request.POST['ugabout']
            ugyear = request.POST['ugyear']
        flag1=1
        flag2=0
        flag3=0
        flag4=0
        flag5=0
        flag6=0
        if('2' in checkbox):
            pgabout =  request.POST['pgabout']
            pgyear = request.POST['pgyear']
            flag2=1
        if('3' in checkbox):
            phdabout =  request.POST['phdabout']
            phdyear = request.POST['phdyear']
            flag3=1
        if('4' in checkbox):
            ac_name = request.POST['ac_name']
            ac_from = request.POST['ac_from']
            ac_to = request.POST['ac_to']
            flag4=1
        if('5' in checkbox):
            in_name = request.POST['in_name']
            in_from = request.POST['in_from']
            in_to = request.POST['in_to']
            flag5=1
        if('6' in checkbox):
            re_name = request.POST['re_name']
            re_from = request.POST['re_from']
            re_to = request.POST['re_to']
            flag6=1
        if Personal.objects.filter(facultyid=facultyid).exists():
            Personal.objects.filter(facultyid=facultyid).update(facultyname=facultyname,facultyid=facultyid,annaid=annaid,aicteid=aicteid,emailid=emailid,mobileno=mobileno,dob=dob,address=address,bgroup=bgroup,department=department,aoi=aoi,ugabout=ugabout,ugyear=ugyear,pgabout=pgabout,pgyear=pgyear,phdabout=phdabout,phdyear=phdyear,ac_name=ac_name,ac_from=ac_from,ac_to=ac_to,re_name=re_name,re_from=re_from,re_to=re_to,in_name=in_name,in_from=in_from,in_to=in_to)
        else:
            if flag1==1:
                pob=Personal.objects.create(facultyname=facultyname,facultyid=facultyid,annaid=annaid,aicteid=aicteid,emailid=emailid,mobileno=mobileno,dob=dob,address=address,bgroup=bgroup,department=department,aoi=aoi,ugabout=ugabout,ugyear=ugyear)
                pob.save()
            if flag2==1:
                Personal.objects.filter(facultyid=facultyid).update(pgabout=pgabout,pgyear=pgyear)
            if flag3==1:
                Personal.objects.filter(facultyid=facultyid).update(phdabout=phdabout,phdyear=phdyear)
            if flag4==1:
                Personal.objects.filter(facultyid=facultyid).update(ac_name=ac_name,ac_from=ac_from,ac_to=ac_to)
            if flag5==1:
                Personal.objects.filter(facultyid=facultyid).update(in_name=ain_name,in_from=in_from,in_to=in_to)
            if flag6==1:
                Personal.objects.filter(facultyid=facultyid).update(re_name=re_name,re_from=re_from,re_to=re_to)
        request.session['c']=1
        return redirect("personal")
    else:
        if(request.session["a"]==1):
            if(request.session["z"]==0):
                request.session["z"]=1
                if Personal.objects.filter(facultyid=facultyid).exists():
                    return render(request,'backend/personal.html',{"facultyname":facultyname,"facultyid":facultyid,"annaid":annaid,"aicteid":aicteid,"emailid":emailid,"mobileno":mobileno,"dob":dob,"address":address,"bgroup":bgroup,"department":department,"aoi":aoi,"ugabout":ugabout,"ugyear":ugyear,"pgabout":pgabout,"pgyear":pgyear,"phdabout":phdabout,"phdyear":phdyear,"ac_name":ac_name,"ac_from":ac_from,"ac_to":ac_to,"in_name":in_name,"in_from":in_from,"in_to":in_to,"re_name":re_name,"re_from":re_from,"re_to":re_to,"flagper":True})
                else:
                    return render(request,'backend/personal.html',{'flagper':False})
            else:
                if Personal.objects.filter(facultyid=facultyid).exists():
                    return render(request,'backend/personal.html',{"facultyname":facultyname,"facultyid":facultyid,"annaid":annaid,"aicteid":aicteid,"emailid":emailid,"mobileno":mobileno,"dob":dob,"address":address,"bgroup":bgroup,"department":department,"aoi":aoi,"ugabout":ugabout,"ugyear":ugyear,"pgabout":pgabout,"pgyear":pgyear,"phdabout":phdabout,"phdyear":phdyear,"ac_name":ac_name,"ac_from":ac_from,"ac_to":ac_to,"in_name":in_name,"in_from":in_from,"in_to":in_to,"re_name":re_name,"re_from":re_from,"re_to":re_to,"flagper":True})
                else:
                    return render(request,'backend/personal.html',{'flagper':False})
        else:
            return redirect("home")

def eveat(request):
    if request.method == 'POST':
        checkbox3 = request.POST.getlist('checkbox3')
        flag31=0
        flag32=0
        flag33=0
        flag34=0
        if('1' in checkbox3):
            flag31=1
            facultyid = request.POST['facultyid']
            fname1 = request.POST['ifname']
            fdesig1 = request.POST['ifdesig']
            fdept1 = request.POST['ifdept']
            evname1 = request.POST['iname']
            evby1 = request.POST['iby']
            venue1 = request.POST['ivenue']
            date1 = request.POST['idate']
            desc1 = request.POST['idesc']
        if('2' in checkbox3):
            flag32=1
            facultyid = request.POST['facultyid']
            fname2 = request.POST['pfname']
            fdesig2 = request.POST['pfdesig']
            fdept2 = request.POST['pfdept']
            evname2 = request.POST['pname']
            evby2 = request.POST['pby']
            venue2 = request.POST['pvenue']
            date2 = request.POST['pdate']
            desc2 = request.POST['pdesc']
        if('3' in checkbox3):
            flag33=1
            facultyid = request.POST['facultyid']
            fname3 = request.POST['wfname']
            fdesig3 = request.POST['wfdesig']
            fdept3 = request.POST['wfdept']
            evname3 = request.POST['wname']
            evby3 = request.POST['wby']
            venue3 = request.POST['wvenue']
            date3 = request.POST['wdate']
            desc3 = request.POST['wdesc']
        if('4' in checkbox3):
            flag34=1
            facultyid = request.POST['facultyid']
            fname4 = request.POST['ofname']
            fdesig4 = request.POST['ofdesig']
            fdept4 = request.POST['ofdept']
            evname4 = request.POST['oname']
            evby4 = request.POST['oby']
            venue4 = request.POST['ovenue']
            date4 = request.POST['odate']
            desc4 = request.POST['odesc']
        if(flag31==1):
            eventtype="1"
            eventsatobj = Eveat.objects.create(facultyid=facultyid,facultyname=fname1,facultydesig=fdesig1,facultydep=fdept1,eventtype=eventtype,eventname=evname1,eventby=evby1,eventdesc=desc1,venue=venue1,date=date1)
            eventsatobj.save()
        if(flag32==1):
            eventtype="2"
            eventsatobj = Eveat.objects.create(facultyid=facultyid,facultyname=fname2,facultydesig=fdesig2,facultydep=fdept2,eventtype=eventtype,eventname=evname2,eventby=evby2,eventdesc=desc2,venue=venue2,date=date2)
            eventsatobj.save()
        if(flag33==1):
            eventtype="3"
            eventsatobj = Eveat.objects.create(facultyid=facultyid,facultyname=fname3,facultydesig=fdesig3,facultydep=fdept3,eventtype=eventtype,eventname=evname3,eventby=evby3,eventdesc=desc3,venue=venue3,date=date3)
            eventsatobj.save()
        if(flag34==1):
            eventtype="4"
            eventsatobj = Eveat.objects.create(facultyid=facultyid,facultyname=fname4,facultydesig=fdesig4,facultydep=fdept4,eventtype=eventtype,eventname=evname4,eventby=evby4,eventdesc=desc4,venue=venue4,date=date4)
            eventsatobj.save()
        return render(request,'backend/eveat.html')
    else:
        if(request.session["a"]==1):
            flevat = request.session["flagevat"]
            if flevat == 1:
                request.session["flagevat"]=0
                return render(request,'backend/eveat.html',{'flagz':True})
            elif flevat==2:
                request.session["flagevat"]=0
                return render(request,'backend/eveat.html',{'flagdel':True})
            else:
                return render(request,'backend/eveat.html')
        else:
            return redirect("home")

def evcon(request):
    if request.method == 'POST':
        facultyid=request.POST['facultyid']
        checkbox2 = request.POST.getlist('checkbox2')
        flag21=0
        flag22=0
        flag23=0
        flag24=0
        flag25=0
        if('1' in checkbox2):
            flag21=1
            fdptitle = request.POST['fdptitle']
            fdprpname = request.POST['fdprpname']
            fdprpdesignation = request.POST['fdprpdesignation']
            fdprpcompany = request.POST['fdprpcompany']
            fdprpphone = request.POST['fdprpphone']
            fdprpmailid = request.POST['fdprpmailid']
            fdporganizer = request.POST['fdporganizer']
            fdpbeneficiaries = request.POST['fdpbeneficiaries']
            fdpdescription = request.POST['fdpdescription']
        if('2' in checkbox2):
            flag22=1
            daatitle = request.POST['daatitle']
            daarpname = request.POST['daarpname']
            daarpdesignation = request.POST['daarpdesignation']
            daarpcompany = request.POST['daarpcompany']
            daarpphone = request.POST['daarpphone']
            daarpmailid = request.POST['daarpmailid']
            daaorganizer = request.POST['daaorganizer']
            daadate = request.POST['daadate']
            daadept = request.POST['daadept']
            daadescription = request.POST['daadescription']
        if('3' in checkbox2):
            flag23=1
            vactitle = request.POST['vactitle']
            vacrpname = request.POST['vacrpname']
            vacrpdesignation = request.POST['vacrpdesignation']
            vacrpcompany = request.POST['vacrpcompany']
            vacrpphone = request.POST['vacrpphone']
            vacrpmailid = request.POST['vacrpmailid']
            vacorganizer = request.POST['vacorganizer']
            vacdate = request.POST['vacdate']
            vacdept = request.POST['vacdept']
            vacnostudents = request.POST['vacnostudents']
            vacdescription = request.POST['vacdescription']
        if('4' in checkbox2):
            flag24=1
            glctitle = request.POST['glctitle']
            glcrpname = request.POST['glcrpname']
            glcrpdesignation = request.POST['glcrpdesignation']
            glcrpcompany = request.POST['glcrpcompany']
            glcrpphone = request.POST['glcrpphone']
            glcrpmailid = request.POST['glcrpmailid']
            glcorganizer = request.POST['glcorganizer']
            glcdate = request.POST['glcdate']
            glcnostudents = request.POST['glcnostudents']
            glcdescription = request.POST['glcdescription']
        if('5' in checkbox2):
            flag25=1
            wtitle = request.POST['wtitle']
            wrpname = request.POST['wrpname']
            wrpdesignation = request.POST['wrpdesignation']
            wrpcompany = request.POST['wrpcompany']
            wrpphone = request.POST['wrpphone']
            wrpmailid = request.POST['wrpmailid']
            worganizer = request.POST['worganizer']
            wdate = request.POST['wdate']
            wnostudents = request.POST['wnostudents']
            wdescription = request.POST['wdescription']
        if(flag21==1):
            eventtype="1"
            eventsconobject = Evcon.objects.create(facultyid=facultyid,eventtitle=fdptitle,eventtype=eventtype,rpname=fdprpname,rpdesig=fdprpdesignation,rpcompany=fdprpcompany,rpphone=fdprpphone,rpmail=fdprpmailid,organizer=fdporganizer,nofac=fdpbeneficiaries,eventdesc=fdpdescription)
            eventsconobject.save()
        if(flag22==1):
            eventtype="2"
            eventsconobject = Evcon.objects.create(facultyid=facultyid,eventtitle=daatitle,eventtype=eventtype,rpname=daarpname,rpdesig=daarpdesignation,rpcompany=daarpcompany,rpphone=daarpphone,rpmail=daarpmailid,organizer=daaorganizer,date=daadate,dept=daadept,eventdesc=daadescription)
            eventsconobject.save()
        if(flag23==1):
            eventtype="3"
            eventsconobject = Evcon.objects.create(facultyid=facultyid,eventtitle=vactitle,eventtype=eventtype,rpname=vacrpname,rpdesig=vacrpdesignation,rpcompany=vacrpcompany,rpphone=vacrpphone,rpmail=vacrpmailid,organizer=vacorganizer,date=vacdate,dept=vacdept,nostud=vacnostudents,eventdesc=vacdescription)
            eventsconobject.save()
        if(flag24==1):
            eventtype="4"
            eventsconobject = Evcon.objects.create(facultyid=facultyid,eventtitle=glctitle,eventtype=eventtype,rpname=glcrpname,rpdesig=glcrpdesignation,rpcompany=glcrpcompany,rpphone=glcrpphone,rpmail=glcrpmailid,organizer=glcorganizer,nostud=glcnostudents,date=glcdate,eventdesc=glcdescription)
            eventsconobject.save()
        if(flag25==1):
            eventtype="5"
            eventsconobject = Evcon.objects.create(facultyid=facultyid,eventtitle=wtitle,eventtype=eventtype,rpname=wrpname,rpdesig=wrpdesignation,rpcompany=wrpcompany,rpphone=wrpphone,rpmail=wrpmailid,organizer=worganizer,date=wdate,nostud=wnostudents,eventdesc=wdescription)
            eventsconobject.save()
        return render(request,'backend/evcon.html')
    else:
        if(request.session["a"]==1):
            flaw=request.session["flagevcon"]
            if(flaw==1):
                request.session["flagevcon"]=0
                return render(request,'backend/evcon.html',{'flagz':True})
            elif(flaw==2):
                request.session["flagevcon"]=0
                return render(request,'backend/evcon.html',{'flagdel':True})
            else:
                return render(request,'backend/evcon.html')
        else:
            return redirect("home")

def awards(request):
    if request.method == 'POST':
        facultyname = request.POST['facultyname']
        facultyid = request.POST['facultyid']
        date = request.POST['date']
        awardname = request.POST['awardname']
        awarddes = request.POST['awarddes']
        dept = request.POST['dept']
        awardedby = request.POST['awardedby']
        awardobject = Awards.objects.create(facultyname=facultyname,facultyid=facultyid,dateawarded=date,awardname=awardname,awarddescription=awarddes,department=dept,awardedby=awardedby)
        awardobject.save()
        return render(request,'backend/awards.html')
    else:
        if(request.session["a"]==1):
            flaw=request.session["flagawards"]
            if(flaw==1):
                request.session["flagawards"]=0
                return render(request,'backend/awards.html',{'flagz':True})
            elif(flaw==2):
                request.session["flagawards"]=0
                return render(request,'backend/awards.html',{'flagdel':True})
            else:
                return render(request,'backend/awards.html')
        else:
            return redirect("home")

def update(request):
    userid=request.user
    flag=0
    if Awards.objects.filter(facultyid=userid).exists():
        flag=1
        updateobj=Awards.objects.filter(facultyid=userid)
    if request.method == 'POST':
        for i in updateobj:
            if(str(i.id) in request.POST):
                request.session['update']=str(i.id)
                break
        return redirect('updateawards')
    else:
        if(request.session["a"]==1):
            if(flag==1):
                return render(request,'backend/update.html',{'upob':updateobj})
            else:
                request.session["flagawards"]=1
                return redirect('awards')
        else:
            return redirect("home")

def update1(request):
    userid=request.user
    flag=0
    if Evcon.objects.filter(facultyid=userid).exists():
        flag=1
        evconobj = Evcon.objects.filter(facultyid=userid)
    if request.method == 'POST':
        for i in evconobj:
            if(str(i.id) in request.POST):
                request.session['update1']=str(i.id)
                break
        return redirect("updateevcon")
    else:
        if(request.session["a"]==1):
            if(flag==1):
                return render(request,'backend/update1.html',{'evconobj':evconobj})
            else:
                request.session["flagevcon"]=1
                return redirect("evcon")
        else:
            return redirect("home")

def update2(request):
    userid=request.user
    flag=0
    if Eveat.objects.filter(facultyid=userid).exists():
        flag=1
        evatobj = Eveat.objects.filter(facultyid=userid)
    if request.method == 'POST':
        for i in evatobj:
            if(str(i.id) in request.POST):
                request.session['update2']=str(i.id)
                break
        return redirect("updateeveat")
    else:
        if(request.session["a"]==1):
            if(flag==1):
                return render(request,'backend/update2.html',{'evatobj':evatobj})
            else:
                request.session["flagevat"]=1
                return redirect("eveat")
        else:
            return redirect("home")

def login(request):
    if request.method == 'POST':
        facultyid = request.POST['facultyid']
        facultypassword = request.POST['facultypassword']
        user = auth.authenticate(username=facultyid,password=facultypassword)
        if user is not None:
            auth.login(request,user)
            request.session["a"]=1
            return redirect("personal")
        else:
            return render(request,'backend/login.html',{'flag':True})
    else:
        if(request.session["a"]==1):
            return redirect("personal")
        else:
            return render(request,'backend/login.html')

def logout(request):
    auth.logout(request)
    request.session["a"]=0
    request.session["z"]=0
    return redirect('home')

def report(request):
    request.session['evecon']=[]
    request.session['award']=[]
    request.session['eveat']=[]
    ec=['Faculty Development Program','Department Association Activites','Value Added Courses Conducted','Guest Lecture Conducted','Workshop Conducted']
    ea=['International Conference','PSG CARE Program','Workshop','Online Course']
    cu = request.user
    if Evcon.objects.filter(facultyid=cu).exists():
        evconobj = Evcon.objects.filter(facultyid=cu)
        for i in evconobj:
            t1=int(i.eventtype)
            request.session['evecon']+=[[ec[t1-1],i.eventtitle,i.id]]
    if Awards.objects.filter(facultyid=cu).exists():
        awardobj = Awards.objects.filter(facultyid=cu)
        for i in awardobj:
            request.session['award']+=[[i.awardname,i.id]]
    if Eveat.objects.filter(facultyid=cu).exists():
        evatobj = Eveat.objects.filter(facultyid=cu)
        for i in evatobj:
            t2=int(i.eventtype)
            request.session['eveat']+=[[ea[t2-1],i.eventname,i.id]]
    print(request.session['eveat'])
    if request.method == 'POST':
        request.session['checkboxr'] = request.POST.getlist('checkboxr')
        request.session['checkboxevcon'] = request.POST.getlist('checkboxevcon')
        request.session['checkboxaward'] = request.POST.getlist('checkboxaward')
        request.session['checkboxeveat'] = request.POST.getlist('checkboxeveat')
        print(request.session['checkboxr'])
        return redirect('submit')
    else:
        if(request.session["a"]==1):
            return render(request,'backend/report.html',{'award':request.session['award'],'evecon':request.session['evecon'],'eveat':request.session['eveat']})
        else:
            return redirect("home")

def updateawards(request):
    id2=request.session["update"]
    award=Awards.objects.filter(id=id2)
    for i in award:
        test1=i.facultyname
        facultyname=i.facultyname
        test2=i.facultyid
        facultyid=i.facultyid
        dateawarded=i.dateawarded
        awardname=i.awardname
        department=i.department
        awarddescription=i.awarddescription
        awardedby=i.awardedby
    if request.method == 'POST':
        if 'updateaward' in request.POST:
            if(request.POST['facultyname'] != ""):
                if(test1!=request.POST['facultyname']):
                    return render(request,'backend/updateawards.html',{'flagtest1':True,'facultyname':facultyname,'facultyid':facultyid,'dateawarded':dateawarded,'awardname':awardname,'awarddescription':awarddescription,'department':department,'awardedby':awardedby})
                else:
                    facultyname = request.POST['facultyname']
            if(request.POST['facultyid'] != ""):
                if(test2!=request.POST['facultyid']):
                    return render(request,'backend/updateawards.html',{'flagtest2':True,'facultyname':facultyname,'facultyid':facultyid,'dateawarded':dateawarded,'awardname':awardname,'awarddescription':awarddescription,'department':department,'awardedby':awardedby})
                else:
                    facultyid = request.POST['facultyid']
            if(request.POST['dateawarded'] != ""):
                dateawarded = request.POST['dateawarded']
            if(request.POST['awardname'] != ""):
                awardname = request.POST['awardname']
            if(request.POST['awarddescription'] != ""):
                awarddescription = request.POST['awarddescription']
            if(request.POST['dept'] != ""):
                department = request.POST['dept']
            if(request.POST['awardedby'] != ""):
                awardedby = request.POST['awardedby']
            Awards.objects.filter(id=id2).update(facultyname=facultyname,facultyid=facultyid,dateawarded=dateawarded,awardname=awardname,department=department,awarddescription=awarddescription,awardedby=awardedby)
            return render(request,'backend/updateawards.html',{'facultyname':facultyname,'facultyid':facultyid,'dateawarded':dateawarded,'awardname':awardname,'awarddescription':awarddescription,'department':department,'awardedby':awardedby,'flagupdate':True})
        elif 'deleteaward' in request.POST:
            Awards.objects.filter(id=id2).delete()
            request.session['flagawards']=2
            return redirect('awards')
    else:
        if(request.session["a"]==1):
            return render(request,'backend/updateawards.html',{'facultyname':facultyname,'facultyid':facultyid,'dateawarded':dateawarded,'awardname':awardname,'awarddescription':awarddescription,'department':department,'awardedby':awardedby})
        else:
            return redirect("home")

def updateevcon(request):
    id3=request.session["update1"]
    evcon=Evcon.objects.filter(id=id3)
    for i in evcon:
        facultyid = i.facultyid
        eventtitle = i.eventtitle
        eventtype = i.eventtype
        rpname = i.rpname
        rpdesig = i.rpdesig
        rpcompany = i.rpcompany
        rpphone = i.rpphone
        rpmail = i.rpmail
        organizer = i.organizer
        date = i.date
        nofac = i.nofac
        nostud = i.nostud
        dept = i.dept
        eventdesc = i.eventdesc
        flagval=eventtype
    if request.method == 'POST':
        if 'Updateevent' in request.POST:
            if(request.POST["facultyid"]!=""):
                facultyid=request.POST["facultyid"]
            if(request.POST["eventtitle"]!=""):
                eventtitle=request.POST["eventtitle"]
            if(request.POST["rpname"]!=""):
                rpname=request.POST["rpname"]
            if(request.POST["rpdesig"]!=""):
                rpdesig=request.POST["rpdesig"]
            if(request.POST["rpcompany"]!=""):
                rpcompany=request.POST["rpcompany"]
            if(request.POST["rpphone"]!=""):
                rpphone=request.POST["rpphone"]
            if(request.POST["rpmail"]!=""):
                rpmail=request.POST["rpmail"]
            if(request.POST["organizer"]!=""):
                organizer=request.POST["organizer"]
            if(request.POST["date"]!=""):
                date=request.POST["date"]
            if eventtype == "1":
                if(request.POST["nofac"]!=""):
                    nofac=request.POST["nofac"]
            elif(eventtype == "3" or eventtype == "4" or eventtype == "5"):
                if(request.POST["nostud"]!=""):
                    nostud=request.POST["nostud"]
            if(eventtype== "2" or eventtype=="3"):
                if(request.POST["dept"]!=""):
                    dept=request.POST["dept"]
            if(request.POST["eventdesc"]!=""):
                eventdesc=request.POST["eventdesc"]
            Evcon.objects.filter(id=id3).update(facultyid=facultyid,eventtitle=eventtitle,eventtype=eventtype,rpname=rpname,rpdesig=rpdesig,rpcompany=rpcompany,rpphone=rpphone,rpmail=rpmail,organizer=organizer,nofac=nofac,eventdesc=eventdesc,date=date,nostud=nostud,dept=dept)
            return render(request,'backend/updateevcon.html',{'facultyid':facultyid,'eventtitle':eventtitle,'eventtype':eventtype,'rpname':rpname,'rpdesig':rpdesig,'rpcompany':rpcompany,'rpphone':rpphone,'rpmail':rpmail,'organizer':organizer,'date':date,'nofac':nofac,'nostud':nostud,'dept':dept,'eventdesc':eventdesc,'flagval':flagval,'flagupdate':True})
        elif 'Delevent' in request.POST:
            Evcon.objects.filter(id=id3).delete()
            request.session['flagevcon']=2
            return redirect('evcon')
    else:
        if(request.session["a"]==1):
            return render(request,'backend/updateevcon.html',{'facultyid':facultyid,'eventtitle':eventtitle,'eventtype':eventtype,'rpname':rpname,'rpdesig':rpdesig,'rpcompany':rpcompany,'rpphone':rpphone,'rpmail':rpmail,'organizer':organizer,'date':date,'nofac':nofac,'nostud':nostud,'dept':dept,'eventdesc':eventdesc,'flagval':flagval})
        else:
            return redirect("home")

def updateeveat(request):
    id4=request.session["update2"]
    evat=Eveat.objects.filter(id=id4)
    for i in evat:
        facultyid = i.facultyid
        facultyname = i.facultyname
        facultydesig = i.facultydesig
        facultydep = i.facultydep
        eventtype = i.eventtype
        eventname = i.eventname
        eventby = i.eventby
        eventdesc = i.eventdesc
        venue = i.venue
        date = i.date
    if request.method == 'POST':
        if 'Updateevent' in request.POST:
            if(request.POST["facultyid"]!=""):
                facultyid=request.POST["facultyid"]
            if(request.POST["facultyname"]!=""):
                facultyname=request.POST["facultyname"]
            if(request.POST["facultydesig"]!=""):
                facultydesig=request.POST["facultydesig"]
            if(request.POST["facultydep"]!=""):
                facultydep=request.POST["facultydep"]
            if(request.POST["eventname"]!=""):
                eventname=request.POST["eventname"]
            if(request.POST["eventby"]!=""):
                eventby=request.POST["eventby"]
            if(request.POST["eventdesc"]!=""):
                eventdesc=request.POST["eventdesc"]
            if(request.POST["venue"]!=""):
                venue=request.POST["venue"]
            if(request.POST["date"]!=""):
                date=request.POST["date"]
            Eveat.objects.filter(id=id4).update(facultyid=facultyid,facultyname=facultyname,facultydesig=facultydesig,facultydep=facultydep,eventtype=eventtype,eventname=eventname,eventby=eventby,eventdesc=eventdesc,venue=venue,date=date)
            return render(request,'backend/updateeveat.html',{'facultyid':facultyid,'facultyname':facultyname,'facultydesig':facultydesig,'facultydep':facultydep,'eventtype':eventtype,'eventname':eventname,'eventby':eventby,'eventdesc':eventdesc,'venue':venue,'date':date,'flagupdate':True})
        elif 'Delevent' in request.POST:
            Eveat.objects.filter(id=id4).delete()
            request.session['flagevat']=2
            return redirect('eveat')
    else:
        if(request.session["a"]==1):
            return render(request,'backend/updateeveat.html',{'facultyid':facultyid,'facultyname':facultyname,'facultydesig':facultydesig,'facultydep':facultydep,'eventtype':eventtype,'eventname':eventname,'eventby':eventby,'eventdesc':eventdesc,'venue':venue,'date':date})
        else:
            return redirect("home")

def submit(request):
    flag1=0
    flag2=0
    flag3=0
    flag4=0
    request.session["genj"]=0
    request.session["gend"]=0
    if request.method == 'POST':
        if 'View PDF File' in request.POST:
            request.session["genj"]=1
            return redirect("gen")
        if 'Download PDF File' in request.POST:
            request.session["gend"]=1
            return redirect("gen")
    else:
        if(request.session["a"]==1):
            userid = request.user
            if('1' in request.session['checkboxr']):
                if Personal.objects.filter(facultyid=userid).exists():
                    flag1=1
                    persobj = Personal.objects.filter(facultyid=userid)
            if(len(request.session['checkboxevcon'])!=0):
                if Evcon.objects.filter(facultyid=userid).exists():
                    flag2=1
                    evconobj1=[]
                    for i in request.session['checkboxevcon']:
                        evconobj1+=[Evcon.objects.filter(id=i)]
            if(len(request.session['checkboxaward'])!=0):
                if Awards.objects.filter(facultyid=userid).exists():
                    flag3=1
                    awardobj1=[]
                    for i in request.session['checkboxaward']:
                        awardobj1+=[Awards.objects.filter(id=i)]
            if(len(request.session['checkboxeveat'])!=0):
                if Eveat.objects.filter(facultyid=userid).exists():
                    flag4=1
                    evatobj1=[]
                    for i in request.session['checkboxeveat']:
                        evatobj1+=[Eveat.objects.filter(id=i)]
            print(flag1,flag2,flag3,flag4)
            if(flag1==1):
                if(flag2==1):
                    if(flag3==1):
                        if(flag4==1):
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'flag4':flag4,'evconobj':evconobj1,'awardobj':awardobj1,'persobj':persobj,'evatobj':evatobj1})
                        else:
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'evconobj':evconobj1,'awardobj':awardobj1,'persobj':persobj})
                    else:
                        if(flag4==1):
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'flag4':flag4,'evconobj':evconobj1,'persobj':persobj,'evatobj':evatobj1})
                        else:
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'evconobj':evconobj1,'persobj':persobj})
                else:
                    if(flag3==1):
                        if(flag4==1):
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'flag4':flag4,'persobj':persobj,'awardobj':awardobj1,'evatobj':evatobj1})
                        else:
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'persobj':persobj,'awardobj':awardobj1})
                    else:
                        if(flag4==1):
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'flag4':flag4,'persobj':persobj,'evatobj':evatobj1})
                        else:
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'persobj':persobj})
            else:
                if(flag2==1):
                    if(flag3==1):
                        if(flag4==1):
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'flag4':flag4,'evconobj':evconobj1,'awardobj':awardobj1,'evatobj':evatobj1})
                        else:
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'evconobj':evconobj1,'awardobj':awardobj1})
                    else:
                        if(flag4==1):
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'flag4':flag4,'evconobj':evconobj1,'evatobj':evatobj1})
                        else:
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'evconobj':evconobj1})
                else:
                    if(flag3==1):
                        if(flag4==1):
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'flag4':flag4,'awardobj':awardobj1,'evatobj':evatobj1})
                        else:
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'awardobj':awardobj1})
                    else:
                        if(flag4==1):
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'flag4':flag4,'evatobj':evatobj1})
                        else:
                            return render(request,'backend/submit.html',{'flag1':flag1,"flag2":flag2,'flag3':flag3,'flag4':flag4})
        else:
            return redirect("home")

from telegram.ext import *
from datetime import datetime
print("Bot started...")
keys = '#:#'
#RESPONSES
def sample_responses(input_text):
    user_message = str(input_text).lower()
    print(user_message.split())
    if(user_message in ("hello","hi","sup",)):
        return "Hey! How's it going?"
    if(user_message in ("who are you","who are you?",)):
        return "I am a #!"
    if user_message in ("time","time?"):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y,%H:%M:%S")
        return str(date_time)
    return "I don't understand you."


def start_command(update,context):
    update.message.reply_text('Type something you want to get started!')

def help_command(update,context):
    update.message.reply_text('If you need further help try visiting our Website!')

def handle_message(update,context):
    awardobj = Awards.objects.filter(id="4",facultyid="#")
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
