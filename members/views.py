from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm,loginf, carc, paym
from .models import User, Car, Rent, Payment
from django.utils import timezone
from django.db.models import F


#import hashlib
"""
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")"""
def home(request):
    return render(request,"home.html",{})  

def signup(request):
    if request.method=="POST":
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            form=UserForm()
            return render(request,"signup.html",{'form':form, 'done':"done"})
        else:
            return render(request,"signup.html",{'form':form})
        
    form=UserForm()
    return render(request,"signup.html",{'form':form})

def login(request):
    if request.method=="POST":
        form=loginf(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            user=User.objects.filter(email=email)
            for ino in user:
                uuid=ino.uid
            request.session['curid']=uuid
            return redirect('/account/')
        else:
            return render(request,"login.html",{'form':form})
        
    form=loginf()
    return render(request,"login.html",{'form':form})
def acc(request):
    if 'curid' not in request.session:
        return render(request,"temp.html",{})
    user=User.objects.get(uid=request.session['curid'])
    return render(request,"acc.html",{'user':user})
def logout(request):
    if 'curid' in request.session:
        del request.session['curid']
        return render(request,"logout.html", {'done':'1'})
    else:
        return render(request,"logout.html",{})

def rent(request):
    if 'curid' not in request.session:
        return render(request,"temp.html",{})
    if request.method=="POST":
        form=carc(request.POST)
        if form.is_valid():
            vno=form.cleaned_data['dropdown']
            days=form.cleaned_data['days']
            user=User.objects.get(uid=request.session['curid'])
            car=Car.objects.get(vno=vno)
            car.occup=True
            car.save()
            total=days*car.rate
            cd=timezone.now().date()
            newr=Rent(total=total,nod=days, start=cd, uid=user, vno=car )
            newr.save()
            return render(request, 'congo.html',{ 'name':car.model, 'days': days})

        else:
            cars=Car.objects.all()
            return render(request,"rent.html",{'form':form, 'cars':cars})
    cars=Car.objects.all()   
    form=carc()
    return render(request,"rent.html",{'form':form,'cars':cars })

def history(request):
    if 'curid' not in request.session:
        return render(request,"temp.html",{})
    rents = Rent.objects.select_related('vno').filter(uid=request.session['curid'])
    user=User.objects.get(uid=request.session['curid'])
    if len(rents)>0:
        return render(request,'history.html',{'rents':rents, 'user':user})
    else:
        return render(request,'history.html',{'user':user})
def pay(request):
    if 'curid' not in request.session:
        return render(request,"temp.html",{})
    if request.method=="POST":
        form=paym(request.POST)
        if form.is_valid():
            rid=form.cleaned_data['rentid']
            ammo=form.cleaned_data['amount']
            rent=Rent.objects.get(rid=rid)
            rent.given=rent.given+ammo
            rent.save()
            user=User.objects.get(uid=request.session['curid'])
            cd=timezone.now().date()
            newp=Payment(amount=ammo, uid=user, dat=cd, rid=rent )
            newp.save()
            return render(request, 'congopay.html',{ 'rid': rid, 'amount': ammo})

        else:
            rents=Rent.objects.filter(uid=request.session['curid'], total__gt=F('given'))   
            return render(request,"pay.html",{'form':form, 'rents':rents})
    rents=Rent.objects.filter(uid=request.session['curid'], total__gt=F('given'))   
    if len(rents)>0:
        form=paym()
        return render(request,"pay.html",{'form':form,'rents':rents })
    else:
        return render(request,"pay.html",{})
    
def payhistory(request):
    if 'curid' not in request.session:
        return render(request,"temp.html",{})
    uid=request.session['curid']
    pays=Payment.objects.filter(uid=uid).order_by('-dat')
    user=User.objects.get(uid=uid)
    if len(pays)>0:
        return render(request, 'payhistory.html', {'pays': pays, 'user': user})
    else:
        return render(request, 'payhistory.html', {'user': user})

    


    




