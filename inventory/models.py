from django.db import models
from django.utils.text import slugify

#მოკლედ ეს დაგვჭირდა იმიტომ რომ მინიმალური ფასის რაოდენობა მიგვეთითებინა
from decimal import Decimal
from django.core.validators import MinValueValidator

#ეს არის ტექსტის თარგმნისთვის
from django.utils.translation import gettext_lazy as _

#კაროჩე ვიცი ეს რაც არის რა
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import User, AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Costumer(AbstractUser):
    name = models.CharField(max_length=25, null=True)
    email = models.EmailField(null=True, unique=True)

    # ანუ იუზერნეიმ ფიელდ იქნება ემაილი ეხლა
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = self.email  # Set username to email for compatibility
    
    def save(self, *args, **kwargs):
        self.username = self.email  # Ensure username stays synced with email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class Category(MPTTModel):
    name = models.CharField(
        max_length=100,
    )
    slug = models.SlugField(max_length=150, unique=True)
    is_active = models.BooleanField(
        default=False,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
    )

    #ეს ნიშნავს რომ როდესაც რომელიმე მშობელ ელემენტს მიეცემა შვილი ელემენტი მათი ორდერი იქნება სახელით
    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    web_id = models.CharField(
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
    )
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        related_name="product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.name


#ფერი ზომა და ასშ...
class ProductAttribute(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    
    #ატრიბუტები რაც ამ ტიპთან არის დაკავშირებული
    product_type_attributes = models.ManyToManyField(
        ProductAttribute,
        related_name="product_type_attributes",
        through="ProductTypeAttribute",
    )

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    #ვაკავშირებთ ატრიბუტთან რათა შემდეგ ამ ატრიბუტს დავუწეროთ მნიშვნელობა მაგ: წითელი, XL და ასშ...
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="product_attribute",
        on_delete=models.PROTECT,
    )
    attribute_value = models.CharField(
        max_length=255,
    )


class ProductInventory(models.Model):
    sku = models.CharField(
        max_length=20,
        unique=True,
    )
    #ეს არის უნიკალური იდენთიფიკატორი
    upc = models.CharField(
        max_length=12,
        unique=True,
    )
    product_type = models.ForeignKey(ProductType, related_name="product_type", on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name="product", on_delete=models.PROTECT)
    brand = models.ForeignKey(
        Brand,
        related_name="brand",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="product_attribute_values",
        through="ProductAttributeValues",
    )
    is_active = models.BooleanField(
        default=False,
    )
    is_default = models.BooleanField(
        default=False,
    )
    #როცა იქნება დისქოუნთი უნდა გამოვაჩინო სთოურ ფრაისი და რითეილ ფრაისი სხვა ფრად ან გადახაზულად ანუ სთოურ ფრაისი არის დისქოუნთი და ის მთავარი ფასი
    retail_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    store_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    weight = models.FloatField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.sku


class Media(models.Model):
    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.PROTECT,
        related_name="media",
    )
    img_url = models.ImageField(upload_to="static/images", null=True, blank=True, default='No image.svg')
    alt_text = models.CharField(
        max_length=255,
    )
    #ანუ რომელიც უნდა გამოჩნდეს დიფოულტათ
    is_feature = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )


class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name="product_inventory",
        on_delete=models.PROTECT,
    )
    last_checked = models.DateTimeField(
        null=True,
        blank=True,
    )
    units = models.IntegerField(
        default=0,
    )
    units_sold = models.IntegerField(
        default=0,
    )

    def __str__(self):
        return str(self.product_inventory.sku)

#ეს არის through მოდელი
#ვაკავშირებთ პროდუქტ ინვენტორის და მნიშვნელობებს ასევე ამ მნიშვნელობებიდან შეგვიძლია მივწვდეთ ატრიბუტებს და ასშ...
class ProductAttributeValues(models.Model):
    attributevalues = models.ForeignKey(
        "ProductAttributeValue",
        related_name="attributevaluess",
        on_delete=models.PROTECT,
    )
    productinventory = models.ForeignKey(
        ProductInventory,
        related_name="productattributevaluess",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (("attributevalues", "productinventory"),)


#ეს არის through მოდელი
#ვაკავშირებთ პროდუქტ ტიპს და ატრიბუტებს
#product_type ამით მოკლედ დავაკავშირებთ პროდუქტ ინვენტორს პროდუქტის ტიპთან და შემდეგ ამ ტიპს ხო აქ კავშირი ატრიბუტებთან და ასე შევადგინეთ კავშირი
class ProductTypeAttribute(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="productattribute",
        on_delete=models.PROTECT,
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name="producttype",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (("product_attribute", "product_type"),)


class Order(models.Model):
    costumer = models.ForeignKey(Costumer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False) #ეს ცვლის ჩვენი cartის სტატუს ამას მერე თუ გავიგებ კარგად შევცვლი|ჩვენი ორდერი complete არის თუ არა

    #ეს ასერომვთქვათ არის ანუ როდესაც იუზერი შეიძენს რამეს მაგისი უნიკალური იდენთიფიკატორი
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_all_total(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total
    
    @property
    def get_all_items(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product.product.name)

    @property
    def get_total(self):
        total = self.product.retail_price * self.quantity
        return total


class ShippingAddress(models.Model):
    costumer = models.ForeignKey(Costumer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=500, null=True)
    Postal_code = models.CharField(max_length=30, null=True)
    phone_number = PhoneNumberField(region="GE")
    email = models.EmailField(null=True)

    def __str__(self):
        return self.address