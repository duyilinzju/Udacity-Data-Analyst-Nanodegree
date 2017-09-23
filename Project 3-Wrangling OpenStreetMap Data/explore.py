import xml.etree.ElementTree as ET
from collections import defaultdict
import pprint
import re
import os
import operator

osm_file = open("sanjose.osm")

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)


# get the size of the osm file
def get_filesize(filename_str):
    byte_size = os.stat(filename_str).st_size/(1024 ** 2) # byte to Mb
    print("The size of the osm file is: " + str(byte_size) + " mb")


def get_user(element):
    return element.attrib["uid"]


# get a set of unique user id
def user_set(filename):
    users = set()
    for _, element in ET.iterparse(filename, events=("start",)):
        if element.get("uid") is not None:
            users.add(get_user(element))

    return users


# get the number of unique users
def number_of_user():

    users = user_set(osm_file)
    # pprint.pprint(users)
    print("Number of Unique Users: " + str(len(users)))
    return len(users)


# get the number of nodes ways and relations
def number_of_elems(filename):
    data = {
        "node": 0,
        "way": 0,
        "relation": 0
    }
    for _, element in ET.iterparse(filename, events=("start",)):
        for key in data:
            if element.tag == key:
                data[key] += 1
    print("Number of nodes: " + str(data["node"]))
    print("Number of ways: " + str(data["way"]))
    print("Number of relations: " + str(data["relation"]))
    return data


# get unique tags in way for further exploration on different places
def tags_in_way(filename):
    tag_name = set()
    for event, elem in ET.iterparse(osm_file, events = ("start",)):
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                tag_name.add(tag.attrib["k"])

    pprint.pprint(tag_name)
    return tag_name


# get unique tag values which have a key of "leisure"
def leisure_kind(filename):
    leisure = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib["k"] == "leisure":
                    leisure.add(tag.attrib["v"])

    pprint.pprint(leisure)
    return leisure


# from the function leisure_kind, we get a list of unique leisure place.
# This function return the count to each of the leisure places
def leisure_count(filename):
    place_count = {
        'bandstand': 0,
        'bleachers': 0,
        'casino': 0,
        'common': 0,
        'court': 0,
        'dog_park': 0,
        'escape_game': 0,
        'farm': 0,
        'fitness_centre': 0,
        'garden': 0,
        'golf_course': 0,
        'ice_rink': 0,
        'marina': 0,
        'maze': 0,
        'miniature_golf': 0,
        'nature_reserve': 0,
        'park': 0,
        'pitch': 0,
        'playground': 0,
        'pool': 0,
        'skate_park': 0,
        'slipway': 0,
        'sports_centre': 0,
        'stadium': 0,
        'swimming_pool': 0,
        'track': 0,
        'water_park': 0
    }
    for _, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib["k"] == "leisure":
                    place_count[tag.attrib["v"]] += 1
    sorted_place_count = sorted(place_count.iteritems(), key=operator.itemgetter(1))
    pprint.pprint(sorted_place_count)

    return place_count


#number_of_user()
#get_filesize("sanjose.osm")
#number_of_elems(osm_file)
#tags_in_way(osm_file)
#leisure_kind(osm_file)
leisure_count(osm_file)