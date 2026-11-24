# Lab 3: API data page
# TODO: Rename this file to fit your page. Keep the number at the front, since it sets the
#       page's order in the sidebar (for example, 2_Pokedex.py).
#
# This page shows data from your API, processed with your own Python code. No AI on this page.
# It should have:
#   - at least 2 meaningful user inputs (for example st.selectbox, st.text_input, st.slider)
#   - at least 2 dynamic visuals that change based on the user's input: charts, displays of
#     images, or other visualizations (see the example website for examples!)


import requests
import streamlit as st
import plotly.express as px
import pandas as pd

st.title("What would you like to Learn?")
st.header("Artwork samples are all from the Art Institute of Chicago")

base_url = f"https://api.artic.edu/api/v1/artworks?page=2&limit=45"




Behaviors = st.multiselect(
    "What Data would you like to see about the select paintings?",
    ["Visualization", "Characteristic Statistics"],
)
if st.button("Save Selection"):
    st.session_state["submitted"] = True
    
if st.session_state.get("submitted"):
#Graphs
    if "Characteristic Statistics" in Behaviors:
        
        Domain_True = 0
        Domain_False = 0
        US_counter = 0
        French_counter = 0
        German_counter = 0
        other = 0
        Titles = ""
        Start = 0
        End = 0

        try:
            headers = {"User-Agent": "MyStudentApp/1.0"}
            response = requests.get(base_url, headers=headers)
            if response.status_code == 200:
                artworks = response.json()
                for i in range(len(artworks["data"])):
                    if artworks["data"][i]["is_public_domain"] == True:
                        Domain_True += 1
                    elif artworks["data"][i]["is_public_domain"] == False:
                        Domain_False += 1
                for i in range(len(artworks["data"])):
                    if artworks["data"][i]["place_of_origin"] == "United States":
                        US_counter += 1
                    elif artworks["data"][i]["place_of_origin"] == "France":
                        French_counter += 1
                    elif artworks["data"][i]["place_of_origin"] == "Germany":
                        German_counter += 1
                    else:
                        other += 1
                    

        except ValueError:
            print("Something went wrong")


        Graph_Data = st.radio(
            "Please select the type of that you would like to see",
            ["Public Domains", "Place of Origins", "Start and End Dates"],
        )

        if Graph_Data == "Public Domains":    
            myDict = {
                "Public Domain": int(Domain_True),
                "Not Public Domain": int(Domain_False)
            }
            st.bar_chart(myDict, x_label = "How many artworks are apart of the Public Domain", y_label = "Number of Paintings")
        elif Graph_Data == "Place of Origins":
            myDict = {
                "United States": int(US_counter),
                "France": int(French_counter),
                "Germany": int(German_counter),
                "Other Origins": int(other)
            }
            st.bar_chart(myDict, x_label = "Country of Origins", y_label = "Number of Paintings")
        elif Graph_Data == "Start and End Dates":
            rows = []
            for i in range(len(artworks["data"])):
                Titles = artworks["data"][i]["title"]
                Start = artworks["data"][i]["date_start"]
                End = artworks["data"][i]["date_end"]
                if artworks["data"][i]["date_start"] == None:
                    st.warning(f"{artworks['data'][i]['title']} is not applicable...")
                    continue
                rows.append(
                        dict(
                            Names = Titles,
                            Beginning = f"{int(Start):04d}",
                            Finish = f"{int(End):04d}",
                        )
                    )
            df = pd.DataFrame(rows)
            fig = px.timeline(df, x_start="Beginning", x_end="Finish", y="Names")
            fig.update_yaxes(autorange="reversed") 
            st.plotly_chart(fig)



#Images
    if "Visualization" in Behaviors:
        try:
            headers = {"User-Agent": "MyStudentApp/1.0"}
            response = requests.get(base_url, headers=headers)
            if response.status_code == 200:
                artworks = response.json()
        except:
            print("there is something wrong")

        Color = st.radio(
        "Would you like to meet the artists?",
        ["No thanks!", "Sure why not!"],
        )
        myDict = {}
        if Color == "No thanks!":
            st.warning("Nothing to see")
        elif Color == "Sure why not!":
            for i in range(len(artworks["data"])):
                item = artworks["data"][i]
                artist_list = item.get("artist_titles", [])
                artist = artist_list[0] if artist_list else "Unknown"
                myDict[artist] = myDict.get(artist, 0) + 1

            for artist, count in myDict.items():
                if artist == "Unknown":  
                    st.write(f"There are {count} unknown artists.")
                else:
                    st.write(f"{artist} has {count} artwork(s) from this collection!")
                
        headers = {"User-Agent": "MyStudentApp/1.0"}
        response = requests.get(base_url, headers=headers)
        artworks = response.json()
        image_data = st.radio(
        "Filter Artworks by Type",
        ["Oil on Canvas", "Oil on Panel", "Painting", "Palladium Print", "Other"],
    )
        if "success" not in st.session_state:
            st.session_state["success"] = False

        if st.button("Show Titles"):
            st.session_state["success"] = True

        if image_data == "Oil on Canvas":
            for i in range(len(artworks["data"])):
                if artworks["data"][i]["classification_title"] == "oil on canvas":
                    x = i
                    image_id = artworks["data"][i]["image_id"]
                    image_url= (f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg")
                    headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
            }
                    response = requests.get(image_url, headers=headers)


                    if response.status_code == 200:
                        image_url= (f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg")
                        st.image(response.content, width = 400)
                    else:
                        st.error(f"Failed to load image: {response.status_code}")
                        
                    if st.session_state.get("success"):
                        st.write(artworks["data"][x]["title"])                  

        elif image_data == "Oil on Panel":
            for i in range(len(artworks["data"])):
                if artworks["data"][i]["classification_title"] == "oil on panel":
                    x = i
                    image_id = artworks["data"][i]["image_id"]
                    image_url= (f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg")
                    headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
            }
                    response = requests.get(image_url, headers=headers)

                    if response.status_code == 200:
                        image_url= (f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg")
                        st.image(response.content, width = 400)
                    else:
                        st.error(f"Failed to load image: {response.status_code}")
                    if st.session_state.get("success"):
                        st.write(artworks["data"][x]["title"])
        elif image_data == "Painting":
            for i in range(len(artworks["data"])):
                if artworks["data"][i]["classification_title"] == "painting":
                    x = i
                    image_id = artworks["data"][i]["image_id"]
                    image_url= (f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg")
                    headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
            }
                    response = requests.get(image_url, headers=headers)

                    if response.status_code == 200:
                        image_url= (f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg")
                        st.image(response.content, width = 400)
                    else:
                        st.error(f"Failed to load image: {response.status_code}")
                    if st.session_state.get("success"):
                        st.write(artworks["data"][x]["title"])
        elif image_data == "Palladium Print":
            for i in range(len(artworks["data"])):
                if artworks["data"][i]["classification_title"] == "palladium print":
                    x = i
                    image_id = artworks["data"][i]["image_id"]
                    image_url= (f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg")
                    headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
            }
                    response = requests.get(image_url, headers=headers)

                    if response.status_code == 200:
                        image_url= (f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg")
                        st.image(response.content, width = 400)
                    else:
                        st.error(f"Failed to load image: {response.status_code}")
                    if st.session_state.get("success"):
                        st.write(artworks["data"][x]["title"])
                        
        elif image_data == "Other":
            for i in range(len(artworks["data"])):
                if artworks["data"][i]["classification_title"] != "painting" and artworks["data"][i]["classification_title"] != "oil on panel" and artworks["data"][i]["classification_title"] != "oil on canvas" and artworks["data"][i]["classification_title"] != "palladium print":
                    x = i
                    image_id = artworks["data"][i]["image_id"]
                    image_url= (f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg")
                    headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
            }
                    response = requests.get(image_url, headers=headers)

                    if response.status_code == 200:
                        image_url= (f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg")
                        st.image(response.content, width = 400)
                    else:
                        st.error(f"Failed to load image: {response.status_code}")
                    if st.session_state.get("success"):
                        st.write(artworks["data"][x]["title"])

                



    

