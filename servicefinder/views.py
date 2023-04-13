from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout
from servicefinder.models import Userdetail,Contact,Booking,PartnerProfile,PartnerService,PartnerBookings
# Create your views here.

def home(request):
    try:
        return render(request,"home.html")
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")


def home1(request,slug,slug2):
    try:
        obj=PartnerService.objects.filter(city=slug,service=slug2)
        # print(obj)
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

def partnerHome(request):
    if request.user.is_authenticated:
        
        user=request.user
        obj2=Userdetail.objects.filter(username=user)
        if request.method=='POST':
            profile_img=request.FILES.getlist('pimg')[0]
            address=request.POST.get('address','')
            adhar=request.POST.get('adhar','')
            print(profile_img,address,adhar)
            
            obj=PartnerProfile(userid=obj2[0],profile_img=profile_img,address=address,aadhar=adhar)
            obj.save()
            messages.success(request,"Your Response submitted successfully")
        
        if PartnerProfile.objects.filter(userid=obj2[0]).exists():
            return redirect('partnerform')
        else:
            return render(request,'phome.html')
    else:
        messages.error(request,'Please login first')
        return redirect('login')


def partnerForm(request):
    if request.user.is_authenticated:
        
        user=request.user
        obj2=Userdetail.objects.filter(username=user)
        pprofile=PartnerProfile.objects.filter(userid=obj2[0])
        if pprofile:
            if request.method=='POST':
                service=request.POST.get('service','')
                city=request.POST.get('city','')
                fee=request.POST.get('fee','')
                time=request.POST.get('time','')
                form=PartnerService(profile=pprofile[0],service=service,city=city,fee=fee,timing=time)
                form.save()
                messages.success(request,"Your Response submitted successfully")
                return redirect('home')
            if PartnerService.objects.filter(profile=pprofile[0],status=True).exists():
                return redirect('dashboard')
            elif PartnerService.objects.filter(profile=pprofile[0]).exists():
                return render(request,'pform.html',{'status':True})
            else:
                return render(request,'pform.html',{'status':False}) 
        else:
            messages.error(request,'Please fill your profile first')
            return redirect('partnerhome')
    else:
        messages.error(request,'Please login first')
        return redirect('login')

def partnerUpdateForm(request):
    if request.user.is_authenticated:
        user=request.user
        obj2=Userdetail.objects.filter(username=user)
        pprofile=PartnerProfile.objects.filter(userid=obj2[0])
        if pprofile:
            if PartnerService.objects.filter(profile=pprofile[0],status=True).exists():
                if request.method=='POST':
                    service=request.POST.get('service','')
                    city=request.POST.get('city','')
                    fee=request.POST.get('fee','')
                    time=request.POST.get('time','')
                    PartnerService.objects.filter(profile=pprofile[0],status=True).update(service=service,city=city,fee=fee,timing=time)

                    messages.success(request,"Your Response Updated successfully")
                    return redirect('dashboard')

                obj=PartnerService.objects.filter(profile=pprofile[0],status=True)
                print(obj)
                return render(request,'pupdateform.html',{'obj':obj[0]})
        else:
            return HttpResponse('404')
    else:
        return HttpResponse('404')

    

def dashboard(request):
    if request.user.is_authenticated:
        
        user=request.user
        obj2=Userdetail.objects.filter(username=user)
        pprofile=PartnerProfile.objects.filter(userid=obj2[0])
        if pprofile:
            if PartnerService.objects.filter(profile=pprofile[0],status=True).exists():
                obj=PartnerBookings.objects.filter(p_username=request.user)
                print(obj)

                return render(request,'dashboard.html',{'obj':obj})
            else:
                return HttpResponse('404')
        else:
            return HttpResponse('404')


def checkout(request,slug,slug2,id):
    try:

        if request.user.is_authenticated:
            
            obj=PartnerService.objects.filter(sno=id)[0]
            partner_username=obj.profile.userid.username
            print(partner_username)
        
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
                


                form=Booking(name=name,phone=phone,address=address,date=date,f_time=f_time,a_time=a_time,description=problem,userid=obj2[0],servicer=PartnerService.objects.filter(sno=id)[0])
                form.save()
                form2=PartnerBookings(p_username=partner_username,Booking_details=Booking.objects.filter(sno=form.sno)[0])
                form2.save()
                messages.success(request,"Your Response is saved we'll contact you shortly")
                return redirect("home")

            
            
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
    



def AcceptRequest(request,id):
    if request.user.is_authenticated:
        obj=PartnerBookings.objects.filter(sno=id)[0]
        if(obj.p_username==str(request.user)):
            PartnerBookings.objects.filter(sno=id).update(confirm=True)
            # print(obj.Booking_details.sno)
            Booking.objects.filter(sno=obj.Booking_details.sno).update(status='True')
            messages.success(request,"Request Accepted")

            

        return redirect('dashboard')
    else:
        return HttpResponse('404')


def DeclineRequest(request,id):
    if request.user.is_authenticated:
        obj=PartnerBookings.objects.filter(sno=id)[0]
        if(obj.p_username==str(request.user)):
            PartnerBookings.objects.filter(sno=id).update(cancel=True)
            # print(obj.Booking_details.sno)
            Booking.objects.filter(sno=obj.Booking_details.sno).update(status='False')
            messages.success(request,"Request Declined")

            

        return redirect('dashboard')
    else:
        return HttpResponse('404')

