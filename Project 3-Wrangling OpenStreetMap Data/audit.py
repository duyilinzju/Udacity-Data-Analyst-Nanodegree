import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
from collections import defaultdict
import pprint
import re
import os
import operator

osm_file = open("sanjose.osm")
tree = ElementTree()
# Auditing Validity: get the representation for all phone numbers
def phone(filename):
    phone = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if tag.attrib["k"] == "phone":
                    phone.add(tag.attrib["v"])
    print("Number of phone number record: " + str(len(phone)))
    #pprint.pprint(phone)
    return phone


# format "18005555555" as '1-800-555-5555'
def phone_format(number):
    return format(int(number[:-1]), ",").replace(",", "-") + number[-1]


# Auditing Validity: check is a string is a valid phone number, and return
# a bool value and the string representation of that phone number
def phone_is_valid(phone_number):
    digit_string = filter(str.isdigit, phone_number)
    if len(digit_string) == 10:
        digit_string = "1" + digit_string # add country code
    if len(digit_string) == 11: # valid phone number
        format_num = phone_format(digit_string)
        return True, format_num
    return False, phone_number


def update_number_pending(filename):
    invalid_phone = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if tag.attrib["k"] == "phone":
                    print tag.attrib['v']
                    if phone_is_valid(tag.attrib["v"])[0]:
                        print phone_is_valid(tag.attrib["v"])[1]
                        tag.set("phone", phone_is_valid(tag.attrib["v"])[1])
                    else:
                        invalid_phone.add(tag.attrib["v"])

    pprint.pprint(invalid_phone)


def update_number(filename):
    invalid_phone = set()
    valid_phone = set()
    phone_list = phone(filename)
    for number in phone_list:
        if type(number) == type("") and phone_is_valid(number)[0]:
            valid_phone.add(phone_is_valid(number)[1])
        else:
            invalid_phone.add(number)
    print("formatted valid phone list")
    pprint.pprint(valid_phone)
    print("invalid phone list")
    pprint.pprint(invalid_phone)


def building(filename):
    building_type = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if tag.attrib["k"] == "building":
                    building_type.add(tag.attrib["v"])
    print("Number of building record: " + str(len(building_type)))
    pprint.pprint(building_type)
    return building_type


def update_building(name):
    map = {
        "garages": "garage",
        "train": "train_station",
        "truck": "food_truck"
    }
    if name in ("garages", "train", "truck"):
        return map[name]
    else:
        return name


#phone(osm_file)
#update_number(osm_file)
#building(osm_file)