import calendar
import datetime

from fpdf import FPDF  # https://pyfpdf.github.io/fpdf2/


class Iterator:
	'''
	Simple iterator class. Just has_next(), get_next() and peek()
	'''

	def __init__(self, lst):
		self.list = lst
		self.index = 0

	def has_next(self):
		return self.index < len(self.list) - 1

	def peek(self):
		return self.list[self.index]

	def get_next(self):
		self.index += 1
		return self.list[self.index - 1]


pdf = FPDF(orientation="l")
pdf.set_margin(0)

# general constants
YEAR = 2022
include_mini_cal = True
extra_rows_monday = 3  # extra rows for monday
rows_per_day = 7

# layout constants
indent_padding = 15  # smaller lines for each date padding
day_horizontal_spacing = 10  # horizontal space between days
vertical_padding = 10
horizontal_padding = 10

# Compute more constants
day_height = (pdf.h - vertical_padding * 2) / 4
day_width = (pdf.w - horizontal_padding * 2 - day_horizontal_spacing) / 2
row_spacing = day_height / (rows_per_day + 1)
links = dict()  # date to page links
cw = row_spacing * 6  # mini calendar width
ch = row_spacing * 5  # mini calendar height
crh, ccw = ch / 8, cw / 7  # mini calendar row height and column width
cx, cy = pdf.w - horizontal_padding - cw, pdf.h - vertical_padding - ch  # mini calendar x and y

# Get all dates in a year - there probably exists a more efficient way
# dates_with_dup contains full weeks for each month (even when month doesn't start on monday and end on sunday)
# so there are duplicated dates
dates_with_dup = [i for m in range(1, 13) for i in calendar.Calendar(firstweekday=0).itermonthdates(YEAR, m)]
dates = []
for date in dates_with_dup:
	if date not in dates:
		dates.append(date)
date_iter = Iterator(dates)

# Add title page
pdf.add_page()
pdf.set_font('helvetica', 'B', 30)
pdf.set_y(pdf.h / 2)
pdf.cell(txt=str(YEAR) + " PLANNER", center=True, ln=2)
pdf.set_font('helvetica', '', 15)
pdf.cell(txt="https://github.com/jpperret/python-planner", link="https://github.com/jpperret/python-planner",
		 center=True)

while date_iter.has_next():
	pdf.add_page()
	page_link = pdf.add_link()
	pdf.set_link(page_link, page=pdf.page)

	first_date_of_week = date_iter.peek()

	pdf.set_text_color(0)

	# add week title
	pdf.set_font('helvetica', 'B', 20)
	pdf.set_xy(0, vertical_padding)
	pdf.cell(w=horizontal_padding + day_horizontal_spacing + day_width, align="C",
			 txt=first_date_of_week.strftime("Week Beginning %b %d, %Y"))

	# Add lines to separate days
	pdf.set_line_width(.3)
	for y in range(5):
		if y == 1:  # monday
			line_y = vertical_padding + day_height * y - extra_rows_monday * row_spacing
			pdf.line(horizontal_padding, line_y, horizontal_padding + day_width, line_y)
		elif not y == 0:  # skip first day on left side
			line_y = vertical_padding + day_height * y
			pdf.line(horizontal_padding, line_y, horizontal_padding + day_width, line_y)
		line_y = vertical_padding + day_height * y
		pdf.line(horizontal_padding + day_horizontal_spacing + day_width, line_y, pdf.w - horizontal_padding, line_y)

	# add lines in each day
	pdf.set_line_width(.12)
	for y in range(4):
		for line in range(1, rows_per_day + 1):
			if y == 1:  # monday
				for extra_line in range(extra_rows_monday + 1):
					line_y = vertical_padding + day_height * y + row_spacing * (
							line + extra_line) - extra_rows_monday * row_spacing
					pdf.line(horizontal_padding + indent_padding, line_y, horizontal_padding + day_width, line_y)
			elif not y == 0:  # skip first day on left side
				line_y = vertical_padding + day_height * y + row_spacing * line
				pdf.line(horizontal_padding + indent_padding, line_y, horizontal_padding + day_width, line_y)

			# add line on right side
			line_y = vertical_padding + day_height * y + row_spacing * line
			pdf.line(horizontal_padding + indent_padding + day_width + day_horizontal_spacing, line_y,
					 horizontal_padding + day_width + day_width + day_horizontal_spacing, line_y)

	# Add date labels on left
	date = date_iter.get_next()
	links[date] = page_link

	pdf.set_font('helvetica', "", 15)
	pdf.set_xy(horizontal_padding, vertical_padding + day_height + 11 - extra_rows_monday * row_spacing)
	pdf.cell(w=indent_padding, align="C", txt=date.strftime("%a"))

	pdf.set_font('helvetica', 'B', 25)
	pdf.set_xy(horizontal_padding, vertical_padding + day_height + 2 - extra_rows_monday * row_spacing)
	pdf.cell(w=indent_padding, align="C", txt=str(date.day))
	for i in range(2, 4):
		date = date_iter.get_next()
		links[date] = page_link

		pdf.set_font('helvetica', "", 15)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 11)
		pdf.cell(w=indent_padding, align="C", txt=date.strftime("%a"))

		pdf.set_font('helvetica', 'B', 25)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 2)
		pdf.cell(w=indent_padding, align="C", txt=str(date.day))

	# Add date labels on right
	for i in range(4):
		date = date_iter.get_next()
		links[date] = page_link

		pdf.set_font('helvetica', "", 15)
		pdf.set_xy(horizontal_padding + day_width + day_horizontal_spacing, vertical_padding + day_height * i + 11)
		pdf.cell(w=indent_padding, align="C", txt=date.strftime("%a"))

		pdf.set_font('helvetica', 'B', 25)
		pdf.set_xy(horizontal_padding + day_width + day_horizontal_spacing, vertical_padding + day_height * i + 2)
		pdf.cell(w=indent_padding, align="C", txt=str(date.day))

	if include_mini_cal:
		# insert month overview in bottom right corner
		pdf.set_font('helvetica', "", 10)

		# set grey background
		pdf.set_xy(cx, cy)
		pdf.set_fill_color(235)
		pdf.cell(cw, ch, txt="", fill=True)

		# If month changes on thurs then use next month
		first_date_of_month = dates[dates.index(first_date_of_week) + 3]
		# Get first day of month to start mini calendar
		index_start_calendar = max(dates.index(first_date_of_month) - first_date_of_month.day + 1, 0)
		# Get calendar month. If before year starts then use January
		cal_month = dates[index_start_calendar].month if dates[index_start_calendar].year == YEAR else 1
		# get monday
		while dates[index_start_calendar].weekday() != 0:
			index_start_calendar -= 1

		# Add month header
		pdf.set_xy(cx, cy)
		pdf.cell(w=cw, txt=datetime.datetime(YEAR, cal_month, 1).strftime("%B"), align="C")

		# Add weekday headers
		for c in range(7):
			pdf.set_xy(cx + ccw * c, cy + crh)
			pdf.cell(txt=["M", "T", "W", "T", "F", "S", "S"][c])

		# Add dates and links to page
		for r in range(6):
			for c in range(7):
				if index_start_calendar >= len(dates):
					break
				pdf.set_xy(cx + ccw * c, cy + crh * (r + 2))
				link = pdf.add_link()
				# divided by 7 for week. Add 2 for rounding down and title page
				page = int((index_start_calendar / 7) + 2)
				pdf.set_link(link, page=page)
				if dates[index_start_calendar].month != cal_month:
					pdf.set_text_color(200)
				else:
					pdf.set_text_color(0)
				pdf.cell(txt=str(dates[index_start_calendar].day), link=link)

				# Add a border around this week
				if dates[index_start_calendar] == first_date_of_week:
					pdf.set_xy(cx + ccw * c + ccw / 10, cy + crh * (r + 2))
					pdf.cell(w=cw - ccw / 5, h=crh, border=True)

				index_start_calendar += 1

pdf.output(str(YEAR) + "planner.pdf")
