import cv2
import pandas as pd
import numpy as np
import easyocr

def run_pipeline(image_path, output_excel, output_image):

    image = cv2.imread(image_path)

    reader = easyocr.Reader(['en'], gpu=True)
    results = reader.readtext(image_path)

    data = []

    for (bbox, text, prob) in results:
        x = int(min([p[0] for p in bbox]))
        y = int(min([p[1] for p in bbox]))
        w = int(max([p[0] for p in bbox]) - x)
        h = int(max([p[1] for p in bbox]) - y)

        text = text.strip()

        if len(text) < 2:
            continue

        data.append({"text": text, "x": x, "y": y, "w": w, "h": h})

    df = pd.DataFrame(data).sort_values("y")

    # Row grouping
    rows = []
    current = []
    threshold = 25

    for _, r in df.iterrows():
        if not current:
            current.append(r)
            continue

        if abs(r["y"] - current[-1]["y"]) < threshold:
            current.append(r)
        else:
            rows.append(current)
            current = [r]

    if current:
        rows.append(current)

    # Build table
    table = []
    for row in rows:
        row_df = pd.DataFrame(row).sort_values("x")
        texts = row_df["text"].tolist()

        if len(texts) < 2:
            continue

        table.append(texts)

    # Normalize
    max_len = max(len(r) for r in table)
    normalized = [r + [None]*(max_len - len(r)) for r in table]

    df_table = pd.DataFrame(normalized).T

    # Rename columns
    df_table.columns = [f"Parameter {i+1}" for i in range(df_table.shape[1])]

    # Add Table ID
    df_table.insert(0, "Table ID", [f"Table{i+1}" for i in range(len(df_table))])

    # Clean values
    df_table.replace(["-", "-/-", ""], np.nan, inplace=True)

    df_table.to_excel(output_excel, index=False)

    # Annotated image
    annotated = image.copy()

    for item in data:
        x, y, w, h = item["x"], item["y"], item["w"], item["h"]
        text = item["text"]

        param_index = int((x / image.shape[1]) * df_table.shape[1])
        label = f"P{param_index+1}:{text}"

        cv2.rectangle(annotated, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(annotated, label, (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1)

    # Table box
    x_min = int(df["x"].min())
    y_min = int(df["y"].min())
    x_max = int(df["x"].max()+100)
    y_max = int(df["y"].max()+50)

    cv2.rectangle(annotated, (x_min,y_min),(x_max,y_max),(0,0,255),3)
    cv2.putText(annotated, "Table1",(x_min,y_min-10),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    cv2.imwrite(output_image, annotated)

    print("✅ Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline(
        image_path="data/Input_image.png",
        output_excel="output/output.xlsx",
        output_image="output/annotated_output.png"
    )
