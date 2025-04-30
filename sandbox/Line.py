import re
from collections import Counter
import plotly.graph_objects as go
from plotly.offline import offline
import json
import datetime

def create_interactive_chat_report_html(filename: str, output_filename: str = 'interactive_chat_report.html'):
    """Generates an interactive HTML report from chat log data with improved styling, tabs, and user filtering."""

    messages = []
    links = []
    current_date = None

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        date_match = re.match(r'(\d{4}\.\d{2}\.\d{2} [A-Za-z]+)', line)
        if date_match:
            current_date = date_match.group(1)
            continue

        time_match = re.match(r'(\d{2}:\d{2}) (.*)', line)
        if time_match:
            time = time_match.group(1)
            rest = time_match.group(2)

            sender_message = rest.split(' ', 1)
            if len(sender_message) == 2:
                sender, message = sender_message
            else:
                sender = rest
                message = ""

            if sender in ["Message", "Photos", "Word", "Videos", "Stickers", "Audio"]:
                if sender == "Message":
                    sender = "Hans"
                    message = "unsent a message"
                else:
                    message = "unsent a message"
                    sender = "Unknown"

            messages.append({
                'date': current_date,
                'time': time,
                'sender': sender,
                'message': message,
            })

            url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
            urls = url_pattern.findall(message)
            for url in urls:
                links.append({
                    'date': current_date,
                    'time': time,
                    'sender': sender,
                    'url': url
                })

    sender_counts = Counter(message['sender'] for message in messages)
    unique_senders = sorted(list(sender_counts.keys()))
    sender_options = "".join([f'<option value="{sender}">{sender}</option>' for sender in unique_senders])

    # Graph generation:

    # Bar Graph (Sender Message Count):
    fig_sender_count = go.Figure(data=[go.Bar(x=list(sender_counts.keys()), y=list(sender_counts.values()))])
    fig_sender_count.update_layout(title='Message Count by Sender', xaxis_title='Sender', yaxis_title='Message Count')
    div_sender_count = offline.plot(fig_sender_count, include_plotlyjs='cdn', output_type='div')

    # Pie Chart (Sender Message Distribution):
    fig_sender_pie = go.Figure(data=[go.Pie(labels=list(sender_counts.keys()), values=list(sender_counts.values()))])
    fig_sender_pie.update_layout(title='Sender Message Distribution')
    div_sender_pie = offline.plot(fig_sender_pie, include_plotlyjs='cdn', output_type='div')

    # Stacked Bar Graph (Message Types):
    message_types = ["message", "Photos", "Videos", "Stickers", "Audio"]
    sender_message_types = {sender: {msg_type: 0 for msg_type in message_types} for sender in unique_senders}
    for msg in messages:
        sender = msg["sender"]
        for msg_type in message_types:
            if msg["message"] == msg_type:
                sender_message_types[sender][msg_type] += 1
            elif msg_type == "message" and msg["message"] != "unsent a message" and msg["message"] not in message_types:
                sender_message_types[sender][msg_type] += 1

    fig_message_types = go.Figure(data=[go.Bar(name=msg_type, x=unique_senders, y=[sender_message_types[sender][msg_type] for sender in unique_senders]) for msg_type in message_types])
    fig_message_types.update_layout(title='Message Types by Sender', barmode='stack')
    div_message_types = offline.plot(fig_message_types, include_plotlyjs='cdn', output_type='div')

    # Bar Graph (Links Shared Per Sender):
    link_counts = Counter(link['sender'] for link in links)
    fig_link_sender = go.Figure(data=[go.Bar(x=list(link_counts.keys()), y=list(link_counts.values()))])
    fig_link_sender.update_layout(title='Links Shared Per Sender', xaxis_title='Sender', yaxis_title='Link Count')
    div_link_sender = offline.plot(fig_link_sender, include_plotlyjs='cdn', output_type='div')

    # Bar Graph (Media/Action Counts):
    media_action_counts = {"Photos": 0, "Videos": 0, "Stickers": 0, "Audio": 0, "Profile Changes": 0, "Members Added": 0, "Notes Added": 0}
    for msg in messages:
        if msg["message"] == "Photos":
            media_action_counts["Photos"] += 1
        elif msg["message"] == "Videos":
            media_action_counts["Videos"] += 1
        elif msg["message"] == "Stickers":
            media_action_counts["Stickers"] += 1
        elif msg["message"] == "Audio":
            media_action_counts["Audio"] += 1
        elif "changed the group's profile picture" in msg["message"]:
            media_action_counts["Profile Changes"] += 1
        elif "added " in msg["message"]:
            media_action_counts["Members Added"] += len(msg["message"].split("added ")[1].split(","));
        elif "Added a new note." in msg["message"]:
            media_action_counts["Notes Added"] += 1

    fig_media_actions = go.Figure(data=[go.Bar(x=list(media_action_counts.keys()), y=list(media_action_counts.values()))])
    fig_media_actions.update_layout(title='Media and Action Counts', xaxis_title='Action', yaxis_title='Count')
    div_media_actions = offline.plot(fig_media_actions, include_plotlyjs='cdn', output_type='div')

    # Line Graph (Message Activity Over Time):
    daily_message_counts = Counter(msg['date'] for msg in messages)
    dates = sorted(list(daily_message_counts.keys()))
    message_counts = [daily_message_counts[date] for date in dates]
    fig_message_activity = go.Figure(data=[go.Scatter(x=dates, y=message_counts, mode='lines+markers')])
    fig_message_activity.update_layout(title='Message Activity Over Time', xaxis_title='Date', yaxis_title='Message Count')
    div_message_activity = offline.plot(fig_message_activity, include_plotlyjs='cdn', output_type='div')

    json_messages = json.dumps(messages)

    if links:
        link_list_html = "".join([f'<li><strong>{link["date"]} {link["time"]} {link["sender"]}:</strong> <a href="{link["url"]}" target="_blank">{link["url"]}</a></li>' for link in links])
    else:
        link_list_html = "<li>No links found.</li>"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Interactive Line Chat Report</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: sans-serif; margin: 20px; }}
            .tab {{ overflow: hidden; border: 1px solid #ccc; background-color: #f1f1f1; }}
            .tab button {{ background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; transition: 0.3s; }}
            .tab button:hover {{ background-color: #ddd; }}
            .tab button.active {{ background-color: #ccc; }}
            .tabcontent {{ display: none; padding: 6px 12px; border: 1px solid #ccc; border-top: none; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
            strong {{ color: #007bff; }}
            select {{ padding: 8px; margin-bottom: 10px; width: 200px; }}
            .collapsible {{ background-color: #eee; color: #444; cursor: pointer; padding: 18px; width: 100%; border: none; text-align: left; outline: none; font-size: 15px; }}
            .active, .collapsible:hover {{ background-color: #ccc; }}
            .content {{ padding: 0 18px; display: none; overflow: hidden; background-color: #f1f1f1; }}
        </style>
    </head>
        <body>
            <h1>Interactive Line Chat Report</h1>
            <div class="tab">
                <button class="tablinks active" onclick="openTab(event, 'graph')">Graphs</button>
                <button class="tablinks" onclick="openTab(event, 'messages')">Messages</button>
                <button class="tablinks" onclick="openTab(event, 'links')">Links</button>
            </div>
            <div id="graph" class="tabcontent" style="display:block;">
                <div class = "tab">
                    <button class = "tablinks active" onclick = "openTab(event,'sender_messages')">Sender Messages</button>
                    <button class = "tablinks" onclick = "openTab(event,'message_types')">Message Types</button>
                    <button class = "tablinks" onclick = "openTab(event,'media_actions')">Media and Actions</button>
                    <button class = "tablinks" onclick = "openTab(event,'message_activity')">Message Activity</button>
                    <button class = "tablinks" onclick = "openTab(event, 'links_shared')">Links Shared</button>
                </div>
                <div id = "sender_messages" class = "tabcontent" style = "display:block;">
                    <h2>Message Count by Sender</h2>
                    {div_sender_count}
                    <h2>Sender Message Distribution</h2>
                    {div_sender_pie}
                </div>
                <div id = "message_types" class = "tabcontent">
                    <h2>Message Types by Sender</h2>
                    {div_message_types}
                </div>
                <div id = "media_actions" class = "tabcontent">
                    <h2>Media and Action Counts</h2>
                    {div_media_actions}
                </div>
                <div id = "message_activity" class = "tabcontent">
                    <h2>Message Activity Over Time</h2>
                    {div_message_activity}
                </div>
                <div id = "links_shared" class = "tabcontent">
                    <h2>Links Shared Per Sender</h2>
                    {div_link_sender}
                </div>
            </div>
            <div id="messages" class="tabcontent">
                <h2>Message List</h2>
                <select id="senderFilter" onchange="filterMessages()">
                    <option value="All">All Senders</option>
                    REPLACE_SENDER_OPTIONS
                </select>
                <button class="collapsible" onclick="collapser()">Show Datas</button>
                <div id = "statsContent" class = "content">
                    <p>Total Message Count: <span id="totalCount">0</span></p>
                    <p>Unsent Message Count: <span id="unsentCount">0</span></p>
                    <p>Photos Sent: <span id="photoCount">0</span></p>
                    <p>Videos Sent: <span id="videoCount">0</span></p>
                    <p>Stickers Sent: <span id="stickerCount">0</span></p>
                    <p>Audios Sent: <span id="audioCount">0</span></p>
                    <p>Profile Picture Changes: <span id="profilePicChanges">0</span></p>
                    <p>Members Added: <span id="membersAdded">0</span></p>
                    <p>Notes Added: <span id="notesAdded">0</span></p>
                </div>
                <ul id="messageList">
                </ul>
            </div>
            <div id="links" class="tabcontent">
                <h2>Links</h2>
                <ul>
                    {link_list_html}
                </ul>
            </div>
            <script>
                function openTab(evt, tabName) {{
                    var i, tabcontent, tablinks;
                    tabcontent = document.getElementsByClassName("tabcontent");
                    for (i = 0; i < tabcontent.length; i++) {{
                        tabcontent[i].style.display = "none";
                    }}
                    tablinks = document.getElementsByClassName("tablinks");
                    for (i = 0; i < tablinks.length; i++) {{
                        tablinks[i].className = tablinks[i].className.replace(" active", "");
                    }}
                    document.getElementById(tabName).style.display = "block";
                    evt.currentTarget.className += " active";
                }}

                function filterMessages() {{
                    var selectedSender = document.getElementById("senderFilter").value;
                    var messageList = document.getElementById("messageList");
                    var messages = REPLACE_MESSAGES;
                    messageList.innerHTML = "";

                    var totalCount = 0;
                    var unsentCount = 0;
                    var photoCount = 0;
                    var videoCount = 0;
                    var stickerCount = 0;
                    var audioCount = 0;
                    var profilePicChanges = 0;
                    var membersAdded = 0;
                    var notesAdded = 0;

                    messages.forEach(function(message) {{
                        if (selectedSender === "All" || message.sender === selectedSender) {{
                            messageList.innerHTML += "<li><strong>" + message.date + " " + message.time + " " + message.sender + ":</strong> " + message.message + "</li>";
                            totalCount++;
                            if (message.message === "unsent a message") {{
                                unsentCount++;
                            }} else if (message.message === "Photos") {{
                                photoCount++;
                            }} else if (message.message === "Videos") {{
                                videoCount++;
                            }} else if (message.message === "Stickers") {{
                                stickerCount++;
                            }} else if (message.message === "Audio") {{
                                audioCount++;
                            }} else if (message.message.includes("changed the group's profile picture")) {{
                                profilePicChanges++;
                            }} else if (message.message.includes("added ")) {{
                                membersAdded += message.message.split("added ")[1].split(",").length;
                            }} else if (message.message.includes("Added a new note.")){{
                                notesAdded++;
                            }}
                        }}
                    }});
                    document.getElementById("totalCount").textContent = totalCount;
                    document.getElementById("unsentCount").textContent = unsentCount;
                    document.getElementById("photoCount").textContent = photoCount;
                    document.getElementById("videoCount").textContent = videoCount;
                    document.getElementById("stickerCount").textContent = stickerCount;
                    document.getElementById("audioCount").textContent = audioCount;
                    document.getElementById("profilePicChanges").textContent = profilePicChanges;
                    document.getElementById("membersAdded").textContent = membersAdded;
                    document.getElementById("notesAdded").textContent = notesAdded;
                }}

                function collapser() {{
                    var content = document.getElementById("statsContent");
                    if (content.style.display === "block") {{
                        content.style.display = "none";
                    }} else {{
                        content.style.display = "block";
                    }}
                }}

                document.getElementsByClassName("tablinks")[0].click();
                filterMessages();
                document.getElementsByClassName("tablinks")[1].click();
            </script>
        </body>
        </html>
    """

    html_content = html_content.replace('REPLACE_MESSAGES', json_messages).replace('REPLACE_SENDER_OPTIONS', sender_options).replace('{link_list_html}', link_list_html)

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)






filename = '/media/hans/Torens_Time_Capsle/0) Other/6) Other Shortcuts/高校生活/東工大付属（２C～３C）ラインメッセージ.txt'  # テキストファイルのパスを指定
filename = "/mnt/f/0) Other/6) Other Shortcuts/高校生活/東工大付属（２C～３C）ラインメッセージ.txt"
create_interactive_chat_report_html(filename)
