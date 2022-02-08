import glob


def get_book_summary(bookfile):
    book_summary = {'title': '', 'author': '', 'subtype': '', 'year': '', 'lang': ''}
    
    content = bookfile.readlines()
    for line in content:
        if (line.strip() > ''): 
            if 'title=' in line:
                book_summary['title'] = line.split('=')[1].strip()
            elif 'author=' in line:
                book_summary['author'] = line.split('=')[1].strip()
            elif 'type=' in line:
                book_summary['subtype'] = line.split('=')[1].strip()
            elif 'year=' in line:
                book_summary['year'] = line.split('=')[1].strip()
            elif 'lang=' in line:
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

with open('data/livros.txt', 'w', encoding='utf-8') as new_bookfile:
    new_bookfile.write("{\"data\":")
    new_bookfile.write(str(books_to_data))
    new_bookfile.write("}")
