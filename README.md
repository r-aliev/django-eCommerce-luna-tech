# Luna Tech Co. eCommerce Website
  
  This is a fully functional eCommerce Website with guest checkout capability and payment integration. 
  
  **Note**: Luna Tech Co. is not a real company. Inspired from different ecommerce projects to design and built it.

  ### Website Features:
  
  - Unauthenticated users as authenticated users can perform a checkout. (used "Cookies" for storing unauthenticated users data)
  - User can perform payments using their [Paypal](https://www.paypal.com/) account or debit/credit card.
  - Users can add multiple products to cart, varying from physical to digital products.
  - Users can search for specific products by their names.
  - There is a pagination on the bottom of the store page. (Built by using Django Paginator Class)
    
  ### Demo

   Quick website demo as guest(unauthenticated) user.
  
   ![Website demo](demo-gif/ecom.gif)

 
    
  ### Technologies used in developement
   Back-end:
   - [Django](https://www.djangoproject.com/)
   - [Docker](https://www.docker.com/)
  
   Front-end:
   - HTML, JS, CSS and Bootstrap
   
   Payment:
    - [Paypal Developer](https://developer.paypal.com/) tools. (client side integration)
  
  
  ### Installation
  
   In order to run the application in local environment follow instructions below:
  
  ```bash
  # clone
  git clone https://github.com/r-aliev/django-ecommerce-luna-tech
  
  cd django-ecommerce-luna-tech
  
  docker build .
  
  docker-compose up

  ```
    Check your localhost on :8000 port
  
  ### Future improvements:
   - Add Login/Register Page
   - Add Home, Blog, Contact pages
   - Add a detail page for each product with description and reviews.
   - Send a success email to a client after a payment is done.
   - Prepare for deployment