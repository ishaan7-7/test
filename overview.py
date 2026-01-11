from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dashboard.app.dependencies import get_dashboard_state

router = APIRouter()

@router.get("/overview")
def overview(state=Depends(get_dashboard_state)):
    snapshot = state.snapshot()

    replay = snapshot.get("replay", {})
    ingest = snapshot.get("ingest", {})
    kafka = snapshot.get("kafka", {})

    return JSONResponse(
        content={
            "replay": {
                "active_sources": replay.get("active_sources"),
            },
            "ingest": {
                "rows_accepted": ingest.get("ingest_rows_accepted_total"),
                "rows_rejected": ingest.get("ingest_rows_rejected_total"),
            },
            "kafka": {
                "total_rows": kafka.get("kafka_total_rows"),
                "latency_p50": kafka.get("kafka_latency_ms_p50"),
                "latency_p95": kafka.get("kafka_latency_ms_p95"),
            },
        }
    )