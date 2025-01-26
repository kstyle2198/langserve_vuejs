<template>
  <div class="p-4">
    <h1 class="text-xl font-bold mb-4">Streaming Response Example</h1>
    <textarea
      v-model="inputMessage"
      class="w-full p-2 border rounded mb-4"
      placeholder="Enter your message"
    ></textarea>
    <button
      @click="startStreaming"
      class="px-4 py-2 bg-blue-500 text-white rounded"
      :disabled="isStreaming"
    >
      {{ isStreaming ? "Streaming..." : "Start Streaming" }}
    </button>
    <div v-if="responseStream.length" class="mt-4">
      <h2 class="text-lg font-semibold mb-2">Response:</h2>
      <div class="p-2 border rounded whitespace-pre-wrap">
        {{ responseStream }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      inputMessage: "", // Input message from the user
      responseStream: "", // Holds the streaming response
      isStreaming: false, // Flag to indicate if streaming is in progress
    };
  },
  methods: {
    async startStreaming() {
      if (!this.inputMessage.trim()) {
        alert("Please enter a message to send.");
        return;
      }

      this.responseStream = ""; // Clear previous response
      this.isStreaming = true; // Indicate streaming has started

      const requestBody = {
        input: { messages: [this.inputMessage] },
        config: {},
        kwargs: {},
      };

      try {
        const response = await fetch("http://localhost:8000/langgraph/stream", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.body) {
          throw new Error("No response body available.");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        /* eslint-disable no-constant-condition */
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          this.responseStream += decoder.decode(value, { stream: true });
        }
        /* eslint-enable no-constant-condition */
      } catch (error) {
        console.error("Error during streaming:", error);
      } finally {
        this.isStreaming = false; // Indicate streaming has stopped
      }
    },
  },
};
</script>
