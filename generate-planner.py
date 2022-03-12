import calendar

from fpdf import FPDF  # https://pyfpdf.github.io/fpdf2/


class Iterator:
	def __init__(self, lst):
		self.list = lst
		self.index = 0
		self.last = None

	def has_next(self):
		return self.index < len(self.list) - 1

	def peek(self):
		return self.list[self.index]

	def get_next(self):
		self.index += 1
		self.last = self.list[self.index - 1]
		return self.last

	def get_last(self):
		return self.last


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
calendar_width = row_spacing * 6
calendar_height = row_spacing * 5
calendar_row_height, calendar_col_width = calendar_height / 7, calendar_width / 7
calendar_x, calendar_y = pdf.w - horizontal_padding - calendar_width, pdf.h - vertical_padding - calendar_height
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

pdf.add_page()
page += 1
pdf.set_font('helvetica', 'B', 30)
pdf.set_y(pdf.h / 2)
pdf.cell(txt=str(YEAR) + " PLANNER", center=True, ln=2)
pdf.set_font('helvetica', '', 15)
pdf.cell(txt="https://github.com/jpperret/python-planner", link="https://github.com/jpperret/python-planner",
		 center=True)

date_iter = Iterator(dates)

while date_iter.has_next():
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

	pdf.set_font('helvetica', 'B', 25)
	pdf.set_xy(0, vertical_padding * 2)
	pdf.cell(w=horizontal_padding + day_horizontal_spacing + day_width, align="C",
			 txt=date_iter.peek().strftime("Week Beginning %b %d"))

	for i in range(1, 4):
		date = date_iter.get_next()
		links[date] = page_link
		pdf.set_font('helvetica', 'B', 25)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 2)
		pdf.cell(w=indent_padding, align="C", txt=str(date.day))

		pdf.set_font('helvetica', "", 15)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 11)
		pdf.cell(w=indent_padding, align="C", txt=date.strftime("%a"))

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

	# get date to start calendar - want a monday
	index_start_calendar = dates.index(date_iter.get_last()) - date_iter.get_last().day + 1
	while dates[index_start_calendar].weekday() > 0:
		index_start_calendar -= 1

	# set grey background
	pdf.set_xy(calendar_x, calendar_y)
	pdf.set_fill_color(235)
	pdf.cell(calendar_width, calendar_height, txt="", fill=True)

	# Add month header
	# Pick month based off of index_start_calendar + 2 in case month changes early week
	pdf.set_font('helvetica', "", 11)
	pdf.set_xy(calendar_x, calendar_y)
	pdf.cell(w=calendar_width, txt=dates[index_start_calendar + 2].strftime("%B"), align="C")

	# Add weekday headers
	pdf.set_xy(calendar_x, calendar_y + calendar_row_height)
	weekdays = ["M", "T", "W", "T", "F", "S", "S"]
	for c in range(7):
		pdf.set_xy(calendar_x + calendar_col_width * c, calendar_y + calendar_row_height)
		pdf.cell(txt=weekdays[c])

	# Add dates and links to page
	for r in range(5):
		for c in range(7):
			page = int((index_start_calendar / 7) + 2)
			if page < 2:
				page = 2  # don't link to title page
			link = pdf.add_link()
			pdf.set_link(link, page=page)

			pdf.set_xy(calendar_x + calendar_col_width * c, calendar_y + calendar_row_height * (r + 2))
			pdf.cell(txt=str(dates[index_start_calendar].day), link=link)

			# Add a border around this week
			if dates[index_start_calendar] == date_iter.get_last():
				pdf.set_xy(calendar_x + calendar_col_width * c + calendar_col_width / 10,
						   calendar_y + calendar_row_height * (r + 2))
				pdf.cell(w=calendar_width - calendar_col_width / 5, h=calendar_row_height, border=True)

			index_start_calendar += 1

pdf.output(str(YEAR) + "planner.pdf")
