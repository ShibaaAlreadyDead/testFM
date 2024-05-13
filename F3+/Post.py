import requests
import re

from requests import RequestException


# POST request
def get_fm_text(imei):
    payload = {
        'num': imei
    }
    with requests.Session() as s:
        try:
            p = s.post("https://911.fm/adm/?luke", data=payload)
        except RequestException as err:
            print('Requests failure %s' % err)
            return None

        print(p.status_code, p.text)

        if p.status_code == 200:
            return p.text
        else:
            return None


# get table tag from html text
def get_table(text):
    table_index_start = text.index("<table id=\"mondata\"")
    table_index_end = text.index("</table>", table_index_start)
    return text[table_index_start:table_index_end + 8]


# get thead tag from html text
def get_thead(table):
    thead_index_start = table.index("<thead>")
    thead_index_end = table.index("</thead>", thead_index_start)
    return table[thead_index_start:thead_index_end + 8]


def get_tbody(table):
    tbody_index_start = table.index("<tbody>")
    tbody_index_end = table.index("</tbody>", tbody_index_start)
    return table[tbody_index_start:tbody_index_end + 8]


def __split_by_tag(text, tag):
    rows = re.split('\\s*<' + tag + '[^>]*>\\s*', text)
    rows = [re.split('\\s*</' + tag + '>', row)[0] for row in rows]
    return rows


def __skip_first_and_last(array):
    return array[1:]


def split_n_skip(text, tag):
    return __skip_first_and_last(__split_by_tag(text, tag))


def get_rows(t_part):
    return split_n_skip(t_part, 'tr')


def get_inner_cells(inner_row):
    return split_n_skip(inner_row, 'td')


def get_value_of_cell(inner_cell):
    res = ''.join(__split_by_tag(inner_cell, '[^>]+')).strip()
    if res:
        return res

    left = inner_cell.find("title=\"")
    if left == -1:
        return inner_cell
    else:
        left = (left + 7)
        right = inner_cell.find("\"", left)
        return inner_cell[left:right]


def parse_fm(imei='863051060074027'):
    html = get_fm_text(imei)
    if html is None:
        print("Server is down or IMEI doesn't match")
        return None

    try:
        table = get_table(html)
        head = get_thead(table)
        body = get_tbody(table)
        rows = get_rows(body)
        a = []
        for row in get_inner_cells():
        a.append {}
        value = get_value_of_cell(cell)
        for value in get_value_of_cell()
        -> [{},{},{},{}]
    except IndexError as err:
        print("Bad HTML: %s" % err)
        return None

# print(get_fm_text())
# print(get_rows(get_tbody(get_table(get_fm_text()))))
print('|', get_value_of_cell(get_inner_cells(get_rows(get_tbody(get_table(get_fm_text())))[0])[2]), '|')
