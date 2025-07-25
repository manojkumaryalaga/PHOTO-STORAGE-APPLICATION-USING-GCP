# 📁 PROJECT - PHOTO STORAGE APPLICATION

## 📌 Introduction

This course project involves developing, deploying, and enhancing a web application using **Google Cloud Run**. The web application enables users to upload images, which are then stored in a **Google Cloud Storage** bucket. Upon each upload, the **Gemini API** is invoked to generate a JSON file containing a **title and description** for the uploaded image. This JSON file, named to match the uploaded image, is stored in the same bucket.

The application provides a **user-friendly interface** where images are displayed as clickable links, each linking to the respective image along with its generated metadata (title and description).

Building upon this foundation, the project further explores **automated deployment and revision management** within the Cloud Run environment. The existing Cloud Run service is integrated with **GitHub**, enabling **continuous deployment**: every time changes are pushed to the GitHub repository, a **new revision is automatically deployed**. Traffic is set to **100% for the latest deployed revision**, ensuring that all users are served the most up-to-date version of the application.

This automation streamlines development and ensures **hands-free updates** to the live application.

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



---

## 🧠 Tech Stack

- Google Cloud Run  
- Google Cloud Storage  
- Gemini API  
- Python / Flask (or relevant backend framework)  
- GitHub for version control and deployment automation  

---

## 🚀 Live Demo

🔗 [Your Deployed Web App Link Here](https://your-app-link)

---

