# eShop_management

## Introduction
This is an application of Super Shop Management System which have some basic functionalities as stated below:

### 1. Product Management:
The whole process to manage product is considered here. Product can be created, updated and deleted here.
### 2. Order Management
This is the main part of this project. The process to maintain order, add customer, manage item and lastly generate invoice with qr ocde and the pdf
also taken into consideration here. Item can also search through product_code or by selecting product_name through dropdown. Validation is also done 
if the product is out of stock.

### Below shows a higher level overview of database design

|    Orders     | order_product (AddItem) | products     |
|---------------|-------------------------|--------------|
| order_number  |         order(pk)       | product_code |
|customer_name  |        product(pk)      | product_name |
|phone_number   |        quantity         | category     |
|email          |        total_price      | unit_price   |
|confirm        |                         | quantity     |
|grand_total_price|                       | created_at   |
|created_at    |                          | updated_at   |
|updated_at    |                          |              |
|qr_code       |                          |              |

## Installation (Run the project locally)
1. Download or Clone the project from:
> git clone https://github.com/parves-ahmed/eShop_management.git
2. Go to project root:
> cd djangoProject
3. Create Virtual envvironment and activate it
4. Install all requirements from requirements.txt:
> pip install -r requirements.txt
5. Run the server
> python manage.py runserver
6. Result generates in:
> http://127.0.0.1:8000
