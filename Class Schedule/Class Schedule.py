import json
import re
import math
from datetime import date,datetime,time,timedelta

user_information = {
    "blueLunch": "B",
    "goldLunch": "D",
    "cohort": "greyhound",
    "blueday_classes": {
        "Block 1": "AP World History",
        "Block 2": "Spanish II",
        "Block 3": "Honors Algebra 2",
        "Block 4": "Honors ELA"
    },
    "goldday_classes": {
        "Block 1": "Honors Biology",
        "Block 2": "SSRT",
        "Block 3": "Counterpoints",
        "Block 4": "Health and Wellness Education"
    }
}

now = datetime.now()

with open("/Users/davidracovan/Documents/VS Code/Class Schedule/schoolInfo.json") as school_info_json:
    school_info_dict = json.load(school_info_json)

# setting values
current_day = school_info_dict["days"][user_information["cohort"]][now.strftime("%m/%d/%Y")]
if("Late" in current_day):
    day_type = "late"
elif(re.search("(Blue|Gold)",current_day)):
    day_type = "normal"
else:
    day_type = "none"

if(day_type != "none"):
    day_lunch = re.search("(Blue|Gold)",current_day).group().lower() + "Lunch"
    day_classes = user_information[re.search("(Blue|Gold)",current_day).group().lower() + "day_classes"]
    current_class_dict = school_info_dict["currentClass"][day_type][user_information[day_lunch]]
    overview_dict = school_info_dict["overview"][day_type][user_information[day_lunch]]
else:
    day_lunch = ""
    day_classes = ""
    current_class_dict = ""
    overview_dict = ""

# date
date_result = "Date\n"
date_result += "Today is %s (%s)." % (now.strftime("%A, %B %d, %Y"), current_day)

# currentClass
current_class_result = "Current Class\n"
day_overview_raw_blocks = [""]
day_status = ""
if(day_type != "none"):
    for item in sorted(current_class_dict.keys()):
        if(not current_class_result):
            formatted_item = datetime.combine(now,datetime.strptime(item,"%H:%M").time())
            time_between_dates = formatted_item - now
            if(time_between_dates > timedelta()): # if time_between_dates is greater than zero
                new_item = datetime.strptime(item,"%H:%M").strftime("%I:%M %p")
                current_class_result += "%s%s minute(s) (%s)." % (current_class_dict[formatted_item.strftime("%H:%M")],
                math.ceil(time_between_dates.seconds/60),new_item)
        elif(current_class_result):
            day_overview_raw_blocks.append(overview_dict[item])
    if(not current_class_result):
        time_between_dates = datetime.strptime("15:45","%H:%M") - now
        current_class_result += "Block 4 ended %s minutes ago (3:45 PM)." % (time_between_dates)
        day_status = "finished"
else:
    current_class_result += "There is no school today."

if(day_type != "none"): # replace block name
    if(""):
        current_class_result = re.sub("(Block\s[0-9])",day_classes[re.search("(Block\s[0-9])",current_class_result).group()],current_class_result)

# dayOverview
day_overview_result = "Day Overview\n"
if(re.search("(3:45)",current_class_result)):
    day_overview_result += "There are no more classes today."
elif(re.search("(today)",current_class_result)):
    day_overview_result += "There are no classes today."
elif(not re.search("(3:45|today)",current_class_result)):
    for item in day_overview_raw_blocks:
        if ("Lunch" not in item and ""):
            item = re.sub("Block\s[0-9]",day_classes[re.search("(Block\s[0-9])",item).group()],item)

# weekOverview
week_overview_result = "Week Overview"
for i in range (7):
    week_overview_result += ("\n" + (now + timedelta(days = i + 1)).strftime("%a, %b %d, %Y: ")
    + school_info_dict["days"][user_information["cohort"]][(now + timedelta(days = i + 1)).strftime("%m/%d/%Y")])

# finalResult
final_result = date_result + "\n\n" + current_class_result + "\n\n" + day_overview_result + "\n\n" + week_overview_result
print(final_result)

final_result_file = open("/Applications/AppleScriptTemp/ClassScheduleResult.txt","w")
final_result_file.write(final_result)
final_result_file.close()