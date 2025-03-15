from client_supabase import supabase


# def cargar_clientes():
#     """Carga los clientes desde Supabase."""
#     try:
#         response = supabase.table("clientes").select("*").execute()
#         return response.data
#     except Exception as e:
#         print(f"Error al cargar los clientes{e}")
#         return []
