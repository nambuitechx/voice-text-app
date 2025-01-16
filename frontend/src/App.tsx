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
      formData.append("voice", blob, "voice.wav");

      const response = await axios.post("http://localhost:8000/api/v1/messages/audio", formData);
      console.log(response);
    } catch(err) {
      console.error(err);
    }
  }

  return (
    <div className="container">
      <div>Hello world</div>
      <div>
        <p>Status: {status}</p>
        <button onClick={startRecording}>Start Recording</button>
        <button onClick={stopRecording}>Stop Recording</button>
        <div><audio src={mediaBlobUrl} controls /></div>
    </div>
    </div>
  );
}

export default App;
