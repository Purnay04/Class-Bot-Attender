# Google Meet Online Class Attender Bot
Specifically designed for Google Meet Platform. Just run the program on Cloud VM. Add the schedule &amp; put the program in execution stage. It will Notify you at every starting / Ending / No Class situation through a Discord Webhook.

# Installation 
1. Clone the repository `git clone https://github.com/Purnay087/Class-Bot-Attender.git`.
2. Install requirements using  `pip install -r requirements.txt`

# Configure

 1. Open `bot.py` and put your google login credentials in variables below to the comment line.
 2.  If you want to add some new details into schedule like `Teacher Name` etc then make sure you follow below points:  
   i. Insert Correct name in every `INSERT, CREATE, SELECT` Queries.   
   ii. Modify the `join_class` function with new changes & accept the new details in `modify_timetable` function.
 3. Open `attende_bot.py` and put the Discord Webhook Url in variable below to the comment line.
 4. If you want to add some fields into the message then use `add_field` function.
 
# Execution
Run the bot `python bot.py`

```
Note: 
This program require PC / Laptop in focused mode that means the window used by bot while
attending lecture should be at front 
