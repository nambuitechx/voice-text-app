import axios from "axios";
import { useReactMediaRecorder } from "react-media-recorder";

function App() {
  const { status, startRecording, stopRecording, mediaBlobUrl } = useReactMediaRecorder({
    video: false,
    audio: true,
    onStop: handleOnStop
  });

  async function handleOnStop(_: string, blob: Blob) {
    // const url = URL.createObjectURL(blob);
    // const audio = document.createElement("audio");
    // audio.src = url;
    // audio.controls = true;
    // document.body.appendChild(audio);

    try {
      const formData = new FormData();
      formData.append("file", blob, "file.wav");

      const response = await axios.post("http://localhost:8000/api/v1/messages/audio", formData);
      console.log(response);
      const text = document.createElement("p");
      text.append("Bạn vừa nói: " + response?.data?.data)
      document.body.appendChild(text);
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
    </div>
  );
}

export default App;
