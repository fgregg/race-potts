import csv
import cStringIO

def collapse_header(header) :
    collapsed_header = []
    header_f = cStringIO.StringIO(header)
    reader = csv.reader(header_f) 
    for each in reader.next() :
        head = each.split()[0]
        if 'Error' in each :
            head += ', Error'
        collapsed_header.append(head)

    collapsed_f = cStringIO.StringIO()
    csv.writer(collapsed_f).writerow(collapsed_header)
    print collapsed_f.getvalue().strip()


if __name__ == '__main__' :
    import sys
    head = sys.stdin.read()
    collapse_header(head)
    
