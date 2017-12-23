## Anomaly Detecton in Stock Trading

Stock manipulation is one of the major problems in stock market. 
These manipulations can be categorized with respect
to data under two categories. They are structured data manipulation and unstructured data
manipulation. Changing the stock market behavior because of a twitter message can be given as
an example for unstructured data manipulation. Apart from that traders are doing many
disruptive trading in stock market using structured data. Pump and dump, insider trading,
Momentum Ignition and Spoofing Corner are some examples. These names have originated
from the starting behavior of each manipulation.

### Goal

Automatically detect and analyze fraudulent behaviors in stock trading
The proposed solution satisfies the desirable properties for Momentum Ignition manipulation
pattern in stock trading. Solution consists with mainly three ways to detect the manipulated time
frames in stock trading. They are two machine learning approaches and one visualization approach.
It is easy to integrate new modules to the project and develop for future perspectives to detect more
manipulated patterns in stock trading.

### Contribution

Contribution for this project can be included as below.
1. Preprocessed data and extracted relevant features.
2. Used unsupervised machine learning models to detect manipulated time/order frames.
3. Orderbook simulation to visualize how stock market behaves in a particular frame.
4. Visualization based techniques.

Our approach is an automated system which only rely on stock market end of the day data. Data
will be fetched into different machine learning techniques and identify which are the time frames
with manipulative behavior. Apart from that, this tool supports visualization techniques to further
analyze and identify whether the given frame can be a fraudulent time frame or not.

### Installation
This project uses a Python server and an AngularJS client. The server code is in the /app directory.
The client code is in the /web directory.

##### Setup MySQL database
Make sure to import adist.sql(Final_Year_Project/adist.sql) database to MySQL server.

##### Running from console
1. Run command `SET FLASK_APP=fyp_flask_main.py`
2. Run command `SET FLASK_DEBUG=1`
3. Run command `python -m flask run`
4. Navigate to /web directory and run command `http-server -u localhost -p 8000`

##### Running from Jetbrains PyCharm
1. Run file `fyp_flask_main.py`
2. Navigate to the /web directory using the IDE's terminal and run command `http-server -u localhost -p 8000`

Make sure you have all the necessary imported dependencies and `bower install` run before proceeding.
Also you'll have to install `http-server` by `npm`.

### Members
Supun Arunoda  
Buddhi Vikasitha  
Hishara Yasas  
Nilanga Virajith  

Supervisor - Dr. Dilum Bandara

Department of Computer Science & Engineering, University of Moratuwa