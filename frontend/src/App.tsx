import axios, { HttpStatusCode } from "axios";

import { AudioRecorder } from "react-audio-voice-recorder";

function App() {
  return (
    <>
      <div>Hello world</div>
      <AudioRecorder
        onRecordingComplete={recordingCompleteHandler}
        audioTrackConstraints={{
          noiseSuppression: true,
          echoCancellation: true,
        }}
        // downloadOnSavePress={true}
        // downloadFileExtension="webm"
      />
    </>
  );
}

const recordingCompleteHandler = async (blob: any) => {
  console.log("Blob: ");
  console.log(blob);

  // const url = URL.createObjectURL(blob);
  // const audio = document.createElement("audio");
  // audio.src = url;
  // audio.controls = true;
  // document.body.appendChild(audio);

  try {
    const formData = new FormData();
    formData.append("blob", blob, "blob.webm");

    const response = await axios.post("http://localhost:8000/api/v1/audio/speak", formData);
    console.log(response);
  } catch(err) {
    console.error(err);
  }
};

export default App;
