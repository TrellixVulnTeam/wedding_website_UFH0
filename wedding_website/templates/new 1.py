import datetime
stop = False
while stop == False:
	disp.reset()
	list_select = disp.newlistselect(["Past Week Ending Today", "Past Month Ending Today", "Custom Date Range"], False)
	list_select.text = "Choose a report or make a custom date range below."
	list_select.row = 0
	disp.addcntrl(list_select)
	disp.addbtn(0, "OK")

	disp.popup(True, "Choose a report date period.", 500, 400, 500, 350)
	
	if list_select.value == "":
		disp.message("You must pick one of the three options.")
		disp.reset()
		continue
	elif list_select.value == "Past Week Ending Today":
		period_string = "4161|0|20100101000000000|20161229235959999"
		period_string = '16'
		a_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
		sql1 = "select rtrim(udl1), rtrim(udl4), rtrim(partno) from " + sql.tables.vdata + " where datetime > '" + str(hsidate.format_to_db(str(a_week_ago))) + "' and partno like '%weight%' group by udl1, udl4, partno order by udl1, udl4, partno"
		plp = sql.gettable(sql1)
		try:
			plp[0][1]
			stop = True
			today = datetime.datetime.now()
			start_date = '{:0>2}'.format(a_week_ago.month) + "/" + '{:0>2}'.format(a_week_ago.day) + "/" + str(a_week_ago.year)
			end_date = '{:0>2}'.format(today.month) + "/" + '{:0>2}'.format(today.day) + "/" + str(today.year)
		except:
			disp.message("No data found for the date period selected.")
			continue
	elif list_select.value == "Past Month Ending Today":
		period_string = "4162|0|20100101000000000|20161229235959999"
		period_string = '17'
		a_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
		sql1 = "select rtrim(udl1), rtrim(udl4), rtrim(partno) from " + sql.tables.vdata + " where datetime > '" + str(hsidate.format_to_db(str(a_month_ago))) + "' and partno like '%weight%' group by udl1, udl4, partno order by udl1, udl4, partno"
		plp = sql.gettable(sql1)
		try:
			plp[0][1]
			stop = True
			today = datetime.datetime.now()
			start_date = '{:0>2}'.format(a_month_ago.month) + "/" + '{:0>2}'.format(a_month_ago.day) + "/" + str(a_month_ago.year)
			end_date = '{:0>2}'.format(today.month) + "/" + '{:0>2}'.format(today.day) + "/" + str(today.year)
		except:
			disp.message("No data found for the date period selected.")
			continue
	else:
		disp.reset()
		date_start = disp.newdatepicker("MM/dd/yyyy")
		date_start.text = "Custom Start Date"
		date_start.row = 0
		date_start.value = ""
		disp.addcntrl(date_start)

		date_end = disp.newdatepicker("MM/dd/yyyy")
		date_end.text = "Custom End Date"
		date_end.row = 1
		disp.addcntrl(date_end)
		disp.addbtn(0, "OK")

		disp.popup(True, "Choose a report date period.", 500, 400, 500, 350)

		print "Date Start: " + str(date_start.value) + " Date End: " + str(date_end.value)
		print "Formatted: " + str(hsidate.format_to_db(str(date_start.value).replace("/", "-"))) + " Formatted: " + str(hsidate.format_to_db(str(date_end.value).replace("/", "-")))
		
		start_date = str(date_start.value)
		end_date = str(date_end.value)
		start_date_long = hsidate.format_to_db(str(date_start.value).replace("/", "-"))
		end_date_long = hsidate.format_to_db(str(date_end.value).replace("/", "-"))
		if start_date_long == -1 or end_date_long == -1:
			disp.message("Please choose a correct date value.")
		elif start_date_long > end_date_long:
			disp.message("Please make sure start date is an older date than your end date.")
		else:
			period_string = "12288|0|" + str(start_date_long) + "|" + str(end_date_long)[:-9] + "235959000"
			sql1 = "select rtrim(udl1), rtrim(udl4), rtrim(partno) from " + sql.tables.vdata + " where datetime > '" + str(start_date_long) + "' and datetime < '" + str(end_date_long)[:-9] + "235959000" + "' and partno like '%weight%' group by udl1, udl4, partno order by udl1, udl4, partno"
			plp = sql.gettable(sql1)
			try:
				plp[0][1]
				stop = True
			except:
				disp.message("No data found for the date period selected.")
				continue




#read filter
#filter_name = sql.gettable("select * from " + sql.tables.filterspc + " where name='ccc plant line DO NOT EDIT'")[0][1]
filter_name = sql.gettable("select * from " + "FILTER" + " where name='Plant and Line DO NOT EDIT'")[0][1]
full_filter_name = file.getpath(1) + filter_name + ".vf"


#Perform SQL Query
#sql1 = "select rtrim(udl1), rtrim(udl4), rtrim(partno) from " + sql.tables.vdata + " where datetime > '" + db_a_week_ago + "' group by udl1, udl4, partno order by udl1, udl4, partno"
#plp = sql.gettable(sql1)
#TO DO: modify the query
#End SQL Query
data_dict = {}

for x in range(0, len(plp)):
	#print plp[x]
	index = plp[x][0] + plp[x][1]
	data_dict[index] = [0, 0, 0, 0, 0.]

#grab stats for each combination
#once for prev week, once for prev month

	
#Setup retrieval
#retrspc.partno = "12-35001-Hold Time"
#retrspc.count = 1000
#retrspc.periodstr = '4161|0|20100101000000000|20161229235959999' #previous week
#retrspc.periodstr = '4162|0|20100101000000000|20161229235959999' #previous month
#retrspc.filter = "ccc plant line DO NOT EDIT"  
retrspc.count = 5000 #we think the max would be around 800 for a month

for x in range(0, len(plp)):
	retrspc.filter = ""
	retrspc.partno = plp[x][2]
	retrspc.periodstr = period_string
	filter_contents = "1000|-|EQ|-|" + plp[x][0] + "|-|AND|-|\r\n1003|-|EQ|-|" + plp[x][1] + "|-|AND|-|\r\n0|-|CO|-|weight|-|NONE|-|\r\n"		#TO DO: update the traceability references (1002 = udl3)
	file.text.write(full_filter_name, filter_contents, False)
	retrspc.filter = "Plant and Line DO NOT EDIT"
	
	pp = statspc.getstat(126) 	#Pp
	index = plp[x][0] + plp[x][1]
	if pp == None:
		print "Line: " + plp[x][1] + "  PartNo: " + plp[x][2] + "  Pp: " + str(pp)
		data_dict[index][0] += 1
	elif pp < 1.0:
		data_dict[index][1] += 1
	else:
		data_dict[index][2] += 1

	
#check pp for each standard and compile them into buckets

#loop through dict and write out the bucket values

prev_plant = plp[0][0]
prev_index = "xxx"
na_count = 0
pp_bad = 0
pp_good = 0
gt_na = 0
gt_bad = 0
gt_good = 0

#master_table = []
master_line_list = []
master_list = []

for x in range(0, len(plp)):
	index = plp[x][0] + plp[x][1]
	if prev_index != index:
		if prev_plant != plp[x][0]:
			sub_total = pp_bad + pp_good
			if sub_total == 0:
				master_line_list.append(["Grand Total", str(na_count), str(pp_bad), str(pp_good), str(sub_total), 0.0])
				master_list.append([prev_plant, str(na_count), str(pp_bad), str(pp_good), str(sub_total), 0.0])
			else:
				master_line_list.append(["Grand Total", str(na_count), str(pp_bad), str(pp_good), str(sub_total), float("{0:.1f}".format(float(pp_good) / float(sub_total) * 100.0))])
				master_list.append([prev_plant, str(na_count), str(pp_bad), str(pp_good), str(sub_total), float("{0:.1f}".format(float(pp_good) / float(sub_total) * 100.0))])
			gt_na += na_count
			gt_bad += pp_bad
			gt_good += pp_good
			na_count = 0
			pp_bad = 0
			pp_good = 0
			prev_plant = plp[x][0]
		data_dict[index][3] = data_dict[index][1] + data_dict[index][2]
		try:
			data_dict[index][4] = "{0:.1f}".format(float(data_dict[index][2]) / float(data_dict[index][3]) * 100.0)
		except:
			data_dict[index][4] = 0.0
		na_count += data_dict[index][0]
		pp_bad += data_dict[index][1]
		pp_good += data_dict[index][2]
		disp_index = plp[x][1]
		#print disp_index + "\t" + str(data_dict[index][0]) + "\t" + str(data_dict[index][1]) + "\t" + str(data_dict[index][2]) + "\t" + str(data_dict[index][3]) + "\t" + str(data_dict[index][4])
		master_line_list.append([disp_index, str(data_dict[index][0]), str(data_dict[index][1]), str(data_dict[index][2]), str(data_dict[index][3]), float(data_dict[index][4])])
		prev_index = index
		
sub_total = pp_bad + pp_good
if sub_total == 0:
	master_line_list.append(["Grand Total", str(na_count), str(pp_bad), str(pp_good), str(sub_total), 0.0])
	master_list.append([prev_plant, str(na_count), str(pp_bad), str(pp_good), str(sub_total), 0.0])
else:
	master_line_list.append(["Grand Total", str(na_count), str(pp_bad), str(pp_good), str(sub_total), float("{0:.1f}".format(float(pp_good) / float(sub_total) * 100.0))])
	master_list.append([prev_plant, str(na_count), str(pp_bad), str(pp_good), str(sub_total), float("{0:.1f}".format(float(pp_good) / float(sub_total) * 100.0))])
gt_na += na_count
gt_bad += pp_bad
gt_good += pp_good
gt_sub_total = gt_bad + gt_good
#st = str(gt_na) + "\t" + str(gt_bad) + "\t" + str(gt_good) + "\t" + str(gt_sub_total) + "\t" + str("{0:.1f}".format(float(gt_good) / float(gt_sub_total) * 100.0))
#master_table.append("Grand Total\t" + st)
if gt_sub_total == 0:
	master_list.append(["Grand Total", str(gt_na), str(gt_bad), str(gt_good), str(gt_sub_total), 0.0])
else:
	master_list.append(["Grand Total", str(gt_na), str(gt_bad), str(gt_good), str(gt_sub_total), float("{0:.1f}".format(float(gt_good) / float(gt_sub_total) * 100.0))])

master_line_list = sorted(master_line_list[:-1], key=lambda sort: sort[5], reverse=True) + master_line_list[-1:]
header_list = ["Row Labels", "NA", "No", "Yes", "Grand Total", "% Items Pp > 1.0"]
google_list = [['Plant', '% Items Pp > 1.0']]

for x in range(0, len(master_line_list)):
	google_list.append([master_line_list[x][0], float(master_line_list[x][5])])


html = """<html><head>
    <!--Load the AJAX API-->
	<script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">

      // Load the Visualization API and the corechart package.
      google.load('visualization', '1', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table,
      // instantiates the bar chart, passes in the data and
      // draws it.
      function drawChart() {

        // Create the data table.
        var data = new google.visualization.arrayToDataTable(""" + str(google_list) + """);

        // Set chart options
        var options = {'title':'% Items / Lines Capable'};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>

  <body>
   <table><tr><td colspan="2" align="center" bgcolor = "\#ADD8E6">Plant: """ + plp[0][0] + """&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Line Capability Data From:&nbsp;&nbsp;""" + start_date + "   -   " + end_date + """</td></tr><tr><td>
    <table rules="all"><tr bgcolor = "\#ADD8E6">"""
for x in header_list:
	html += "<td>" + x + "</td>"
html += "</tr>"
for x in range(0, len(master_line_list)):
	html += "<tr>"
	for y in range(0, len(master_line_list[x])):
		html += "<td>" + str(master_line_list[x][y]) + "</td>"
	html += "</tr>"
#html += "</table><br /><br /><table><tr bgcolor = '\#ADD8E6'>"
#for x in header_list:
#	html += "<td>" + x + "</td>"
#html += "</tr>"
#for x in range(0, len(master_list)):
#	html += "<tr>"
#	for y in range(0, len(master_list[x])):
#		html += "<td>" + str(master_list[x][y]) + "</td>"
#	html += "</tr>"
html += """</table></td><td valign="top">
	<!--Div that will hold the bar chart-->
    <div id="chart_div" style="width: 900px; height: 800px;"></div>
    </td></table></body></html>"""

disp.reset()
display = disp.newbrowser()
file = open("\\\\entvgsapp01\\GSAPP\\Data\\Data001\\line_capability_plant.html", 'w')
file.write(html)
file.close()
display.url = "\\\\entvgsapp01\\GSAPP\\Data\\Data001\\line_capability_plant.html"
disp.addcntrl(display)
disp.show()