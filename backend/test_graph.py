try:
    from api.culture import app_graph
    print("Graph compiled successfully.")
except Exception as e:
    import traceback
    traceback.print_exc()
