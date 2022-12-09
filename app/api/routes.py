
from fastapi import APIRouter

from app.api.routers import predict, report
router = APIRouter()

router.include_router(predict.router, prefix="/infer",
                      tags=["Predict Flower Specie "])
router.include_router(report.router, prefix="/report",
                      tags=["Report about executed predicitons and data distribution"])
