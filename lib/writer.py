import xlsxwriter
workbook = xlsxwriter.Workbook('podcast_data.xlsx')
worksheet = workbook.add_worksheet()

def write_header():
    worksheet.set_column('A:A', 50)
    worksheet.set_column('B:B', 30)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 15)
    worksheet.set_column('H:H', 20)
    worksheet.set_column('I:I', 20)
    worksheet.set_column('J:J', 30)
    worksheet.set_column('K:K', 50)
    worksheet.set_column('L:L', 40)
    worksheet.set_column('M:M', 50)
    worksheet.set_column('N:N', 20)
    worksheet.set_column('O:O', 80)
    bold = workbook.add_format({'bold': True})
    worksheet.write(0, 0, "Title", bold)
    worksheet.write(0, 1, "Genre", bold)
    worksheet.write(0, 2, "Location", bold)
    worksheet.write(0, 3, "Active", bold)
    worksheet.write(0, 4, "Rating", bold)
    worksheet.write(0, 5, "Listeners", bold)
    worksheet.write(0, 6, "Episodes count", bold)
    worksheet.write(0, 7, "Latest episode", bold)
    worksheet.write(0, 8, "Ad cost per episode", bold)
    worksheet.write(0, 9, "Url", bold)
    worksheet.write(0, 10, "Description", bold)
    worksheet.write(0, 11, "Email", bold)
    worksheet.write(0, 12, "Audio name", bold)
    worksheet.write(0, 13, "Audio date", bold)
    worksheet.write(0, 14, "Audio url", bold)

def write_row(data, row):
    worksheet.write(row, 0, data["title"])
    worksheet.write(row, 1, data["genre"])
    worksheet.write(row, 2, data["location"])
    worksheet.write(row, 3, data["active"])
    worksheet.write(row, 4, data["rating"])
    worksheet.write(row, 5, data["listeners"])
    worksheet.write(row, 6, data["episodes_count"])
    worksheet.write(row, 7, data["latest_episode"])
    worksheet.write(row, 8, data["ad_cost_per_episode"])
    worksheet.write(row, 9, data["url"])
    worksheet.write(row, 10, data["description"])
    r = row
    end_row = r
    if(data["emails"] and len(data["emails"]) > 0):
        for email in data["emails"]:
            worksheet.write(r, 11, email)
            r += 1
        if(r > end_row):
            end_row = r
    if(data["episodes"] and len(data["episodes"]) > 0):
        r = row
        for episode in data["episodes"]:
            worksheet.write(r, 12, episode["name"])
            worksheet.write(r, 13, episode["date"])
            worksheet.write(r, 14, episode["audio"])
            r += 1
        if(r > end_row):
            end_row = r
    return end_row