# 📁 PROJECT - PHOTO STORAGE APPLICATION

## Introduction

This course project involves developing, deploying, and enhancing a web application using Google Cloud Run. The web application of the deployed Cloud Run service enables users to upload images, which are then stored in a Google Cloud Storage bucket. Upon each upload, the Gemini API is invoked to generate a JSON file containing a title and description for the uploaded image. This JSON file, named to match the uploaded image, is stored in the same bucket.

The application provides a user-friendly interface where images are displayed as clickable links, each linking to the respective image along with its generated metadata (title and description).

Building upon this foundation, the project further explores automated deployment and revision management within the Cloud Run environment. The existing Cloud Run service is integrated with GitHub, enabling continuous deployment. Every time changes are pushed to the GitHub repository, a new revision is automatically deployed in the Revisions section of the existing Cloud Run service. Traffic is set to 100% for the latest deployed revision, ensuring that all users are served the most up-to-date version of the application.

This automation streamlines development and ensures efficient, hands-free updates to the live application.


---

## 🎯 Goals and Objectives

- ✅ Deploy a scalable and user-friendly web application using Google Cloud Run.
- ✅ Enable users to upload images through the web application.
- ✅ Store uploaded images securely in Google Cloud Storage.
- ✅ Integrate the Gemini API to generate metadata (title and description) for each image and store it as a JSON file.
- ✅ Display uploaded images as clickable links for easy access and viewing.
- ✅ Ensure that clicking on an image shows both the image and its associated metadata.
- ✅ Implement a deployment process using Cloud Run's revision and traffic management.
- ✅ Set traffic to 100% for the latest revision to ensure users always access the newest version.
- ✅ Automate deployment so that any GitHub push triggers an auto-deploy to Cloud Run.

---
## Implemented Features

- **Image upload functionality:** Users can select and upload images through a file upload interface.

- **Cloud Storage integration:** Uploaded images are securely stored in a Google Cloud Storage bucket.

- **Gemini API integration:** For each uploaded image, the Gemini API generates a title and description, which are stored as a JSON file in the same bucket with the same name as the image.

- **Image display and interaction:** Uploaded images are shown as clickable links. Clicking on a link opens the image along with its generated metadata (title and description).

- **Scalable deployment:** The application is deployed on Google Cloud Run, allowing it to scale automatically based on traffic, ensuring high availability and performance.

- **Automated deployment:** Any changes made to the GitHub repository are automatically deployed to the Cloud Run service. When a commit is pushed, a new revision is created and deployed without the need for manual steps, ensuring the application stays updated.

- **Traffic management:** The traffic is set to 100% for the latest deployed revision, ensuring that all users access the most up-to-date version of the application.

- **Revision management:** Google Cloud Run creates a new revision each time a change is committed to the integrated GitHub repository. The service automatically updates to the latest revision, maintaining the most current version of the application in production.

---
### Architecture

![Architecture Diagram](screenshots/Picture1.jpg)
---

## 🔄 Application Workflow (Component-Wise Explanation)

### 🧑‍💻 Users → Cloud Run: Upload Images
Users interact with the web application to upload images through a simple interface.  
**Importance:** This is the starting point of the workflow. Without user-uploaded images, no processing can begin.

---

### ☁️ Cloud Run → Google Cloud Storage (Bucket): Store Images and Metadata
Cloud Run stores uploaded images in Google Cloud Storage. Metadata (title and description from Gemini API) is stored as a JSON file alongside the image.  
**Importance:** Centralized and scalable storage solution for both files and metadata.

---

### 🤖 Cloud Run → Gemini API: Request Metadata Generation
Cloud Run sends the image to Gemini API to generate AI-based title and description.  
**Importance:** Adds contextual information to each image, improving user experience and searchability.

---

### 🔁 Gemini API → Cloud Run: Return Metadata
Gemini returns the generated metadata (title + description) back to Cloud Run.  
**Importance:** This metadata is stored in GCS to complete the upload cycle with content and context.

---

### 🔐 Cloud Run → IAM: Grant Permissions to GCS and Gemini API
IAM policies allow Cloud Run to interact with both GCS and Gemini API.  
**Importance:** Security and authorization. Without these, the application cannot function.

---

### 🛠️ GitHub → Cloud Run: Auto-Deploy on Push
Code pushed to GitHub auto-triggers a deployment to Cloud Run.  
**Importance:** Ensures the app is always live with the latest changes and enables CI/CD.

---

### 📦 Cloud Run → New Revision: Deploy Updates
Every deployment creates a new revision in Cloud Run.  
**Importance:** Enables versioning, rollbacks, and stability during updates.

---

### 🚦 Latest Revision → Traffic Management
Cloud Run routes 100% of user traffic to the latest deployed revision.  
**Importance:** Ensures users always access the most updated version of the application.

---

## ⚙️ Implementation Breakdown

### 1. Users (Interacting with the App)
**Frontend:** HTML form to upload images via `/` endpoint.  
**Uploads:** Supports JPEG and PNG files.  
- **POST request** uploads the image.
- **GET request** lets users view the image + metadata.
- Endpoint `/files/<filename>` serves metadata from JSON.

**How it works:**  
- User uploads → backend sends to GCS → Gemini generates metadata → app fetches metadata + displays it.

---

### 2. Cloud Run (Deployment Platform)
**Framework:** Flask App  
**Port:** 8080 (default for Cloud Run)  
**Deployment:** Cloud Run handles auto-scaling, traffic routing, HTTPS access.  
**No firewall config needed.**  
**How it helps:** No manual infrastructure setup, reliable public endpoint, autoscaling.

---

### 3. Google Cloud Storage (Bucket)
**Purpose:** Stores both image files and JSON metadata.  
**Bucket Setup:**  
- Uses environment variable `BUCKET_NAME`  
- Private access by default  
**Storage Logic:**  
- Uploaded image → stored as `.jpg` or `.png`  
- Metadata → stored as `.json` (same name)

How it helps: Links every image to a context-rich JSON file. Fast, durable, and scalable.
---

### 4. Gemini API (Image Metadata Generation)
**Function:** Sends uploaded images to Gemini API to generate a title and description.  
**API Key:** Stored in environment variable `GEMINI_API_KEY`.  
**Example:**  
```python
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
```
---
Function: Gemini API returns a title and description for each uploaded image.
Storage: Parses and saves this metadata as a JSON file in Google Cloud Storage linked to the image.
How it helps: Automatically generates meaningful metadata for every uploaded image.
---
5. GitHub Repository
Files: Contains three files needed to deploy the current web application to Cloud Run.
Deployment: Connected to Cloud Run for continuous deployment; pushing updates to main.py triggers automatic deployment.
How it helps: Ensures seamless, automated deployment without manual steps.
---
6. Latest Deployed Revision
Details: Each deployment gets a unique revision ID that appears above previous revisions.
Purpose: Each revision is a snapshot of the app at deployment time, preserving previous versions for reference or rollback.
How it helps: Enables version control and easy rollback.
---
7. Traffic Management
Current Setup: 100% of user traffic is routed to the latest deployed revision with a white background.
Older Revisions: Displayed with green or blue backgrounds, inactive but available for rollback.
How it helps: Controls which app version users interact with, ensuring they see the latest features and UI consistently.
---

 

