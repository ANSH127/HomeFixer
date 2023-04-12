from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout
from servicefinder.models import Userdetail,Contact,Partner,Booking
# Create your views here.

def home(request):
    try:
        return render(request,"home.html")
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")

def home1(request,slug,slug2):
    try:
        print(slug)
        print(slug2)
        obj=Partner.objects.filter(city=slug,service=slug2)
        print(obj)
        return render(request,"home1.html",{'myobj':obj,'len':len(obj),'city':slug,'service':slug2})
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")


def about(request):
    try:
        return render(request,"about.html")
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")

def contact(request):
    try:
        if request.method=='POST':
            name=request.POST.get('name','')
            c_email=request.POST.get('email','')
            phone=request.POST.get('phone','')
            msg=request.POST.get('msg','')
            contact=Contact(name=name,email=c_email,phone=phone,message=msg)
            contact.save()
            
            messages.success(request,"Your Response submitted successfully")
            return redirect('/')

            
        else:
            return render(request,'contact.html')
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")

def handlelogin(request):
    try:
        if request.method=='POST':
            loginusername=request.POST.get('username','')
            loginpassword=request.POST.get('password','')
            user=authenticate(username=loginusername, password=loginpassword)
            if user is not None:
                login(request,user)
                
                messages.success(request,"Successfully Logged in")

                return redirect('/')
            else:
                messages.error(request,'Invalid Credentials, Please Try Again')
                return redirect('login')



            
        else:
            return render(request,'login.html')
        
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")

def hanldesignup(request):
    try:

        if request.method=='POST':
            # get the post parameter
            username=request.POST.get('username','')
            name=request.POST.get('name','')
            signup_email=request.POST.get('signup_email','')
            phone=request.POST.get('phone','')
            password=request.POST.get('password','')
            password1=request.POST.get('password1','')
            print(username,name,signup_email,phone,password,password1)
            if len(name.split())!=2:
                messages.error(request,'Enter your full name')
                return redirect('signup')

            fname=name.split()[0]
            lname=name.split()[1]
            # username should be atleast 10 character long
            if len(username)>10:
                messages.error(request,'username must be under 10 characters')
                return redirect('signup')
            # username should be alphanumeric
            
            if not  username.isalnum():
                messages.error(request,'username should only cantain letters and number')
                return redirect('signup')
            # password should be match with confirm password field
            if password!=password1:
                messages.error(request,'Password does not match')
                return redirect('signup')
            
            myuser=User.objects.create_user(username,signup_email,password)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
            userdetail=Userdetail(username=username,name=name,phone=phone,email=signup_email,password=password)
            userdetail.save()


            user=authenticate(username=username, password=password)
            login(request,user)


            messages.success(request,"Your JustDialHere account successfully created")
            return redirect('/')
            
        return render(request,"signup.html")
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")




def handlelogout(request):
    try:
    
        logout(request)
        messages.success(request,'Successfully Logout')
        return redirect('/')
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")
def partner(request):
    try:
        if request.method=='POST':
            profile_img=request.FILES.getlist('pimg')[0]

            name=request.POST.get('name','')
            email=request.POST.get('email','')
            phone=request.POST.get('phone','')
            address=request.POST.get('address','')
            service=request.POST.get('service','')
            city=request.POST.get('city','')
            fee=request.POST.get('fee','')
            time=request.POST.get('time','')
            adhar=request.POST.get('adhar','')
            form=Partner(profile_img=profile_img,name=name,email=email,phone=phone,aadhar=adhar,service=service,fee=fee,city=city,address=address,timing=time)
            form.save()
            
            messages.success(request,"Your Response submitted successfully")
            return redirect('home')
            # print(name,email,phone,service,fee,adhar,profile_img,address,city,time)
        return render(request,"partner.html")
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")


def checkout(request,slug,slug2,id):
    try:

        if request.user.is_authenticated:
        
            if request.method=='POST':
                name=request.POST.get('name','')
                phone=request.POST.get('phone','')
                address=request.POST.get('address','')
                date=request.POST.get('date','')
                f_time=request.POST.get('f_time','')
                a_time=request.POST.get('t_time','')
                problem=request.POST.get('problem','')
                print(name,phone,address,date,f_time,a_time,problem)
                
                user=request.user
                obj2=Userdetail.objects.filter(username=user)
                


                form=Booking(name=name,phone=phone,address=address,date=date,f_time=f_time,a_time=a_time,description=problem,userid=obj2[0],servicer=Partner.objects.filter(sno=id)[0])
                form.save()
                messages.success(request,"Your Response is saved we'll contact you shortly")
                return redirect("home")
            
            obj=Partner.objects.filter(sno=id)[0]
            
            return render(request,"checkout.html",{'obj':obj})
        else:
            messages.error(request,'Please Login First')
            return redirect('login')
        
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")



def booking(request):
    try:
        if request.user.is_authenticated:

        
            obj=Booking.objects.filter(userid=Userdetail.objects.filter(username=request.user)[0])
            print(obj)

            return render(request,"booking.html",{'obj':obj})
        else:
            messages.error(request,'Login to see your bookings.')
            return redirect('login')
        
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")