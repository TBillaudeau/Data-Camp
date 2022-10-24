import streamlit as st

st.set_page_config(
        page_title="What'Said",
        page_icon="favicon.ico",
)

def main_page():
    st.markdown("")

def sentiment():
    st.markdown("")

def main():
    # Sidebar
    st.sidebar.markdown("# Choose a page 📚")
    st.sidebar.write("")
    st.sidebar.markdown("Access the source files here : [GitHub](https://github.com/TBillaudeau/Data-Camp)")

    # Main Page
    st.markdown("# What'Said 📊")
    st.markdown("## Analyse what is said of an entreprise on Twitter")
    st.markdown("")
    st.markdown("")
    link = '[APP](https://whatsaid.streamlitapp.com/sentiment)'
    st.success("Go to the SENTIMENT "+ link +" 📚 by clicking on the sidebar on the left")
    st.image("images/logo_datacamp.png", use_column_width=True)
    st.write("")
    st.write('> *made by Thomas Billaudeau, Louis Arbey & Pierre-Louis Cretinon.*')
    
if __name__ == "__main__":
    main()