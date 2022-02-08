import glob
import json

def get_book_summary(bookfile):
    book_summary = {'title': '', 'author': '', 'subtype': '', 'year': '', 'lang': ''}
    
    content = bookfile.readlines()
    for line in content:
        if (line.strip() > ''): 
            if line.startswith('title='):
                book_summary['title'] = line.split('=')[1].strip()
            elif line.startswith('author='):
                book_summary['author'] = line.split('=')[1].strip()
            elif line.startswith('subtype='):
                book_summary['subtype'] = line.split('=')[1].strip()
            elif line.startswith('year='):
                book_summary['year'] = line.split('=')[1].strip().replace('[', '').replace(']', '')
            elif line.startswith('lang='):
                book_summary['lang'] = line.split('=')[1].strip()

    return book_summary


book_list = glob.glob('RealBooks/**/*.book', recursive=True)
# To include files that begin with ".", that are not caught by the first command
book_list.extend(glob.glob('RealBooks/**/.*.book', recursive=True))
books_to_data = []
total_books = 0

for book in book_list:
    try:
        with open(book, 'r', encoding='utf-8') as bookfile:
            book_summary = get_book_summary(bookfile)
            if book_summary['title'] > '':
                books_to_data.append(list(book_summary.values()))
                total_books = total_books+1
            else:
                print (book, book_summary)
    except UnicodeDecodeError:
        try:
            with open(book, 'r', encoding='cp1252') as bookfile:
                book_summary = get_book_summary(bookfile)
                if book_summary['title'] > '':
                    books_to_data.append(list(book_summary.values()))
                    total_books = total_books+1
                else:
                  print (book, book_summary)
        except Exception:
            print ("Cannot parse file:", book, " - Encoding: ", bookfile.encoding)

print ("Total books read:", total_books)

datatables_obj = {'data': books_to_data}

with open('data/livros.txt', 'w', encoding='utf-8') as new_bookfile:
    json.dump(datatables_obj, new_bookfile, ensure_ascii=False, indent=4)
