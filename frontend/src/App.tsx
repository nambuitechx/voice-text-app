import axios from "axios";
import { useState, useEffect } from "react";
import { useReactMediaRecorder } from "react-media-recorder";

const BASE_URL = "http://localhost:8000/api/v1"

function App() {
  const { status, startRecording, stopRecording, mediaBlobUrl } = useReactMediaRecorder({
    video: false,
    audio: true,
    onStop: onRecordingStopHandler
  });

  const [messages, setMessages] = useState([]);

  useEffect(() => {
    async function getAllMessages() {
      try {
        const response = await axios.get(`${BASE_URL}/messages/all`);
        const messages = response.data.data;
        setMessages(messages);
      } catch(err) {
        console.log(err);
      }
    }
    getAllMessages();
  }, []);

  async function onRecordingStopHandler(_: string, blob: Blob) {
    // const url = URL.createObjectURL(blob);
    // const audio = document.createElement("audio");
    // audio.src = url;
    // audio.controls = true;
    // document.body.appendChild(audio);

    try {
      const formData = new FormData();
      formData.append("file", blob, "file.wav");

      const response = await axios.post(`${BASE_URL}/messages/audio`, formData);
      const text = document.createElement("p");
      text.append("Bạn vừa nói: " + response?.data?.data.query)
      document.body.appendChild(text);
    } catch(err) {
      console.error(err);
    }
  }

  async function onDeleteMessageHandler(id: string) {
    try {
      console.log("Deleting message with id" + id);
      await axios.delete(`${BASE_URL}/messages/message/${id}`);
      const remainMessages = messages.filter((message: any) => message.id != id);
      setMessages(remainMessages);
    } catch(err) {
      console.error(err);
    }
  }

  return (
    <div className="container">
      <div>Hello world</div>
      <div>
        <h2>Status: {status}</h2>
        <button onClick={startRecording}>Start Recording</button>
        <button onClick={stopRecording}>Stop Recording</button>
      </div>
      <div>
        <p>Messages:</p>
        {messages.length > 0 && messages.map((message: any) => (
          <div key={message.id}>
            <p>id - {message.id}</p>
            <p>message - {message.query}</p>
            <button onClick={() => onDeleteMessageHandler(message.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
