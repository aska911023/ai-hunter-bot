import streamlit as st
from supabase import create_client, Client

# Initialize connection
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def get_all_resources(**kwargs):
    """
    Fetch resources from Supabase with optional filtering.
    """
    try:
        supabase: Client = init_connection()
        query = supabase.table("resources").select("*")

        # 1. Filter by Category
        if "category_filter" in kwargs and kwargs["category_filter"]:
            query = query.eq("category", kwargs["category_filter"])

        # 2. Search Query (Title or Summary)
        if "search_query" in kwargs and kwargs["search_query"]:
            term = kwargs["search_query"]
            # Supabase ilike syntax for OR condition
            # We use % for wildcards
            query = query.or_(f"title.ilike.%{term}%,summary.ilike.%{term}%")

        response = query.execute()
        return response.data if response.data else []
        
    except Exception as e:
        # In case of table not found or other errors, return empty list and let app show message
        print(f"Database Error: {e}")
        return []