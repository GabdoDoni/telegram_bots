# Не удаляйте эти объекты - просто используйте
BOOK: str = 'book.txt'
PAGE_SIZE = 1050
book: dict[int, str] = {}


def _get_part_text(text, start, page_size):
    end = min(start + page_size, len(text))
    for i in range(end, start, -1):
        if len(text) == i:
            continue
        else:
            if text[i] in (',','.','!',':',';','?'):
                if len(text) > i+1 and text[i+1] in (',','.','!',':',';','?'):
                    continue
                else:
                    if len(text[start:i+1]) > page_size:
                        continue
                    else:
                        return text[start:i+1], len(text[start:i+1])


# Дополните эту функцию, согласно условию задачи
def prepare_book(path: str) -> None:
    start = 0
    for i in range(1, 100):
        with open(path, 'r', encoding='utf-8') as file:
            txt = file.read()
            if start >= len(txt):
                break
            else:
                txt_text, page_size = _get_part_text(txt, start, PAGE_SIZE)
                book[i] = txt_text.strip()
                start += page_size
    return book

print(prepare_book(BOOK))

