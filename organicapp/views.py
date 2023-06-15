from django.shortcuts import render,redirect,HttpResponse
from organicapp.models import Product,Cart,Order,OrderHistory,Contact
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from organicapp.forms import UserForm
from django.db.models import Q
from django.contrib.auth.models import User
import random
import razorpay
from django.core.mail import send_mail
from django.conf import settings
import datetime
# Create your views here.
def index(request):
    p=Product.objects.filter(status=1)
    content={}
    content['product']=p
    return render(request,'index.html',content)

def about(request):
    return render(request,'about.html')

def user_register(request):
    # regobj=UserForm
    # print(regobj)#object bana
    # content['userform']=regobj
    content={}
    if request.method=="POST":
        uname=request.POST['uname']
        f=request.POST['fname']
        l=request.POST['lname']
        m=request.POST['umail']
        upass=request.POST['upass']
        cpass=request.POST['ucpass']
        
        #Fetch data from form POST request
        # print(uname)
        # print(mb)
        # print(upass)
        # print(cpass)
       
        
        if uname=="" or f=="" or l=="" or  m=="" or upass=="" or cpass=="":
            content['errmsg']="Field Cannot be Empty"
        elif upass != cpass:
            content['errmsg']="Password and Confirm Password didn't match"
        else:
            
            try:    
                u=User.objects.create(username=uname,password=upass,email=m,first_name=f,last_name=l,is_active=1,date_joined=datetime.datetime.now())
                u.set_password(upass)
                u.save()
            except Exception:
                content['errmsg']="Username Already Exists!!!"
                return render(request,'register.html',content)
            
            if u:
                url='/verifyscreen/'+str(u.id)
                return redirect(url)
            
            content['success']='User Created Successfully'
        return render(request,'user_register.html',content)

    else:
        # regobj=UserCreationForm()
        # print(regobj)
        return render(request,'user_register.html',content)

def verifyscreen(request,rid):  
      u=User.objects.filter(id=rid) 
      rec_mail=u[0].email
      s="Email Verfication"
      otp=str(random.randrange(1000,9999))
      msg="OTP for Email Verification: "+str(otp)
      # print(m)
      # r=u.email
      # print(r)
      
      request.session[rec_mail]=otp
      send_mail(
            s,
            msg,
            settings.EMAIL_HOST_USER,
            [rec_mail],
            fail_silently=False,
            )
      content={}
      content['userid']=rid
      #store otp in the database
      return render(request,'verifyscreen.html',content)
    

def verifyotp(request,rid):
    content={}
    otp=request.POST['uotp']
    print("userid: ",rid)
    u=User.objects.filter(id=rid)
    uemail=u[0].email
    sess_otp=request.session[uemail]
    if otp == sess_otp :
    
        content['success'] = "Gmail Verified Successfully"
        content['redirecting']="Redirecting You to Login Page"
        
        
    return render(request,'verifyscreen.html',content)
     
     

def user_login(request):
    if request.method=="POST":
        dataobj=AuthenticationForm(request=request,data=request.POST)
        print(dataobj)
        uname=dataobj.cleaned_data['username']
        upass=dataobj.cleaned_data['password']
        print('Username:',uname)
        print('Password:',upass)
        user=authenticate(username=uname,password=upass)
        print(user)
        if user:
                print('hello i am kitty')
                login(request,user)
                return redirect('/')
    else:
        lobj=AuthenticationForm
        print(lobj)
        content={}
        content['loginform']=lobj
        return render(request,'user_login.html',content)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        # print("User ID:",userid)
        # print("Product ID:",pid)
        q1=Q(pid=pid)
        q2=Q(uid=userid)
        c=Cart.objects.filter(q1 & q2)
        p=Product.objects.filter(id=pid)
        content={}
        content['products']=p
        if c:
            content['msg']="Product Already Exists in the Cart"
            # return render(request,'product_details.html',content)
        else:

            u=User.objects.filter(id=userid)
            # print(u[0])
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            content['success']="Product Added in Cart"
            # return render(request,'product_details.html',content)
            # return HttpResponse("product added successfully")
            # return HttpResponse("usereid and productid fetched")
        return render(request,'product_details.html',content)
    else:
        return redirect('/login')


   
def user_logout(request):

    logout(request)
    return redirect('/login')
    

def  product_details(request,pid):
    # print('Id of the product',pid)
    data=Product.objects.filter(id=pid)
    content={}
    content['products']=data
    return render(request,'product_details.html',content)

def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    # print(c)
    # print(c[0])
    # print(c[0].uid)
    # print(c[0].pid)
    sum=0
    for x in c:
        sum=sum+(x.qty*x.pid.price)
        print("Total Product Price: ",sum)
    content={}
    content['products']=c
    content['nitems']=len(c)
    content['total']=sum
    return render(request,'viewcart.html',content)

def changeqty(request,pid,f):
    content={}
    c=Cart.objects.filter(pid=pid)
    if f=='1':
        # print(c)
        # print(c[0])
        # print(c[1])
        x=c[0].qty+1
    else:
        x=c[0].qty-1
     
    if x>0:
        c.update(qty=x)
    
    return redirect('/viewcart')

def placeorder(request):
    oid=random.randrange(1000,9999)
    print(oid)
    user_id=request.user.id
    c=Cart.objects.filter(uid=user_id)
    print(c)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    
    o=Order.objects.filter(uid=user_id)
    sum=0
    for x in o:
        sum=sum+(x.qty*x.pid.price)
    content={}
    content['products']=o
    content['nitems']=len(o)
    content['total']=sum
    return render(request,'placeorder.html',content)
    # return HttpResponse("oid generated")

def makepayment(request):
    userid=request.user.id
    # print("heloooo",userid)
    client = razorpay.Client(auth=("rzp_test_qgLbJ7Y1aAU51U", "GXgOqIxPsffNa6UMJN1jMrZb"))
    o=Order.objects.filter(uid=userid)
    sum=0
    for x in o:
        sum=sum+(x.qty*x.pid.price)
    sum=sum*100  #conversion of Rs into Paise
    oid=str(o[0].id)
    data = { "amount": sum, "currency": "INR", "receipt": oid}
    payment = client.order.create(data=data)
    print(payment)
    content={}
    content['payment']=payment
    return render(request,'pay.html',content)
    # return HttpResponse("oid generated")


def storedetails(request):
    pay_id=request.GET['pid']
    order_id=request.GET['oid']
    sign=request.GET['sign']
    userid=request.user.id
    u=User.objects.filter(id=userid)
    # print(u[0])
    # print(u[0].email)
    # print(pay_id)
    # print(order_id)
    # print(sign)
    email=u[0].email
    msg="Order Placed Successfully. Details are Payement Id: "+pay_id+" and Order Id is"+order_id
    send_mail(
        "Order Status-Ekart",
        msg,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    
    oh=OrderHistory.objects.create(order_id=order_id,pay_id=pay_id,sign=sign,uid=u[0])

    return render(request,'final.html')

def product(request):
    p=Product.objects.filter(status=1)
    content={}
    content['products']=p
    return render(request,"products.html",content)

def sort(request,sv):
    if sv=='0':
        param='price' #column name price
    else:
        param='-price'

    data=Product.objects.order_by(param).filter(status=1)
    content={}
    content['products']=data
    return render(request,'products.html',content)

def catfilter(request,catv):
    if catv=='0':
        data=Product.objects.all()
    else:

        q1=Q(cat=catv)
        q2=Q(status=1)
        data=Product.objects.filter(q1 & q2)
    content={}
    content['products']=data
    return render(request,'products.html',content)

def pricefilter(request,pv):
    q1=Q(status=1)
    
    if pv=='0':
        q2=Q(price__lt=5000)
    else:
        q2=Q(price__gte=5000)
    
    data=Product.objects.filter(q1 & q2)
    content={}
    content['products']=data
    return render(request,'products.html',content)

def pricerange(request):
    
    low=request.GET['min']
    high=request.GET['max']
    # print(low)
    # print(high)
    #select * from ecommapp_product where price>=low and price<=high and status=1;
    q1=Q(status=1)
    q2=Q(price__gte=low)
    q3=Q(price__lte=high)
    data=Product.objects.filter(q1 & q2 & q3)
    content={}
    content['products']=data
    return render(request,'products.html',content)

def contact(request):
    if request.method=='POST':
        n=request.POST['uname']
        e=request.POST['umail']
        m=request.POST['umob']
        msg=request.POST['msg']
   
        print(n)
        print(e)
        print(m)
        print(msg)
        data=Contact.objects.create(name=n,email=e,mobile=m,message=msg)
        data.save()

        return render(request,'contact.html')
    else:
      return render(request,'contact.html')