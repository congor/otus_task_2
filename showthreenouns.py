# -*- coding: utf8 -*-
from argparse import ArgumentParser
from urllib.request import urlopen
from datetime import datetime, timedelta
from datetime import date as create_date
import pymorphy2
import calendar
import numpy as np

def validate(pages_input):    
    if pages_input <= 0:
        print("Минимальное количество страниц дожно быть не менее 1")
        pages = 1
    elif pages_input > 100:
        print("Минимальное количество страниц дожно быть не более 100 включительно")
        pages = 100
    else:
        pages = pages_input
    print("Выбрано страниц:", pages)
    return pages

def get_list(page):
    
    def extract_content_from_tag(text):
        
        left_index = text.find(">")
        right_index = text.rfind("</")
        content = text[left_index+1:right_index]
        return content
    
    def format_date(raw_date):
                
        def define_year_day(raw_date, month):
            
            day_index = raw_date.find(month)
            day = raw_date[:day_index]
            len_month = len(month)
            time_index = raw_date.find(month) + len_month    
            year = raw_date[time_index+1:]
            if len(year) >= 8:
                year = year[:-8]
                year = int(year)
            else:
                year = datetime.now().year            
            return year, int(day)
        
        if "сегодня" in raw_date:
            date = datetime.now().date()
        elif "вчера" in raw_date:
            date = datetime.now().date() - timedelta(days = 1)
        else:
            months = {
                "января": 1,
                "февраля": 2,
                "марта": 3,
                "апреля": 4,
                "мая": 5,
                "июня": 6,
                "июля": 7,
                "августа": 8,
                "сентября": 9,
                "октября": 10,
                "ноября": 11,
                "декабря": 12,
                }
            for month in months:
                if month in raw_date:
                    year, day = define_year_day(raw_date, month)
                    date = create_date(year, months[month], day)
        return date
    
    def create_nouns(row):
        
        def word_cleaner(word):
            
            symbols = ["!", "(", ")", ",", ".", "?", ":", ";", "...", "[", "]", "-", "“", "”", "«", "»" '"', "'"]
            for symbol in symbols:
                while len(word) > 1 and word[0] == symbol:
                    word = word[1:]
                while len(word) > 1 and word[-1] == symbol:
                    word = word[:-1]
            word = word.lower()                
            return word
        
        if "\xa0" in row:
            row = row.replace("\xa0", "\x20")
        words = row.split("\x20")        
        nouns = []
        
        for word in words:            
            word_clearned = word_cleaner(word)    
            word_analized = morph.parse(word_clearned)[0]            
            if word_analized.tag.POS == 'NOUN':                
                nouns.append(word_analized.normal_form)
        return nouns

    url = "https://habr.com/all/page" + str(page) # upto https://habr.com/all/page100 or https://habr.com/all/top100/page100/
    html_raw = urlopen(url)
    
    class_name_date = "post__time"
    class_name_title = "post__title_link"
    dates = []
    nouns = []
    
    for row in html_raw:
        row = row.decode("utf-8")
        if class_name_date in row:
            date_raw = extract_content_from_tag(row)
            date = format_date(date_raw)
            dates.append(date)
        elif class_name_title in row:
            title = extract_content_from_tag(row)
            nouns_in_title = create_nouns(title)            
            nouns.append(nouns_in_title)
    
    list_dates_nouns = []
    for date_index in range(len(dates)):
        list_dates_nouns.append((dates[date_index], nouns[date_index]))    
    return list_dates_nouns

def create_weeks_list(late_date, early_date):
           
    late_month = late_date.month
    late_year = late_date.year
    early_month = early_date.month
    early_year = early_date.year
    
    months_years = []
            
    for year in range(early_year, late_year+1, 1):
        if year == late_year:
            finish_month = late_month
        else:
            finish_month = 12    
        if year == early_year:
            start_month = early_month
        else:
            start_month = 1
        
        for month in range(start_month, finish_month+1, 1):
            months_years.append((year, month))
                    
    cal = calendar.Calendar()
    weeks_total = []
    for month_year in months_years:
        week_per_month = cal.monthdatescalendar(month_year[0], month_year[1])
        for week in week_per_month:
            week = [week[0], week[-1]]
            if (len(weeks_total) > 0 and weeks_total[-1] != week and week[0] <= late_date) or (len(weeks_total) == 0 and week[-1] >= early_date):
                weeks_total.append(week)        
    weeks = list(reversed(weeks_total))
    return weeks

def define_frequent_words(nouns): 
    
    nouns_array = np.array(nouns)
    unique, counts = np.unique(nouns_array, return_counts=True)
    nouns = list(unique)
    counts = list(counts)
    nouns_counts = []
    for index in range(len(counts)):
        nouns_counts.append([counts[index], nouns[index]])
    top = 3
    nouns_counts = sorted(nouns_counts, reverse=True)[:3]
    nouns = []
    for noun_count in nouns_counts:
        nouns.append(noun_count[-1])
    return nouns

def output_results(week_nouns='title_row'):    

    def create_output_tuple(week_nouns):
        output_row = []
        for first_element in week_nouns:
            for second_element in first_element:
                output_row.append(second_element)
        output_row = tuple(output_row)
        return output_row
    
    def output(output_pattern, output_row):
        print(output_pattern % tuple(output_row))
    
    output_line = "-" * 46
    
    if week_nouns == 'title_row':
        print(output_line)
        week_nouns = [["Дата начала", "Дата конца"], ["Самые частые слова"]]
        output_pattern = " %s | %s | %s"
        output_row_titles = create_output_tuple(week_nouns)        
        output(output_pattern, output_row_titles)        
    elif week_nouns == 'last_row':
        print(output_line)
    else:
        output_row = create_output_tuple(week_nouns)
        output_pattern = " %s  | %s | %s %s %s"
        output(output_pattern, output_row)
    
global morph
morph = pymorphy2.MorphAnalyzer()
parser = ArgumentParser()
parser.add_argument('-p', '--pages',
                  type=int, default=1,
                  help="установить количество страниц для анализа")
options = parser.parse_args()

inputed_pages = options.pages
pages = validate(inputed_pages)

output_results('title_row')

list_dates_nouns = []

for page in range(1, pages+1):
    for row in get_list(page):
        list_dates_nouns.append(row)

weeks = create_weeks_list(list_dates_nouns[0][0], list_dates_nouns[-1][0])    

for week in weeks:    
    nouns = []
    for date_nouns in list_dates_nouns:
        if week[0] <= date_nouns[0] <= week[-1]:                
            nouns += date_nouns[-1]   
    nouns = define_frequent_words(nouns)
    output_results([week, nouns])
    
output_results('last_row')