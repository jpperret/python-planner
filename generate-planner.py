from fpdf import FPDF
import calendar

# https://pyfpdf.github.io/fpdf2/

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
	pdf.cell(w=indent_padding, align="C", txt=first_date.strftime("%a"))

	for i in range(2, 4):
		date = next(date_iter)

		pdf.set_font('helvetica', 'B', 25)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 2)
		pdf.cell(w=indent_padding, align="C", txt=str(date.day))

		pdf.set_font('helvetica', "", 15)
		pdf.set_xy(horizontal_padding, vertical_padding + day_height * i + 11)
		pdf.cell(w=indent_padding, align="C", txt=date.strftime("%a"))

	for i in range(4):
		date = next(date_iter)

		pdf.set_font('helvetica', 'B', 25)
		pdf.set_xy(horizontal_padding + day_width + day_horizontal_spacing, vertical_padding + day_height * i + 2)
		pdf.cell(w=indent_padding, align="C", txt=str(date.day))

		pdf.set_font('helvetica', "", 15)
		pdf.set_xy(horizontal_padding + day_width + day_horizontal_spacing, vertical_padding + day_height * i + 11)
		pdf.cell(w=indent_padding, align="C", txt=date.strftime("%a"))

	# insert month overview in bottom right corner
	cw = row_spacing * 6  # calendar width
	ch = cw  # calendar height
	crh = ch / 7  # calendar row height
	cch = cw / 7 # calendar column height
	cx = pdf.w-horizontal_padding-cw # calendar x
	cy = pdf.h-vertical_padding - ch # calendar y
	pdf.set_xy(cx, cy)
	pdf.set_fill_color(215)
	pdf.cell(cw, ch, txt="", fill=True)
	pdf.set_margin(0)
	pdf.set_xy(cx, cy)
	pdf.set_font('helvetica', "", 10)
	pdf.cell(w=cw, txt=first_date.strftime("%B"), align="C")
	pdf.set_xy(cx, cy + crh)
	weekdays = ["M", "T",  "W",  "T", "F", "S", "S"]
	for c in range(7):
		pdf.set_xy(cx + cch*c,cy+crh)
		pdf.cell(txt=weekdays[c])

	for c in range(7):
		for r in range(5):
			pdf.set_xy(cx+cch*c, cy + crh*(r+2))
			pdf.cell(txt=str(r*7 + c))

pdf.output(str(YEAR) + "planner.pdf")
