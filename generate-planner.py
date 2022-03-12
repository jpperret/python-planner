from fpdf import FPDF
import calendar

# https://pyfpdf.github.io/fpdf2/


class Iterator:
	def __init__(self, lst):
		self.list = lst
		self.index = 0

	def has_next(self):
		return self.index < len(self.list) - 1

	def peek(self):
		return self.list[self.index]

	def get_next(self):
		self.index += 1
		return self.list[self.index -1]


pdf = FPDF(orientation="l")
pdf.set_margin(0)

# Set constants
YEAR = 2022
vertical_padding = 10
horizontal_padding = 10
indent_padding = 15  # smaller lines for each date padding
rows_per_day = 7
day_horizontal_spacing = horizontal_padding  # horizontal space between days

# Compute more constants
day_height = (pdf.h - vertical_padding * 2) / 4
day_width = (pdf.w - horizontal_padding * 2 - day_horizontal_spacing) / 2
row_spacing = day_height / (rows_per_day + 1)
links = dict()

# Get all dates in a year
dates_with_dup = [i for m in range(1, 13) for i in calendar.Calendar(firstweekday=0).itermonthdates(YEAR, m)]
dates = []
for date in dates_with_dup:
	if date not in dates:
		dates.append(date)
date_iter = Iterator(dates)

# Add title page
pdf.add_page()
pdf.set_font('helvetica', 'B', 30)
pdf.set_y(pdf.h/2)
pdf.cell(txt=str(YEAR) + " PLANNER", center=True, ln=2)
pdf.set_font('helvetica', '', 15)
pdf.cell(txt="https://github.com/jpperret/python-planner", link="https://github.com/jpperret/python-planner", center=True)


while date_iter.has_next():
	pdf.add_page()

	page_link = pdf.add_link()
	pdf.set_link(page_link, page=pdf.page)

	first_date_of_week = date_iter.peek()

	# add week title
	pdf.set_font('helvetica', 'B', 20)
	pdf.set_xy(0, vertical_padding*2)
	pdf.cell(w=horizontal_padding+day_horizontal_spacing+day_width, align="C",
	         txt=first_date_of_week.strftime("Week Beginning %b %d"))

	# Add lines to separate days
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

	# add lines in each day
	for y in range(4):
		for line in range(1, rows_per_day + 1):
			if not y == 0:
				with pdf.new_path() as path:
					path.style.stroke_width = .14
					path.move_to(horizontal_padding + indent_padding,
					             vertical_padding + day_height * y + row_spacing * line)
					path.line_to(horizontal_padding + day_width, vertical_padding + day_height * y + row_spacing * line)
					path.close()

			with pdf.new_path() as path:
				path.style.stroke_width = .14
				path.move_to(horizontal_padding + indent_padding + day_width + day_horizontal_spacing,
				             vertical_padding + day_height * y + row_spacing * line)
				path.line_to(horizontal_padding + day_width + day_width + day_horizontal_spacing,
				             vertical_padding + day_height * y + row_spacing * line)
				path.close()

	# Add date on left
	for i in range(1, 4):
		date = date_iter.get_next()
		links[date] = page_link
		pdf.set_font('helvetica', 'B', 25)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 2)
		pdf.cell(w=indent_padding, align="C", txt=str(date.day))

		pdf.set_font('helvetica', "", 15)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 11)
		pdf.cell(w=indent_padding, align="C", txt=date.strftime("%a"))

	# Add date labels on right
	for i in range(4):
		date = date_iter.get_next()
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
	# get monday
	index_start_calendar = dates.index(first_date_of_week) - first_date_of_week.day + 1
	while dates[index_start_calendar].weekday() > 0:
		index_start_calendar -= 1

	# set grey background
	pdf.set_xy(cx, cy)
	pdf.set_fill_color(235)
	pdf.cell(cw, ch, txt="", fill=True)

	# Add month header
	# Pick month based off of index_start_calendar + 2 in case month changes early week
	pdf.set_xy(cx, cy)
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
			if dates[index_start_calendar] == first_date_of_week:
				pdf.set_xy(cx + ccw * c + ccw/10, cy + crh * (r + 2))
				pdf.cell(w=cw-ccw/5, h=crh, border=True)

			index_start_calendar += 1

pdf.output(str(YEAR) + "planner.pdf")
