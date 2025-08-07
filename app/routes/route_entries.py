from . import (
    auth_route,
    syllabus_route,
    batch_route,
    student_route,
    user_route
)

"""
add your protected route here
"""
PROTECTED_ROUTES = [
    user_route.router,
    syllabus_route.router,
    batch_route.router,
    student_route.router
]


"""
add your public route here
"""
PUBLIC_ROUTES = [
    auth_route.router,
]
