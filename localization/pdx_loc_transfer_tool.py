# By 1230james
# 2023-11-13
# Copies definitions from a source YML file to a specified output YML file, replacing all matching keys found in the
# output file with the definitions from the source file whilst maintaining the structure of the output file.

import sys
import os

# ==================================================================================================================== #

def get_key(line):
    start_index = len(line) - len(line.lstrip())
    end_index   = line.find(":")
    
    if end_index != -1:
        return line[start_index : end_index]
        
    else:
        return None
    
def get_value(line):
    start_index = line.find('"')
    end_index   = line.rfind('"')
    if start_index != -1 and end_index != -1:
        return line[start_index + 1 : end_index]
    return None

def process_lines(in_lines, out_lines):
    data = dict()
    
    for line in in_lines:
        key = get_key(line)
        if key != None and len(key) > 0 and key[0] != "#":
            # print(f"Found key `{key}`")
            value     = get_value(line)
            if value != None:
                # print(f"Found value `{value}`")
                data[key] = value
    
    # lazy programming => high inefficiency baybee
    for key, value in data.items():
        found = False
        for i, line in enumerate(out_lines):
            out_key = get_key(line)
            if key == out_key:
                # print(f"Replacing key `{key}`")
                
                out_lines[i] = line[: line.find('"') + 1] + value + line[line.rfind('"') :]
                
                found = True
                break
        if not found:
            print(f"Did not find key `{key}` in output file; skipping...")
            
    # Cleanup (remove Crowdin-isms)
    for i, line in enumerate(out_lines):
        out_lines[i] = line.replace('\\"', '"')

# ==================================================================================================================== #

print("Localization Transfer Tool - by 1230james")

argc     = len(sys.argv)
in_path  = "english"
out_path = "test"
if argc == 3:
    in_path  = sys.argv[1]
    out_path = sys.argv[2]
    
in_file  = open(in_path,  "r",  encoding="utf-8-sig")
out_file = open(out_path, "r+", encoding="utf-8-sig")

in_lines  = in_file.read().splitlines(True)
out_lines = out_file.read().splitlines(True)

process_lines(in_lines, out_lines)

out_file.seek(0)
out_file.truncate(0)
out_file.write("".join(out_lines))
out_file.close()
in_file.close()
print(f"Completed transferring values from {in_path} to {out_path}")