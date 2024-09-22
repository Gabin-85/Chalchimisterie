# This executable is a part of Chalchimisterie project.
# It is used to filter the animation of an entity and 
# rid of all unwanted data.
import json

# Json name here
name = input("Template name: ")
input_file = json.load(open("assets/sprites/"+name+".json", "r"))
output_file = json.load(open("resources/storage/animations.json", "r"))

filtered_data = {}

# Filter all frames
for frame in input_file["frames"]:
    del frame["filename"]
    del frame["rotated"]
    del frame["trimmed"]
    del frame["spriteSourceSize"]
    del frame["sourceSize"]
filtered_data["frames"] = input_file["frames"]

# Filter all tags
for tag in input_file["meta"]["frameTags"]:
    del tag["color"]
    del tag["direction"]
    try: 
        del tag["data"]
    except KeyError:
        pass
filtered_data["anim"] = {}
for tag in input_file["meta"]["frameTags"]:
    filtered_data["anim"][tag["name"]] = {"from": tag["from"], "to": tag["to"]}
filtered_data["total_size"] = input_file["meta"]["size"]
filtered_data["file"] = name+".png"

# Write the new json
print("Here is the file: ")
print(json.dumps(filtered_data, indent=4)+"\n")

# Ask if okay or not
if input("Is the json okay? (y/n) ").lower() == "y":
    output_file[name] = filtered_data
    json.dump(output_file, open("resources/storage/animations.json", "w"), indent=4)
    print("Done!")
else:
    print("Aborted!")

