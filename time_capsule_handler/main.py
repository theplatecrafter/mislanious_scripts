import random_functions.main as rf
import os
from datetime import datetime
import colorsys
import folium



TimeCapsulePWDLinux = {
    "general":"/media/hans/Toren's Time Capsle",
    "unknown date":"/media/hans/Toren's Time Capsle/Unknown date",
    "other":"/media/hans/Toren's Time Capsle/0) Other",
    "before 2019":"/media/hans/Toren's Time Capsle/1) before 2019",
    "2019":"/media/hans/Toren's Time Capsle/2) 2019",
    "2020":"/media/hans/Toren's Time Capsle/3) 2020",
    "2021":"/media/hans/Toren's Time Capsle/4) 2021",
    "2022":"/media/hans/Toren's Time Capsle/5) 2022",
    "2023":"/media/hans/Toren's Time Capsle/6) 2023",
    "2024":"/media/hans/Toren's Time Capsle/7) 2024",
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


def create_interactive_media_map(media_path:list, output_dir:str = "", output_name:str='media_map'):
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
    for file in rf.get_all_file_paths(path):
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


def add_media():
    """a concel centered media adder"""
    # Get metadata for each file (dates and associated files)
    root = rf.prompt_for_path("Please enter root directory ('cancel' to cancel)",must_be_directory=True)
    path = rf.prompt_for_path("Please enter media path (glob accepted) ('cancel' to cancel)",allow_glob=True)
    dates_metadata = get_date_metadata(path)
    
    # Store the status (significant/insignificant) and title for each date
    dates_data = {}
    # Loop through each date and its associated files
    for date, files in dates_metadata.items():
        print(f"\nDate: {date} ({len(files)} files)")
        
        # Display the list of files
        for idx, file in enumerate(files, start=1):
            print(f"  {idx}. {file}")
        
        # Ask the user if the date is significant
        while True:
            status = input("Is this date significant? (yes/no): ").strip().lower()
            if status in ["yes", "no"]:
                status = "significant" if status == "yes" else "insignificant"
                break
            else:
                print("Invalid input. Please type 'yes' or 'no'.")
        
        # Ask the user for an optional title for the date
        title = input(f"Enter a title for {date} (optional, press Enter to skip): ").strip()
        
        # Store the date information
        dates_data[date] = {"status": status, "files": files, "title": title}
    
    # Prepare the result data to send to add_media
    result_data = {"significant": {}, "insignificant": {}}
    
    for date, data in dates_data.items():
        category = result_data[data["status"]]
        category[date] = {"title": data["title"], "files": data["files"]}
    
    DEVadd_media(result_data,root)
    
    
def DEVadd_media(list,root):
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
                out_dir = rf.combinePATH([root,"1) before 2019",f"{year}",f"{year}-{month}-{day}{title}"])
            else:
                out_dir = rf.combinePATH([root,f"{year-2017}) {year}",f"{year}-{month}-{day}{title}"])
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
                out_dir = rf.combinePATH([root,"1) before 2019",f"{year}","other",f"{year}-{month}-{day}{title}"])
            else:
                out_dir = rf.combinePATH([root,f"{year-2017}) {year}","other",f"{year}-{month}-{day}{title}"])
            for file in files:
                rf.copy_file_path_generative(file,os.path.join(out_dir,os.path.split(file)[1]))
                print(f"copied {file} to {os.path.join(out_dir,os.path.split(file)[1])} y: {year} m: {month} d: {day}")
    
    for group in list["grouped"]:
        for date in list["grouped"][group]:
            home = list["grouped"][group][date]
            title = home["title"]
            files = home["files"]
            if year < 2019:
                out_dir = rf.combinePATH([root,"1) before 2019"])
