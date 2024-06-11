
# RMS V0.1.2
## Restaurant Management System 

 - [**Video Link**](https://youtu.be/JIb5oQDGY3c)


 - **General introduction**
	Restaurants nowadays require modern solutions to handle daily tasks, especially when it comes to order handling as book keeping is outdated for modern times, in which human fault might cost the facility lots of money. Restaurant Management System (will be referred as RMS from now on) offers following to tackle the problem:

	1. Store the configuration of the given restaurant and its menu to easily handle reservations and orders

	2. Create and store orders for the requested tables

	3. Generate and save bills when requested
	
 - **RMS Capabilities**

	• Storing the restaurant configuration: configure facility name, table/seat counts and menu with the ability to modify them in the future. Users will have the ability to modify the data through “Configure Facility/Menu” section of the app


 - Create bills for chef (backend): Application will first send the order to  kitchen for cooks to see, prepare and fulfil the order.
   
	❖ First stage of this process is confirmation of the order by the	customer,

	❖ second stage is informing the kitchen staff so they start the cooking process,

	❖ third stage is finishing the meals and getting fulfillment of the chef so customers can receive their orders

	❖ fourth stage is keeping the order active as long as customer requests for a final receipt

 - Create bills for customers (frontend): upon request program will
   generate a custom made, i.e., restaurant name  embedded
   receipt for customers. GUI will have a template for order creation
   with dropdown menus to get menu data from the database by the
   cashier. Upon fulfillment, orders will be stored in the database for
   further data analysis. 

3. **Technical side**

	Application will have Graphical User Interface using Python’s built-in module Tkinter. SQLite3 will be the database of choice; hence no active internet connection is required. Initial start will start with main window.Application doesn’t require third-party packages in order to run.


## Use of the application

Clone the repo to your local machine:
```
 git clone https://github.com/nurlan-aliyev/RestaurantManagementSystem.git
 cd RestaurantManagementSystem
```

Run pip install to get required packages:
```
 pip install
```

Run the command below to initialize the app:
```
 python BASE/Components/rms.py
```
1. **Initial run**

- When started Main Window will pop up. Through its filebar we can access all the necessary windows.

   ![Main Window](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/9617897106429e6d8a990bc693b6aae53da14bda/assets/bast/main_w.png)

- Filebar let's us see the current state of the application. At first as there is no database file we can only open up the "Configure Facility/Menu" window to store configurations.

   ![Filebar](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/9617897106429e6d8a990bc693b6aae53da14bda/assets/bast/main_w2.png)

2. **Configuration Window**

- In this window we can see the main configuration form to be filled. All of the Entry widgets have validation so, there is quite amount of error handling.

   ![Config Win](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/9617897106429e6d8a990bc693b6aae53da14bda/assets/bast/config_m.png)

- Below is the correct way of configuring the application. First, facility name, table (max. 50) and seat (max. 400) numbers should be filled and saved. Next up, filling name and price of the product and clicking "Add Product" button to store it. By this time there will be a database file created and data will be stored on-the-go. And if you want to change the menu item, you can either click "Remove" or press the "Delete" button AFTER selecting the menu item. 

   ![Config Win Filled](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/90e3e465fe90150ea18a93059e357fc1d3201823/assets/bast/config_m1.png)
   
- This window includes various validations as listed below:


  1. Table Number validation is handled as you type, when it exceeds maximum allowed amount the window below will show error (you can't enter anything other than digits) 

   ![Error handling 1](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/90e3e465fe90150ea18a93059e357fc1d3201823/assets/bast/config_m_tval.png)
   
  2. Seat Number exceeds maximum allowed (working principle is the same as table validation)
 
   ![Error hanling 2](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/90e3e465fe90150ea18a93059e357fc1d3201823/assets/bast/config_m_sval.png)
   
  3. Add button checks for the empty fields:
  
   ![Error handling 3](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/1619cdf36d6ff237ff3096204ff1ca49ba97a7b6/assets/bast/config_m_addval1.png)
   
  4. Add button validates product name length (max. allowed length 20) and price (max. allowed 10 mln Hungarian Forints and real numbers of type float)
  
   ![Error handling 4](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/9c9aadf0ffebf62bbab87761098e737cf5985cb9/assets/bast/config_m_addval2.png)
   
   
3. **Create Orders Window**

- As soon as the configuration menu closed and if there is configurations stored, a new window will be accessible through the main window

   ![New menu item](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/9c9aadf0ffebf62bbab87761098e737cf5985cb9/assets/bast/main_w3.png)
   
- In this new window we will be able to create orders and send them to the kitchen

   ![Create orders Window](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/8805825680f721421ff8bf78c126c0d1eda394ec/assets/bast/cr_order.png)
   
- The correct way of filling out the forms is as follows:

   ![Create orders window 1](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/aeecf17a0adf24a12c207e63d1caadf6ddef6ddb/assets/bast/cr_order_1.png)
 
- There is no limit on the number of products you can add to this list, and after getting orders and quantities, "Send to kitchen" button is activated, then the user is prompted to keep getting orders or return to the main window:

   ![Create orders Window 2](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/7db1237d70eb7b77a1f472a801d49e617d888ad3/assets/bast/cr_order_4.png)
   
- This window includes various validations as listed below:

1. Table number is not entered correctly or left empty:

   ![Error handling 3.1](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/bc84dbb167720ad86f33f6d6f0018669fd955200/assets/bast/cr_order_3.png)


2. There is at least one meal that is not selected, if this is the case, the items should all be deleted and started over (if you have better solutions please open up PR)

   ![Error handling 3.2](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/a5d64530f0c8826b5710586fa40068ff465d6fac/assets/bast/cr_order_2.png)
   
   
4. **Kitchen**

- As soon as the previous window closes and there are orders stored in the database, "Kitchen" will be activated in the filebar

   ![Kitchen](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/ff70c96437ccef07dc25a890ed5d5da437fceca1/assets/bast/main_w4.png)
   
- This window registers orders to a Notebook widget and lists the orders with quantities

   ![Kitchen 1](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/77ba876e30d319cb5b75780f81c03581539f99ec/assets/bast/ktc_1.png)
   
- In order to fulfil an order, the item has to be chosen, "Cook" button should be clicked and if and only if all of the items are cooked then "Fulfil order" button will be activated. When clicked on, this button will remove this order from "Orders" table and store it to "Cooked_Orders" table. It also deletes the current Notebook tab, hence if it's the only tab then the window is closed and "Kitchen" is deactivated until new orders are sent.


   ![Kitchen 2](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/77ba876e30d319cb5b75780f81c03581539f99ec/assets/bast/ktc_2.png)
   
  
5. **Print Orders Window**

- This window is activated right after an order is completed in the kitchen. Interface is similiar to "Create Orders" window.

   ![Print orders](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/d77e8ea3c7bad73077868eac0c59edecc09d9dd1/assets/bast/pr_or.png)
   
   
- After filling out the table number correctly the orders can be loaded via "Load orders" button. When the orders are listed the "Print receipt" button is activated

   ![Print orders 2](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/dca7e3b168afd01194382ca021b7fe56d97204ee/assets/bast/pr_or_2.png)
   
   
- The receipt is created based on a template HTML file and stored with the given table number as its file name. Right after storing the file is opened in the default browser where it can be printed

   ![Print orders 3](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/d90f8700d9687fdd1a07fd148429a3b00e44f987/assets/bast/pr_or_3.png)


- This window includes various validations as listed below:


1. Table number is not entered or entered incorrectly:

   ![Error handling 5.1](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/d90f8700d9687fdd1a07fd148429a3b00e44f987/assets/bast/pr_or_1.png)
   
   
2.  There is no any order made for the given table number (Warning message is used instead of Error):


   ![Warning 5.2](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/d90f8700d9687fdd1a07fd148429a3b00e44f987/assets/bast/pr_or_4.png)
   


6. **Conclusion**

- This app is made as the finals project for the Programming subject of the course of Msc. in Construction Information Technology Engineering during Dec 2022 - 2023 Jan.



Author: [Nurlan Aliyev](https://linktr.ee/nurlan_aliyev13)
   
   

