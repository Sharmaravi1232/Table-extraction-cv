# Table-extraction-cv
Extract structured tables from images using OCR and computer vision with Excel export and visual annotation.
# 📊 Table Extraction using Computer Vision

This project focuses on extracting structured tabular data from images using OCR and computer vision techniques. It reconstructs parameter-value relationships and exports the data into a structured Excel format, along with a visual annotated output for verification.

---

## 🚀 Features

- OCR-based text extraction using EasyOCR  
- Table reconstruction using spatial grouping  
- Parameter-value mapping  
- Handling multi-value entries (`/` separated)  
- Missing value handling (`-`, `-/-`)  
- Excel export (`.xlsx`)  
- Annotated image with bounding boxes and labels  

---

## 🧠 Approach

The solution follows a rule-based pipeline combining OCR and spatial reasoning:

1. **Text Extraction**  
   - Extract text and bounding boxes using EasyOCR  

2. **Row Grouping**  
   - Group text into rows based on Y-coordinate proximity  

3. **Table Reconstruction**  
   - Sort each row from left to right  
   - Identify structure of parameter and value columns  

4. **Data Normalization**  
   - Handle uneven rows by padding missing values  

5. **Transformation**  
   - Transpose table so that:
     - Columns represent parameters  
     - Rows represent records  

6. **Data Cleaning**  
   - Convert invalid values (`-`, `-/-`) to NaN  

7. **Visualization**  
   - Draw bounding boxes around detected text  
   - Label each value with parameter index  
   - Highlight table region as `Table1`  

---

## 📂 Project Structure
