import csv

def recomment(numUsers):
    csv_dict = [dict() for x in range(numUsers)]
    authors = {}
    with open('probabilities.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
            #row[0] : Author, row[1] : Rating, row[3] : HotelId, row[4] : Anger, row[7] : Joy, row[8] : Sadness
                if row[0] in authors.values():
                    for k, v in authors.items():
                        if v== row[0]:
                            #print(row[0], " : ",csv_dict[k])
                            if not row[3] in csv_dict:
                                csv_dict[k][row[3]]= {}
                            csv_dict[k][row[3]]['Overall'] = int((row[1].partition('Overall\':')[2])[2:3])
                            csv_dict[k][row[3]]['Joy'] = float(row[7])
                            csv_dict[k][row[3]]['Anger'] = float(row[4])
                            csv_dict[k][row[3]]['Sadness'] = float(row[8])

                else:
                    authors[line_count] = row[0]
                    csv_dict[line_count][row[3]] = {}
                    csv_dict[line_count][row[3]]['Overall'] = int((row[1].partition('Overall\':')[2])[2:3])
                    csv_dict[line_count][row[3]]['Joy'] = float(row[7])
                    csv_dict[line_count][row[3]]['Anger'] = float(row[4])
                    csv_dict[line_count][row[3]]['Sadness'] = float(row[8])
                line_count += 1
    return csv_dict
