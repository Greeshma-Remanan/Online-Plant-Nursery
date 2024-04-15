from django.shortcuts import render,redirect
from django.views.generic import View,ListView,CreateView
from Store.models import Category,Product,Cart,Order
from Store.forms import Register,Login,OrderForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
#decorator 
from django.utils.decorators import method_decorator
# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            return redirect('login')
    return wrapper



class Home(ListView):
    model=Category
    template_name='Store\index.html'
    context_object_name='categories'


#Product View

class ProductView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Product.objects.filter(category_id=id)
        name=Category.objects.get(id=id)
        return render(request,'Store\category_details.html',{'data':data,'name':name})

   
    
  
        
#Product Details

class ProductDetail(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        p_data=Product.objects.filter(id=id)
        return render(request,'Store\Product_Details.html',{"p_data":p_data})   

#Register

class RegisterView(CreateView):
    template_name="Store/register.html"
    form_class=Register
    model=User
    success_url=reverse_lazy('login')

#login
class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=Login()
        return render(request,'Store\login.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form=Login(request.POST)
        print(request.user)
        if form.is_valid():
            print(form.cleaned_data)
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=u_name,password=pwd)
            if user_obj:
                print("valid crendential")
                login(request,user_obj)
                print(request.user)
                return redirect("home")
            else:
                print("invalid credentials")
        else:
            print("get out")
        return render(request,"Store/login.html",{"form":form})

#LOGOUT

class logoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('home')

#add to cart
@method_decorator(signin_required,name='dispatch')
class Addtocart(View):
   def get(self, request, *args, **kwargs):
        # Get the product ID from the URL parameters
        product_id = kwargs.get('pk')
        
        # Retrieve the product from the database
        product = Product.objects.get(id=product_id)
        
        # Get the quantity selected by the user (you might need to adjust this based on your HTML)
        quantity = int(request.GET.get('quantity', 1))  # Default to 1 if quantity is not provided
        
        # Calculate the total price based on the product's selling price and the quantity selected
        total_price = product.selling_price * quantity
        
        # Create a new Cart object with the selected product, user, quantity, and total price
        cart_item = Cart.objects.create(
            item=product,
            user=request.user,
            qty=quantity,
            price=total_price
        )
        
        # Redirect the user to the cart detail page or any other desired page
        return redirect('cart_detail')
  
#display all items that are present in the cart

@method_decorator(signin_required,name='dispatch')
class CartDetail(View):
    def get(self,request,*args,**kwargs):
        #data,pk are the default context name in django
        data=Cart.objects.filter(user=request.user)#request.user : means logged user
        return render(request,'Store/cart.html',{'data':data})


#delete item from cart
class CartDelete(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Cart.objects.get(id=id).delete()
        return redirect('cart_detail')

@method_decorator(signin_required,name='dispatch')
class OrderView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk") 
        product=Product.objects.get(id=id)  
        form=OrderForm()
        return render(request,'Store/order_page.html',{'form':form,"product":product})

    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        product=Product.objects.get(id=id)
        form=OrderForm(request.POST)
        if form.is_valid():
            address=form.cleaned_data.get('address')
            Order.objects.create(order_item=product,customer=request.user,address=address)
            return redirect('home')

        return redirect('cart')


#view order
class OrderListView(View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(customer=request.user)
        return render(request, 'Store/order_list.html', {'orders': orders})

#remove order //url id pass :remove

class remove_order(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Order.objects.get(id=id).delete()
        return render('cart')


#Search view

class SearchView(View):
    def get(Self,request,*args,**kwargs):
        query=request.GET.get('q')

        if query:
            results=Product.objects.filter(name__icontains=query) #icontains:case insencitive akkan
        else:
            results= None
        return render(request,'Store/search_results.html',{'results':results})