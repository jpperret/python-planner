from fpdf import FPDF
import calendar

# https://pyfpdf.github.io/fpdf2/
# TODO might be able to use margin in FPDF instead of creating it

pdf = FPDF(orientation="l")
YEAR = 2022
vertical_padding = 10
horizontal_padding = 10
indent_padding = 15
day_height = (pdf.h - vertical_padding * 2) / 4
day_horizontal_spacing = horizontal_padding
day_width = (pdf.w - horizontal_padding * 2 - day_horizontal_spacing) / 2
rows_per_day = 7
row_spacing = day_height / (rows_per_day + 1)
DAYS_OF_WEEK = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

# Each month has enough days to fill out every week, when the month ends midweek this means the week is in the ending
# month and starting month
# There is probably a better way to get all the dates for a given year
dates_with_dup = [i for m in range(1, 13) for i in calendar.Calendar(firstweekday=0).itermonthdates(YEAR, m)]
dates = []
for date in dates_with_dup:
	if date not in dates:
		dates.append(date)
date_iter = iter(dates)

pdf.add_page()
pdf.set_font('helvetica', 'B', 25)
pdf.cell(txt="PLANNER" + str(YEAR))

for first_date in date_iter:
	pdf.add_page()
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

	pdf.set_font('helvetica', "", 15)
	pdf.set_xy(horizontal_padding, vertical_padding + day_height + 11)
	pdf.cell(w=indent_padding, align="C", txt=DAYS_OF_WEEK[first_date.weekday()])

	for i in range(2, 4):
		date = next(date_iter)

		pdf.set_font('helvetica', 'B', 25)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 2)
		pdf.cell(w=indent_padding, align="C", txt=str(date.day))

		pdf.set_font('helvetica', "", 15)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 11)
		pdf.cell(w=indent_padding, align="C", txt=DAYS_OF_WEEK[date.weekday()])

	for i in range(4):
		date = next(date_iter)

		pdf.set_font('helvetica', 'B', 25)
		pdf.set_xy(horizontal_padding + day_width + day_horizontal_spacing, vertical_padding + day_height * i + 2)
		pdf.cell(w=indent_padding, align="C", txt=str(date.day))

		pdf.set_font('helvetica', "", 15)
		pdf.set_xy(horizontal_padding + day_width + day_horizontal_spacing, vertical_padding + day_height * i + 11)
		pdf.cell(w=indent_padding, align="C", txt=DAYS_OF_WEEK[date.weekday()])

pdf.output(str(YEAR) + "planner.pdf")
