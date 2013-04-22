# def register_geometric_types(connection):
#     import objects

#     for objectname in objects.object_names:
#         obj_class = getattr(objects, objectname)
#         obj_class.register_cast(connection)
#         obj_class.register_adapter()


# from djorm_core.models import connection_handler
# connection_handler.attach_handler(register_geometric_types, vendor="postgresql", unique=True)