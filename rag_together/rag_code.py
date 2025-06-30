import json
from pathlib import Path
from collections import defaultdict

# Load JSON
with open("Data/all_store_data_region.json", "r") as f:
    all_store_data_region = json.load(f)

chunk_list = []

region_totals = defaultdict(lambda: defaultdict(float))
coach_totals = defaultdict(lambda: defaultdict(float))

for region, region_data in all_store_data_region.items():
    for coach, stores in region_data.items():
        for store, periods in stores.items():
            for period, items in periods.items():
                if period == 'metadata' or period.endswith('B'):
                    continue

                for item, value in items.items():
                    region_totals[(region, period)][item] += value
                    coach_totals[(region, coach, period)][item] += value

                # Create store-level chunk
                line_item_descriptions = [f"{item} was ${value:,.0f}" for item, value in items.items()]
                line_summary = "; ".join(line_item_descriptions)

                chunk_text = (
                    f"In {period}, {store} (Region: {region}, Area Coach: {coach}) had the following financials: {line_summary}."
                )

                chunk_list.append({
                    "text": chunk_text,
                    "metadata": {
                        "region": region,
                        "area_coach": coach,
                        "store": store,
                        "period": period,
                        "type": "store_period"
                    }
                })

# Add region-level chunks
for (region, period), items in region_totals.items():
    summary = "; ".join([f"{k} was ${v:,.0f}" for k, v in items.items()])
    text = f"In {period}, Region {region} total financials were: {summary}."
    chunk_list.append({
        "text": text,
        "metadata": {
            "region": region,
            "period": period,
            "type": "region_total"
        }
    })

# Add area coach-level chunks
for (region, coach, period), items in coach_totals.items():
    summary = "; ".join([f"{k} was ${v:,.0f}" for k, v in items.items()])
    text = f"In {period}, Area Coach {coach} (Region: {region}) total financials were: {summary}."
    chunk_list.append({
        "text": text,
        "metadata": {
            "region": region,
            "area_coach": coach,
            "period": period,
            "type": "area_total"
        }
    })

# Save to file
Path("rag_chunks").mkdir(exist_ok=True)
with open("rag_chunks/store_chunks.jsonl", "w") as f:
    for entry in chunk_list:
        f.write(json.dumps(entry) + "\n")

print(f"✅ Generated {len(chunk_list)} chunks including store, area, and region totals. Saved to rag_chunks/store_chunks.jsonl")
