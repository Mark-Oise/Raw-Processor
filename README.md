# Cloud-Native RAW Image Processor

A high-performance asynchronous backend service designed to handle large-scale image processing. This system ingests professional RAW camera files (.NEF, .CR2, .ARW), extracts deep EXIF metadata, and generates web-optimized previews and thumbnails using a distributed task architecture.

## 🏗️ Architecture Overview

The project is built as a cloud-native distributed system to ensure the main API remains responsive during heavy computational tasks.

* **API Layer:** Django REST Framework (DRF) for robust, scalable endpoints.
* **Task Queue:** Celery + Redis to handle CPU-intensive RAW decoding off-thread.
* **Storage Layer:** Cloudflare R2 (S3-Compatible) for cost-effective, high-availability object storage with zero egress fees.
* **Processing Engine:** `rawpy` (LibRaw wrapper) for high-fidelity 14-bit image decoding.

## ✨ Key Features

* **Asynchronous Pipeline:** Immediate API response upon upload while background workers handle heavy processing.
* **Full Resolution Decoding:** No quality loss during processing; supports full-frame sensor data.
* **Metadata Extraction:** Automatically extracts ISO, Aperture, Shutter Speed, and Camera Model using `exifread`.
* **Secure Delivery:** Generates time-limited, pre-signed URLs to protect assets from unauthorized access.
* **Containerized Environment:** Fully Dockerized setup for consistent deployment across any infrastructure.

## 🛠️ Tech Stack

* **Language:** Python 3.12+
* **Framework:** Django 5.x + Django REST Framework
* **Task Management:** Celery & Redis
* **Storage:** Cloudflare R2 (Boto3 / S3 Protocol)
* **Processing:** RawPy, ImageIO, Pillow
* **DevOps:** Docker, Docker Compose, `uv` (Fast Python package manager)

---

## 🐳 Running with Docker (Recommended)

The simplest way to run the entire stack (Web, Worker, and Redis) is using Docker Compose. This ensures all services are correctly networked and configured.

### 1. Configure Environment

Ensure your `.env` file is set up in the root directory.

> **Note:** For Docker, the `REDIS_URL` in your `.env` should point to the container name: `redis://redis:6379/0`.

### 2. Build and Start

Run the following command to build the images and start the containers:

```bash
docker compose up --build

```

### 3. Management Commands

* **Run Migrations:** `docker compose exec web python manage.py migrate`
* **View Logs:** `docker compose logs -f`
* **Stop System:** `docker compose down`

---

## 🚀 Manual Installation & Setup

If you prefer to run the services natively, follow these steps.

### 1. Clone & Install

```bash
git clone https://github.com/Mark-Oise/Raw-Processor.git
cd raw-processor
uv sync

```

### 2. Configure Environment

Create a `.env` file in the root directory:

```text
AWS_ACCESS_KEY_ID=your_r2_key
AWS_SECRET_ACCESS_KEY=your_r2_secret
AWS_BUCKET_NAME=your_bucket_name
AWS_S3_ENDPOINT_URL=https://<id>.r2.cloudflarestorage.com
REDIS_URL=redis://localhost:6379/0

```

### 3. Initialize & Run

**Terminal 1 (Migrations & Web Server):**

```bash
uv run python manage.py migrate
uv run python manage.py runserver

```

**Terminal 2 (Celery Worker):**

```bash
uv run celery -A config worker --loglevel=info

```

---

## 📊 API Usage

### Upload Asset

`POST /api/upload/`
Provide a RAW file under the `file` key as `multipart/form-data`.

### List Assets & Metadata

`GET /api/upload/`
Returns a detailed JSON list including status, EXIF metadata, and pre-signed S3 links for the original and processed variants.

---

