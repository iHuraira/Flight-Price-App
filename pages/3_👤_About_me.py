import streamlit as st

col_first, col_second = st.columns(2, gap="large", vertical_alignment="top")

with col_first:
    st.image("assets/edited.png", width=250)
    pass

with col_second:
    st.title("M. Hurrarah", anchor=False)
    st.write("**Bioinformatician** **|** **Data Scientist** ")
    st.markdown(
    """
    <div style="text-align: justify; margin: 10px 0px">
        Passionate about translating complex biological data into actionable knowledge.
    </div>
    """, 
    unsafe_allow_html=True)
    # st.write("Passionate about translating complex biological data into actionable knowledge.")
    st.markdown(
    """
    <div style="text-align: justify;">
        <b>Interests</b> Computational Biology, Artificial Intelligence, Data Science
    </div>
    """, 
    unsafe_allow_html=True)
    # st.write("**Interests** Computational Biology, Artificial Intelligence, Data Science")


# Justified text sections
st.write("### About Me")
st.markdown(
    """
    <div style="text-align: justify;">

I am a biotech graduate with a strong foundation in bioinformatics and machine learning. I have hands-on experience in developing bioinformatics tools for pangenome and phylogenetic analysis. My technical skills include proficiency in Python and JavaScript, which I leverage to create innovative solutions in genomics and computational biology.

I began my career as a Research Assistant at NUST in Pakistan, where I gained valuable experience in bioinformatics research. Later, I expanded my professional horizon by moving to Germany on a fellowship, which eventually led to a full-time position as a Bioinformatician at MHH (Hannover Medical School).

Currently, I am deepening my expertise in artificial intelligence to further enhance my ability to tackle complex datasets and contribute to the next generation of bioinformatics tools and methodologies.
    </div>
    """, 
    unsafe_allow_html=True
)

skills_col_one, skills_col_two = st.columns(2)

skills_expander = st.expander(label="Skills & Expertise", icon=":material/online_prediction:")

with skills_expander:
    st.markdown(
        """
        <div>
        <b>Data Analysis & Programming</b> <br> 
        <blockquote>Proficient in Python for data analysis, scripting, and automation. Experienced with libraries such as pandas, NumPy, and matplotlib for handling and visualizing biological datasets.</blockquote>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div>
        <b>Genomic Data Analysis</b> <br> 
        <blockquote>Hands-on experience analyzing genomic data using Python-based tools like Biopython and custom scripts for pangenome and phylogenetic studies.</blockquote>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div>
        <b>Machine Learning & AI</b> <br> 
        <blockquote>Familiar with building ML models using scikit-learn. Interested in applying AI to solve biological and medical data problems.</blockquote>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div>
        <b>Statistical Modeling</b> <br> 
        <blockquote>Comfortable applying statistical concepts for data interpretation using Python. Experienced in regression analysis and hypothesis testing.</blockquote>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div>
        <b>Web Development & Visualization</b> <br> 
        <blockquote>Built web interfaces using Vue.js and React.js, styled with Tailwind CSS and Sass. Familiar with creating interactive components for scientific dashboards.</blockquote>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div>
        <b>Containerization & Deployment</b> <br> 
        <blockquote>Basic knowledge of Docker for packaging applications. Experience deploying Streamlit apps and using GitHub for version control.</blockquote>
        </div>
        """, 
        unsafe_allow_html=True
    )

        
st.write("### Contact Me")
st.write("Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/hurrarah/).")


footer = """
<style>
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #f1f1f1;
    color: #000;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    border-top: 1px solid #e1e1e1;
}
</style>
<div class="footer">
    ⏱️ Built with ❤️ using Streamlit | © 2025 Your Name or Company
</div>
"""

st.markdown(footer, unsafe_allow_html=True)