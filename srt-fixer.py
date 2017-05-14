#**********************************************************************************************
#**********************************************************************************************
#********         1η Ε Ρ Γ Α Σ Ι Α  Σ Τ Ο Υ Σ  Μ Ε Τ Α Γ Λ Ω Τ Τ Ι Σ Τ Ε Σ           **********
#********                                                                            **********
#********         		12/5/2017  ΓΙΑΝΝΙΟΣ ΑΝΤΩΝΙΟΣ   ΑM:Π2013153           **********
#********                                                                            **********
#********                                                                            **********
#********                                                                            **********
#**********************************************************************************************
#********************************************************************************************** 

#beginning of code

#importing needed modules
import sys
import re
import argparse

#handling input arguments (.srt file and offset float number) with argparse module
parser = argparse.ArgumentParser()
parser.add_argument("fname",help = "input srt file name")
parser.add_argument("offset",type = float,help = "subtitle offset in seconds to apply (can be fractional)")
args = parser.parse_args()

#regular expression pattern for seeking time data, formed as (hour1:min1:sec1) --> (hour2:min2:sec2)
#first time data hour1:min1:sec1
#second time data hour2:min2:sec2
rexp = re.compile("(([0-9]{2}):([0-9]{2}):([0-9]{2},[0-9]{3})) --> (([0-9]{2}):([0-9]{2}):([0-9]{2},[0-9]{3}))") 

#regular expression pattern for seeking ',' and '.' 
rexp1 = re.compile(",")
rexp2 = re.compile("\.")

#function that reconstructs string back to two digits form
#receives an int or float number (string) and an int number (length) which 
#represents the length of the number
#function returns the reconstructed string as string in two digit form
def stringReconstruct(string,length):
	if len(string) == length:
				string = str(string)
				string = '0' + string
	else:
				string == str(string)
	return string


with open(args.fname,newline='') as ifp:	

	for line in ifp:

		#using finditer method	
		mi = rexp.finditer(line)

		for m in mi:

			#group(2) represents hour1
			#group(3) represents min1
			#group(4) represents sec1
			#totalsec1 represents total mseconds of first time data plus time offset 
			hour1 = int(m.group(2))
			min1 = int(m.group(3))
			
			#replacing ',' with '.' for converting string to float
			sec1 = float(rexp1.sub(".",m.group(4)))  
			
			#variable off as offset input argument
			off = args.offset

			#I multiplied each variable with 1000 for working with non float numbers, avoiding so, accuracy problems
			#before conversion and then added time offset to total seconds. Then I divided with 1000 again converting to msecs
			totalsec1 = (((hour1 * 3600) * 1000) + ((min1 * 60) * 1000) + (sec1 * 1000) + (off * 1000))
			hour1 = (totalsec1 - (totalsec1 % (3600 * 1000))) / (3600 * 1000)
			totalsec1 = (totalsec1 % (3600 * 1000))

			#computing again hour1, min1, sec1 after adding offset to total seconds
			min1 = (totalsec1 - (totalsec1 % (60 * 1000))) / (60 * 1000)
			totalsec1 = (totalsec1 % (60 * 1000))
			sec1 = totalsec1 / 1000

			#reconstructing back to two digits form strings
			hour1 = str(int(hour1))
			hour1 = stringReconstruct(hour1,1)

			min1 = str(int(min1))
			min1 = stringReconstruct(min1,1)
			
			sec1 = str(sec1)
			sec1 = stringReconstruct(sec1,5)

			#--------------------------------------------------------------------------------------------------------------------
			#doing exactly the same for second time data
			hour2 = int(m.group(6))
			min2 = int(m.group(7))
			
			sec2 = float(rexp1.sub(".",m.group(8)))  			
			
			totalsec2 = (((hour2 * 3600) * 1000) + ((min2 * 60) * 1000) + (sec2 * 1000) + (off * 1000)) 	
			hour2 = (totalsec2 - (totalsec2 % (3600 * 1000))) / (3600 * 1000) 			
			totalsec2 = (totalsec2 % (3600 * 1000))

			min2 = (totalsec2 - (totalsec2 % (60 * 1000))) / (60 * 1000) 
			totalsec2 = (totalsec2 % (60 * 1000))
			sec2 = totalsec2 / 1000
			
			hour2 = str(int(hour2))
			hour2 = stringReconstruct(hour2,1)

			min2 = str(int(min2))
			min2 = stringReconstruct(min2,1)
			
			sec2 = str(sec2)
			sec2 = stringReconstruct(sec2,5)
			#--------------------------------------------------------------------------------------------------------------------

			#replacing new time data to old time data in both of first and second time data
			line = line.replace(m.group(2),hour1)
			line = line.replace(m.group(3),min1)

			#replacing back '.' with ',' for converting seconds inside srt file in to their original form (having , instead of .)
			sec1 = rexp2.sub(",",sec1)
			line = line.replace(m.group(4),sec1)

			line = line.replace(m.group(6),hour2)
			line = line.replace(m.group(7),min2)

			#replacing back '.' with ',' for converting seconds inside srt file in to their original form (having , instead of .)
			sec2 = rexp2.sub(",",sec2)
			line = line.replace(m.group(8),sec2)

		#writing to stdout 
		sys.stdout.write(line)

#end of code

