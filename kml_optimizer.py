# Connor Sanders
# 10/13/2017
# KML File Optimization

# Usage Example
# python kml_optimizer.py "kml_file" "sensitivity"
# python kml_optimizer.py "England local council overlay.kml" "medium"

# TODO
# Loosen up kml file format requirements needed for script to work

import os
import sys

# Script common variables
cwd = os.getcwd()
os_system = os.name
if os_system == 'nt':
    data_dir = cwd + '\\kml_data\\'
    output_dir = cwd + '\\optimized_files\\'
else:
    data_dir = cwd + '/kml_data/'
    output_dir = cwd + '/optimized_files/'
opt_dict = {'low': 0.000001, 'medium': 0.00001, 'high': 0.0001}


# Function to open and read data
def get_kml_data(kml_file):
    kml_data_list = []
    opened_kml_file = open(data_dir + kml_file)
    for data_row in opened_kml_file:
        kml_data_list.append(data_row)
    opened_kml_file.close()
    return kml_data_list


# Function to parse coordinate data from kml file data and build coordinate dictionary with
def build_coord_obj(kml_data_list):
    coord_dict = {}
    coords_list = []
    multi_coords_list = []
    place_name = ''
    placemark = False
    coords = False
    for data_row in kml_data_list:
        if '<Placemark>' in data_row:
            placemark = True
        elif '</Placemark>' in data_row:
            dict_ent = {place_name: multi_coords_list}
            coord_dict.update(dict_ent)
            multi_coords_list = []
            placemark = False
        if placemark:
            if coords:
                if '</coordinates>' not in data_row:
                    coords_list.append(str(data_row).replace('\n', '').replace(' ', ''))
                else:
                    coords = False
                    multi_coords_list.append(coords_list)
                    coords_list = []
            if '<name>' in data_row and '</name>' in data_row:
                place_name = str(data_row).split('<name>')[1].split('</name>')[0]
            elif '<coordinates>' in data_row:
                coords = True
    return coord_dict


# Function to determine optimizer value from user sensitivity input
def get_opt_value(sensitivity):
    lower_sensitivity = sensitivity.lower()
    opt_value = opt_dict[lower_sensitivity]
    return opt_value


# Function to build coordinate string
def construct_coord_str(cur_lat, cur_longi, cur_alt):
    coords_string = cur_lat + ',' + cur_longi
    if cur_alt == '':
        coords_string += '\n'
    else:
        coords_string += ',' + cur_alt + '\n'
    return coords_string


# Function to optimize coordinates
def optimize_kml_coordinates(kml_data_dict, optimizer_val):
    optimized_data_dict = {}
    for place_name, raw_multi_coords_list in kml_data_dict.items():
        opt_multi_coords_list = []
        for raw_coords_list in raw_multi_coords_list:
            list_len = len(raw_coords_list) - 1
            i = 0
            prev_lat = ''
            prev_longi = ''
            opt_coords_list = []
            for raw_coords_set in raw_coords_list:
                cur_lat = raw_coords_set.split(',')[0]
                cur_longi = raw_coords_set.split(',')[1]
                cur_alt = ''
                if len(raw_coords_set.split(',')) == 3:
                    cur_alt = raw_coords_set.split(',')[2]
                if i == 0 or i == list_len:
                    coords_string = construct_coord_str(cur_lat, cur_longi, cur_alt)
                    opt_coords_list.append(coords_string)
                if 0 < i < list_len:
                    delta_lat = abs(float(cur_lat) - float(prev_lat))
                    delta_longi = abs(float(cur_longi) - float(prev_longi))
                    if delta_lat > optimizer_val and delta_longi > optimizer_val:
                        coords_string = construct_coord_str(cur_lat, cur_longi, cur_alt)
                        opt_coords_list.append(coords_string)
                prev_lat = cur_lat
                prev_longi = cur_longi
                i += 1
            opt_multi_coords_list.append(opt_coords_list)
        dict_ent = {place_name: opt_multi_coords_list}
        optimized_data_dict.update(dict_ent)
    return optimized_data_dict


# Function to write data to new KML file
def create_output_data_list(opti_dict, raw_data_list):
    output_data_list = []
    placemark = False
    coord = False
    opt_coord_set = []
    i = 0
    for raw_data_row in raw_data_list:
        if '<' in raw_data_row and '>' in raw_data_row:
            output_data_list.append(raw_data_row)
        if '<Placemark>' in raw_data_row:
            placemark = True
        elif '</Placemark>' in raw_data_row:
            placemark = False
        if placemark:
            if coord:
                set_len = len(opt_coord_set)
                if i < set_len:
                    if set_len > 1:
                        space_string = '                  '
                    else:
                        space_string = '                '
                    sel_set = opt_coord_set[i]
                    for opt_coords in sel_set:
                        output_data_list.append(space_string + opt_coords)
                    i += 1
                    coord = False
                else:
                    i = 0
            if '<coordinates>' in raw_data_row:
                coord = True
            if '<name>' in raw_data_row and '</name>' in raw_data_row:
                place_name = str(raw_data_row).split('<name>')[1].split('</name>')[0]
                opt_coord_set = opti_dict[place_name]
    return output_data_list


# Function to create output file and write optimized data to it
def create_output_file(output_data_list, file_name, sensitivity):
    out_file_name = sensitivity.lower() + '_optimized_' + file_name
    opened_out_file = open(output_dir + out_file_name, 'wt')
    for data_row in output_data_list:
        opened_out_file.write(data_row)
    opened_out_file.close()


# Main Function
def main(file_name, sensitivity):
    try:
        raw_data_list = get_kml_data(file_name)
        coord_dict = build_coord_obj(raw_data_list)
        optimizer_val = get_opt_value(sensitivity)
        optimized_dict = optimize_kml_coordinates(coord_dict, optimizer_val)
        output_data_list = create_output_data_list(optimized_dict, raw_data_list)
        create_output_file(output_data_list, file_name, sensitivity)
        print(sensitivity.lower() + ' sensitivity optimization process on ' + file_name + ' is complete!')
    except:
        print('There was an error with the process!\n Please ensure you entered the full file name with the extension.')
        print('Also please ensure you entered either low, medium, or high as the sensitivity setting.')
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])