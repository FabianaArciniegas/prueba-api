from api.auth.controllers.auth_controller import auth_router
from api.products.controllers.products_controller import products_router
from api.users.controllers.users_controller import users_router

routes: list = [users_router, products_router, auth_router]
