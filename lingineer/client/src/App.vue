<template>
    <div id="app">
      <h1>AICoach Text Correction</h1>
      <div>
        <label for="text-input">Enter your text:</label>
        <textarea
          id="text-input"
          v-model="inputText"
          placeholder="Type your text here..."
          rows="5"
        ></textarea>
      </div>
      <button @click="submitText">Correct Text</button>
  
      <div v-if="errorMessage" class="error">
        <p>{{ errorMessage }}</p>
      </div>
  
      <div v-if="correctedText || feedback" class="result">
        <h2>Results:</h2>
        <p><strong>Original Text:</strong> {{ inputText }}</p>
        <p><strong>Corrected Text:</strong> {{ correctedText }}</p>
        <p><strong>Feedback:</strong> {{ feedback }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios"; // Import Axios for API requests
  
  export default {
    name: "App",
    data() {
      return {
        inputText: "", // Holds the text input by the user
        correctedText: "", // Holds the corrected text returned by the backend
        feedback: "", // Holds the feedback returned by the backend
        errorMessage: "", // Holds any error messages
      };
    },
    methods: {
      async submitText() {
        if (!this.inputText) {
          this.errorMessage = "Please enter text to correct.";
          return;
        }
  
        this.errorMessage = ""; // Clear previous errors
        try {
          // Send POST request to the Flask backend
          const response = await axios.post("http://127.0.0.1:5000/correct_text", {
            text: this.inputText,
          });
  
          // Update the results
          this.correctedText = response.data.corrected_text;
          this.feedback = response.data.feedback;
        } catch (error) {
          // Handle errors
          this.errorMessage =
            error.response?.data?.error || "An error occurred. Please try again.";
        }
      },
    },
  };
  </script>
  
  <style>
  /* Add basic styles */
  #app {
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 20px;
  }
  
  textarea {
    width: 100%;
    max-width: 500px;
    margin: 10px 0;
    padding: 10px;
  }
  
  button {
    padding: 10px 20px;
    margin: 10px 0;
    cursor: pointer;
  }
  
  .error {
    color: red;
  }
  
  .result {
    margin-top: 20px;
    text-align: left;
    max-width: 600px;
    margin: 20px auto;
  }
  </style>
  