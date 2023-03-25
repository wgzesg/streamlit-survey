import streamlit as st

class Pages(object):
    def __init__(self, n_pages, key="__Pages_curent", on_submit=None):
        """
        Parameters
        ----------
        n_pages: int
            Number of pages
        key: str
            Key to use to store the current page in Streamlit's session state
        on_submit: Callable
            Callback to call when the user clicks the submit button
        
        Example
        -------
        >>> page = Pages(2)
        >>> with page:
        >>>     if page.current == 0:
        >>>         st.text_input("Email address:", id="email")
        >>>     if page.current == 1:
        >>>         st.text_input("Phone number:", id="phone")
        """
        self.n_pages = n_pages
        self.current_page_key = key
        self.on_submit = on_submit

    @property
    def current(self):
        """
        Returns
        -------
        int:
            Current page
        """
        if self.current_page_key not in st.session_state:
            st.session_state[self.current_page_key] = 0
        return st.session_state[self.current_page_key]
    
    @current.setter
    def current(self, value):
        """
        Parameters
        ----------
        value: int
            Current page

        Raises
        ------
        ValueError:
            If the value is out of range
        """
        if value >= 0 and value < self.n_pages - 1:
            st.session_state[self.current_page_key] = value
        else:
            raise ValueError("Page index out of range")

    def previous(self):
        """
        Go to the previous page
        """
        if self.current > 0:
            self.current -= 1

    def next(self):
        """
        Go to the next page
        """
        if self.current < self.n_pages - 1:
            self.current += 1

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        """
        Display the navigation buttons
        """
        left, _, right = st.columns([2, 4, 2])
        with left:
            st.button("Previous", use_container_width=True, disabled=self.current == 0, on_click=self.previous)
        with right:
            if self.current == self.n_pages - 1 and self.on_submit is not None:
                st.button("Submit", type="primary", use_container_width=True, on_click=self.on_submit)
            else:
                st.button("Next", type="primary", use_container_width=True, on_click=self.next, disabled=self.current == self.n_pages - 1)
