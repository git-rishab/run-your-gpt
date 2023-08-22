import { useState } from "react";
import { Input, Button, Loader } from "@mantine/core";
import styles from "../styles/dashboard.module.css";
import { url } from "../notification";
import { Microphone } from 'tabler-icons-react';
import { useRef } from "react";

export default function Dashboard() {
  const [messages, setMessages] = useState<any>([
    { type: "client", message: "Welcome to chat App. How can I help you?" },
  ]);
  const userString = sessionStorage.getItem('user');
  const user: any = userString ? JSON.parse(userString) : null;
  const [loading, setLoading] = useState<Boolean>(false);
  const [chat, setChat] = useState<string>("");
  const [audioSrc, setAudioSrc] = useState("");
  const [textResponse, setTextResponse] = useState<string>('');
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const [limit, setLimit] = useState(user.limit);

  const startRecording = () => {
    const constraints: MediaStreamConstraints = { audio: true };
    navigator.mediaDevices.getUserMedia(constraints)
      .then((stream: MediaStream) => {
        mediaRecorderRef.current = new MediaRecorder(stream);
        const chunks: BlobPart[] = [];

        mediaRecorderRef.current.ondataavailable = (event: BlobEvent) => {
          if (event.data.size > 0) {
            chunks.push(event.data);
          }
        };

        mediaRecorderRef.current.onstop = () => {
          const audioBlob = new Blob(chunks, { type: 'audio/wav' });
          const audioUrl = URL.createObjectURL(audioBlob);
          setAudioSrc(audioUrl);
          sendAudioToBackend(audioBlob);
        };

        mediaRecorderRef.current.start();
      })
      .catch((error: Error) => {
        console.error('Error accessing microphone:', error);
      });
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
  };

  const sendAudioToBackend = async (audioBlob: Blob) => {
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob);

      const response = await fetch(`${url}/audiototext`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      console.log(data);
      
      setTextResponse(data.text);
    } catch (error) {
      console.error('Error sending audio to backend:', error);
    }
  };

  const playAudio = async (message:any) => {
    setLoading(true)
    try {
      const response:any = await fetch(`${url}/audio`, {
        method:"POST",
        headers:{
            "content-type":"application/json"
        },
        body:JSON.stringify({prompt:message})
      });

      const blob = await response.blob();
      const audioUrl = URL.createObjectURL(blob);
      setAudioSrc(audioUrl);
    } catch (error) {
      console.error(error);
    }
    setLoading(false)
  };
  const handleMessage = async () => {
    setLoading(true);

    const newChats = [...messages]; // Create a new array to avoid mutation

    // Add client message
    newChats.push({ type: "client", message: chat });
    setChat("");

    try {
      const req = await fetch(`${url}/chat`, {
        method: "POST",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify({ prompt: chat, limit:limit, id:user.id }),
      });

      const res = await req.json();

      // Add server response
      newChats.push({ type: "server", message: res.message });
      playAudio(res.message)
    } catch (error) {
      console.log(error);
    }

    setMessages(newChats); // Update messages with the new array
    setLimit(limit-1)
    setLoading(false);
  };

  return (
    <div className={styles.dashboard}>
      <h3>Limit: {limit}</h3>
      <div className={styles.chat}>
        {messages.map((el: any, i: any) => (
          <div
            key={i}
            className={el.type === "client" ? styles.client : styles.server}
          >
            {el.message}
          </div>
        ))}
        <audio controls src={audioSrc} />
        {loading && <Loader variant="dots" size="lg" />}
        <div></div>
      </div>
  
      <div className={styles.box}>

        <Input
          className={styles.input}
          placeholder="Type your message..."
          onChange={(e) => setChat(e.target.value)}
          value={chat}
        />
        <Button leftIcon={<Microphone />} onClick={startRecording} variant="white"></Button>
        <Button onClick={handleMessage}>Send</Button>
      </div>
    </div>
  );
}
