import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="About Us",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.title("👥 Our Team")

st.markdown("""
<style>
.team-member {
    padding: 20px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.1);
    margin-bottom: 20px;
}
.linkedin-btn {
    display: inline-block;
    padding: 8px 16px;
    background-color: #d3d3d3;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    margin-top: 10px;
}
.linkedin-btn:hover {
    background-color: #006399;
}
</style>
""",
            unsafe_allow_html=True)

# Create two columns for team members
col1, col2 = st.columns(2)

# Team member information with image paths
team_members = [{
    "name": "Ashrit Kulkarni",
    "role": "Project Lead & Senior AI Solutions Architect",
    "linkedin": "https://www.linkedin.com/in/ashrit-kulkarni/",
    "image": "images/ashrit.jpeg",
    "column": col1
}, {
    "name": "Padmaja Kakulavarapu",
    "role": "Senior Systems Engineer",
    "linkedin": "https://www.linkedin.com/in/padmaja-kakulavarapu/",
    "image": "images/paddu.jpeg",
    "column": col1
}, {
    "name": "Phani Bhushan Kolla",
    "role": "ML Scientist",
    "linkedin": "https://www.linkedin.com/in/phanibhushanksa/",
    "image": "images/phani.jpeg",
    "column": col2
}, {
    "name": "Nagarjuna Kanneganti",
    "role": "Senior AI/ML Engineer",
    "linkedin": "https://www.linkedin.com/in/nagarjuna-kanneganti-20ab218a/",
    "image": "images/naga.jpeg",
    "column": col2
}]


# Function to get base64 encoded image
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        # Return a placeholder if image not found
        return ""


# Display team members with images
for member in team_members:
    with member["column"]:
        image_base64 = get_image_base64(member["image"])

        if image_base64:
            image_html = f'<img src="data:image/jpeg;base64,{image_base64}" style="width:150px; height:220px; border-radius:10%; object-fit:cover;">'
        else:
            # Placeholder image if file not found
            image_html = '<div style="width:150px; height:150px; border-radius:50%; background-color:#e0e0e0; display:flex; align-items:center; justify-content:center;"><span>No Image</span></div>'

        st.markdown(f"""
        <div class="team-member">
            <div style="display:flex; align-items:center;">
                {image_html}
                <div style="margin-left:20px;">
                    <h3>{member["name"]}</h3>
                    <p>{member["role"]}</p>
                    <a href="{member["linkedin"]}" target="_blank" class="linkedin-btn">
                        LinkedIn
                    </a>
                </div>
            </div>
        </div>
        """,
                    unsafe_allow_html=True)

# Footer
st.markdown("---")
