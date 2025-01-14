import { AudioRecorder } from 'react-audio-voice-recorder';

function App() {
  return (
    <>
      <div>Hello world</div>
      <AudioRecorder 
        onRecordingComplete={addAudioElement}
        audioTrackConstraints={{
          noiseSuppression: true,
          echoCancellation: true,
        }} 
        downloadOnSavePress={true}
        downloadFileExtension="webm"
      />
    </>
  )
}

const addAudioElement = (blob: any) => {
  console.log("Blob: ");
  console.log(blob)
  // const url = URL.createObjectURL(blob);
  // const audio = document.createElement("audio");
  // audio.src = url;
  // audio.controls = true;
  // document.body.appendChild(audio);

  // Send to backend
};

export default App
