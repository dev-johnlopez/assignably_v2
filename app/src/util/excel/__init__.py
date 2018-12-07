import xlsxwriter
import io

def getExportArray(contacts):
    export = []
    headers = ['First Name', 'Last Name', 'Email', 'Phone']
    export.append(headers)
    for contact in contacts:
        export.append([contact.first_name, contact.last_name, contact.email, contact.phone])
    return export

def createContactExportFile(contacts):
    output = io.BytesIO()
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for contact in contacts:
        worksheet.write(row, col,     contact.first_name)
        worksheet.write(row, col + 1, contact.last_name)
        worksheet.write(row, col + 2, contact.email)
        worksheet.write(row, col + 3, contact.phone)
        row += 1

    workbook.close()
    output.seek(0)
    return output
