#!/usr/bin/env python3
import re
import sys
import urllib.request

import pandas as pd
from bs4 import BeautifulSoup


def buttonz_counter(file_with_websites, counted_websites):
    addresses = pd.read_csv(file_with_websites, header=None).values
    counted = []

    for add in addresses:
        url = 'http://' + add[0]
        page = open_page(url)
        all_buttonz = find_elements(page, "button")
        all_buttonz += find_elements_with_class(page, has_class_button)
        all_buttonz += find_elements_with_type(page, has_proper_type)
        all = set(all_buttonz)

        counted.append((add[0], len(all)))

    counted = sorted(counted, key=lambda t: t[1], reverse=True)

    save_to_file(counted_websites, 'address, number_of_buttons', counted)


def save_to_file(file_name, header, data):
    with open(file_name, 'w') as f:
        f.write(header + '\n')
        for add, count in data:
            f.write(f'{add}, {count} \n')


def open_page(page_url):
    page = urllib.request.urlopen(page_url)
    return BeautifulSoup(page, "lxml")


def find_elements(soup_page, element, func=None):
    return soup_page.find_all(element, func)


def find_elements_with_class(soup_page, class_func):
    return soup_page.find_all(class_=class_func)


def find_elements_with_type(soup_page, type_func):
    return soup_page.find_all(type=type_func)


def has_class_button(css_class):
    reg_btn = re.compile('btn', re.IGNORECASE)
    reg_button = re.compile('button', re.IGNORECASE)
    return css_class and (reg_btn.search(css_class) or reg_button.search(css_class))


def has_proper_type(elem_type):
    reg_submit = re.compile('submit', re.IGNORECASE)
    reg_reset = re.compile('reset', re.IGNORECASE)
    reg_button = re.compile('button', re.IGNORECASE)
    return elem_type and (reg_submit.search(elem_type) or reg_button.search(elem_type) or reg_reset.search(elem_type))


address = sys.argv[1]
file_to_save = sys.argv[2]
buttonz_counter(address, file_to_save)
