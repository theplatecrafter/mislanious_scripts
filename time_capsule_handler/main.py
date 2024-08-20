import random_functions.main as rf
import os
from datetime import datetime
import colorsys
import folium
from folium.plugins import MarkerCluster


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

def create_interactive_media_map(media_path:str, output_dir:str = "", output_name:str='media_map'):
    """creates media map based on where the media was created. returns the path to the html media map"""

    m = folium.Map()
    map_created = False

    media_files = rf.get_all_file_paths(media_path)

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
        else:
            print(f"Fail {count}/{len(media_files)}: could not load {file_path} to map")

    output_name += ".html"
    if map_created:
        m.save(os.path.join(output_dir,output_name))
        print(f"Interactive map created and saved as {os.path.join(output_dir,output_name)}")
        return os.path.join(output_dir,output_name)
    else:
        print("No media files with location data found.")

