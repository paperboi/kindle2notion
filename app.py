from io import StringIO

import streamlit as st

from kindle2notion.__main__ import (
    update_kindle_clippings_streamlit,
)

st.set_page_config(
    page_title="Kindle 2 Notion",
    page_icon="📓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com/paperboi/kindle2notion",
        "Report a bug": "https://github.com/paperboi/kindle2notion/issues",
        "About": "Streamlit adaptation for [Kindle2Notion library](https://github.com/paperboi/kindle2notion)",
    },
)


def main():
    st.write(
        """
    # Kindle 2 Notion
    
    Streamlit adaptation for [Kindle2Notion library](https://github.com/paperboi/kindle2notion)
    
    ## Prerequisites
    """
    )
    with st.expander("**Show requirements**", expanded=False):
        st.write(
            """ 
    1. Create an integration on Notion.
    
        1. Duplicate this [database template](https://kindle2notion.notion.site/6d26062e3bb04dd89b988806978c1fe7?v=0d394a8162cc481280966b35a37465c2) to your the workspace you want to use for storing your Kindle clippings.
        2. Open _Settings & Members_ from the left navigation bar.
        3. Select the _Integrations_ option listed under _Workspaces_ in the settings modal.
        4. Click on _Develop your own integrations_ to redirect to the integrations page.
        5. On the integrations page, select the _New integration_ option and enter the name of the integration and the workspace you want to use it with. Hit submit and your internal integration token will be generated.
    
    2. Go back to your database page and click on the _Share_ button on the top right corner. Use the selector to find your integration by its name and then click _Invite_. Your integration now has the requested permissions on the new database. 
    """
        )
    form = st.form("kindle_form")
    notion_database_id = form.text_input(
        "Notion Database ID",
        help="""
        Find your _notion_database_id_ from the URL of the database you have copied to your workspace. For reference: 
        
        `https://www.notion.so/myworkspace/a8aec43384f447ed84390e8e42c2e089?v=...` 
        
        **_a8aec43384f447ed84390e8e42c2e089_** is the database_id
        """,
    )
    notion_api_auth_token = form.text_input(
        "Notion API Token",
        type="password",
    )
    clippings_file = form.file_uploader("Upload your clippings file", type=["txt"])
    enable_highlight_date = form.toggle(
        "Enable Highlight Date",
        help="Set to False if you don't want to see the _Date Added_ information in",
    )
    enable_book_cover = form.toggle(
        "Enable Book Cover",
        help="Set to False if you don't want to store the book cover in Notion.",
    )
    clippings_data = None

    submit = form.form_submit_button("Send Kindle Clippings to Notion")
    if submit:
        if clippings_file is not None:
            # To convert to a string based IO:
            stringio = StringIO(clippings_file.getvalue().decode("utf-8-sig"))
            # To read file as string:
            clippings_data = stringio.read()
        with st.spinner("Uploading data to Notion..."):
            update_kindle_clippings_streamlit(
                notion_api_auth_token,
                notion_database_id,
                clippings_data,
                enable_highlight_date,
                enable_book_cover,
            )
        st.success("Kindle Clippings have been synced.")


if __name__ == "__main__":
    main()
