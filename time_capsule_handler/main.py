import random_functions.main as rf
from tools import *


TimeCapsulePWDLinux = {
    "general":"/media/hans/Torens_Time_Capsle",
    "unknown date":"/media/hans/Torens_Time_Capsle/Unknown date",
    "other":"/media/hans/Torens_Time_Capsle/0) Other",
    "before 2019":"/media/hans/Torens_Time_Capsle/1) before 2019",
    "2019":"/media/hans/Torens_Time_Capsle/2) 2019",
    "2020":"/media/hans/Torens_Time_Capsle/3) 2020",
    "2021":"/media/hans/Torens_Time_Capsle/4) 2021",
    "2022":"/media/hans/Torens_Time_Capsle/5) 2022",
    "2023":"/media/hans/Torens_Time_Capsle/6) 2023",
    "2024":"/media/hans/Torens_Time_Capsle/7) 2024",
    "2025":"/media/hans/Torens_Time_Capsle/8) 2025"
}


TimeCapsulePWDWindowBASH = {
  "general":"/mnt/e",
}

def get_color_for_date(date_str):
    try:
        date = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
        # Use the day of the year to determine color
        hue = (date.timetuple().tm_yday % 365) / 365.0
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
    except:
        return 'gray'  # Default color if date parsing fails


def create_Geo_Map(media_path:list, output_dir:str = "", output_name:str='media_map'):
    """creates media map based on where the media was created. returns the path to the html media map"""

    m = folium.Map()
    map_created = False

    media_files = []
    for i in media_path:
        for o in rf.get_all_file_paths(i):
            media_files.append(o)

    count = 0
    for file_path in media_files:
        count += 1
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension in ['.jpg', '.jpeg', '.png', '.tiff', '.webp']:
            metadata = rf.get_image_metadata(file_path)
            is_image = True
        elif file_extension in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
            metadata = rf.get_video_metadata(file_path)
            is_image = False
            if metadata is None:
                print(f"Failed to get metadata for video file: {file_path}")
                continue
        else:
            print(f"Unsupported file type: {file_extension}")
            continue

        if metadata and 'GPS Latitude' in metadata and 'GPS Longitude' in metadata:
            lat = metadata['GPS Latitude']
            lon = metadata['GPS Longitude']

            if not map_created:
                m = folium.Map(location=[lat, lon], zoom_start=10)
                map_created = True

            # Create popup content
            popup_content = f"""
            <h3>{os.path.basename(file_path)}</h3>
            <b>Type:</b> {'Image' if is_image else 'Video'}<br>
            <b>Date Taken:</b> {metadata.get('Date Taken', 'Unknown')}<br>
            <b>File Path:</b> {file_path}<br>
            """
            if 'Camera Make' in metadata and 'Camera Model' in metadata:
                popup_content += f"<b>Camera:</b> {metadata['Camera Make']} {metadata['Camera Model']}<br>"
            if 'Width' in metadata and 'Height' in metadata:
                popup_content += f"<b>Resolution:</b> {metadata['Width']}x{metadata['Height']}<br>"
            if 'Duration' in metadata:
                popup_content += f"<b>Duration:</b> {metadata['Duration']:.2f} seconds<br>"

            # Add link to view full-resolution media
            full_res_link = f"file://{os.path.abspath(file_path)}"
            popup_content += f'<a href="{full_res_link}" target="_blank">View Full Resolution</a>'

            # Determine marker color based on creation date
            color = get_color_for_date(metadata.get('Date Taken', ''))

            # Add marker directly to the map
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                popup=folium.Popup(popup_content, max_width=300),
                color=color,
                fill=True,
                fillColor=color
            ).add_to(m)
            print(f"Success {count}/{len(media_files)}: loaded {file_path} to map")

    output_name += ".html"
    if map_created:
        m.save(os.path.join(output_dir,output_name))
        print(f"Interactive map created and saved as {os.path.join(output_dir,output_name)}")
        return os.path.join(output_dir,output_name)
    else:
        print("No media files with location data found.")


def get_date_metadata(path:str):
    out = []
    i = 0
    paths = rf.get_all_file_paths(path)
    for file in paths:
        i += 1
        print(f"{i}/{len(paths)}: ",end="")
        if rf.get_file_type(file) == "video":
            try:
                out.append((rf.get_video_metadata(file)["Date Taken"][:10],file))
                print(f"successfully loaded {file}")
            except:
                out.append(("Unknown Date",file))
                print(f"{file} has no date")
        elif rf.get_file_type(file) == "image":
            try:
                out.append((rf.get_image_metadata(file)["Date Taken"][:10].replace(":","-"),file))
                print(f"successfully loaded {file}")
            except:
                out.append(("Unknown Date",file))
                print(f"{file} has no date")
        else:
            out.append(("Unknown Date",file))
            print(f"{file} is unsupported")
    
    ouOUT = {}
    
    for media in out:
        ouOUT[media[0]] = []
    for media in out:
        ouOUT[media[0]].append(media[1])
    
    sort = sorted(ouOUT)
    out = {}
    for date in sort:
        out[date] = ouOUT[date]
    
    return out


def time_capsule_handler(root:str = None):
    dates_data = {}
    if not root:
        root = rf.prompt_for_path("Please enter the root path ('cancel' to cancel)",must_be_directory=True)
    if not root:
        return
    
    def prompt_user_options():
        print("\n--- Time Capsule Handler ---")
        print("1. Add Media")
        print("2. View Geographical Media Map")
        print("3. Close")
        choice = input("Choose an option (1-3): ")
        return choice
    
    def open_file_dialog():
        path = input("Enter the path to the media folder: ")
        if os.path.isdir(path):
            process_media(path)
        else:
            print("Invalid path! Please try again.")

    def process_media(path):
        dates_metadata = get_date_metadata(path)
        display_dates_menu(dates_metadata)

    def display_dates_menu(dates_metadata):
        for date, files in dates_metadata.items():
            add_date_option(date, files)

        while True:
            print("\n--- Dates Menu ---")
            print("1. Group/Ungroup Dates")
            print("2. Add Media")
            print("3. preview adding media data")
            print("4. redo dates titles/options")
            print("5. Back to Main Menu")
            choice = input("Choose an option: ")

            if choice == "1":
                groupOrUn()
            elif choice == "2":
                confirm_selection()
                break
            elif choice == "3":
                print(dates_data)
                preview_structure()
            elif choice == "4":
                for date, files in dates_metadata.items():
                    add_date_option(date, files)
            elif choice == "5":
                break
            else:
                print("Invalid option! Please try again.")

    def add_date_option(date, files):
        title = ""
        dates_data[date] = {"status": "insignificant", "files": files, "title": title, "addin?": True}
        print(f"\nDate: {date}")
        for file in files:
            print(file)
        if input(f"Mark {date} as significant? (y/N): ").lower() == "y":
            dates_data[date]["status"] = "significant"
        else:
            dates_data[date]["status"] = "insignificant"
        
        if input(f"Add a title for {date}? (y/N): ").lower() == "y":
            while True:
                title = input(f"Enter title for {date} ('cancel' to cancel): ")
                if title == "cancel":
                    title = ""
                    break
                if rf.checkStrValidicityOnPath(title):
                    break
                else:
                    print("Invalid input!")
            dates_data[date]["title"] = title
        else:
            dates_data[date]["title"] = ""
        
        if input(f"Do you want to add media for {date}? (Y/n): ").lower() == "n":
            dates_data[date]["addin?"] = False
        else:
            dates_data[date]["addin?"] = True
        
    def groupOrUn():
        while True:
            print("\n--- Group/Ungroup ---")
            print("1. Group")
            print("2. Ungroup")
            print("3. Back")
            choice = input("Choose an option: ")

            if choice == "1":
                group_selected()
            elif choice == "2":
                select_ungroup()
            elif choice == "3":
                break
            else:
                print("Invalid option! Please try again.")
    
    def select_ungroup():
        """
        Interactive function to allow the user to select a group to ungroup.
        The function will list all groups in dates_data, prompt the user to select one,
        and then call the ungroup() function to ungroup the selected group.
        """
        # Get all group titles from dates_data
        groups = [title for title, data in dates_data.items() if "grouped" in data and data["grouped"]]
        
        if not groups:
            print("No groups available to ungroup.")
            return
        
        # Display all groups to the user
        print("\nAvailable groups:")
        for idx, group in enumerate(groups, 1):
            print(f"  {idx}. {group}")
        
        # Prompt the user to select a group by number
        while True:
            user_input = input("\nSelect a group number to ungroup, or press Enter to cancel: ").strip()
            
            if not user_input:
                print("Ungrouping cancelled.")
                return
            
            try:
                group_idx = int(user_input) - 1
                if 0 <= group_idx < len(groups):
                    group_title = groups[group_idx]
                    # Call ungroup function on the selected group
                    ungroup(group_title)
                    return
                else:
                    print("Invalid selection. Please choose a valid group number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def ungroup(group_title):
        """
        Ungroups the dates from a specified group and moves them back to the main dates_data dictionary.
        The group itself will be removed from dates_data.
        """
        # Check if the group exists in dates_data
        if group_title not in dates_data or "grouped" not in dates_data[group_title]:
            print(f"No group found with the title '{group_title}'.")
            return

        # Retrieve the group data
        group_data = dates_data[group_title]["dates"]

        # Move each date back to the main dictionary
        for date, data in group_data.items():
            dates_data[date] = data

        # Remove the group from dates_data
        del dates_data[group_title]
        print(f"Group '{group_title}' has been removed.")
    
    def group_selected():
        selected_dates = []
        for date in dates_data:
            print(f"{date}: {len(dates_data[date])}")
        for date in dates_data:
            if input(f"Do you want to group {date}? (y/N): ").lower() == "y":
                selected_dates.append(date)
        
        if selected_dates:
            while True:
                group_title = input("Enter a title for the group ('cancel' to cancel): ")
                if group_title == "cancel":
                    print("canceled")
                    return
                if rf.checkStrValidicityOnPath(group_title) and not group_title == "":
                    break
                else:
                    print("Invalid group name")
            create_group(selected_dates, group_title)
        else:
            print("No dates selected for grouping.")
    
    def preview_structure():
        data_dict = {"significant": {}, "insignificant": {}, "grouped": {}}
        
        for date, data in dates_data.items():
            if "grouped" not in data:  # Not a group
                if data["addin?"]:
                    status = data["status"]
                    data_dict[status][date] = {"title": data["title"], "files": data["files"]}
            else:  # It's a group
                group_data = {}
                for grouped_date, grouped_data in data["dates"].items():
                    if grouped_data["addin?"]:
                        group_data[grouped_date] = {"title": grouped_data["title"], "files": grouped_data["files"]}
                data_dict["grouped"][date] = group_data

        def display_layer(current_data, layer_name="root"):
            """
            Recursively display the current layer of the structure and allow navigation.
            """
            while True:
                print(f"\n--- {layer_name} ---")

                # Check if we are at the file level
                if all("files" in item for item in current_data.values()):
                    # Display files for each date
                    for idx, (date, data) in enumerate(current_data.items(), 1):
                        title = data.get("title", "No Title")
                        print(f"{idx}. {date} (Title: {title})")
                        for file_path in data["files"]:
                            print(f"   File: {file_path}")

                    input("\nPress Enter to go back.")
                    return

                # Otherwise, we're still in a layer with categories or groups
                to_be_added = current_data  # This layer's data

                # Display options in numbered format
                if to_be_added:
                    for idx, (date, data) in enumerate(to_be_added.items(), 1):
                        title = data.get("title", "No Title")
                        print(f"{idx}. {date} (Title: {title})")

                # Handle input
                user_input = input("\nSelect a number to explore further, press Enter to go back, or type 'exit' to quit: ").strip()

                # Go back if input is empty
                if not user_input:
                    return

                # Exit
                if user_input.lower() == "exit":
                    print("Exiting preview.")
                    return "exit"

                # Try to process the user's choice
                try:
                    choice_idx = int(user_input) - 1

                    if 0 <= choice_idx < len(to_be_added):
                        date, data = list(to_be_added.items())[choice_idx]

                        # Check if it's a group or a single date with files
                        if isinstance(data, dict) and "files" in data:
                            # Display files for the selected date
                            print(f"\n--- Media for {date} ---")
                            for file_path in data["files"]:
                                print(f"   File: {file_path}")

                            input("\nPress Enter to go back.")
                            return
                        else:
                            # It's a group of dates
                            if display_layer(data, layer_name=f"Group: {date}") == "exit":
                                return "exit"

                except ValueError:
                    print("Invalid input. Please enter a number.")

        # Start the recursive display from the root of the data dictionary
        print("\n--- Preview Media Structure ---")
        categories = ["insignificant", "significant", "grouped"]
        
        while True:
            print("\nAvailable categories:")
            for idx, category in enumerate(categories, 1):
                print(f"  {idx}. {category}")
            
            user_input = input("\nSelect a category (1-3), or type 'exit' to quit: ").strip()

            # Exit option
            if user_input.lower() == "exit":
                print("Exiting preview.")
                break

            # Process category selection
            try:
                category_idx = int(user_input) - 1
                if 0 <= category_idx < len(categories):
                    category_name = categories[category_idx]
                    if category_name in data_dict:
                        # Navigate into the selected category
                        if display_layer(data_dict[category_name], layer_name=category_name) == "exit":
                            break
                    else:
                        print(f"No data available for {category_name}.")
                else:
                    print("Invalid choice. Please select a valid category.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def create_group(selected_dates, group_title):
        group_data = {}
        for date in selected_dates:
            group_data[date] = dates_data.pop(date)
        dates_data[group_title] = {"grouped": True, "dates": group_data}
        print(f"Grouped {', '.join(selected_dates)} under {group_title}")

    def confirm_selection():
        result_data = {"significant": {}, "insignificant": {}, "grouped": {}}
        
        for date, data in dates_data.items():
            if "grouped" not in data:  # Not a group
                if data["addin?"]:
                    status = data["status"]
                    result_data[status][date] = {"title": data["title"], "files": data["files"]}
            else:  # It's a group
                group_data = {}
                for grouped_date, grouped_data in data["dates"].items():
                    if grouped_data["addin?"]:
                        group_data[grouped_date] = {"title": grouped_data["title"], "files": grouped_data["files"]}
                result_data["grouped"][date] = group_data
        
        add_media(result_data,root)
        print("Media added successfully!")
    
    def open_file_chooser_map():
        path = input("Enter the path to the file or folder to view on the geographical map: ")
        if os.path.isdir(path):
            open_map(path)
        else:
            print("Invalid path! Please try again.")

    def open_map(path):
        out = os.path.join(os.getcwd(), "geo_map")
        os.makedirs(out, exist_ok=True)
        dir_name = os.path.basename(path)
        map_path = create_Geo_Map([path], out, f"geo_map_for_{dir_name}")
        webbrowser.open(map_path)
    
    while True:
        user_choice = prompt_user_options()

        if user_choice == "1":
            open_file_dialog()
        elif user_choice == "2":
            open_file_chooser_map()
        elif user_choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")
 
 
def add_media(list,root):
    print(list)
    for date in list["significant"]:
        if date == "Unknown Date":
            home = list["significant"]["Unknown Date"]
            title = home["title"]
            files = home["files"]
            out_dir = os.path.join(root,"Unknown Date")
            for file in files:
                rf.copy_file_path_generative(file,os.path.join(out_dir,os.path.split(file)[1]))
                print(f"copied {file} to {os.path.join(out_dir,os.path.split(file)[1])}")
        else:
            year = int(date[:4])
            month = int(date[5:7])
            day = int(date[8:])
            home = list["significant"][date]
            title = home["title"]
            files = home["files"]
            if year < 2019:
                out_dir = rf.combinePATH([root,"1) before 2019",f"{year}",f"{year}-{month}-{day} {title}"])
            else:
                out_dir = rf.combinePATH([root,f"{year-2017}) {year}",f"{year}-{month}-{day} {title}"])
            for file in files:
                rf.copy_file_path_generative(file,os.path.join(out_dir,os.path.split(file)[1]))
                print(f"copied {file} to {os.path.join(out_dir,os.path.split(file)[1])} y: {year} m: {month} d: {day}")
    
    for date in list["insignificant"]:
        if date == "Unknown Date":
            home = list["insignificant"]["Unknown Date"]
            title = home["title"]
            files = home["files"]
            out_dir = rf.combinePATH([root,"Unknown Date","other"])
            for file in files:
                rf.copy_file_path_generative(file,os.path.join(out_dir,os.path.split(file)[1]))
                print(f"copied {file} to {os.path.join(out_dir,os.path.split(file)[1])}")
        else:
            year = int(date[:4])
            month = int(date[5:7])
            day = int(date[8:])
            home = list["insignificant"][date]
            title = home["title"]
            files = home["files"]
            if year < 2019:
                out_dir = rf.combinePATH([root,"1) before 2019",f"{year}","other",f"{year}-{month}-{day} {title}"])
            else:
                out_dir = rf.combinePATH([root,f"{year-2017}) {year}","other",f"{year}-{month}-{day} {title}"])
            for file in files:
                rf.copy_file_path_generative(file,os.path.join(out_dir,os.path.split(file)[1]))
                print(f"copied {file} to {os.path.join(out_dir,os.path.split(file)[1])} y: {year} m: {month} d: {day}")
    

    for group in list["grouped"]:
        year = []
        month = []
        for date in list["grouped"][group]:
            if int(date[:4]) not in year:
                year.append(int(date[:4]))
            if int(date[5:7]) not in month:
                month.append(int(date[5:7]))
        
        y = rf.list_to_string(year,",")
        m = rf.list_to_string(month,",")
        if year[0] < 2019:
            group_dir = rf.combinePATH([root,"1) before 2019",f"{y}-{m} {group}"])
        else:
            group_dir = rf.combinePATH([root,f"{year-2017}) {year}",f"{y}-{m} {group}"])
        for date in list["grouped"][group]:
            home = list["grouped"][group][date]
            title = home["title"]
            files = home["files"]
            year = int(date[:4])
            month = int(date[5:7])
            day = int(date[8:])
            out_dir = rf.combinePATH([group_dir,f"{year}-{month}-{day} {title}"])
            for file in files:
                rf.copy_file_path_generative(file,os.path.join(out_dir,os.path.split(file)[1]))
                print(f"copied {file} to {os.path.join(out_dir,os.path.split(file)[1])} y: {year} m: {month} d: {day} group: {group}")


def update_tag_list(root):
    tag_path = rf.combinePATH(root,".tags/tags.csv")
    tag_list = rf.combinePATH(root,".tags/tag_types.csv")
    if not rf.check_file_existence(".tags/tags.csv"):
        print(f"initiating tagging system in {root}")
        os.mkdir(rf.combinePATH(root,".tags"))
        open(tag_path,"w")
        open(tag_list,"w")

    
    new_file_paths = set(rf.get_all_file_paths(root))
    
    file =  open(".tags/tags.csv","r")
    reader = csv.reader(file)
    old_file_paths = {row for row in reader}
    
    removed_or_updated = list(old_file_paths - new_file_paths)
    new = list(new_file_paths - old_file_paths)
    
    
