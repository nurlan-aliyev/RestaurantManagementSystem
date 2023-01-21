
# RMS V0.1.1
## Restaurant Management System 

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
   
- Here are the results of error handling:

1. Table Number validation is handled as you type, when it exceeds maximum allowed amount the window below will show error (you can't enter anything other than digits) 

   ![Error handling 1](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/90e3e465fe90150ea18a93059e357fc1d3201823/assets/bast/config_m_tval.png)
   
   2. Seat Number exceeds maximum allowed (working principle is the same as table validation)
 
   ![Error hanling 2](https://github.com/nurlan-aliyev/RMSV0.1.1/blob/90e3e465fe90150ea18a93059e357fc1d3201823/assets/bast/config_m_sval.png)

