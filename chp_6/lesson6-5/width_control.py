import streamlit as st

def select_block_container_style():
    """Add selection section for setting setting the max-width and padding
    of the main block container"""
    st.sidebar.header("Block Container Style")
    max_width_100_percent = st.sidebar.checkbox("Max-width: 100%?", False)
    if not max_width_100_percent:
        max_width = st.sidebar.slider("Select max-width in px", 100, 2000, 1200, 100)
    else:
        max_width = 1200
    dark_theme = st.sidebar.checkbox("Dark Theme?", False)
    padding_top = st.sidebar.number_input("Select padding top in rem", 0, 200, 5, 1)
    padding_right = st.sidebar.number_input("Select padding right in rem", 0, 200, 1, 1)
    padding_left = st.sidebar.number_input("Select padding left in rem", 0, 200, 1, 1)
    padding_bottom = st.sidebar.number_input(
        "Select padding bottom in rem", 0, 200, 10, 1
    )
    if dark_theme:
        BACKGROUND_COLOR = "rgb(17,17,17)"
        COLOR = "#fff"

    else:
        BACKGROUND_COLOR = "rgb(255,255,255)"
        COLOR = "#000"

    _set_block_container_style(
        BACKGROUND_COLOR,
        COLOR,
        max_width,
        max_width_100_percent,
        padding_top,
        padding_right,
        padding_left,
        padding_bottom,
    )


def _set_block_container_style(
    bg_color: str,
    color: str,
    max_width: int = 1200,
    max_width_100_percent: bool = False,
    padding_top: int = 5,
    padding_right: int = 1,
    padding_left: int = 1,
    padding_bottom: int = 10,
):
    if max_width_100_percent:
        max_width_str = f"max-width: 100%;"
    else:
        max_width_str = f"max-width: {max_width}px;"
    st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        {max_width_str}
        padding-top: {padding_top}rem;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: {padding_bottom}rem;
    }}
    .reportview-container .main {{
        color: {color};
        background-color: {bg_color};
    }}
</style>
""",
        unsafe_allow_html=True,
    )
