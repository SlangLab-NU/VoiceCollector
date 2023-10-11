## Welcome to Voice Collector! 🎙️

Hello there! We're thrilled to have you here. We're on a mission to make voice recognition inclusive for everyone, especially for those with speech impairments.

### **About this app! 🌟**
Voice Collector is a simple application designed to collect voice data. It comprises a web application and a backend server, working harmoniously to provide a seamless user experience.

Web Application

The web application is built with React, a powerful JavaScript library for building user interfaces, and Material-UI, a popular React UI framework. The main component RecordMUI orchestrates the user interface, allowing users to navigate through prompts, record their responses, and submit recordings. It fetches data from the backend using Axios and manages various states to control the recording and submission process. The AudioRecorder component, imported from AudioRecorderCommon.js, handles audio recording through the browser, managing microphone permissions and providing feedback to the user through UI elements.

Backend Server

The backend server is crafted using Flask, a lightweight WSGI web application framework in Python. It handles requests related to reference text, recording, receiving audio files, and validation of audio files. It consists of two main blueprints: Speak and Validate. The Speak blueprint handles the retrieval and submission of audio data. The Validate blueprint manages the validation pipeline to ensure the audio data is in the correct format and has appropriate volume and pauses. The server employs Minio for S3-compatible storage service to securely store the audio recordings. The backend functionalities are encapsulated into Docker containers which are orchestrated using Docker Compose, ensuring easy deployment and management.

### **Host It Yourself! 🛠️**

Want to host this application on your platform and give it a whirl? Check out our [release guide](RELEASE.md) for all the details to get you started.

### **Join Our Journey! 🚀**

At Happy Prime, we're not just building a platform; we're fostering a community that believes in the power of inclusive voice recognition. If you're as excited about this as we are, dive in, explore our datasets, and see how our application can serve you.

And always remember, every voice matters, and together we're making sure they are all recognized. Cheers to a world where technology understands everyone! 🥂