# apps/ai/tests/seed_10_coach_inspection.py
import random
import requests
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

url = "http://127.0.0.1:8000/api/v1/ai/results/"

def make_tank(coach_number, side, index, defected):
    tank_id = f"{side}{index}"
    if defected:
        # pick 1-2 random defect conditions for this tank
        conditions = random.sample(
            ["pipe", "support", "surface"], k=random.choice([1, 2])
        )
        return {
            "coach_number": coach_number,
            "tank_id": tank_id,
            "camera_side": "LEFT" if side == "L" else "RIGHT",
            "timestamp_sec": round(random.uniform(5, 300), 2),
            "maintenance_status": "Maintenance Required",
            "tank_image_path": f"cropped_tanks/coach{coach_number}/{tank_id}.jpg",
            "surface_status": "Not Clean" if "surface" in conditions else "Clean",
            "pipe_support_status": "Absent" if "support" in conditions else "Present",
            "pipe_status": "Not Connected" if "pipe" in conditions else "Connected",
            "detection_confidence": round(random.uniform(0.85, 0.99), 2),
        }
    return {
        "coach_number": coach_number,
        "tank_id": tank_id,
        "camera_side": "LEFT" if side == "L" else "RIGHT",
        "timestamp_sec": round(random.uniform(5, 300), 2),
        "maintenance_status": "Normal",
        "tank_image_path": f"cropped_tanks/coach{coach_number}/{tank_id}.jpg",
        "surface_status": "Clean",
        "pipe_support_status": "Present",
        "pipe_status": "Connected",
        "detection_confidence": round(random.uniform(0.9, 0.99), 2),
    }


def build_payload(run_id, defect_coaches):
    tanks = []
    for coach_number in range(1, 11):
        has_defect = coach_number in defect_coaches
        for side in ("L", "R"):
            for index in (1, 2):
                # if this coach has a defect, only give it to one tank so it's not every tank
                defected_tank = has_defect and side == "L" and index == 1
                tanks.append(make_tank(coach_number, side, index, defected_tank))

    return {
        "inspection_run_id": run_id,
        "processing_timestamp": datetime.now(IST).isoformat(),
        "status": "COMPLETE",
        "tanks": tanks,
    }


if __name__ == "__main__":
    # 4 of the 10 coaches get a defect, 6 are clean
    defect_coaches = random.sample(range(1, 11), k=4)

    payload = build_payload("INSP_TEST_10COACH_001", defect_coaches)
    response = requests.post(url, json=payload)

    print(response.status_code)
    print(response.json())
    print("Coaches with defects:", sorted(defect_coaches))