# Cloud-Native RAW Image Processor

A high-performance asynchronous backend service designed to handle large-scale image processing. This system ingests professional RAW camera files (.NEF, .CR2, .ARW), extracts deep EXIF metadata, and generates web-optimized previews and thumbnails using a distributed task architecture.

## 🏗️ Architecture Overview

The project is built as a cloud-native distributed system to ensure the main API remains responsive during heavy computational tasks.



- **API Layer:** Django REST Framework (DRF) for robust, scalable endpoints.
- **Task Queue:** Celery + Redis to handle CPU-intensive RAW decoding off-thread.
- **Storage Layer:** Cloudflare R2 (S3-Compatible) for cost-effective, high-availability object storage.
- **Processing Engine:** `rawpy` (LibRaw wrapper) for high-fidelity 14-bit image decoding.

## ✨ Key Features

- **Asynchronous Pipeline:** Immediate API response upon upload while background workers handle heavy processing.
- **Full Resolution Decoding:** No quality loss during processing; supports full-frame sensor data.
- **Metadata Extraction:** Automatically extracts ISO, Aperture, Shutter Speed, and Camera Model using `exifread`.
- **Secure Delivery:** Generates time-limited, pre-signed URLs to protect assets from unauthorized access.
- **Multi-Cloud Ready:** Built on the S3 protocol, making it easily portable between AWS, Cloudflare, or DigitalOcean.

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** Django 5.x + Django REST Framework
- **Task Management:** Celery & Redis
- **Storage:** Cloudflare R2 (Boto3)
- **Processing:** RawPy, ImageIO, Pillow
- **Environment:** uv (Modern Python package manager)

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Redis Server (local or managed)
- Cloudflare R2 Bucket (or any S3 provider)

## 🚀 Installation & Setup

To get the system running locally, follow these steps to install dependencies, configure your environment, and start the processing engine.

### 1. Clone the Repository
```bash
git clone https://github.com/Mark-Oise/Raw-Processor.git
cd raw-processor

```

### 2. Install Dependencies

Using `uv` for fast, reliable package management:

```bash
uv sync

```

### 3. Configure Environment

Create a `.env` file in the root directory and add your credentials. This file is ignored by Git to keep your keys secure.

```text
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_BUCKET_NAME=your_bucket
AWS_S3_ENDPOINT_URL=https://<id>.r2.cloudflarestorage.com
REDIS_URL=redis://localhost:6379/0

```

### 4. Run Migrations

Prepare the database schema for the asset and variant models:

```bash
uv run python manage.py migrate

```

---

## 🏃 Running the System

The system requires two separate processes to run simultaneously: one to handle API requests and another to process the heavy RAW files in the background.

### Terminal 1: Web Server

This handles the API endpoints and file uploads.

```bash
uv run python manage.py runserver

```

### Terminal 2: Celery Worker

This handles the actual image processing and metadata extraction.

```bash
uv run celery -A config worker --loglevel=info

```

---


