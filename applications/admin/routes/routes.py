import logging
from fastapi import Path
from fastapi import APIRouter
from sqlalchemy import create_engine
from config.database import DatabaseDetails
from applications.admin.rq_rs.admin_rq import UserInput
from applications.admin.rq_rs.admin_rs import AddUserResponse
from applications.admin.utils.db_utils import add_user_details
from applications.admin.utils.db_utils import (
    add_product, get_products, update_product, delete_product,
    add_scenario, get_scenarios_by_product, update_scenario, delete_scenario,
)
from applications.admin.utils.db_utils import delete_user

from applications.admin.rq_rs.admin_rq import (
    ProductRQ, ScenarioRQ
)
from applications.admin.rq_rs.admin_rs import (
    GenericResponse, ProductRS, ScenarioRS
)

logger = logging.getLogger(__name__)

add_user_router = APIRouter()

@add_user_router.post("/api/add-user",
                      response_model=AddUserResponse,
                      response_model_exclude_unset=True)
def add_user_endpoint(user_info: UserInput) -> AddUserResponse:
    logger.info("Received request to add user")
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp=add_user_details(engine,user_info)
    engine.dispose()
    return resp

@add_user_router.delete("/api/admin/user/{user_id}", response_model=GenericResponse)
def delete_user_endpoint(user_id: int):
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = delete_user(engine, user_id)
    engine.dispose()
    return resp
# ---------- PRODUCTS ----------
@add_user_router.post("/api/admin/product", response_model=GenericResponse)
def add_product_endpoint(product_info: ProductRQ):
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = add_product(engine, product_info)
    engine.dispose()
    return resp

@add_user_router.get("/api/admin/product", response_model=ProductRS)
def get_products_endpoint():
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = get_products(engine)
    engine.dispose()
    return resp

@add_user_router.put("/api/admin/product/{product_id}", response_model=GenericResponse)
def update_product_endpoint(
    product_id: int = Path(..., description="ID of the product to update"),
    product_info: ProductRQ = ...
):
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = update_product(engine, product_id, product_info)
    engine.dispose()
    return resp

@add_user_router.delete("/api/admin/product/{product_id}", response_model=GenericResponse)
def delete_product_endpoint(product_id: int):
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = delete_product(engine, product_id)
    engine.dispose()
    return resp

# ---------- SCENARIOS ----------
@add_user_router.post("/api/admin/scenario", response_model=GenericResponse)
def add_scenario_endpoint(scenario_info: ScenarioRQ):
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = add_scenario(engine, scenario_info)
    engine.dispose()
    return resp

@add_user_router.get("/api/admin/scenario/by-product/{product_id}", response_model=ScenarioRS)
def get_scenarios_by_product_endpoint(product_id: int):
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = get_scenarios_by_product(engine, product_id)
    engine.dispose()
    return resp

@add_user_router.put("/api/admin/scenario/{scenario_id}", response_model=GenericResponse)
def update_scenario_endpoint(
    scenario_id: int = Path(..., description="ID of the scenario to update"),
    scenario_info: ScenarioRQ = ...
):
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = update_scenario(engine, scenario_id, scenario_info)
    engine.dispose()
    return resp

@add_user_router.delete("/api/admin/scenario/{scenario_id}", response_model=GenericResponse)
def delete_scenario_endpoint(scenario_id: int):
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    resp = delete_scenario(engine, scenario_id)
    engine.dispose()
    return resp