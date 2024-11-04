from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, user_name, password):
        if not user_name:
            raise ValueError('user name is required')
        if not password:
            raise ValueError('password is required')
        
        user = self.model(user_name=user_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,user_name,password,**kwargs):
        user = self.create_user(
            user_name ,password
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user



class CoreUser(AbstractBaseUser,PermissionsMixin):
        user_id = models.AutoField(primary_key=True)
        user_name = models.CharField(max_length=255,unique=True)
        is_admin=models.BooleanField(default=False)
        is_staff=models.BooleanField(default=False)
        role = models.ForeignKey('Role',on_delete=models.SET_NULL,null=True)
        # role = models.ForeignKey('Role',on_delete=models.SET_NULL,related_name='user_role',null=True)

        USERNAME_FIELD = 'user_name'
        objects = UserManager() 
        DisplayField = ['user_id','user_name','is_admin','is_staff','role']
        
        class Meta: 
            db_table = 'core_user'
            
        def __str__(self):
            return self.user_name
        
        
class Role(models.Model):
    role_id=models.AutoField(primary_key=True)
    role_type=models.CharField(max_length=255)
    
    DisplayField = ['role_id','role_type']
    
    def __str__(self):
        return self.role_type
    
    class Meta:
        db_table = 'role'
        

class CompanyDetails(models.Model):
    company_details_id = models.AutoField(primary_key=True)
    user_id =models.ForeignKey(CoreUser,on_delete=models.CASCADE,related_name='company_user')
    company_name = models.CharField(max_length=155)
    company_contact =PhoneNumberField(unique=True)
    company_email = models.EmailField(unique=True)
    h_no = models.CharField(max_length=155)
    area = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    city = models.CharField(max_length=55)
    pincode = models.CharField(max_length=55)
    state = models.CharField(max_length=155)
    country = models.CharField(max_length=155)
    # address_id = models.ForeignKey('Address',on_delete=models.CASCADE,related_name='address_detail')
    bank_name=models.CharField(max_length=155)
    branch_name=models.CharField(max_length=155)
    account_number=models.CharField(max_length=155)
    ifsc_code=models.CharField(max_length=155)
    gst_in=models.CharField(max_length=155)
    inv_num_format = models.CharField(max_length=30)
    company_logo=models.ImageField(upload_to='CompanyLogo/')
    digital_seal=models.ImageField(upload_to='CompanyLogo/')
    digital_signature=models.ImageField(upload_to='CompanyLogo/')
    show_bank_data = models.BooleanField(null=False)
    
    
    DisplayField = ['company_details_id','company_name','company_contact','h_no','area','landmark','city','pincode','state','country','bank_name','show_bank_data']
    
    def __str__(self):
        return self.company_name
    class Meta:
        db_table='company_details'
                
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    h_no = models.CharField(max_length=155)
    area = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    city = models.CharField(max_length=55)
    pincode = models.CharField(max_length=55)
    state = models.CharField(max_length=155)
    country = models.CharField(max_length=155)
    # address_id = models.ForeignKey('Address',on_delete=models.CASCADE,related_name='address_details')
    email = models.EmailField(unique=True)
    phone =PhoneNumberField(unique=True)
    
    DisplayField = ['customer_id','customer_name','email','phone','h_no','area','landmark','city','pincode','state','country']
    
    def __str__(self):
        return self.customer_name    
    
    class Meta:
        db_table = 'customer'



class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10,decimal_places=3)
    stock_quantity = models.IntegerField()
    
    DisplayField = ['product_id','product_name','description','stock_quantity']

    def __str__(self):
        return self.product_name
    
    class Meta:
        db_table = 'product'
        
class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    invoice_number=models.CharField(max_length=100,unique=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,related_name='client_invoice')
    generated_date = models.DateField()
    due_date = models.DateField() 
    tax = models.ManyToManyField('Tax')
    invoice_item_id = models.ManyToManyField("Invoice_item")
    tax_amount=models.DecimalField(max_digits=10,decimal_places=2)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,null=False)
    status = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='media/',default=True)

    

    DisplayField = ['invoice_id','customer','total_amount','tax_amount','status','generated_date','invoice_number','pdf']

    def __str__(self):
        return self.customer.customer_name   
    
    class Meta:
        db_table = 'invoice'        
        
class Invoice_item(models.Model):
    invoice_item_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    invoice_number = models.CharField(max_length=55)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    taxable_value = models.DecimalField(decimal_places=2,max_digits=10,null=True)
    calculated_amount = models.DecimalField(decimal_places=2,max_digits=10,null=True)
 

    DisplayField = ['invoice_item_id','product_id','invoice_number','quantity','unit_price','taxable_value','calculated_amount']
 

    def __str__(self):
        return self.invoice_number
    
    class Meta:
        db_table = 'invoice_item'        
        

        
                
class Tax(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_name = models.CharField(max_length=155)
    rate = models.DecimalField(decimal_places=2,max_digits=5)

    DisplayField = ['tax_id','tax_name','rate']

    def __str__(self):
        return f'{self.tax_name} - {self.rate}%'
    
    class Meta:
        db_table = 'tax'        
        
   
   
class Payment_method(models.Model):
    payment_method_id = models.AutoField(primary_key=True)
    payment_type = models.CharField(max_length=55)

    DisplayField = ['payment_method_id','payment_type']

    def __str__(self):
        return self.payment_type
    
    class Meta:
        db_table = 'payment_method'
        
                
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    invoice_id = models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True)
    method_id = models.ForeignKey(Payment_method,on_delete=models.CASCADE,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(blank=False)

    DisplayField = ['payment_id','invoice_id','method_id','amount','payment_date']

    # def __str__(self):
    #     return self.payment_id
    
    class Meta:
        db_table = 'payment'        





# class Address(models.Model):
#     address_id = models.AutoField(primary_key=True)
#     h_no = models.CharField(max_length=155)
#     area = models.CharField(max_length=255)
#     landmark = models.CharField(max_length=255)
#     city = models.CharField(max_length=55)
#     pincode = models.CharField(max_length=55)
#     state = models.CharField(max_length=155)
#     country = models.CharField(max_length=155)
    

#     DisplayField = ['address_id','h_no','area','landmark','city','pincode','state','country']

#     def __str__(self):
#         return self.h_no
    

#     class Meta:
#         db_table = 'address'