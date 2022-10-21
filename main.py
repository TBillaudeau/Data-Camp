import streamlit as st

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
    st.markdown("# DataCamp Project 📊")
    st.markdown("")
    st.markdown("")
    st.success("Go to the SENTIMENT app 📚 by clicking on the sidebar on the left")
    st.image("images/logo_datacamp.png", use_column_width=True)
    st.write("")
    st.write('> *made by Thomas Billaudeau, Louis Arbey & Pierre-Louis Cretinon.*')
    
if __name__ == "__main__":
    main()

