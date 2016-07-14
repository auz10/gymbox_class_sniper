import time
from splinter import Browser
from datetime import datetime
from threading import Timer



current_time = datetime.today()
booking_time = current_time.replace(day=current_time.day,
						   hour=7,
						   minute=1,
						   second=0,
						   microsecond=0)
delta_t = booking_time - current_time
secs = delta_t.seconds + 1

browser = Browser("chrome")#("phantomjs") run in browser or headless
username = ''#USER_NAME
password = ''#PASS_WORD

class Day(object):
	def __init__(self, day):
		self.day = day
		self.classes = []

	def add_day(self, day):
		self.day = day

	def add_class(self, each_class):
		self.classes.append(each_class)

print "Visiting: https://gymbox.legendonlineservices.co.uk/enterprise/account/Login"
browser.visit("https://gymbox.legendonlineservices.co.uk/enterprise/account/Login")
print "\tSuccess"

# LOGIN #
print "Logging In.."
browser.find_by_id("login_Email").fill(username)
browser.find_by_id("login_Password").fill(password)
browser.find_by_id("login").click()
print "\tSuccess"

# NAVIGATE TO CLASSES #
print "Navigating to: /enterprise/BookingsCentre/MemberTimetable"
browser.click_link_by_href("/enterprise/BookingsCentre/MemberTimetable")
print "\tSuccess"

# CREATE LIST OF OBJECTS CONTAINING DAYS AND CLASSES #
print "Building Classes Timetable.."
list_of_days = []
for each_row in browser.find_by_id("MemberTimetable").find_by_tag("tr"):
	each_class = {}
	if each_row.has_class("dayHeader"):
		day_obj = Day(each_row)
	else:
		day_obj.add_class(each_row)
	if day_obj not in list_of_days:
		list_of_days.append(day_obj)

print "\tSuccess\n"

# PRINT LIST OF CLASSES FOR SELECTED DAY #
print list_of_days[1].day.text
for index, each_class in enumerate(list_of_days[1].classes):
	print str(index)+": "+each_class.text

class_choice = raw_input("Choose a class number: ")
print "Waiting until: "+str(booking_time)

def makeBooking():
	list_of_days[1].classes[int(class_choice)].find_by_tag("td")[6].click()
	print "\nRedirected to basket.."
	browser.find_by_id("btnPayNow").click()
	print "Booking complete!"


t = Timer(secs, makeBooking)
t.start()
