from . import (
    auth_route,
    super_admin_route,
    syllabus_route
    )

"""
add your protected route here
"""
PROTECTED_ROUTES = [
    super_admin_route.router,
    syllabus_route.router
]


"""
add your public route here
"""
PUBLIC_ROUTES = [
    auth_route.router,
]
