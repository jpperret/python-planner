from fpdf import FPDF
import calendar
import datetime

# https://pyfpdf.github.io/fpdf2/

pdf = FPDF(orientation="l")
pdf.set_margin(0)

YEAR = 2022
vertical_padding = 10
horizontal_padding = 10
indent_padding = 15
day_height = (pdf.h - vertical_padding * 2) / 4
day_horizontal_spacing = horizontal_padding
day_width = (pdf.w - horizontal_padding * 2 - day_horizontal_spacing) / 2
rows_per_day = 7
row_spacing = day_height / (rows_per_day + 1)
links = dict()
# Each month has enough days to fill out every week, when the month ends midweek this means the week is in the ending
# month and starting month
# There is probably a better way to get all the dates for a given year
dates_with_dup = [i for m in range(1, 13) for i in calendar.Calendar(firstweekday=0).itermonthdates(YEAR, m)]
dates = []
page = 0
for date in dates_with_dup:
	if date not in dates:
		dates.append(date)
date_iter = iter(dates)

pdf.add_page()
page += 1
pdf.set_font('helvetica', 'B', 25)
pdf.cell(txt="PLANNER" + str(YEAR))

for first_date in date_iter:
	pdf.add_page()
	page += 1
	page_link = pdf.add_link()
	pdf.set_link(page_link, page=page)
	for y in range(5):
		if not y == 0:
			with pdf.new_path() as path:
				path.style.stroke_width = 0.3
				path.move_to(horizontal_padding, vertical_padding + day_height * y)
				path.line_to(horizontal_padding + day_width, vertical_padding + day_height * y)
				path.close()

		with pdf.new_path() as path:
			path.style.stroke_width = 0.3
			path.move_to(horizontal_padding + day_horizontal_spacing + day_width, vertical_padding + day_height * y)
			path.line_to(pdf.w - horizontal_padding, vertical_padding + day_height * y)
			path.close()

	for y in range(4):
		for line in range(1, rows_per_day + 1):
			if not y == 0:
				with pdf.new_path() as path:
					path.style.stroke_width = .15
					path.move_to(horizontal_padding + indent_padding,
					             vertical_padding + day_height * y + row_spacing * line)
					path.line_to(horizontal_padding + day_width, vertical_padding + day_height * y + row_spacing * line)
					path.close()

			with pdf.new_path() as path:
				path.style.stroke_width = .15
				path.move_to(horizontal_padding + indent_padding + day_width + day_horizontal_spacing,
				             vertical_padding + day_height * y + row_spacing * line)
				path.line_to(horizontal_padding + day_width + day_width + day_horizontal_spacing,
				             vertical_padding + day_height * y + row_spacing * line)
				path.close()

	pdf.set_y(10)
	pdf.set_font('helvetica', 'B', 25)
	pdf.cell(txt=first_date.strftime("Week Beginning %b %d"))

	pdf.set_font('helvetica', 'B', 25)
	pdf.set_xy(horizontal_padding, vertical_padding + day_height + 2)
	pdf.cell(w=indent_padding, align="C", txt=str(first_date.day))

	links[first_date] = page_link

	pdf.set_font('helvetica', "", 15)
	pdf.set_xy(horizontal_padding, vertical_padding + day_height + 11)
	pdf.cell(w=indent_padding, align="C", txt=first_date.strftime("%a"))

	for i in range(2, 4):
		date = next(date_iter)
		links[date] = page_link
		pdf.set_font('helvetica', 'B', 25)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 2)
		pdf.cell(w=indent_padding, align="C", txt=str(date.day))

		pdf.set_font('helvetica', "", 15)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 11)
		pdf.cell(w=indent_padding, align="C", txt=date.strftime("%a"))

	for i in range(4):
		date = next(date_iter)
		links[date] = page_link

		pdf.set_font('helvetica', 'B', 25)
		pdf.set_xy(horizontal_padding + day_width + day_horizontal_spacing, vertical_padding + day_height * i + 2)
		pdf.cell(w=indent_padding, align="C", txt=str(date.day))

		pdf.set_font('helvetica', "", 15)
		pdf.set_xy(horizontal_padding + day_width + day_horizontal_spacing, vertical_padding + day_height * i + 11)
		pdf.cell(w=indent_padding, align="C", txt=date.strftime("%a"))

	# insert month overview in bottom right corner
	cw = row_spacing * 6  # calendar width
	ch = row_spacing * 5  # calendar height
	crh, ccw = ch / 7, cw / 7  # calendar row height and column width
	cx, cy = pdf.w-horizontal_padding-cw, pdf.h-vertical_padding - ch  # calendar x and y
	pdf.set_font('helvetica', "", 11)

	# index in dates list of the first day in current month
	index_start_calendar = dates.index(first_date) - first_date.day + 1
	# get monday
	while dates[index_start_calendar].weekday() > 0:
		index_start_calendar -= 1

	# set grey background
	pdf.set_xy(cx, cy)
	pdf.set_fill_color(235)
	pdf.cell(cw, ch, txt="", fill=True)

	# Add month header
	pdf.set_xy(cx, cy)
	# Pick month based off of index_start_calendar + 2 in case month changes early week
	pdf.cell(w=cw, txt=dates[index_start_calendar + 2].strftime("%B"), align="C")

	# Add weekday headers
	pdf.set_xy(cx, cy + crh)
	weekdays = ["M", "T",  "W",  "T", "F", "S", "S"]
	for c in range(7):
		pdf.set_xy(cx + ccw*c, cy+crh)
		pdf.cell(txt=weekdays[c])

	# Add dates and links to page
	for r in range(5):
		for c in range(7):
			pdf.set_xy(cx+ccw*c, cy + crh*(r+2))
			link = pdf.add_link()
			page = int((index_start_calendar / 7) + 2)
			if page < 2:
				page = 2
			pdf.set_link(link, page=page)
			pdf.cell(txt=str(dates[index_start_calendar].day), link=link)
			# Add a border around this week
			if dates[index_start_calendar] == first_date:
				pdf.set_xy(cx + ccw * c + ccw/10, cy + crh * (r + 2))
				pdf.cell(w=cw-ccw/5, h=crh, border=True)

			index_start_calendar += 1

pdf.output(str(YEAR) + "planner.pdf")
