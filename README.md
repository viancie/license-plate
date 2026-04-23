# 🚓 PatrolPlate: Automatic License Plate Recognition System

PatrolPlate is a real-time Automatic License Plate Recognition (ALPR) system that captures, extracts, validates, and stores vehicle license plate data. Built with Python and a Flask web interface, it processes live video streams to detect and log plate information efficiently.

## Features
- Real-time license plate detection via webcam
- YOLO-based object detection for plate localization
- PaddleOCR for text extraction
- Validation based on LTO plate standards
- Web dashboard for viewing and managing records
- Export data as Excel (ZIP format)

## System Overview
**Detection**: A webcam streams video while YOLO detects license plates using bounding boxes.

**Extraction**: PaddleOCR extracts alphanumeric characters from detected plates.

**Validation**: Custom logic (`util.py`) ensures extracted text follows LTO standards.

**Storage**: Plate numbers, timestamps, and images are stored using Pandas and displayed in a Flask web interface.

## Tech Stack
- Python
- Flask
- OpenCV
- PyTorch (YOLO)
- PaddleOCR
- Pandas

## Installation 
```
git clone https://github.com/viancie/license-plate.git

cd license-plate

pip install -r requirements.txt
```

## Usage
```
python app.py
```

## Output
- Web dashboard with captured plate records
- Downloadable Excel file (ZIP format)
- Saved plate images with timestamps

## Limitations
- Sensitive to poor lighting, blur, and glare
- Performance depends on hardware (CPU/GPU)
- Limited to standard LTO plate formats

## License
This project is for academic and research purposes.
